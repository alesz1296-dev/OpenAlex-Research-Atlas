"""
Minimal OpenAlex ingestion flow for one work at a time.

This module is intentionally small and explicit so you can trace:
1. fetch one OpenAlex work payload
2. normalize the payload into our schema shape
3. upsert the related rows into PostgreSQL
4. record the ingestion run and any failures
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.database.models import (
    Author,
    IngestionError,
    IngestionRun,
    Source,
    Topic,
    Work,
    WorkAuthor,
    WorkTopic,
)


def reconstruct_abstract(inverted_index: dict[str, list[int]] | None) -> str | None:
    """
    OpenAlex often returns abstracts as an inverted index.

    Example:
    {"hello": [0], "world": [1]} -> "hello world"
    """
    if not inverted_index:
        return None

    positions: dict[int, str] = {}
    for token, indexes in inverted_index.items():
        for index in indexes:
            positions[index] = token

    return " ".join(token for _, token in sorted(positions.items()))


def normalize_openalex_work_id(openalex_id: str) -> str:
    """Accept either a bare OpenAlex work id or the full OpenAlex URL."""
    cleaned = openalex_id.strip()
    if cleaned.startswith("https://openalex.org/"):
        return cleaned
    return f"https://openalex.org/{cleaned}"


@dataclass
class IngestionSummary:
    ingestion_run_id: int
    work_id: int
    work_openalex_id: str
    created: bool
    authors_synced: int
    topics_synced: int
    source_synced: bool


@dataclass(frozen=True)
class ErrorClassification:
    stage: str
    error_type: str
    retryable: bool


class OpenAlexClient:
    """Very small HTTP client for the one-work learning slice."""

    def __init__(self) -> None:
        self.base_url = settings.OPENALEX_BASE_URL.rstrip("/")
        self.timeout = settings.OPENALEX_TIMEOUT_SECONDS
        self.user_agent = settings.OPENALEX_USER_AGENT
        self.mailto = settings.OPENALEX_MAILTO

    def fetch_work(self, openalex_id: str) -> dict[str, Any]:
        normalized_id = normalize_openalex_work_id(openalex_id)
        work_key = normalized_id.rsplit("/", maxsplit=1)[-1]
        query = urlencode({"mailto": self.mailto}) if self.mailto else ""
        url = f"{self.base_url}/works/{work_key}"
        if query:
            url = f"{url}?{query}"

        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": self.user_agent,
            },
        )
        with urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))


class OpenAlexIngestionService:
    """
    Minimal ingestion service with explicit upsert behavior.

    Upsert strategy:
    - if a row already exists, update selected metadata fields from OpenAlex
    - if relationship rows already exist, replace them with the latest linkage

    Recency policy:
    - for Phase 1 single-work ingestion, publication recency does not change persistence
    - "newer first" is reserved for future batch fetch ordering
    """

    def __init__(self, db: Session, client: OpenAlexClient | None = None) -> None:
        self.db = db
        self.client = client or OpenAlexClient()

    def ingest_work_by_openalex_id(self, openalex_id: str) -> IngestionSummary:
        ingestion_run = IngestionRun(
            query_type="work",
            query_params={"openalex_id": normalize_openalex_work_id(openalex_id)},
            status="running",
        )
        self.db.add(ingestion_run)
        self.db.commit()
        self.db.refresh(ingestion_run)

        try:
            payload = self.client.fetch_work(openalex_id)
        except Exception as exc:
            self._persist_ingestion_error(
                openalex_id=openalex_id,
                ingestion_run_id=ingestion_run.id,
                exc=exc,
                stage="fetch",
            )
            raise

        try:
            summary = self._persist_work_graph(payload, ingestion_run.id)

            ingestion_run.record_count = 1
            ingestion_run.status = "completed"
            ingestion_run.completed_at = datetime.utcnow()

            self.db.commit()
            return summary
        except Exception as exc:
            self.db.rollback()
            self._persist_ingestion_error(
                openalex_id=openalex_id,
                ingestion_run_id=ingestion_run.id,
                exc=exc,
                payload=payload,
                stage="persist",
            )
            raise

    def retry_ingestion_error(self, ingestion_error_id: int) -> IngestionSummary:
        """
        Retry a previously recorded ingestion error when it was classified as retryable.

        Phase 1 behavior:
        - keep the original error record as audit history
        - start a fresh ingestion run for the retry attempt
        """
        ingestion_error = self.db.get(IngestionError, ingestion_error_id)
        if ingestion_error is None:
            raise ValueError(f"Ingestion error {ingestion_error_id} was not found")
        if not ingestion_error.retryable:
            raise ValueError(f"Ingestion error {ingestion_error_id} is not retryable")

        openalex_id = ingestion_error.external_id
        if not openalex_id and ingestion_error.ingestion_run and ingestion_error.ingestion_run.query_params:
            openalex_id = ingestion_error.ingestion_run.query_params.get("openalex_id")
        if not openalex_id:
            raise ValueError(
                f"Ingestion error {ingestion_error_id} has no recoverable OpenAlex identifier"
            )

        return self.ingest_work_by_openalex_id(openalex_id)

    def _persist_ingestion_error(
        self,
        openalex_id: str,
        ingestion_run_id: int,
        exc: Exception,
        stage: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        classification = self._classify_exception(exc, stage)
        ingestion_run = self.db.get(IngestionRun, ingestion_run_id)
        if ingestion_run is None:
            ingestion_run = IngestionRun(
                query_type="work",
                query_params={"openalex_id": normalize_openalex_work_id(openalex_id)},
            )
            self.db.add(ingestion_run)
            self.db.flush()

        ingestion_run.error_count = (ingestion_run.error_count or 0) + 1
        ingestion_run.status = "failed"
        ingestion_run.completed_at = datetime.utcnow()

        self.db.add(
            IngestionError(
                ingestion_run_id=ingestion_run_id,
                entity_type="work",
                external_id=normalize_openalex_work_id(openalex_id),
                stage=classification.stage,
                error_type=classification.error_type,
                retryable=classification.retryable,
                error_message=str(exc),
                raw_payload=payload,
            )
        )
        self.db.commit()

    def _persist_work_graph(self, payload: dict[str, Any], ingestion_run_id: int) -> IngestionSummary:
        source = self._upsert_source(payload.get("primary_location", {}).get("source"))
        work, created = self._upsert_work(payload, ingestion_run_id, source)
        authors_synced = self._sync_authors(work, payload.get("authorships", []))
        topics_synced = self._sync_topics(work, payload.get("topics", []))

        self.db.flush()
        return IngestionSummary(
            ingestion_run_id=ingestion_run_id,
            work_id=work.id,
            work_openalex_id=work.openalex_id,
            created=created,
            authors_synced=authors_synced,
            topics_synced=topics_synced,
            source_synced=source is not None,
        )

    def _upsert_work(
        self,
        payload: dict[str, Any],
        ingestion_run_id: int,
        source: Source | None,
    ) -> tuple[Work, bool]:
        normalized_id = normalize_openalex_work_id(payload["id"])
        work = self.db.query(Work).filter(Work.openalex_id == normalized_id).one_or_none()

        created = work is None
        if work is None:
            work = Work(openalex_id=normalized_id)
            self.db.add(work)

        primary_location = payload.get("primary_location") or {}
        # Works use the latest full OpenAlex payload as the source of truth.
        work.title = payload.get("title") or "Untitled work"
        work.abstract = payload.get("abstract") or reconstruct_abstract(payload.get("abstract_inverted_index"))
        work.doi = payload.get("doi")
        work.publish_date = self._parse_date(payload.get("publication_date"))
        work.publication_year = payload.get("publication_year")
        work.work_type = payload.get("type")
        work.language = payload.get("language") or "en"
        work.open_access = bool((payload.get("open_access") or {}).get("is_oa", False))
        work.citation_count = payload.get("cited_by_count") or 0
        work.source_url = primary_location.get("landing_page_url")
        work.pdf_url = primary_location.get("pdf_url")
        work.source = source
        work.ingestion_run_id = ingestion_run_id
        work.raw_payload = payload

        self.db.flush()
        return work, created

    def _upsert_source(self, source_payload: dict[str, Any] | None) -> Source | None:
        if not source_payload or not source_payload.get("id"):
            return None

        normalized_id = source_payload["id"]
        source = self.db.query(Source).filter(Source.openalex_id == normalized_id).one_or_none()
        if source is None:
            source = Source(openalex_id=normalized_id)
            self.db.add(source)

        # Nested sources may be partial. Only overwrite fields that are actually present.
        self._update_if_present(source_payload, "display_name", source, "name", fallback="Unknown source")
        self._update_if_present(source_payload, "type", source, "source_type")
        self._update_if_present(source_payload, "issn_l", source, "issn_l")
        if "issn" in source_payload:
            issn_values = source_payload.get("issn") or []
            source.issn = issn_values[0] if issn_values else None
        self._update_if_present(source_payload, "host_organization_name", source, "publisher")
        self._update_if_present(source_payload, "country_code", source, "country_code")
        self._update_if_present(source_payload, "homepage_url", source, "homepage_url")
        if "is_oa" in source_payload:
            source.is_open_access = bool(source_payload.get("is_oa"))
        source.raw_payload = source_payload

        self.db.flush()
        return source

    def _sync_authors(self, work: Work, authorships: list[dict[str, Any]]) -> int:
        self.db.query(WorkAuthor).filter(WorkAuthor.work_id == work.id).delete(synchronize_session=False)

        synced = 0
        for author_order, authorship in enumerate(authorships, start=1):
            author_payload = authorship.get("author") or {}
            if not author_payload.get("id"):
                continue

            author = self._upsert_author(author_payload)
            self.db.add(
                WorkAuthor(
                    work_id=work.id,
                    author_id=author.id,
                    author_order=author_order,
                )
            )
            synced += 1

        self.db.flush()
        return synced

    def _upsert_author(self, author_payload: dict[str, Any]) -> Author:
        normalized_id = author_payload["id"]
        author = self.db.query(Author).filter(Author.openalex_id == normalized_id).one_or_none()
        if author is None:
            author = Author(openalex_id=normalized_id)
            self.db.add(author)

        self._update_if_present(author_payload, "display_name", author, "name", fallback="Unknown author")
        self._update_if_present(author_payload, "display_name", author, "display_name")
        self._update_if_present(author_payload, "orcid", author, "orcid")
        self._update_if_present(author_payload, "cited_by_count", author, "citation_count")
        self._update_if_present(author_payload, "works_count", author, "works_count")
        self._update_if_present(author_payload, "summary_stats", author, "h_index", nested_key="h_index")
        author.raw_payload = author_payload

        self.db.flush()
        return author

    def _sync_topics(self, work: Work, topic_payloads: list[dict[str, Any]]) -> int:
        self.db.query(WorkTopic).filter(WorkTopic.work_id == work.id).delete(synchronize_session=False)

        synced = 0
        for topic_payload in topic_payloads:
            if not topic_payload.get("id"):
                continue

            topic = self._upsert_topic(topic_payload)
            self.db.add(
                WorkTopic(
                    work_id=work.id,
                    topic_id=topic.id,
                    score=topic_payload.get("score"),
                )
            )
            synced += 1

        self.db.flush()
        return synced

    def _upsert_topic(self, topic_payload: dict[str, Any]) -> Topic:
        normalized_id = topic_payload["id"]
        topic = self.db.query(Topic).filter(Topic.openalex_id == normalized_id).one_or_none()
        if topic is None:
            topic = Topic(openalex_id=normalized_id)
            self.db.add(topic)

        domain_payload = topic_payload.get("domain") or {}
        self._update_if_present(topic_payload, "display_name", topic, "name", fallback="Unknown topic")
        self._update_if_present(topic_payload, "description", topic, "description")
        if "domain" in topic_payload:
            topic.domain = domain_payload.get("display_name")
        self._update_if_present(topic_payload, "level", topic, "level")
        self._update_if_present(topic_payload, "cited_by_count", topic, "citation_count")
        self._update_if_present(topic_payload, "works_count", topic, "works_count")
        if "keywords" in topic_payload:
            keywords = topic_payload.get("keywords") or []
            topic.keywords = [keyword.get("display_name") for keyword in keywords if keyword.get("display_name")] or None
        topic.raw_payload = topic_payload

        self.db.flush()
        return topic

    @staticmethod
    def _parse_date(value: str | None) -> datetime | None:
        if not value:
            return None
        return datetime.fromisoformat(value)

    @staticmethod
    def _update_if_present(
        payload: dict[str, Any],
        source_key: str,
        target: Any,
        target_attr: str,
        *,
        nested_key: str | None = None,
        fallback: Any | None = None,
    ) -> None:
        if source_key not in payload:
            return

        value = payload.get(source_key)
        if nested_key is not None and isinstance(value, dict):
            value = value.get(nested_key)
        if value is None and fallback is not None:
            value = fallback
        setattr(target, target_attr, value)

    @staticmethod
    def _classify_exception(exc: Exception, stage: str) -> ErrorClassification:
        if isinstance(exc, HTTPError):
            retryable = exc.code >= 500 or exc.code == 429
            return ErrorClassification(stage=stage, error_type="http_error", retryable=retryable)
        if isinstance(exc, (URLError, TimeoutError, ConnectionError)):
            return ErrorClassification(stage=stage, error_type="network_error", retryable=True)
        if isinstance(exc, IntegrityError):
            return ErrorClassification(stage=stage, error_type="integrity_error", retryable=False)
        if isinstance(exc, OperationalError):
            return ErrorClassification(stage=stage, error_type="database_operational_error", retryable=True)
        if isinstance(exc, DBAPIError):
            return ErrorClassification(
                stage=stage,
                error_type="database_error",
                retryable=bool(getattr(exc, "connection_invalidated", False)),
            )
        if isinstance(exc, (KeyError, TypeError, ValueError)):
            return ErrorClassification(stage=stage, error_type="payload_mapping_error", retryable=False)
        return ErrorClassification(stage=stage, error_type="unexpected_error", retryable=False)
