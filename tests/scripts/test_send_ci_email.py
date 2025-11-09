"""Tests for CI/CD notification email sender script."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "send-ci-email.py"

pytestmark = pytest.mark.skipif(not SCRIPT_PATH.exists(), reason="Notification script not implemented yet")


def test_send_ci_email_generates_artifact(tmp_path: Path) -> None:
    """Script should render subject/body and persist artifact with structured log."""

    artifact_dir = tmp_path / "notifications"

    env = os.environ.copy()
    env.update(
        {
            "OPS_EMAIL_TO": "operations@example.com",
            "OPS_EMAIL_FROM": "ci@container-base.com",
            "GITHUB_RUN_ID": "run-789",
        }
    )

    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--event",
        "success",
        "--service",
        "api",
        "--environment",
        "production",
        "--ref",
        "v1.4.0",
        "--duration",
        "PT5M",
        "--artifact-url",
        "https://github.com/org/repo/actions/artifacts/1",
        "--workflow-run-url",
        "https://github.com/org/repo/actions/runs/1",
        "--artifact-dir",
        str(artifact_dir),
        "--op-id",
        "notif-api-prod",
    ]

    result = subprocess.run(command, capture_output=True, text=True, env=env)

    assert result.returncode == 0, result.stderr
    output = result.stdout.strip().splitlines()
    assert output, "Structured log output missing"
    log_line = output[-1]
    log_payload = json.loads(log_line)
    assert log_payload["opId"] == "notif-api-prod"
    assert log_payload["code"] == "ci-email"

    artifact_path = artifact_dir / "notif-api-prod-success.eml"
    assert artifact_path.exists(), "Email artifact not created"
    content = artifact_path.read_text(encoding="utf-8")
    assert "[CI/CD][SUCCESS] api production run" in content
    assert "operations@example.com" in content
    assert "https://github.com/org/repo/actions/artifacts/1" in content
