"""Validation tests for the secrets catalog documentation."""
from __future__ import annotations

from pathlib import Path


SECRETS_CATALOG = Path(__file__).parents[2] / "docs" / "deployment" / "secrets-catalog.md"


def test_secrets_catalog_exists() -> None:
    """The secrets catalog document must be present."""
    assert SECRETS_CATALOG.exists(), "docs/deployment/secrets-catalog.md is missing"


def test_secrets_catalog_contains_required_rows() -> None:
    """Ensure critical secrets are documented with rotation cadence."""
    contents = SECRETS_CATALOG.read_text(encoding="utf-8")
    required_entries = {
        "API_SUPABASE_URL",
        "API_SUPABASE_SERVICE_ROLE",
        "API_SUPABASE_ANON_KEY",
        "API_JWT_SECRET",
        "OCR_MAX_IMAGE_MB",
        "OCR_TIMEOUT_MS",
    }
    for entry in required_entries:
        assert entry in contents, f"Missing {entry} entry in secrets catalog"
    assert "Rotation" in contents, "Rotation policy column must be documented"
