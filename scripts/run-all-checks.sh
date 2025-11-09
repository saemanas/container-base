#!/usr/bin/env bash
# Run repository-wide lint and test suites prior to committing changes.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY_ENV="${ROOT_DIR}/.venv"
ARTIFACT_DIR="${RUN_ALL_CHECKS_ARTIFACT_DIR:-${ROOT_DIR}/artifacts/ci}"
TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
SUMMARY_FILE="${ARTIFACT_DIR}/local-summary-${TIMESTAMP}.md"

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
  start=$(date +%s%3N)
  set +e
  "$@"
  status=$?
  set -e
  end=$(date +%s%3N)
  duration=$((end - start))

  if [[ ${status} -eq 0 ]]; then
    printf '| %s | success | %s |\n' "${label}" "${duration}" >>"${SUMMARY_FILE}"
  else
    printf '| %s | failure | %s |\n' "${label}" "${duration}" >>"${SUMMARY_FILE}"
    log "${label} failed. See ${SUMMARY_FILE} for details."
    exit ${status}
  fi
}

run_step "Ruff lint (Python)" "${RUFF_BIN}" check "${ROOT_DIR}/src/apps/api" "${ROOT_DIR}/src/apps/ocr-worker"
run_step "Pytest" "${PY_ENV}/bin/python" -m pytest "${ROOT_DIR}/tests" --maxfail=1 --disable-warnings -q
run_step "ESLint (portal)" bash -c "cd '${ROOT_DIR}/src/apps/portal' && npm run lint"

log "All checks completed successfully. Summary stored at ${SUMMARY_FILE}."
