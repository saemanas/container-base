"""Contract tests ensuring CI pipeline stage ordering and dependencies."""
from __future__ import annotations

import pathlib
from typing import Any

import yaml


CI_WORKFLOW_PATH = pathlib.Path(__file__).resolve().parents[2] / ".github/workflows/ci.yml"
EXPECTED_SEQUENCE = [
    "ruff",
    "eslint",
    "pytest",
    "openapi_lint",
    "build",
    "ghcr",
    "tag_deploy",
]


def _load_workflow() -> dict[str, Any]:
    with CI_WORKFLOW_PATH.open("r", encoding="utf-8") as handle:
        workflow = yaml.safe_load(handle)
    assert isinstance(workflow, dict), "ci.yml must parse to a mapping"
    return workflow


def test_ci_jobs_follow_expected_sequence() -> None:
    """CI jobs must remain in the mandated order (FR-001)."""
    jobs = _load_workflow()["jobs"]
    assert isinstance(jobs, dict), "jobs block must be a mapping"

    actual_order = list(jobs.keys())
    assert actual_order == EXPECTED_SEQUENCE, f"CI job order mismatch: {actual_order}"


def test_ci_jobs_define_needs_chain() -> None:
    """Each job after the first must depend on the previous job to enforce sequencing."""
    jobs = _load_workflow()["jobs"]

    previous_job: str | None = None
    for job_name in EXPECTED_SEQUENCE:
        assert job_name in jobs, f"Missing job {job_name} in ci.yml"
        job_block = jobs[job_name]
        assert isinstance(job_block, dict), f"Job block for {job_name} must be a mapping"
        needs = job_block.get("needs")
        if previous_job is None:
            assert needs is None, "First job must not define needs"
        else:
            if isinstance(needs, list):
                assert previous_job in needs, f"Job {job_name} must depend on {previous_job}"
            elif isinstance(needs, str):
                assert needs == previous_job, f"Job {job_name} must depend on {previous_job}"
            else:
                raise AssertionError(f"Job {job_name} missing needs dependency on {previous_job}")
        previous_job = job_name
