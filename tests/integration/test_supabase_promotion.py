"""Integration tests for the Supabase promotion automation."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "promote-supabase.sh"


def test_supabase_promotion_script_exists() -> None:
    """The staging promotion helper must exist before deployment work begins."""
    assert SCRIPT_PATH.exists(), "scripts/promote-supabase.sh is required"


def test_supabase_promotion_enforces_staging_first() -> None:
    """Promotion script must run staging before production once implemented."""
    contents = SCRIPT_PATH.read_text(encoding="utf-8")
    staging_phrase = "Promoting migrations to staging"
    production_phrase = "Promoting migrations to production"

    staging_idx = contents.find(staging_phrase)
    production_idx = contents.find(production_phrase)

    assert staging_idx != -1, "Script must log staging promotion"
    assert production_idx != -1, "Script must log production promotion"
    assert staging_idx < production_idx, "Staging promotion must precede production promotion"

    assert "db test --project-ref \"${STAGING_REF}\"" in contents, "RLS smoke tests must run on staging before promotion"
    assert "db push --project-ref \"${PRODUCTION_REF}\"" in contents, "Production push command must exist"
