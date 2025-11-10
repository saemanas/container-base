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

    # Given the MiniOps constitution mandates component validations before build → ghcr → tag deploy
    jobs = ci_workflow.get("jobs", {})
    stage_order = list(jobs)

    expected = ["checks", "build", "ghcr", "tag_deploy"]

    # When we compare the defined jobs with the expected guardrail sequence
    # Then they should match exactly to uphold the constitution contract
    assert stage_order == expected, f"CI jobs order mismatch: {stage_order}"


def test_ci_checks_matrix_contains_expected_variants(ci_workflow: dict) -> None:
    """Ensure the consolidated checks job covers all component validations."""

    jobs = ci_workflow.get("jobs", {})
    checks_job = jobs.get("checks")

    assert checks_job is not None, "Expected consolidated 'checks' job to be defined"

    strategy = checks_job.get("strategy", {})
    matrix = strategy.get("matrix", {})
    variants = matrix.get("check")

    expected_variants = ["python", "portal", "openapi"]
    assert variants == expected_variants, (
        "Checks matrix must validate python, portal, and openapi variants sequentially"
    )
