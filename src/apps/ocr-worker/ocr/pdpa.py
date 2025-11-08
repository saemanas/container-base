"""PDPA utilities for the OCR worker service."""
from __future__ import annotations

from typing import Mapping

from pydantic import BaseModel, Field, ValidationError

__all__ = ["ServiceRoleForbiddenError", "SupabaseCredentials", "validate_credentials"]


class ServiceRoleForbiddenError(RuntimeError):
    """Raised when a service-role credential is supplied to the OCR worker."""


class SupabaseCredentials(BaseModel):
    """Validated environment mapping for OCR worker Supabase access."""

    SUPABASE_ANON_KEY: str = Field(..., min_length=1)


def validate_credentials(env: Mapping[str, str]) -> dict[str, str]:
    """Return a sanitized copy of env, forbidding service role usage."""

    if "SUPABASE_SERVICE_ROLE_KEY" in env:
        raise ServiceRoleForbiddenError("Service role key must not be provided to OCR worker")

    try:
        creds = SupabaseCredentials.model_validate(env)
    except ValidationError as exc:  # pragma: no cover
        raise ServiceRoleForbiddenError("SUPABASE_ANON_KEY is required for OCR worker") from exc

    return creds.model_dump()
