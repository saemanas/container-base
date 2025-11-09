"""Integration tests for the Supabase promotion automation."""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "promote-supabase.sh"


def test_supabase_promotion_script_exists() -> None:
    """The staging promotion helper must exist before deployment work begins."""
    assert SCRIPT_PATH.exists(), "scripts/promote-supabase.sh is required"


@pytest.mark.xfail(reason="Supabase promotion script not implemented yet", strict=True)
def test_supabase_promotion_enforces_staging_first() -> None:
    """Promotion script must run staging before production once implemented."""
    contents = SCRIPT_PATH.read_text(encoding="utf-8")
    staging_idx = contents.find("staging")
    production_idx = contents.find("production")
    assert staging_idx != -1, "Script must reference staging promotion"
    assert production_idx != -1, "Script must reference production promotion"
    assert staging_idx < production_idx, "Staging promotion must precede production promotion"
