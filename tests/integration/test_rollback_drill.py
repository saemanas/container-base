"""Integration tests ensuring rollback workflows enforce MTTR guardrails."""
from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO_ROOT = Path(__file__).resolve().parents[2]
ROLLBACK_WORKFLOWS = [
    REPO_ROOT / ".github/workflows/deploy-api.yml",
    REPO_ROOT / ".github/workflows/deploy-ocr.yml",
]


def _load_production_job(workflow_path: Path) -> dict:
    content = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    jobs = content.get("jobs", {})
    assert "deploy-production" in jobs, f"Workflow missing deploy-production job: {workflow_path}"
    production_job = jobs["deploy-production"]
    assert isinstance(production_job, dict), "deploy-production job must be a mapping"
    return production_job


@pytest.mark.parametrize("workflow_path", ROLLBACK_WORKFLOWS)
def test_production_job_enforces_rollback_timeout(workflow_path: Path) -> None:
    """Production rollback must complete within the ≤10 minute MTTR guardrail."""
    production_job = _load_production_job(workflow_path)
    timeout_minutes = production_job.get("timeout-minutes")
    assert isinstance(
        timeout_minutes, (int, float)
    ), "deploy-production job must declare timeout-minutes as per US3 spec"
    assert timeout_minutes <= 10, "Rollback timeout must be ≤10 minutes"


@pytest.mark.parametrize("workflow_path", ROLLBACK_WORKFLOWS)
def test_production_job_emits_structured_rollback_logs(workflow_path: Path) -> None:
    """Rollback workflows must emit structured `{ts, opId, code, duration_ms}` telemetry."""
    production_job = _load_production_job(workflow_path)
    steps = production_job.get("steps", [])

    required_tokens = (
        '"ts"',
        '"opid"',
        '"code"',
        '"duration_ms"',
    )

    def _step_contains_structured_log(step: object) -> bool:
        if not isinstance(step, dict):
            return False
        haystack = " ".join(
            str(step.get(key, "")) for key in ("name", "run", "with", "env")
        ).lower()
        return all(token in haystack for token in required_tokens)

    assert any(
        _step_contains_structured_log(step) for step in steps
    ), "Production rollback job must emit structured logs with {ts, opId, code, duration_ms}"
