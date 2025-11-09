"""Contract tests ensuring CI pipeline stage ordering and dependencies."""
from __future__ import annotations

import pathlib
from typing import Any

import yaml


CI_WORKFLOW_PATH = pathlib.Path(__file__).resolve().parents[2] / ".github/workflows/ci.yml"
EXPECTED_SEQUENCE = [
    "python_checks",
    "portal_checks",
    "openapi_checks",
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


def test_ci_jobs_define_parallel_component_checks() -> None:
    """Component check jobs must run independently and gate downstream stages."""
    jobs = _load_workflow()["jobs"]

    check_jobs = ["python_checks", "portal_checks", "openapi_checks"]
    for job_name in check_jobs:
        assert job_name in jobs, f"Missing component job {job_name} in ci.yml"
        job_block = jobs[job_name]
        assert isinstance(job_block, dict), f"Job block for {job_name} must be a mapping"
        assert job_block.get("needs") in (None, []), f"Component job {job_name} must not declare dependencies"

    build_job = jobs.get("build")
    assert isinstance(build_job, dict), "build job must be defined"
    build_needs = build_job.get("needs")
    assert build_needs is not None, "build job must depend on component checks"
    if isinstance(build_needs, str):
        build_needs = [build_needs]
    assert set(build_needs) == set(check_jobs), "build must depend on all component jobs"

    sequence_pairs = [
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
