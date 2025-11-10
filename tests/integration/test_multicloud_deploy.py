"""Integration tests for multicloud deployment workflow descriptors."""
from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO_ROOT = Path(__file__).resolve().parents[2]
DEPLOY_API_WORKFLOW = REPO_ROOT / ".github/workflows/cd-api.yml"
DEPLOY_OCR_WORKFLOW = REPO_ROOT / ".github/workflows/cd-ocr.yml"


@pytest.mark.parametrize(
    "workflow_path",
    [DEPLOY_API_WORKFLOW, DEPLOY_OCR_WORKFLOW],
)
def test_deploy_workflows_define_environment_options(workflow_path: Path) -> None:
    """Deploy workflows must expose stg/prod options for manual dispatch."""
    assert workflow_path.exists(), f"Workflow missing: {workflow_path}"
    content = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    dispatch = (
        content.get("on", {})
        .get("workflow_dispatch", {})
        .get("inputs", {})
        .get("environment", {})
    )
    options = dispatch.get("options", [])
    assert "stg" in options, "stg option must be available"
    assert "prod" in options, "prod option must be available"


def test_deploy_workflows_require_prod_gate_message() -> None:
    """Prod deploy must mention approval context so reviewers notice the gate."""
    api_workflow = yaml.safe_load(DEPLOY_API_WORKFLOW.read_text(encoding="utf-8"))
    deploy_job = api_workflow["jobs"]["deploy"]
    steps = deploy_job.get("steps", [])

    def mentions_prod_gate(step: object) -> bool:
        if isinstance(step, dict):
            text = " ".join(str(step.get(key, "")) for key in ("name", "run", "with"))
        else:
            text = str(step)
        return "prod" in text.lower() and "approval" in text.lower()

    assert any(mentions_prod_gate(step) for step in steps), "Prod gate messaging must be present"
