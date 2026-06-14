"""add source linkage and ingestion errors

Revision ID: e71dd5afcc09
Revises: dcad9f50b14c
Create Date: 2026-06-14 12:58:42.757083
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision: str = 'e71dd5afcc09'
down_revision: Union[str, Sequence[str], None] = 'dcad9f50b14c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("works", sa.Column("source_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_works_source_id_sources",
        "works",
        "sources",
        ["source_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_table(
        "ingestion_errors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ingestion_run_id", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("stage", sa.String(length=50), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=False),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ingestion_run_id"], ["ingestion_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ingestion_errors_id"), "ingestion_errors", ["id"], unique=False)
    op.create_index(
        op.f("ix_ingestion_errors_ingestion_run_id"),
        "ingestion_errors",
        ["ingestion_run_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_ingestion_errors_ingestion_run_id"), table_name="ingestion_errors")
    op.drop_index(op.f("ix_ingestion_errors_id"), table_name="ingestion_errors")
    op.drop_table("ingestion_errors")

    op.drop_constraint("fk_works_source_id_sources", "works", type_="foreignkey")
    op.drop_column("works", "source_id")
