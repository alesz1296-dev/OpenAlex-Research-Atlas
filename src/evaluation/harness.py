"""Local evaluation harness for retrieval quality."""

from __future__ import annotations

from dataclasses import dataclass

from src.core.observability import EVAL_RUNS_TOTAL
from src.database.schemas import RetrievalRequest, RetrievalResponse


@dataclass(frozen=True)
class RetrievalEvalCase:
    question: str
    expected_openalex_ids: list[str]
    limit: int = 5


@dataclass(frozen=True)
class RetrievalEvalResult:
    question: str
    expected_openalex_ids: list[str]
    returned_openalex_ids: list[str]
    expected_hit_count: int
    precision_at_k: float
    citation_coverage: float


class LocalRetrievalEvaluator:
    """Run deterministic retrieval checks without paid model calls."""

    def __init__(self, retrieval_service) -> None:
        self.retrieval_service = retrieval_service

    def run(self, cases: list[RetrievalEvalCase]) -> list[RetrievalEvalResult]:
        try:
            results = [self._run_case(case) for case in cases]
            EVAL_RUNS_TOTAL.labels("success").inc()
            return results
        except Exception:
            EVAL_RUNS_TOTAL.labels("error").inc()
            raise

    def _run_case(self, case: RetrievalEvalCase) -> RetrievalEvalResult:
        response: RetrievalResponse = self.retrieval_service.search(
            RetrievalRequest(question=case.question, limit=case.limit)
        )
        returned_ids = [item.openalex_id for item in response.evidence]
        expected = set(case.expected_openalex_ids)
        hits = [openalex_id for openalex_id in returned_ids if openalex_id in expected]
        precision_at_k = len(hits) / max(len(returned_ids), 1)
        citation_coverage = len(response.citations) / max(len(response.evidence), 1)

        return RetrievalEvalResult(
            question=case.question,
            expected_openalex_ids=case.expected_openalex_ids,
            returned_openalex_ids=returned_ids,
            expected_hit_count=len(hits),
            precision_at_k=precision_at_k,
            citation_coverage=citation_coverage,
        )
