# `run-all-checks.sh`

## Purpose
Provides a pre‑commit gate that enforces Ruff → Pytest → ESLint locally, mirroring the constitution’s prescribed test-first observability ordering before pushing changes.

## Behavior
- Requires an existing `.venv` with Ruff and Pytest installed; exits with guidance if the environment is missing.
- Runs Ruff against `src/apps/api`/`ocr`, Pytest across `tests/`, and portal ESLint sequentially, capturing durations in `artifacts/ci/local-summary-<timestamp>.md`.
- Uses helper functions to timestamp each stage, so the summary table can be used as evidence of stage order and runtime.

## Usage
```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r src/apps/api/requirements.txt -r src/apps/ocr/requirements.txt ruff pytest
./scripts/run-all-checks.sh
```

## Notes
- When `PDPA_FORCE_FAILURE=1`, the script fails immediately, simulating the PDPA gate in CI.
- The summary file enumerates stage statuses (pass/fail) and durations.

