"""Retrieval over ingested OpenAlex works.

This is intentionally keyword/filter retrieval first. Semantic retrieval with
pgvector comes later, after the API contract is stable.
"""

from __future__ import annotations

import time

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from src.core.observability import RETRIEVAL_LATENCY_SECONDS, RETRIEVAL_REQUESTS_TOTAL
from src.database import schemas
from src.database.models import Work


class RetrievalService:
    """Search ingested works and return evidence with citation metadata."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def search(self, request: schemas.RetrievalRequest) -> schemas.RetrievalResponse:
        start_time = time.perf_counter()
        try:
            evidence = self._search_works(request)
            RETRIEVAL_REQUESTS_TOTAL.labels("success").inc()
            return schemas.RetrievalResponse(
                question=request.question,
                retrieval_method="keyword",
                filters_applied=schemas.RetrievalAppliedFilters(
                    publication_year_min=request.publication_year_min,
                    publication_year_max=request.publication_year_max,
                    require_open_access=request.require_open_access,
                    work_type=request.work_type,
                    language=request.language,
                ),
                evidence=evidence,
                citations=[item.citation for item in evidence],
                result_count=len(evidence),
                grounding_status="retrieval_only",
            )
        except Exception:
            RETRIEVAL_REQUESTS_TOTAL.labels("error").inc()
            raise
        finally:
            RETRIEVAL_LATENCY_SECONDS.observe(time.perf_counter() - start_time)

    def _search_works(self, request: schemas.RetrievalRequest) -> list[schemas.EvidenceItem]:
        pattern = f"%{request.question.strip()}%"
        query = (
            self.db.query(Work)
            .options(joinedload(Work.source), joinedload(Work.authors), joinedload(Work.topics))
            .filter(or_(Work.title.ilike(pattern), Work.abstract.ilike(pattern)))
        )

        if request.publication_year_min is not None:
            query = query.filter(Work.publication_year >= request.publication_year_min)
        if request.publication_year_max is not None:
            query = query.filter(Work.publication_year <= request.publication_year_max)
        if request.require_open_access:
            query = query.filter(Work.open_access.is_(True))
        if request.work_type is not None:
            query = query.filter(Work.work_type == request.work_type)
        if request.language is not None:
            query = query.filter(Work.language == request.language)

        works = (
            query.order_by(Work.citation_count.desc(), Work.publication_year.desc().nullslast())
            .limit(request.limit)
            .all()
        )
        return [self._to_evidence_item(work, request.question) for work in works]

    @staticmethod
    def _to_evidence_item(work: Work, question: str) -> schemas.EvidenceItem:
        citation = schemas.CitationMetadata(
            openalex_id=work.openalex_id,
            title=work.title,
            doi=work.doi,
            source_url=work.source_url,
            publication_year=work.publication_year,
        )
        normalized_question = question.strip().lower()
        matched_fields = []
        if normalized_question and work.title and normalized_question in work.title.lower():
            matched_fields.append("title")
        if normalized_question and work.abstract and normalized_question in work.abstract.lower():
            matched_fields.append("abstract")
        return schemas.EvidenceItem(
            work_id=work.id,
            openalex_id=work.openalex_id,
            title=work.title,
            abstract=work.abstract,
            publication_year=work.publication_year,
            citation_count=work.citation_count or 0,
            source_name=work.source.name if work.source else None,
            author_names=[author.name for author in work.authors if author.name],
            topic_names=[topic.name for topic in work.topics if topic.name],
            retrieval_score=None,
            matched_fields=matched_fields,
            citation=citation,
        )
