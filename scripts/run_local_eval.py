"""Run the local retrieval evaluation harness.

This script does not call Azure OpenAI. It evaluates retrieval behavior against
the current PostgreSQL database.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.database.session import SessionLocal
from src.evaluation.harness import LocalRetrievalEvaluator, RetrievalEvalCase
from src.retrieval.service import RetrievalService


def load_cases(path: Path) -> list[RetrievalEvalCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [RetrievalEvalCase(**item) for item in payload]


def main() -> None:
    cases = load_cases(Path("evals/retrieval_seed.json"))
    with SessionLocal() as db:
        evaluator = LocalRetrievalEvaluator(RetrievalService(db))
        results = evaluator.run(cases)

    print(json.dumps([result.__dict__ for result in results], indent=2))


if __name__ == "__main__":
    main()
