#!/usr/bin/env bash
# Run repository-wide lint and test suites prior to committing changes.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY_ENV="${ROOT_DIR}/.venv"
ARTIFACT_DIR="${RUN_ALL_CHECKS_ARTIFACT_DIR:-${ROOT_DIR}/artifacts/ci}"
TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
SUMMARY_FILE="${ARTIFACT_DIR}/local-summary-${TIMESTAMP}.md"

PYTHON_BIN="${PY_ENV}/bin/python"
RUFF_BIN="${PY_ENV}/bin/ruff"

log() {
  printf '[run-all-checks] %s\n' "$1"
}

timestamp_ms() {
  "${PYTHON_BIN}" - <<'PY'
import time
print(int(time.time() * 1000))
PY
}

if [[ ! -d "${PY_ENV}" ]]; then
  if command -v python3 >/dev/null 2>&1 && command -v ruff >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
    RUFF_BIN="$(command -v ruff)"
    log "Python virtualenv not found at ${PY_ENV}; falling back to $(basename "${PYTHON_BIN}") from PATH."
  else
    log "Python virtualenv not found at ${PY_ENV}; create it before running."
    exit 1
  fi
fi

if [[ ! -x "${PYTHON_BIN}" ]]; then
  log "Python interpreter not executable at ${PYTHON_BIN}."
  exit 1
fi

if [[ ! -x "${RUFF_BIN}" ]]; then
  log "Ruff not found at ${RUFF_BIN}. Install it inside the virtualenv or ensure it is on PATH."
  exit 1
fi

mkdir -p "${ARTIFACT_DIR}"
cat >"${SUMMARY_FILE}" <<EOF
# Local CI Evidence (${TIMESTAMP})

| Stage | Status | Duration (ms) |
| --- | --- | --- |
EOF

if [[ "${PDPA_FORCE_FAILURE:-0}" == "1" ]]; then
  printf '| PDPA compliance gate | failure | 0 |\n' >>"${SUMMARY_FILE}"
  log "PDPA compliance gate forced failure; summary saved to ${SUMMARY_FILE}."
  exit 1
fi

run_step() {
  local label=$1
  shift
  log "Running ${label}"
  local start end duration status
  start=$(timestamp_ms)
  set +e
  "$@"
  status=$?
  set -e
  end=$(timestamp_ms)
  duration=$((end - start))

  if [[ ${status} -eq 0 ]]; then
    printf '| %s | success | %s |\n' "${label}" "${duration}" >>"${SUMMARY_FILE}"
  else
    printf '| %s | failure | %s |\n' "${label}" "${duration}" >>"${SUMMARY_FILE}"
    log "${label} failed. See ${SUMMARY_FILE} for details."
    exit ${status}
  fi
}

run_step "Ruff lint (Python)" "${RUFF_BIN}" check "${ROOT_DIR}/src/apps/api" "${ROOT_DIR}/src/apps/ocr"
run_step "Pytest" "${PYTHON_BIN}" -m pytest "${ROOT_DIR}/tests" --maxfail=1 --disable-warnings -q
run_step "ESLint (portal)" bash -c "cd '${ROOT_DIR}/src/apps/portal' && npm run lint"

log "All checks completed successfully. Summary stored at ${SUMMARY_FILE}."
