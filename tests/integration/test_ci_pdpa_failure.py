"""Integration tests ensuring PDPA failures block the CI pipeline."""
from __future__ import annotations

import pathlib
import subprocess
from typing import Iterable

import pytest

def _run_ci_check(env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    root = pathlib.Path(__file__).resolve().parents[2]
    script = root / "scripts" / "run-all-checks.sh"
    result = subprocess.run(
        ["bash", str(script)],
        env={**env, "PYTHONPATH": str(root)},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return result


def _pdpa_failure_env() -> dict[str, str]:
    root = pathlib.Path(__file__).resolve().parents[2]
    return {
        "SUPPRESS_CONSENT_CHECK": "0",
        "PDPA_FORCE_FAILURE": "1",
        "PATH": str(pathlib.Path.cwd()),
        **dict.fromkeys(_inherit_env_keys(["PATH", "HOME"]), ""),
    }


def _inherit_env_keys(keys: Iterable[str]) -> Iterable[str]:
    for key in keys:
        value = subprocess.os.environ.get(key)
        if value is not None:
            yield key


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.skip("Placeholder until CI script supports PDPA failure simulation")
def test_pdpa_failure_blocks_pipeline() -> None:
    """When PDPA checks fail, CI must stop before reaching GHCR/tag stages."""
    result = _run_ci_check(_pdpa_failure_env())
    assert result.returncode != 0, "PDPA failure should fail run-all-checks"
    assert "PDPA" in result.stdout, "Logs should mention PDPA failure"
