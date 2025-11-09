"""OpenAPI lint stub using Redocly CLI for the Container Base contract."""
from __future__ import annotations

from pathlib import Path
import subprocess
import shutil

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]

OPENAPI_SPEC = REPO_ROOT / "specs" / "001-lowcost-cicd-infra" / "contracts" / "openapi.yaml"


def test_openapi_contract_exists() -> None:
    """Ensure the OpenAPI contract is present before running the linter."""
    assert OPENAPI_SPEC.exists(), "Expected OpenAPI contract to exist for Redocly linting"


_REDOCLY_BIN = shutil.which("redocly")
if _REDOCLY_BIN is None:
    local_cli = REPO_ROOT / "node_modules" / ".bin" / "redocly"
    if local_cli.exists():
        _REDOCLY_BIN = str(local_cli)


@pytest.mark.skipif(_REDOCLY_BIN is None, reason="Redocly CLI not installed")
def test_openapi_passes_redocly_lint() -> None:
    """Run Redocly lint if the CLI is available in the environment."""
    result = subprocess.run(
        [_REDOCLY_BIN, "lint", str(OPENAPI_SPEC)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert (
        result.returncode == 0
    ), f"Redocly lint failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
