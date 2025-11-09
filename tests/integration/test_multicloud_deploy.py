"""Integration tests for multicloud deployment workflow descriptors."""
from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO_ROOT = Path(__file__).resolve().parents[2]
DEPLOY_API_WORKFLOW = REPO_ROOT / ".github/workflows/deploy-api.yml"
DEPLOY_OCR_WORKFLOW = REPO_ROOT / ".github/workflows/deploy-ocr.yml"


@pytest.mark.parametrize(
    "workflow_path",
    [DEPLOY_API_WORKFLOW, DEPLOY_OCR_WORKFLOW],
)
def test_deploy_workflows_define_environments(workflow_path: Path) -> None:
    """Deploy workflows must declare staging and production environments."""
    assert workflow_path.exists(), f"Workflow missing: {workflow_path}"
    content = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    jobs = content.get("jobs", {})
    assert "deploy-staging" in jobs, "Staging job is required"
    assert "deploy-production" in jobs, "Production job is required"


def test_deploy_workflows_require_manual_production_gate() -> None:
    """Production deploy job must document approval gate and environment guard."""
    api_workflow = yaml.safe_load(DEPLOY_API_WORKFLOW.read_text(encoding="utf-8"))
    production_job = api_workflow["jobs"]["deploy-production"]
    environment = production_job.get("environment")

    if isinstance(environment, dict):
        env_name = environment.get("name", "")
    else:
        env_name = environment or ""

    assert env_name.lower() == "production", "Production job must target production environment"

    steps = production_job.get("steps", [])

    def contains_approval(step: object) -> bool:
        if isinstance(step, dict):
            inspect_values = [step.get("name", ""), step.get("run", ""), step.get("with", "")]
            normalized = " ".join(str(value) for value in inspect_values)
        else:
            normalized = str(step)
        return "approval" in normalized.lower()

    assert any(contains_approval(step) for step in steps), "Production job should mention approval gate"
