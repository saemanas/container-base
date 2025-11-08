"""FastAPI application skeleton for Container Base API."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from . import pdpa
from .logging import get_logger, log_event

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler to log startup/shutdown events."""

    log_event(logger, op_id="startup", code="START", duration_ms=0, message="API service boot")
    try:
        yield
    finally:
        log_event(logger, op_id="shutdown", code="STOP", duration_ms=0, message="API service shutdown")


app = FastAPI(title="Container Base API", version="0.1.0", lifespan=lifespan)


@app.middleware("http")
async def enforce_pdpa(request: Request, call_next):
    """Apply PDPA consent, email masking, and GPS rounding for non-health routes."""

    if request.url.path in {"/healthz", "/readyz"}:
        return await call_next(request)

    consent_status = request.headers.get("x-pdpa-consent-status")
    consent_record: pdpa.ConsentRecord | None = None
    if consent_status:
        consent_record = pdpa.ConsentRecord(
            user_id=request.headers.get("x-user-id", "unknown"),
            consented_at=request.headers.get("x-pdpa-consent-at", "1970-01-01T00:00:00Z"),
            revoked_at=None if consent_status.lower() == "active" else "revoked",
        )

    try:
        request.state.consent_record = pdpa.require_consent(consent_record)
    except pdpa.ConsentMissingError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    email = request.headers.get("x-user-email")
    if email:
        request.state.masked_email = pdpa.mask_email(email)

    lat = request.headers.get("x-gps-lat")
    lon = request.headers.get("x-gps-lon")
    if lat and lon:
        try:
            request.state.rounded_gps = pdpa.round_gps(float(lat), float(lon))
        except ValueError:
            pass

    response = await call_next(request)

    if hasattr(request.state, "masked_email"):
        response.headers["x-user-email"] = request.state.masked_email
    if hasattr(request.state, "rounded_gps"):
        lat_val, lon_val = request.state.rounded_gps
        response.headers["x-gps-lat"] = f"{lat_val:.3f}"
        response.headers["x-gps-lon"] = f"{lon_val:.3f}"

    return response

@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Liveness probe endpoint."""
    log_event(logger, op_id="healthz", code="HEALTH", duration_ms=0, message="API liveness probe")
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    """Readiness probe endpoint."""
    log_event(logger, op_id="readyz", code="READY", duration_ms=0, message="API readiness probe")
    return {"status": "ok"}
