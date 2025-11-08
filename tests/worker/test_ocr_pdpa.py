"""OCR worker PDPA credential isolation tests."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
PDPA_MODULE_PATH = REPO_ROOT / "src" / "apps" / "ocr-worker" / "ocr" / "pdpa.py"


def test_ocr_pdpa_module_exists() -> None:
    """The OCR PDPA helper module must exist."""
    assert PDPA_MODULE_PATH.exists(), "Expected src/apps/ocr-worker/ocr/pdpa.py to exist"


def _load_pdpa_module():
    spec = importlib.util.spec_from_file_location("ocr_pdpa", PDPA_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load OCR PDPA module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.skipif(not PDPA_MODULE_PATH.exists(), reason="OCR PDPA module missing")
def test_validate_credentials_rejects_service_role(monkeypatch: pytest.MonkeyPatch) -> None:
    """Service role keys must be rejected for OCR worker runtime."""
    pdpa = _load_pdpa_module()
    env = {"SUPABASE_SERVICE_ROLE_KEY": "secret", "SUPABASE_ANON_KEY": "anon"}
    with pytest.raises(pdpa.ServiceRoleForbiddenError):
        pdpa.validate_credentials(env)


@pytest.mark.skipif(not PDPA_MODULE_PATH.exists(), reason="OCR PDPA module missing")
def test_validate_credentials_allows_anon_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Anon key should be preserved when service role is absent."""
    pdpa = _load_pdpa_module()
    env = {"SUPABASE_ANON_KEY": "anon-key"}
    sanitized = pdpa.validate_credentials(env)
    assert sanitized["SUPABASE_ANON_KEY"] == "anon-key"
    assert "SUPABASE_SERVICE_ROLE_KEY" not in sanitized
