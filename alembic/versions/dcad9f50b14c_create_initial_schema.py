"""create initial schema

Revision ID: dcad9f50b14c
Revises: 
Create Date: 2026-06-14 12:39:32.454662
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision: str = 'dcad9f50b14c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ingestion_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("query_type", sa.String(length=50), nullable=False),
        sa.Column("query_params", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("record_count", sa.Integer(), nullable=True),
        sa.Column("error_count", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ingestion_runs_id"), "ingestion_runs", ["id"], unique=False)

    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("openalex_id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("orcid", sa.String(length=50), nullable=True),
        sa.Column("citation_count", sa.Integer(), nullable=True),
        sa.Column("works_count", sa.Integer(), nullable=True),
        sa.Column("h_index", sa.Integer(), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("orcid"),
    )
    op.create_index(op.f("ix_authors_id"), "authors", ["id"], unique=False)
    op.create_index(op.f("ix_authors_openalex_id"), "authors", ["openalex_id"], unique=True)

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("openalex_id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=True),
        sa.Column("issn", sa.String(length=20), nullable=True),
        sa.Column("issn_l", sa.String(length=20), nullable=True),
        sa.Column("publisher", sa.String(length=255), nullable=True),
        sa.Column("country_code", sa.String(length=2), nullable=True),
        sa.Column("homepage_url", sa.Text(), nullable=True),
        sa.Column("is_open_access", sa.Boolean(), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sources_id"), "sources", ["id"], unique=False)
    op.create_index(op.f("ix_sources_openalex_id"), "sources", ["openalex_id"], unique=True)

    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("openalex_id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("domain", sa.String(length=255), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("citation_count", sa.Integer(), nullable=True),
        sa.Column("works_count", sa.Integer(), nullable=True),
        sa.Column("keywords", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_topics_id"), "topics", ["id"], unique=False)
    op.create_index(op.f("ix_topics_openalex_id"), "topics", ["openalex_id"], unique=True)

    op.create_table(
        "works",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("openalex_id", sa.String(length=50), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("abstract", sa.Text(), nullable=True),
        sa.Column("doi", sa.String(length=255), nullable=True),
        sa.Column("publish_date", sa.DateTime(), nullable=True),
        sa.Column("publication_year", sa.Integer(), nullable=True),
        sa.Column("work_type", sa.String(length=50), nullable=True),
        sa.Column("language", sa.String(length=10), nullable=True),
        sa.Column("open_access", sa.Boolean(), nullable=True),
        sa.Column("citation_count", sa.Integer(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("pdf_url", sa.Text(), nullable=True),
        sa.Column("ingestion_run_id", sa.Integer(), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ingestion_run_id"], ["ingestion_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("doi"),
    )
    op.create_index(op.f("ix_works_id"), "works", ["id"], unique=False)
    op.create_index(op.f("ix_works_openalex_id"), "works", ["openalex_id"], unique=True)
    op.create_index(op.f("ix_works_publication_year"), "works", ["publication_year"], unique=False)

    op.create_table(
        "api_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("endpoint", sa.String(length=255), nullable=False),
        sa.Column("method", sa.String(length=10), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("response_time_ms", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("ingestion_run_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ingestion_run_id"], ["ingestion_runs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_api_logs_id"), "api_logs", ["id"], unique=False)

    op.create_table(
        "citations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_work_id", sa.Integer(), nullable=False),
        sa.Column("cited_work_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["cited_work_id"], ["works.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_work_id"], ["works.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_work_id", "cited_work_id", name="uq_citation"),
    )
    op.create_index(op.f("ix_citations_cited_work_id"), "citations", ["cited_work_id"], unique=False)
    op.create_index(op.f("ix_citations_id"), "citations", ["id"], unique=False)
    op.create_index(op.f("ix_citations_source_work_id"), "citations", ["source_work_id"], unique=False)

    op.create_table(
        "works_authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("work_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("author_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["authors.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["work_id"], ["works.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("work_id", "author_id", name="uq_work_author"),
    )
    op.create_index(op.f("ix_works_authors_author_id"), "works_authors", ["author_id"], unique=False)
    op.create_index(op.f("ix_works_authors_id"), "works_authors", ["id"], unique=False)
    op.create_index(op.f("ix_works_authors_work_id"), "works_authors", ["work_id"], unique=False)

    op.create_table(
        "works_topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("work_id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["work_id"], ["works.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("work_id", "topic_id", name="uq_work_topic"),
    )
    op.create_index(op.f("ix_works_topics_id"), "works_topics", ["id"], unique=False)
    op.create_index(op.f("ix_works_topics_topic_id"), "works_topics", ["topic_id"], unique=False)
    op.create_index(op.f("ix_works_topics_work_id"), "works_topics", ["work_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_works_topics_work_id"), table_name="works_topics")
    op.drop_index(op.f("ix_works_topics_topic_id"), table_name="works_topics")
    op.drop_index(op.f("ix_works_topics_id"), table_name="works_topics")
    op.drop_table("works_topics")

    op.drop_index(op.f("ix_works_authors_work_id"), table_name="works_authors")
    op.drop_index(op.f("ix_works_authors_id"), table_name="works_authors")
    op.drop_index(op.f("ix_works_authors_author_id"), table_name="works_authors")
    op.drop_table("works_authors")

    op.drop_index(op.f("ix_citations_source_work_id"), table_name="citations")
    op.drop_index(op.f("ix_citations_id"), table_name="citations")
    op.drop_index(op.f("ix_citations_cited_work_id"), table_name="citations")
    op.drop_table("citations")

    op.drop_index(op.f("ix_api_logs_id"), table_name="api_logs")
    op.drop_table("api_logs")

    op.drop_index(op.f("ix_works_publication_year"), table_name="works")
    op.drop_index(op.f("ix_works_openalex_id"), table_name="works")
    op.drop_index(op.f("ix_works_id"), table_name="works")
    op.drop_table("works")

    op.drop_index(op.f("ix_topics_openalex_id"), table_name="topics")
    op.drop_index(op.f("ix_topics_id"), table_name="topics")
    op.drop_table("topics")

    op.drop_index(op.f("ix_sources_openalex_id"), table_name="sources")
    op.drop_index(op.f("ix_sources_id"), table_name="sources")
    op.drop_table("sources")

    op.drop_index(op.f("ix_authors_openalex_id"), table_name="authors")
    op.drop_index(op.f("ix_authors_id"), table_name="authors")
    op.drop_table("authors")

    op.drop_index(op.f("ix_ingestion_runs_id"), table_name="ingestion_runs")
    op.drop_table("ingestion_runs")
