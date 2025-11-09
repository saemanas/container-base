"""Unit tests ensuring PDPA retention job triggers are wired into deploy workflows."""
from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = [
    REPO_ROOT / ".github/workflows/cd-api.yml",
    REPO_ROOT / ".github/workflows/cd-ocr.yml",
]

EXPECTED_STEP_NAME = "Run PDPA retention job"
EXPECTED_SCRIPT = "scripts/run-retention-job.sh"
EXPECTED_TOKENS = ("SUPABASE", "PDPA", "retention")


@pytest.mark.parametrize("workflow_path", WORKFLOWS)
def test_production_job_triggers_pdpa_retention_job(workflow_path: Path) -> None:
    """Production jobs must invoke the retention script with PDPA/Supabase metadata."""

    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    production_job = data.get("jobs", {}).get("deploy-production")
    assert isinstance(production_job, dict), "deploy-production job must be defined"

    steps = production_job.get("steps", [])

    def matches(step: object) -> bool:
        if not isinstance(step, dict):
            return False

        name = str(step.get("name", ""))
        run_block = str(step.get("run", ""))
        env_block = step.get("env", {})

        has_expected_name = EXPECTED_STEP_NAME.lower() in name.lower()
        invokes_script = EXPECTED_SCRIPT in run_block
        references_metadata = any(token in run_block or token in str(env_block) for token in EXPECTED_TOKENS)

        return has_expected_name and invokes_script and references_metadata

    assert any(matches(step) for step in steps), (
        f"Workflow {workflow_path.name} must trigger {EXPECTED_SCRIPT} with PDPA metadata"
    )
