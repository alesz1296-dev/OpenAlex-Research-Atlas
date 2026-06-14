from __future__ import annotations

from urllib.error import URLError

import pytest

from src.database.models import Author, IngestionError, IngestionRun, Source, Topic, Work, WorkAuthor, WorkTopic
from src.ingestion.openalex import OpenAlexIngestionService


def make_work_payload() -> dict:
    return {
        "id": "https://openalex.org/W1234567890",
        "title": "Learning Reliable Scholarly Retrieval",
        "abstract_inverted_index": {
            "Learning": [0],
            "reliable": [1],
            "scholarly": [2],
            "retrieval": [3],
        },
        "doi": "https://doi.org/10.1234/example",
        "publication_date": "2025-02-01",
        "publication_year": 2025,
        "type": "article",
        "language": "en",
        "open_access": {"is_oa": True},
        "cited_by_count": 17,
        "primary_location": {
            "landing_page_url": "https://example.org/paper",
            "pdf_url": "https://example.org/paper.pdf",
            "source": {
                "id": "https://openalex.org/S123456789",
                "display_name": "Journal of Retrieval Systems",
                "type": "journal",
                "issn": ["1234-5678"],
                "issn_l": "1234-5678",
                "host_organization_name": "OpenAlex Press",
                "homepage_url": "https://example.org/journal",
                "is_oa": True,
            },
        },
        "authorships": [
            {"author": {"id": "https://openalex.org/A1", "display_name": "Ada Scholar", "orcid": "0000-0001"}},
            {"author": {"id": "https://openalex.org/A2", "display_name": "Turing Researcher"}},
        ],
        "topics": [
            {
                "id": "https://openalex.org/T1",
                "display_name": "Retrieval-Augmented Generation",
                "description": "Grounded retrieval for generation.",
                "domain": {"display_name": "Computer Science"},
                "level": 1,
                "cited_by_count": 100,
                "works_count": 20,
                "score": 0.98,
                "keywords": [{"display_name": "retrieval"}, {"display_name": "grounding"}],
            }
        ],
    }


class FakeClient:
    def __init__(self, payloads_or_errors):
        self.payloads_or_errors = list(payloads_or_errors)

    def fetch_work(self, openalex_id: str) -> dict:
        next_item = self.payloads_or_errors.pop(0)
        if isinstance(next_item, Exception):
            raise next_item
        return next_item


def test_ingest_same_work_twice_upserts_without_duplicates(db_session):
    payload = make_work_payload()
    service = OpenAlexIngestionService(db_session, client=FakeClient([payload, payload]))

    first_result = service.ingest_work_by_openalex_id("W1234567890")
    second_result = service.ingest_work_by_openalex_id("W1234567890")

    assert first_result.created is True
    assert second_result.created is False

    assert db_session.query(Work).count() == 1
    assert db_session.query(Source).count() == 1
    assert db_session.query(Author).count() == 2
    assert db_session.query(Topic).count() == 1
    assert db_session.query(WorkAuthor).count() == 2
    assert db_session.query(WorkTopic).count() == 1
    assert db_session.query(IngestionRun).count() == 2
    assert db_session.query(IngestionError).count() == 0


def test_retryable_fetch_error_can_be_retried(db_session):
    payload = make_work_payload()
    service = OpenAlexIngestionService(
        db_session,
        client=FakeClient([URLError("temporary network issue"), payload]),
    )

    with pytest.raises(URLError):
        service.ingest_work_by_openalex_id("W1234567890")

    error = db_session.query(IngestionError).one()
    assert error.stage == "fetch"
    assert error.retryable is True
    assert error.error_type == "network_error"

    retry_result = service.retry_ingestion_error(error.id)

    assert retry_result.created is True
    assert db_session.query(Work).count() == 1
    assert db_session.query(IngestionRun).count() == 2
