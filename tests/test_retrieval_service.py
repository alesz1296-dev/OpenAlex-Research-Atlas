from __future__ import annotations

from src.database.models import Author, Source, Topic, Work
from src.database.schemas import RetrievalRequest
from src.retrieval.service import RetrievalService


def _make_work(
    *,
    openalex_id: str,
    title: str,
    abstract: str,
    publication_year: int,
    citation_count: int,
    open_access: bool,
    work_type: str,
    language: str,
    source_name: str = "Journal of Retrieval",
    author_names: list[str] | None = None,
    topic_names: list[str] | None = None,
) -> Work:
    work = Work(
        openalex_id=openalex_id,
        title=title,
        abstract=abstract,
        publication_year=publication_year,
        citation_count=citation_count,
        open_access=open_access,
        work_type=work_type,
        language=language,
        source_url=f"https://example.org/{openalex_id.rsplit('/', 1)[-1]}",
    )
    work.source = Source(
        openalex_id=f"https://openalex.org/S{openalex_id.rsplit('/', 1)[-1]}",
        name=source_name,
        source_type="journal",
    )
    work.authors = [Author(openalex_id=f"https://openalex.org/A{index}", name=name) for index, name in enumerate(author_names or [], start=1)]
    work.topics = [Topic(openalex_id=f"https://openalex.org/T{index}", name=name) for index, name in enumerate(topic_names or [], start=1)]
    return work


def test_retrieval_service_orders_by_citation_count_then_publication_year(db_session):
    works = [
        _make_work(
            openalex_id="https://openalex.org/W1",
            title="Reliable Retrieval Foundations",
            abstract="retrieval evidence fundamentals",
            publication_year=2022,
            citation_count=20,
            open_access=True,
            work_type="article",
            language="en",
            author_names=["Ada Scholar"],
            topic_names=["Retrieval"],
        ),
        _make_work(
            openalex_id="https://openalex.org/W2",
            title="Reliable Retrieval Systems",
            abstract="retrieval systems and ranking",
            publication_year=2025,
            citation_count=20,
            open_access=True,
            work_type="article",
            language="en",
            author_names=["Grace Researcher"],
            topic_names=["Ranking"],
        ),
        _make_work(
            openalex_id="https://openalex.org/W3",
            title="Reliable Retrieval at Scale",
            abstract="retrieval systems at scale",
            publication_year=2020,
            citation_count=30,
            open_access=False,
            work_type="preprint",
            language="en",
            author_names=["Lin Architect"],
            topic_names=["Scale"],
        ),
    ]
    db_session.add_all(works)
    db_session.commit()

    response = RetrievalService(db_session).search(RetrievalRequest(question="retrieval", limit=5))

    assert response.retrieval_method == "keyword"
    assert response.result_count == 3
    assert [item.openalex_id for item in response.evidence] == [
        "https://openalex.org/W3",
        "https://openalex.org/W2",
        "https://openalex.org/W1",
    ]
    assert response.citations[0].openalex_id == "https://openalex.org/W3"
    assert response.evidence[0].matched_fields == ["title", "abstract"]


def test_retrieval_service_applies_filters_and_returns_rich_evidence(db_session):
    works = [
        _make_work(
            openalex_id="https://openalex.org/W10",
            title="Reliable Retrieval for Articles",
            abstract="retrieval with grounded evidence",
            publication_year=2025,
            citation_count=15,
            open_access=True,
            work_type="article",
            language="en",
            author_names=["Ada Scholar", "Grace Researcher"],
            topic_names=["Retrieval", "Grounding"],
        ),
        _make_work(
            openalex_id="https://openalex.org/W11",
            title="Reliable Retrieval for Preprints",
            abstract="retrieval with early findings",
            publication_year=2025,
            citation_count=50,
            open_access=True,
            work_type="preprint",
            language="en",
        ),
        _make_work(
            openalex_id="https://openalex.org/W12",
            title="Reliable Retrieval in Spanish",
            abstract="retrieval con evidencia",
            publication_year=2025,
            citation_count=40,
            open_access=True,
            work_type="article",
            language="es",
        ),
        _make_work(
            openalex_id="https://openalex.org/W13",
            title="Reliable Retrieval but Closed Access",
            abstract="retrieval with limited access",
            publication_year=2025,
            citation_count=60,
            open_access=False,
            work_type="article",
            language="en",
        ),
        _make_work(
            openalex_id="https://openalex.org/W14",
            title="Older Reliable Retrieval",
            abstract="retrieval history",
            publication_year=2021,
            citation_count=80,
            open_access=True,
            work_type="article",
            language="en",
        ),
    ]
    db_session.add_all(works)
    db_session.commit()

    response = RetrievalService(db_session).search(
        RetrievalRequest(
            question="retrieval",
            limit=5,
            publication_year_min=2024,
            publication_year_max=2025,
            require_open_access=True,
            work_type="article",
            language="en",
        )
    )

    assert response.result_count == 1
    assert response.filters_applied.publication_year_min == 2024
    assert response.filters_applied.publication_year_max == 2025
    assert response.filters_applied.require_open_access is True
    assert response.filters_applied.work_type == "article"
    assert response.filters_applied.language == "en"

    evidence = response.evidence[0]
    assert evidence.openalex_id == "https://openalex.org/W10"
    assert evidence.author_names == ["Ada Scholar", "Grace Researcher"]
    assert evidence.topic_names == ["Retrieval", "Grounding"]
    assert evidence.source_name == "Journal of Retrieval"
    assert evidence.citation.openalex_id == "https://openalex.org/W10"
    assert response.citations == [evidence.citation]
