#!/usr/bin/env bash
# Supabase promotion script: stg first, then prod with RLS smoke tests.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARTIFACT_DIR="${ROOT_DIR}/artifacts/supabase"
METADATA_FILE="${ARTIFACT_DIR}/promotion-$(date -u +"%Y%m%dT%H%M%SZ").json"

SUPABASE_BIN="$(command -v supabase || true)"
STG_REF="${STG_REF:-container-base-stg}"
PROD_REF="${PROD_REF:-container-base-prod}"
RLS_TEST_PATH="${RLS_TEST_PATH:-supabase/tests/rls}"

log() {
  printf '[promote-supabase] %s\n' "$1"
}

fail() {
  log "ERROR: $1"
  exit 1
}

if [[ -z "${SUPABASE_BIN}" ]]; then
  fail "Supabase CLI not found. Install with 'npm install -g supabase'."
fi

[[ -n "${STG_REF}" ]] || fail "STG_REF is required."
[[ -n "${PROD_REF}" ]] || fail "PROD_REF is required."

mkdir -p "${ARTIFACT_DIR}"

log "Promoting migrations to stg (${STG_REF})"
"${SUPABASE_BIN}" db push --project-ref "${STG_REF}"

log "Running RLS smoke tests on stg"
"${SUPABASE_BIN}" db test --project-ref "${STG_REF}" --tests "${RLS_TEST_PATH}"

log "Promoting migrations to prod (${PROD_REF})"
"${SUPABASE_BIN}" db push --project-ref "${PROD_REF}"

cat > "${METADATA_FILE}" <<EOF
{
  "ts": "$(date -Iseconds)",
  "stg_ref": "${STG_REF}",
  "prod_ref": "${PROD_REF}",
  "rls_tests": "${RLS_TEST_PATH}",
  "actor": "${GITHUB_ACTOR:-local}" }
EOF

log "Promotion complete. Metadata: ${METADATA_FILE}"
