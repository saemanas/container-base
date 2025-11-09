#!/usr/bin/env bash
# Execute the CI component checks locally using `act` for quick validation.
#
# Requirements:
#   - Docker Desktop or compatible daemon running
#   - `act` CLI installed (https://github.com/nektos/act)
#   - `.env.act` (or ACT_ENV_FILE) containing GITHUB_TOKEN / PROJECT_TOKEN, etc.
#
# By default the script replays the pull_request event and runs the component
# guardrail jobs (python_checks, portal_checks, openapi_checks). The script stops
# on the first failure and prints the corresponding log location.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_ROOT="${ROOT_DIR}/artifacts/act"
ACT_BIN="${ACT_BIN:-$(command -v act || true)}"
ACT_ENV_FILE="${ACT_ENV_FILE:-${ROOT_DIR}/.env.act}"
ACT_RUNNER_IMAGE="${ACT_RUNNER_IMAGE:-ghcr.io/catthehacker/ubuntu:full-22.04}"
ACT_FLAGS="${ACT_FLAGS:-}"
if [[ "$(uname -s)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
  if [[ "${ACT_FLAGS}" != *"--container-architecture"* ]]; then
    ACT_FLAGS="${ACT_FLAGS} --container-architecture linux/amd64"
  fi
fi
EVENT="${ACT_EVENT:-pull_request}"
JOBS=("python_checks" "portal_checks" "openapi_checks")
FOLLOW_STREAM=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --follow)
      FOLLOW_STREAM=1
      shift
      ;;
    --verbose|-v)
      ACT_FLAGS="${ACT_FLAGS} -v"
      shift
      ;;
    --very-verbose|-vv)
      ACT_FLAGS="${ACT_FLAGS} -vv"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

log() {
  printf '[run-act-ci] %s\n' "$1"
}

fail() {
  log "ERROR: $1"
  exit 1
}

if [[ -z "${ACT_BIN}" ]]; then
  fail "'act' CLI not found. Install it via 'brew install act' or follow upstream instructions."
fi

if ! command -v docker >/dev/null 2>&1; then
  fail "Docker is required for act runs. Start Docker Desktop before proceeding."
fi

if [[ ! -f "${ACT_ENV_FILE}" ]]; then
  fail "Environment file not found: ${ACT_ENV_FILE}. Create it and include at least GITHUB_TOKEN and PROJECT_TOKEN."
fi

mkdir -p "${LOG_ROOT}"
SUMMARY_FILE="${LOG_ROOT}/summary-$(date -u +"%Y%m%dT%H%M%SZ").md"
cat >"${SUMMARY_FILE}" <<EOF
# act CI Summary

| Job | Status | Log |
| --- | --- | --- |
EOF

run_job() {
  local job=$1
  local log_file="${LOG_ROOT}/${job}-$(date -u +"%Y%m%dT%H%M%SZ").log"
  log "Running job '${job}' (logs: ${log_file})"
  # shellcheck disable=SC2206
  local extra_flags=(${ACT_FLAGS:-})
  if [[ ${FOLLOW_STREAM} -eq 1 ]]; then
    "${ACT_BIN}" "${EVENT}" \
      -P "ubuntu-latest=${ACT_RUNNER_IMAGE}" \
      --env-file "${ACT_ENV_FILE}" \
      "${extra_flags[@]}" \
      -j "${job}" \
      | tee "${log_file}"
    local status=${PIPESTATUS[0]}
  else
    set +e
    "${ACT_BIN}" "${EVENT}" \
      -P "ubuntu-latest=${ACT_RUNNER_IMAGE}" \
      --env-file "${ACT_ENV_FILE}" \
      "${extra_flags[@]}" \
      -j "${job}" \
      >"${log_file}" 2>&1
    local status=$?
    set -e
  fi

  if [[ ${status} -eq 0 ]]; then
    log "Job '${job}' succeeded"
    printf '| %s | ✅ success | %s |
' "${job}" "${log_file}" >>"${SUMMARY_FILE}"
  else
    log "Job '${job}' failed (status ${status}). Inspect ${log_file}"
    printf '| %s | ❌ failure | %s |
' "${job}" "${log_file}" >>"${SUMMARY_FILE}"
    tail -n 40 "${log_file}" || true
    fail "Job '${job}' failed. See log above or ${log_file}"
  fi
}

for job in "${JOBS[@]}"; do
  run_job "${job}"
  log "Sleeping briefly before next job to release docker resources"
  sleep 3

done

log "All component jobs completed. Summary stored at ${SUMMARY_FILE}."
