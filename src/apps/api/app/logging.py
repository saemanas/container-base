"""Structured logging utilities for the Container Base API."""
from __future__ import annotations

import datetime as dt
import json
import logging
import sys
from typing import Any, TypedDict


class LogPayload(TypedDict, total=False):
    ts: str
    opId: str
    code: str
    duration_ms: int
    message: str



def get_logger() -> logging.Logger:
    """Return a configured logger that emits JSON lines."""
    logger = logging.getLogger("container_base.api")
    if logger.handlers:
        # Logger already initialised elsewhere in the process; reuse existing configuration.
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    # Prevent duplicate messages in the root logger when running under Uvicorn/Gunicorn.
    logger.propagate = False

    return logger


def log_event(
    logger: logging.Logger,
    *,
    op_id: str,
    code: str,
    duration_ms: int,
    message: str,
    ts: str | None = None,
    **extra: Any,
) -> None:
    """Emit a structured log following `{ ts, opId, code, duration_ms }` schema."""
    payload: LogPayload = {
        "ts": ts or dt.datetime.now(dt.UTC).isoformat(),
        "opId": op_id,
        "code": code,
        "duration_ms": duration_ms,
        "message": message,
    }
    if extra:
        # Allow callers to attach contextual fields (e.g. request IDs) while keeping schema optional.
        payload.update(extra)

    logger.info(json.dumps(payload, separators=(",", ":")))
