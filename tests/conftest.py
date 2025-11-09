"""Global pytest fixtures and guards."""
from __future__ import annotations

import os
import sys


def pytest_sessionstart(session):  # type: ignore[override]
    """Ensure local Python tests run inside an activated virtual environment."""
    if os.environ.get("CI"):
        return

    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    if not in_venv:
        session.config.warn(
            "E999",
            "Python tests must be executed from an activated virtual environment (.venv).",
        )
        raise SystemExit(
            "Aborting pytest: activate your project virtualenv (source .venv/bin/activate)."
        )
