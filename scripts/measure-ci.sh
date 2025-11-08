#!/usr/bin/env bash
# Measure CI stage durations locally and append results to docs/deployment/ci-pipeline.md.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DOC="${ROOT_DIR}/docs/deployment/ci-pipeline.md"
TIMESTAMP="$(date -Iseconds)"

STAGES=(
  "Ruff::ruff --version"
  "ESLint::npm run lint --prefix ${ROOT_DIR}/src/apps/portal"
  "Pytest::python -m pytest tests/backend/test_ci_guardrails.py"
  "Spectral::npx --yes spectral lint ${ROOT_DIR}/specs/001-lowcost-cicd-infra/contracts/openapi.yaml"
  "Docker Build::docker build -q ${ROOT_DIR}/src/apps/api"
)

STAGE_ROWS=()

log_json() {
  local op_id=$1
  local code=$2
  local message=$3
  local details=${4:-}
  local ts
  ts=$(date -Iseconds)
  if [[ -n "${details}" ]]; then
    printf '{"ts":"%s","opId":"%s","code":"%s","message":"%s","details":%s}\n' "${ts}" "${op_id}" "${code}" "${message}" "${details}"
  else
    printf '{"ts":"%s","opId":"%s","code":"%s","message":"%s"}\n' "${ts}" "${op_id}" "${code}" "${message}"
  fi
}

run_stage() {
  local label=$1
  local cmd=$2
  local binary
  binary=${cmd%% *}

  if [[ "${cmd}" == *"npx"* ]]; then
    binary="npx"
  fi

  if ! command -v "${binary}" >/dev/null 2>&1; then
    log_json "measure-ci" "SKIP" "${label} skipped (command unavailable)" "\"${binary}\""
    STAGE_ROWS+=("| ${label} | skipped | - |")
    return 0
  fi

  local start end duration status
  start=$(date +%s%3N)
  if eval "${cmd}" >/dev/null 2>&1; then
    status="success"
  else
    status="failure"
  fi
  end=$(date +%s%3N)
  duration=$((end - start))

  if [[ "${status}" == "failure" ]]; then
    log_json "measure-ci" "FAIL" "${label} failed" "\"${cmd}\""
  else
    log_json "measure-ci" "OK" "${label} completed" "\"${cmd}\""
  fi

  STAGE_ROWS+=("| ${label} | ${status} | ${duration} |")
}

for stage in "${STAGES[@]}"; do
  IFS="::" read -r label command <<<"${stage}"
  run_stage "${label}" "${command}"
  if [[ "${STAGE_ROWS[-1]}" == *"failure"* ]]; then
    log_json "measure-ci" "INFO" "Halting after failure" "\"${label}\""
    break
  fi
done

{
  printf '\n## CI Timing Snapshot (%s)\n\n' "${TIMESTAMP}"
  printf '| Stage | Status | Duration (ms) |\n| --- | --- | --- |\n'
  for row in "${STAGE_ROWS[@]}"; do
    printf '%s\n' "${row}"
  done
} >>"${OUT_DOC}"

log_json "measure-ci" "DONE" "Report appended" "\"${OUT_DOC}\""
