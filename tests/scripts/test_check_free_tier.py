"""Tests for free-tier quota checker script."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "check-free-tier.py"

pytestmark = pytest.mark.skipif(not SCRIPT_PATH.exists(), reason="Quota checker script missing")


def test_check_free_tier_writes_artifact(tmp_path: Path) -> None:
    """Script should emit structured log and persist quota artifact."""

    artifact_dir = tmp_path / "quotas"
    env = os.environ.copy()
    env["GITHUB_RUN_ID"] = "run-321"

    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--artifact-dir",
        str(artifact_dir),
        "--op-id",
        "quota-prod",
    ]

    result = subprocess.run(command, capture_output=True, text=True, env=env)

    assert result.returncode == 0, result.stderr
    lines = [line for line in result.stdout.strip().splitlines() if line]
    assert lines, "Expected JSON output from script"

    structured_payload = json.loads(lines[-1])
    assert structured_payload["opId"] == "quota-prod"
    assert structured_payload["code"] == "quota-summary"

    artifact_path = artifact_dir / "quota-prod-run-321.json"
    assert artifact_path.exists(), "Quota artifact missing"
    artifact_data = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert "quotas" in artifact_data and artifact_data["quotas"], "Artifact should include quota list"
