"""Portal availability smoke tests."""
from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]

PORTAL_ROOT = REPO_ROOT / "src" / "apps" / "portal"


@pytest.mark.skipif(not PORTAL_ROOT.exists(), reason="Portal app is not initialized")
def test_portal_package_json_exists() -> None:
    """Ensure the portal project has a package.json defined."""
    package_json = PORTAL_ROOT / "package.json"
    assert package_json.exists(), "Portal package.json missing"


@pytest.mark.skipif(not PORTAL_ROOT.exists(), reason="Portal app is not initialized")
def test_portal_env_example_exists() -> None:
    """Verify that the portal env example file is present for deployments."""
    env_example = PORTAL_ROOT / ".env.example"
    assert env_example.exists(), "Portal .env.example missing"
