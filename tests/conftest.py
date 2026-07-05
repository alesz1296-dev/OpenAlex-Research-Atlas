"""
PostgreSQL-backed pytest fixtures for Phase 1 ingestion tests.

These fixtures intentionally use PostgreSQL rather than SQLite so the tests
exercise the same JSONB/ARRAY-capable database family used by the project.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from src.database.models import Base


def _get_test_database_url() -> str:
    test_database_url = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not test_database_url:
        pytest.skip("Set TEST_DATABASE_URL to run PostgreSQL integration tests.")
    if "user:password@" in test_database_url:
        pytest.skip("Replace the placeholder DATABASE_URL before running PostgreSQL integration tests.")
    if (
        os.getenv("ENVIRONMENT", "development") == "development"
        and os.getenv("DATABASE_URL") == test_database_url
    ):
        pytest.skip("Use a separate TEST_DATABASE_URL for destructive PostgreSQL integration tests.")
    return test_database_url


def _build_alembic_config(database_url: str) -> Config:
    project_root = Path(__file__).resolve().parents[1]
    config = Config(str(project_root / "alembic.ini"))
    os.environ["DATABASE_URL"] = database_url
    os.environ["ALEMBIC_DATABASE_URL"] = database_url
    config.set_main_option("script_location", str(project_root / "alembic"))
    return config


@pytest.fixture(scope="session")
def test_engine():
    database_url = _get_test_database_url()
    engine = create_engine(database_url, future=True)
    alembic_config = _build_alembic_config(database_url)

    # Phase 1 tests should validate the migration-owned schema, not only ORM metadata.
    command.upgrade(alembic_config, "head")
    yield engine
    command.downgrade(alembic_config, "base")
    engine.dispose()


@pytest.fixture()
def db_session(test_engine) -> Session:
    session_factory = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)
    session = session_factory()

    table_names = ", ".join(table.name for table in Base.metadata.sorted_tables)
    session.execute(text(f"TRUNCATE {table_names} RESTART IDENTITY CASCADE"))
    session.commit()

    try:
        yield session
    finally:
        session.close()
