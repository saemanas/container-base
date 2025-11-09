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


@pytest.mark.xfail(reason="Workflow smoke simulation not yet implemented", strict=True)
def test_deploy_workflows_require_manual_production_gate() -> None:
    """Production deploy job must mention manual approval guard."""
    api_workflow = yaml.safe_load(DEPLOY_API_WORKFLOW.read_text(encoding="utf-8"))
    production_job = api_workflow["jobs"]["deploy-production"]
    steps = production_job.get("steps", [])
    messages = "\n".join(str(step) for step in steps)
    assert "approval" in messages.lower(), "Production job should document approval gate"
