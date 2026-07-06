"""LangChain document mapping for retrieval-ready scholarly records."""

from __future__ import annotations

from langchain_core.documents import Document

from src.database.models import Work


def work_to_document(work: Work) -> Document:
    """Convert one persisted OpenAlex work into one LangChain Document."""
    title = (work.title or "").strip() or "Untitled work"
    abstract = (work.abstract or "").strip()
    source_name = work.source.name.strip() if work.source and work.source.name else ""
    author_names = [author.name.strip() for author in work.authors if author.name]
    topic_names = [topic.name.strip() for topic in work.topics if topic.name]

    page_content = (
        f"Title: {title}\n\n"
        f"Abstract:\n{abstract}\n\n"
        f"Topics:\n{'; '.join(topic_names)}\n\n"
        f"Source:\n{source_name}"
    )

    metadata = {
        "retrieval_document_type": "openalex_work",
        "work_id": work.id,
        "openalex_id": work.openalex_id,
        "title": title,
        "doi": work.doi,
        "publication_year": work.publication_year,
        "publish_date": work.publish_date.isoformat() if work.publish_date else None,
        "work_type": work.work_type,
        "language": work.language,
        "open_access": work.open_access,
        "citation_count": work.citation_count or 0,
        "source_openalex_id": work.source.openalex_id if work.source else None,
        "source_name": source_name or None,
        "source_type": work.source.source_type if work.source else None,
        "source_url": work.source_url,
        "pdf_url": work.pdf_url,
        "author_names": author_names,
        "topic_names": topic_names,
        "ingestion_run_id": work.ingestion_run_id,
        "citation_openalex_id": work.openalex_id,
        "citation_title": title,
        "citation_doi": work.doi,
        "citation_source_url": work.source_url,
        "citation_publication_year": work.publication_year,
    }
    return Document(page_content=page_content, metadata=metadata)
