"""Azure OpenAI inference adapter.

The adapter is lazy by design: importing the application or running CI should
not create a client or make paid calls. Real calls happen only when explicitly
enabled and invoked.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from src.core.config import settings
from src.core.observability import AZURE_OPENAI_CALLS_TOTAL, AZURE_OPENAI_TOKENS_TOTAL
from src.database.schemas import EvidenceItem


@dataclass(frozen=True)
class GeneratedAnswer:
    question: str
    answer: str
    grounding_status: str


class AzureOpenAIInferenceService:
    """Generate cited answers from already-retrieved evidence."""

    def __init__(self, chat_model=None) -> None:
        self._chat_model = chat_model

    def generate_answer(self, question: str, evidence: list[EvidenceItem]) -> GeneratedAnswer:
        if not evidence:
            return GeneratedAnswer(
                question=question,
                answer="I do not have enough retrieved evidence to answer this question.",
                grounding_status="no_evidence",
            )

        model = self._chat_model or self._build_chat_model()
        prompt = self._build_prompt(question, evidence)
        start_time = time.perf_counter()
        try:
            response = model.invoke(prompt)
            AZURE_OPENAI_CALLS_TOTAL.labels("success").inc()
            self._record_token_usage(response)
            answer = getattr(response, "content", str(response))
            return GeneratedAnswer(question=question, answer=answer, grounding_status="generated_from_evidence")
        except Exception:
            AZURE_OPENAI_CALLS_TOTAL.labels("error").inc()
            raise
        finally:
            _ = time.perf_counter() - start_time

    @staticmethod
    def _build_prompt(question: str, evidence: list[EvidenceItem]) -> str:
        evidence_lines = []
        for index, item in enumerate(evidence, start=1):
            evidence_lines.append(
                f"[{index}] {item.title} ({item.publication_year}). "
                f"OpenAlex: {item.openalex_id}. Abstract: {item.abstract or 'No abstract available.'}"
            )

        return (
            "Answer the research question using only the evidence below. "
            "Cite evidence with bracket numbers like [1]. If evidence is insufficient, say so.\n\n"
            f"Question: {question}\n\n"
            "Evidence:\n"
            + "\n".join(evidence_lines)
        )

    @staticmethod
    def _build_chat_model():
        if not settings.AZURE_OPENAI_ENABLED:
            raise RuntimeError("Azure OpenAI inference is disabled. Set AZURE_OPENAI_ENABLED=true to enable it.")
        if not settings.AZURE_OPENAI_ENDPOINT or not settings.AZURE_OPENAI_API_KEY:
            raise RuntimeError("Azure OpenAI endpoint and API key must be configured.")
        if not settings.AZURE_OPENAI_CHAT_DEPLOYMENT:
            raise RuntimeError("Azure OpenAI chat deployment must be configured.")

        from langchain_openai import AzureChatOpenAI

        return AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
            timeout=settings.AZURE_OPENAI_TIMEOUT_SECONDS,
            max_retries=settings.AZURE_OPENAI_MAX_RETRIES,
            temperature=settings.AZURE_OPENAI_TEMPERATURE,
            max_tokens=settings.AZURE_OPENAI_MAX_TOKENS,
        )

    @staticmethod
    def _record_token_usage(response) -> None:
        usage = getattr(response, "usage_metadata", None) or {}
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        total_tokens = usage.get("total_tokens")
        if input_tokens:
            AZURE_OPENAI_TOKENS_TOTAL.labels("input").inc(input_tokens)
        if output_tokens:
            AZURE_OPENAI_TOKENS_TOTAL.labels("output").inc(output_tokens)
        if total_tokens:
            AZURE_OPENAI_TOKENS_TOTAL.labels("total").inc(total_tokens)
