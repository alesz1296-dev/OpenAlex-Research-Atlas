from datetime import datetime

from src.database.models import Author, Source, Topic, Work
from src.retrieval.documents import work_to_document


def test_work_to_document_maps_page_content_and_metadata():
    work = Work(
        id=1,
        openalex_id="https://openalex.org/W1",
        title="Reliable Retrieval",
        abstract="Evidence should be grounded.",
        doi="https://doi.org/10.1000/test",
        publish_date=datetime(2025, 1, 15),
        publication_year=2025,
        work_type="article",
        language="en",
        open_access=True,
        citation_count=42,
        source_url="https://openalex.org/W1",
        pdf_url="https://example.org/paper.pdf",
        ingestion_run_id=7,
    )
    work.source = Source(openalex_id="https://openalex.org/S1", name="Journal of Reliability", source_type="journal")
    work.authors = [Author(name="Ada Lovelace"), Author(name="Grace Hopper")]
    work.topics = [Topic(name="Retrieval"), Topic(name="Grounding")]

    document = work_to_document(work)

    assert "Title: Reliable Retrieval" in document.page_content
    assert "Evidence should be grounded." in document.page_content
    assert document.metadata["retrieval_document_type"] == "openalex_work"
    assert document.metadata["author_names"] == ["Ada Lovelace", "Grace Hopper"]
    assert document.metadata["topic_names"] == ["Retrieval", "Grounding"]
    assert document.metadata["citation_openalex_id"] == "https://openalex.org/W1"
