"""Prometheus metrics and request observability helpers."""

from __future__ import annotations

import time
import uuid
import logging
from collections.abc import Callable

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import settings

logger = logging.getLogger(__name__)


HTTP_REQUESTS_TOTAL = Counter(
    "openalex_http_requests_total",
    "Total API requests.",
    ["method", "path", "status_code"],
)
HTTP_REQUEST_LATENCY_SECONDS = Histogram(
    "openalex_http_request_latency_seconds",
    "API request latency in seconds.",
    ["method", "path"],
)
INGESTION_RUNS_TOTAL = Counter(
    "openalex_ingestion_runs_total",
    "OpenAlex ingestion runs by status.",
    ["status"],
)
RETRIEVAL_REQUESTS_TOTAL = Counter(
    "openalex_retrieval_requests_total",
    "Retrieval requests by status.",
    ["status"],
)
RETRIEVAL_LATENCY_SECONDS = Histogram(
    "openalex_retrieval_latency_seconds",
    "Retrieval latency in seconds.",
)
AZURE_OPENAI_CALLS_TOTAL = Counter(
    "openalex_azure_openai_calls_total",
    "Azure OpenAI calls by status.",
    ["status"],
)
AZURE_OPENAI_TOKENS_TOTAL = Counter(
    "openalex_azure_openai_tokens_total",
    "Azure OpenAI token usage by token type.",
    ["token_type"],
)
EVAL_RUNS_TOTAL = Counter(
    "openalex_eval_runs_total",
    "Local evaluation runs by status.",
    ["status"],
)


class RequestObservabilityMiddleware(BaseHTTPMiddleware):
    """Attach request IDs and record HTTP metrics for every API request."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get(settings.API_REQUEST_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers[settings.API_REQUEST_ID_HEADER] = request_id
            return response
        finally:
            latency = time.perf_counter() - start_time
            route = request.scope.get("route")
            path = getattr(route, "path", request.url.path)
            HTTP_REQUESTS_TOTAL.labels(request.method, path, str(status_code)).inc()
            HTTP_REQUEST_LATENCY_SECONDS.labels(request.method, path).observe(latency)
            logger.info(
                "API request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": path,
                    "status_code": status_code,
                    "latency_ms": round(latency * 1000, 2),
                },
            )


def metrics_response() -> Response:
    """Return Prometheus exposition text."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
