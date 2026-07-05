"""
Run one OpenAlex work ingestion from the command line.

Example:
python scripts/ingest_one_work.py W2741809807
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

def _bootstrap_project_root() -> None:
    """Make the project root importable for direct script execution."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


_bootstrap_project_root()

from src.database.session import SessionLocal  # noqa: E402
from src.ingestion.openalex import OpenAlexIngestionService  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest one OpenAlex work into PostgreSQL.")
    parser.add_argument("openalex_id", help="OpenAlex work id, e.g. W2741809807")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        service = OpenAlexIngestionService(db)
        result = service.ingest_work_by_openalex_id(args.openalex_id)
        print(
            f"Ingestion run {result.ingestion_run_id} stored work {result.work_openalex_id} "
            f"(db id={result.work_id}, created={result.created}, authors={result.authors_synced}, "
            f"topics={result.topics_synced}, source_synced={result.source_synced})"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
