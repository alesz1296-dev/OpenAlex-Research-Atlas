from src.ai.azure_openai import AzureOpenAIInferenceService
from src.database.schemas import CitationMetadata, EvidenceItem


class FakeResponse:
    content = "Reliable retrieval depends on grounded evidence [1]."
    usage_metadata = {"input_tokens": 10, "output_tokens": 8, "total_tokens": 18}


class FakeChatModel:
    def invoke(self, prompt: str):
        assert "Question:" in prompt
        assert "[1]" in prompt
        return FakeResponse()


def test_azure_inference_service_can_be_mocked_without_remote_call():
    evidence = [
        EvidenceItem(
            work_id=1,
            openalex_id="https://openalex.org/W1",
            title="Reliable Retrieval",
            abstract="A paper about grounded retrieval.",
            publication_year=2025,
            citation_count=3,
            source_name="Journal",
            citation=CitationMetadata(
                openalex_id="https://openalex.org/W1",
                title="Reliable Retrieval",
                publication_year=2025,
            ),
        )
    ]
    service = AzureOpenAIInferenceService(chat_model=FakeChatModel())

    result = service.generate_answer("What makes retrieval reliable?", evidence)

    assert result.grounding_status == "generated_from_evidence"
    assert "[1]" in result.answer


def test_azure_inference_returns_no_evidence_answer_without_model_call():
    service = AzureOpenAIInferenceService(chat_model=FakeChatModel())

    result = service.generate_answer("What makes retrieval reliable?", [])

    assert result.grounding_status == "no_evidence"
