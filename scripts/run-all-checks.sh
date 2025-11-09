#!/usr/bin/env bash
# Run repository-wide lint and test suites prior to committing changes.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY_ENV="${ROOT_DIR}/.venv"

log() {
  printf '[run-all-checks] %s\n' "$1"
}

if [[ ! -d "${PY_ENV}" ]]; then
  log "Python virtualenv not found at ${PY_ENV}; create it before running."
  exit 1
fi

RUFF_BIN="${PY_ENV}/bin/ruff"
if [[ ! -x "${RUFF_BIN}" ]]; then
  log "Ruff not found at ${RUFF_BIN}. Install it with 'python -m pip install ruff' inside the virtualenv."
  exit 1
fi

log "Running Ruff lint (Python)"
"${RUFF_BIN}" check "${ROOT_DIR}/src/apps/api" "${ROOT_DIR}/src/apps/ocr-worker"

log "Running Pytest"
"${PY_ENV}/bin/python" -m pytest "${ROOT_DIR}/tests" --maxfail=1 --disable-warnings -q

log "Running ESLint (portal)"
(cd "${ROOT_DIR}/src/apps/portal" && npm run lint)

log "All checks completed successfully."
