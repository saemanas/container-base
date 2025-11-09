"""CI pipeline contract tests for Container Base."""
from __future__ import annotations

from pathlib import Path

import pytest


yaml = pytest.importorskip("yaml")


CI_WORKFLOW = Path(__file__).parents[2] / ".github" / "workflows" / "ci.yml"


@pytest.fixture
def ci_workflow() -> dict:
    """Load the CI workflow YAML for assertions."""

    if not CI_WORKFLOW.exists():  # Given the workflow should already be defined
        pytest.fail("Expected .github/workflows/ci.yml to exist")

    return yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8"))


def test_ci_has_expected_jobs(ci_workflow: dict) -> None:
    """Ensure the CI pipeline defines all mandated stages."""

    # Given the MiniOps constitution mandates Ruff → ESLint → Pytest → OpenAPI Lint → Build → GHCR → Tag Deploy
    jobs = ci_workflow.get("jobs", {})
    stage_order = list(jobs)

    expected = [
        "ruff",
        "eslint",
        "pytest",
        "openapi_lint",
        "build",
        "ghcr",
        "tag_deploy",
    ]

    # When we compare the defined jobs with the expected guardrail sequence
    # Then they should match exactly to uphold the constitution contract
    assert stage_order == expected, f"CI jobs order mismatch: {stage_order}"
