"""Spectral lint stub for the Container Base OpenAPI contract."""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

import pytest


OPENAPI_SPEC = (
    Path(__file__).parents[3]
    / "specs"
    / "001-lowcost-cicd-infra"
    / "contracts"
    / "openapi.yaml"
)


def test_openapi_contract_exists() -> None:
    """Ensure the OpenAPI contract is present before running spectral."""
    assert OPENAPI_SPEC.exists(), "Expected OpenAPI contract to exist for spectral linting"


@pytest.mark.skipif(shutil.which("spectral") is None, reason="Spectral CLI not installed")
def test_openapi_passes_spectral_lint() -> None:
    """Run Spectral lint if the CLI is available in the environment."""
    result = subprocess.run(
        ["spectral", "lint", str(OPENAPI_SPEC)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert (
        result.returncode == 0
    ), f"Spectral lint failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
