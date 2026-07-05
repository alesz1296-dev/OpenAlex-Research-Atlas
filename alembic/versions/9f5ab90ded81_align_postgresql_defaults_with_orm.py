"""align PostgreSQL defaults with ORM and SQL reference

Revision ID: 9f5ab90ded81
Revises: ccb7e9e6f18a
Create Date: 2026-07-04 10:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f5ab90ded81"
down_revision: Union[str, Sequence[str], None] = "ccb7e9e6f18a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Backfill ingestion run metadata before tightening defaults/nullability.
    op.execute("UPDATE ingestion_runs SET record_count = 0 WHERE record_count IS NULL")
    op.execute("UPDATE ingestion_runs SET error_count = 0 WHERE error_count IS NULL")
    op.execute("UPDATE ingestion_runs SET started_at = CURRENT_TIMESTAMP WHERE started_at IS NULL")
    op.execute("UPDATE ingestion_runs SET status = 'running' WHERE status IS NULL")

    op.alter_column(
        "ingestion_runs",
        "record_count",
        existing_type=sa.Integer(),
        nullable=False,
        server_default=sa.text("0"),
    )
    op.alter_column(
        "ingestion_runs",
        "error_count",
        existing_type=sa.Integer(),
        nullable=False,
        server_default=sa.text("0"),
    )
    op.alter_column(
        "ingestion_runs",
        "started_at",
        existing_type=sa.DateTime(),
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    op.alter_column(
        "ingestion_runs",
        "status",
        existing_type=sa.String(length=50),
        nullable=False,
        server_default=sa.text("'running'"),
    )

    # Add missing server defaults for entity tables so inserts behave correctly
    # even when they bypass SQLAlchemy's Python-side defaults.
    op.execute("UPDATE works SET language = 'en' WHERE language IS NULL")
    op.execute("UPDATE works SET open_access = false WHERE open_access IS NULL")
    op.execute("UPDATE works SET citation_count = 0 WHERE citation_count IS NULL")
    op.execute("UPDATE works SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.execute("UPDATE works SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
    op.alter_column("works", "language", existing_type=sa.String(length=10), server_default=sa.text("'en'"))
    op.alter_column("works", "open_access", existing_type=sa.Boolean(), server_default=sa.text("false"))
    op.alter_column("works", "citation_count", existing_type=sa.Integer(), server_default=sa.text("0"))
    op.alter_column("works", "created_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))
    op.alter_column("works", "updated_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))

    op.execute("UPDATE authors SET citation_count = 0 WHERE citation_count IS NULL")
    op.execute("UPDATE authors SET works_count = 0 WHERE works_count IS NULL")
    op.execute("UPDATE authors SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.execute("UPDATE authors SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
    op.alter_column("authors", "citation_count", existing_type=sa.Integer(), server_default=sa.text("0"))
    op.alter_column("authors", "works_count", existing_type=sa.Integer(), server_default=sa.text("0"))
    op.alter_column("authors", "created_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))
    op.alter_column("authors", "updated_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))

    op.execute("UPDATE topics SET citation_count = 0 WHERE citation_count IS NULL")
    op.execute("UPDATE topics SET works_count = 0 WHERE works_count IS NULL")
    op.execute("UPDATE topics SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.execute("UPDATE topics SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
    op.alter_column("topics", "citation_count", existing_type=sa.Integer(), server_default=sa.text("0"))
    op.alter_column("topics", "works_count", existing_type=sa.Integer(), server_default=sa.text("0"))
    op.alter_column("topics", "created_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))
    op.alter_column("topics", "updated_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))

    op.execute("UPDATE sources SET is_open_access = false WHERE is_open_access IS NULL")
    op.execute("UPDATE sources SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.execute("UPDATE sources SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
    op.alter_column("sources", "is_open_access", existing_type=sa.Boolean(), server_default=sa.text("false"))
    op.alter_column("sources", "created_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))
    op.alter_column("sources", "updated_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))

    op.execute("UPDATE api_logs SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.alter_column("api_logs", "created_at", existing_type=sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"))

    op.execute("UPDATE ingestion_errors SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.alter_column("ingestion_errors", "retryable", existing_type=sa.Boolean(), server_default=sa.text("false"))
    op.alter_column(
        "ingestion_errors",
        "created_at",
        existing_type=sa.DateTime(),
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )


def downgrade() -> None:
    op.alter_column("ingestion_errors", "created_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("ingestion_errors", "retryable", existing_type=sa.Boolean(), server_default=None)

    op.alter_column("api_logs", "created_at", existing_type=sa.DateTime(), server_default=None)

    op.alter_column("sources", "updated_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("sources", "created_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("sources", "is_open_access", existing_type=sa.Boolean(), server_default=None)

    op.alter_column("topics", "updated_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("topics", "created_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("topics", "works_count", existing_type=sa.Integer(), server_default=None)
    op.alter_column("topics", "citation_count", existing_type=sa.Integer(), server_default=None)

    op.alter_column("authors", "updated_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("authors", "created_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("authors", "works_count", existing_type=sa.Integer(), server_default=None)
    op.alter_column("authors", "citation_count", existing_type=sa.Integer(), server_default=None)

    op.alter_column("works", "updated_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("works", "created_at", existing_type=sa.DateTime(), server_default=None)
    op.alter_column("works", "citation_count", existing_type=sa.Integer(), server_default=None)
    op.alter_column("works", "open_access", existing_type=sa.Boolean(), server_default=None)
    op.alter_column("works", "language", existing_type=sa.String(length=10), server_default=None)

    op.alter_column("ingestion_runs", "status", existing_type=sa.String(length=50), nullable=True, server_default=None)
    op.alter_column("ingestion_runs", "started_at", existing_type=sa.DateTime(), nullable=True, server_default=None)
    op.alter_column("ingestion_runs", "error_count", existing_type=sa.Integer(), nullable=True, server_default=None)
    op.alter_column("ingestion_runs", "record_count", existing_type=sa.Integer(), nullable=True, server_default=None)
