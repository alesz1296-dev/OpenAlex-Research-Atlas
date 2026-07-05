"""FastAPI application factory for OpenAlex Research Atlas."""

from __future__ import annotations

import logging
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.api.routes import router
from src.core.config import settings
from src.core.logging import configure_logging
from src.core.observability import RequestObservabilityMiddleware, metrics_response
from src.database.session import SessionLocal

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create the API app with production-oriented middleware and handlers."""
    configure_logging()

    api = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        debug=settings.DEBUG,
    )
    api.add_middleware(RequestObservabilityMiddleware)
    api.include_router(router)

    @api.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return _error_response(request, exc.status_code, "http_error", exc.detail)

    @api.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return _error_response(request, 422, "validation_error", exc.errors())

    @api.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled API error",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "method": request.method,
                "path": request.url.path,
                "status_code": 500,
            },
        )
        return _error_response(request, 500, "internal_server_error", "Unexpected server error")

    return api


def _error_response(request: Request, status_code: int, error_code: str, detail) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "detail": detail,
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )


app = create_app()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.API_TITLE}


@app.get("/ready")
def ready() -> JSONResponse:
    start_time = perf_counter()
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        latency_ms = round((perf_counter() - start_time) * 1000, 2)
        return JSONResponse({"status": "ready", "database": "ok", "latency_ms": latency_ms})
    except SQLAlchemyError as exc:
        logger.warning("Readiness check failed", extra={"error": str(exc)})
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": "error", "detail": "Database is not reachable"},
        )


@app.get("/version")
def version() -> dict:
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/metrics")
def metrics():
    return metrics_response()
