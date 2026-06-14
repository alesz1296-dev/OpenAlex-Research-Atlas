"""add ingestion retry metadata

Revision ID: ccb7e9e6f18a
Revises: e71dd5afcc09
Create Date: 2026-06-14 13:11:42.720425
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'ccb7e9e6f18a'
down_revision: Union[str, Sequence[str], None] = 'e71dd5afcc09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("ingestion_errors", sa.Column("error_type", sa.String(length=100), nullable=True))
    op.add_column("ingestion_errors", sa.Column("retryable", sa.Boolean(), nullable=True))

    op.execute("UPDATE ingestion_errors SET error_type = 'unexpected_error' WHERE error_type IS NULL")
    op.execute("UPDATE ingestion_errors SET retryable = false WHERE retryable IS NULL")

    op.alter_column("ingestion_errors", "error_type", nullable=False)
    op.alter_column("ingestion_errors", "retryable", nullable=False)


def downgrade() -> None:
    op.drop_column("ingestion_errors", "retryable")
    op.drop_column("ingestion_errors", "error_type")
