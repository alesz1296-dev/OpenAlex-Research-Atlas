from src.database.schemas import CitationMetadata, EvidenceItem, RetrievalResponse
from src.evaluation.harness import LocalRetrievalEvaluator, RetrievalEvalCase


class FakeRetrievalService:
    def search(self, request):
        citation = CitationMetadata(
            openalex_id="https://openalex.org/W123",
            title="Reliable Retrieval",
            publication_year=2025,
        )
        return RetrievalResponse(
            question=request.question,
            evidence=[
                EvidenceItem(
                    work_id=1,
                    openalex_id="https://openalex.org/W123",
                    title="Reliable Retrieval",
                    abstract="Grounded evidence.",
                    publication_year=2025,
                    citation_count=10,
                    source_name=None,
                    citation=citation,
                )
            ],
            citations=[citation],
        )


def test_local_retrieval_eval_scores_expected_hits():
    evaluator = LocalRetrievalEvaluator(FakeRetrievalService())

    results = evaluator.run(
        [
            RetrievalEvalCase(
                question="reliable retrieval",
                expected_openalex_ids=["https://openalex.org/W123"],
            )
        ]
    )

    assert results[0].expected_hit_count == 1
    assert results[0].precision_at_k == 1.0
    assert results[0].citation_coverage == 1.0
