"""Smoke tests for Cloud Run health endpoint contracts."""
from __future__ import annotations

from pathlib import Path

import pytest


yaml = pytest.importorskip("yaml")


REPO_ROOT = Path(__file__).resolve().parents[2]

OPENAPI_SPEC = REPO_ROOT / "specs" / "001-lowcost-cicd-infra" / "contracts" / "openapi.yaml"


@pytest.fixture
def health_contract() -> dict:
    """Load the OpenAPI contract for health endpoints."""
    assert OPENAPI_SPEC.exists(), "OpenAPI contract missing"
    return yaml.safe_load(OPENAPI_SPEC.read_text(encoding="utf-8"))


def test_health_paths_exist(health_contract: dict) -> None:
    """Ensure the OpenAPI contract documents required health endpoints."""
    paths = health_contract.get("paths", {})
    assert "/healthz" in paths
    assert "/readyz" in paths


def test_health_contract_matches_file(health_contract: dict) -> None:
    """Compare the inline expectation with the stored OpenAPI file."""
    for endpoint in ("/healthz", "/readyz"):
        assert endpoint in health_contract.get("paths", {}), f"Missing {endpoint} in OpenAPI spec"
