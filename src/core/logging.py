"""Structured logging setup for the API runtime."""

from __future__ import annotations

import logging
import sys

from pythonjsonlogger import jsonlogger

from src.core.config import settings


def configure_logging() -> None:
    """Configure root logging once with JSON output."""
    root_logger = logging.getLogger()
    if getattr(root_logger, "_openalex_json_logging", False):
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(method)s %(path)s %(status_code)s %(latency_ms)s"
    )
    handler.setFormatter(formatter)

    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.LOG_LEVEL.upper())
    root_logger._openalex_json_logging = True
