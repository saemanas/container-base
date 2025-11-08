"""PDPA enforcement helpers for the Container Base API."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, Field, ValidationError

__all__ = [
    "ConsentMissingError",
    "ConsentRecord",
    "require_consent",
    "mask_email",
    "round_gps",
]


class ConsentMissingError(RuntimeError):
    """Raised when an incoming request lacks a valid consent record."""


class ConsentRecord(BaseModel):
    """Pydantic model describing a PDPA consent record."""

    user_id: str = Field(..., min_length=1)
    consented_at: str = Field(..., min_length=1)
    revoked_at: str | None = None


ConsentInput = ConsentRecord | Mapping[str, Any]


def _coerce_record(record: ConsentInput) -> ConsentRecord:
    """Convert arbitrary mapping input into a ConsentRecord."""

    if isinstance(record, ConsentRecord):
        return record

    try:
        return ConsentRecord.model_validate(record)
    except ValidationError as exc:  # pragma: no cover - defensive
        raise ConsentMissingError("Consent record is malformed") from exc


def require_consent(record: ConsentInput | None) -> ConsentRecord:
    """Validate PDPA consent before allowing access and return the normalized record."""

    if record is None:
        raise ConsentMissingError("Consent record is missing")

    normalized = _coerce_record(record)
    if normalized.revoked_at is not None:
        raise ConsentMissingError("Consent has been revoked")

    return normalized


def mask_email(email: str) -> str:
    """Mask the local part of the email, retaining the domain."""

    if "@" not in email:
        return email
    _, domain = email.split("@", maxsplit=1)
    if not domain:
        return email
    return f"***@{domain}"


def round_gps(latitude: float, longitude: float) -> tuple[float, float]:
    """Round GPS coordinates to three decimals for PDPA compliance."""

    return (round(latitude, 3), round(longitude, 3))
