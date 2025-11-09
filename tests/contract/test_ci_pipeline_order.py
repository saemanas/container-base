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


def test_ci_jobs_define_parallel_lint_and_sequenced_followups() -> None:
    """Ruff/ESLint run independently; downstream jobs must depend on both lint stages."""
    jobs = _load_workflow()["jobs"]

    for lint_job in ["ruff", "eslint"]:
        assert lint_job in jobs, f"Missing lint job {lint_job} in ci.yml"
        job_block = jobs[lint_job]
        assert isinstance(job_block, dict), f"Job block for {lint_job} must be a mapping"
        assert job_block.get("needs") in (None, []), f"Lint job {lint_job} must not declare dependencies"

    pytest_job = jobs.get("pytest")
    assert isinstance(pytest_job, dict), "pytest job must be defined"
    pytest_needs = pytest_job.get("needs")
    assert pytest_needs is not None, "pytest job must depend on lint jobs"
    if isinstance(pytest_needs, str):
        pytest_needs = [pytest_needs]
    assert set(pytest_needs) == {"ruff", "eslint"}, "pytest must depend on both lint jobs"

    sequence_pairs = [
        ("pytest", "openapi_lint"),
        ("openapi_lint", "build"),
        ("build", "ghcr"),
        ("ghcr", "tag_deploy"),
    ]
    for upstream, downstream in sequence_pairs:
        downstream_block = jobs.get(downstream)
        assert isinstance(downstream_block, dict), f"Job {downstream} must exist"
        needs = downstream_block.get("needs")
        assert needs is not None, f"Job {downstream} must depend on {upstream}"
        if isinstance(needs, str):
            needs = [needs]
        assert upstream in needs, f"Job {downstream} must depend on {upstream}"
