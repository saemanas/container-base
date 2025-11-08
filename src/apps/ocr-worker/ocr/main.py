"""Entrypoint module for the OCR worker."""
from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI

from . import pdpa
from .logging import get_logger, log_event

logger = get_logger()


async def _run_worker(stop_event: asyncio.Event) -> None:
    """Background worker loop placeholder for OCR processing."""
    log_event(logger, op_id="worker", code="START", duration_ms=0, message="OCR worker loop started")
    try:
        while not stop_event.is_set():
            await asyncio.sleep(60)
            log_event(logger, op_id="heartbeat", code="HEARTBEAT", duration_ms=0, message="OCR worker heartbeat")
    finally:
        log_event(logger, op_id="worker", code="STOP", duration_ms=0, message="OCR worker loop stopped")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for OCR worker."""

    try:
        sanitized_env = pdpa.validate_credentials(os.environ)
    except pdpa.ServiceRoleForbiddenError as exc:
        log_event(logger, op_id="startup", code="PDPA_DENY", duration_ms=0, message=str(exc))
        raise RuntimeError("OCR worker refused to start due to credential violation") from exc

    app.state.supabase_credentials = sanitized_env
    stop_event = asyncio.Event()
    worker_task: asyncio.Task[Any] = asyncio.create_task(_run_worker(stop_event))
    log_event(logger, op_id="startup", code="START", duration_ms=0, message="OCR worker service boot")

    try:
        yield
    finally:
        stop_event.set()
        await worker_task
        log_event(logger, op_id="shutdown", code="STOP", duration_ms=0, message="OCR worker service shutdown")


app = FastAPI(title="Container Base OCR Worker", version="0.1.0", lifespan=lifespan)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Liveness probe endpoint for Cloud Run."""
    log_event(logger, op_id="healthz", code="HEALTH", duration_ms=0, message="OCR worker liveness probe")
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    """Readiness probe endpoint for Cloud Run."""
    log_event(logger, op_id="readyz", code="READY", duration_ms=0, message="OCR worker readiness probe")
    return {"status": "ready"}


def main() -> None:
    """Run the OCR worker service under Uvicorn."""
    uvicorn.run(
        "ocr.main:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )


if __name__ == "__main__":
    main()
