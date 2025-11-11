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
def test_root_env_example_includes_portal_values() -> None:
    """Root env example must exist and contain portal-specific placeholders."""

    env_example = REPO_ROOT / ".env.example"
    assert env_example.exists(), "Root .env.example missing"

    contents = env_example.read_text(encoding="utf-8")
    required_keys = (
        "NEXT_PUBLIC_API_BASE_URL",
        "NEXT_PUBLIC_SUPABASE_URL",
        "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        "NEXT_PUBLIC_LINE_REDIRECT",
    )
    for key in required_keys:
        assert (
            key in contents
        ), f"Root .env.example missing portal placeholder: {key}"
