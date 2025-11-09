"""Guardrail simulation tests for cost and quota thresholds."""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
COST_GUARDRAIL_DOC = REPO_ROOT / "docs" / "deployment" / "cost-guardrails.md"


def test_cost_guardrail_doc_contains_thresholds() -> None:
    """The cost guardrail doc must describe 80% triggers and mitigation steps."""
    assert COST_GUARDRAIL_DOC.exists(), "cost-guardrails.md is missing"
    contents = COST_GUARDRAIL_DOC.read_text(encoding="utf-8")
    assert "80%" in contents or ">=80%" in contents, "Expected quota threshold guidance (80%)"
    assert "Cloud Run" in contents, "Cloud Run cost guardrail missing"
    assert "Supabase" in contents, "Supabase usage guardrail missing"
    assert "Vercel" in contents, "Vercel build guardrail missing"
    assert "rollback" in contents.lower(), "Rollback/remediation steps must be documented"
