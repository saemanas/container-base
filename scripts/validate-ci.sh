#!/usr/bin/env bash
# Baseline CI validation script for Container Base
set -euo pipefail

# Emit a structured error log if any command fails; ERR trap preserves failing command context.
trap 'log_json "validate-ci" "ERROR" "Validation aborted" "\"${BASH_COMMAND}\""' ERR

log_json() {
  local op_id=$1
  local code=$2
  local message=$3
  local extra=${4:-}
  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  if [[ -n "$extra" ]]; then
    printf '{"ts":"%s","opId":"%s","code":"%s","duration_ms":0,"message":"%s","details":%s}\n' "$ts" "$op_id" "$code" "$message" "$extra"
  else
    printf '{"ts":"%s","opId":"%s","code":"%s","duration_ms":0,"message":"%s"}\n' "$ts" "$op_id" "$code" "$message"
  fi
}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Core configuration files that must exist before attempting to run the CI workflow locally.
EXPECT_FILES=(".ruff.toml" ".eslintrc.cjs" ".prettierrc" ".github/workflows")
# Guardrail sequence enforced by the constitution; log the expected order for quick comparison.
STAGES=("Ruff" "ESLint" "Pytest" "OpenAPI Lint" "Build" "GHCR" "Tag Deploy")
# Base tooling required to execute the pipeline steps locally.
REQUIRED_COMMANDS=("python3" "npm" "docker")
REQUIRED_ENV=(
  "API_SUPABASE_URL"
  "API_SUPABASE_ANON_KEY"
  "API_SUPABASE_SERVICE_ROLE"
  "OCR_MAX_IMAGE_MB"
  "OCR_TIMEOUT_MS"
  "API_JWT_SECRET"
)

for file in "${EXPECT_FILES[@]}"; do
  if [[ ! -e "${ROOT_DIR}/${file}" ]]; then
    log_json "validate-ci" "MISSING_FILE" "Required file is missing" "\"${file}\""
    exit 1
  fi
done

missing_cmds=()
for cmd in "${REQUIRED_COMMANDS[@]}"; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    missing_cmds+=("${cmd}")
  fi
done

if [[ ${#missing_cmds[@]} -gt 0 ]]; then
  log_json "validate-ci" "MISSING_COMMAND" "Required CLI tools are not installed" "$(printf '[%s]' "$(printf '"%s",' "${missing_cmds[@]}" | sed 's/,$//')")"
  exit 1
fi

log_json "validate-ci" "FILES_OK" "All required CI configuration files found."

log_json "validate-ci" "STAGE_SEQUENCE" "Expected pipeline order" "$(printf '[%s]' "$(printf '"%s",' "${STAGES[@]}" | sed 's/,$//')")"

log_json "validate-ci" "GUIDANCE" "Review .github/workflows/ci.yml to enforce pipeline stages."

missing_env=()
for var in "${REQUIRED_ENV[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    missing_env+=("$var")
  fi
done

if [[ ${#missing_env[@]} -gt 0 ]]; then
  log_json "validate-ci" "MISSING_ENV" "Required environment variables are unset." "$(printf '[%s]' "$(printf '"%s",' "${missing_env[@]}" | sed 's/,$//')")"
  exit 1
fi

log_json "validate-ci" "ENV_OK" "All required environment variables are set."
