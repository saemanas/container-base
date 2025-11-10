"""Integration tests for the Supabase promotion automation."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "promote-supabase.sh"


def test_supabase_promotion_script_exists() -> None:
    """The stg promotion helper must exist before deployment work begins."""
    assert SCRIPT_PATH.exists(), "scripts/promote-supabase.sh is required"


def test_supabase_promotion_enforces_stg_first() -> None:
    """Promotion script must run stg before prod once implemented."""
    contents = SCRIPT_PATH.read_text(encoding="utf-8")
    stg_phrase = "Promoting migrations to stg"
    prod_phrase = "Promoting migrations to prod"

    stg_idx = contents.find(stg_phrase)
    prod_idx = contents.find(prod_phrase)

    assert stg_idx != -1, "Script must log stg promotion"
    assert prod_idx != -1, "Script must log prod promotion"
    assert stg_idx < prod_idx, "Stg promotion must precede prod promotion"

    assert "db test --project-ref \"${STG_REF}\"" in contents, "RLS smoke tests must run on stg before promotion"
    assert "db push --project-ref \"${PROD_REF}\"" in contents, "Prod push command must exist"
