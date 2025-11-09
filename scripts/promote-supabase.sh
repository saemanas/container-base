#!/usr/bin/env bash
# Supabase promotion script: staging first, then production with RLS smoke tests.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARTIFACT_DIR="${ROOT_DIR}/artifacts/supabase"
METADATA_FILE="${ARTIFACT_DIR}/promotion-$(date -u +"%Y%m%dT%H%M%SZ").json"

SUPABASE_BIN="$(command -v supabase || true)"
STAGING_REF="${SUPABASE_STAGING_REF:-}"
PRODUCTION_REF="${SUPABASE_PRODUCTION_REF:-}"
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

[[ -n "${STAGING_REF}" ]] || fail "SUPABASE_STAGING_REF is required."
[[ -n "${PRODUCTION_REF}" ]] || fail "SUPABASE_PRODUCTION_REF is required."

mkdir -p "${ARTIFACT_DIR}"

log "Promoting migrations to staging (${STAGING_REF})"
"${SUPABASE_BIN}" db push --project-ref "${STAGING_REF}"

log "Running RLS smoke tests on staging"
"${SUPABASE_BIN}" db test --project-ref "${STAGING_REF}" --tests "${RLS_TEST_PATH}"

log "Promoting migrations to production (${PRODUCTION_REF})"
"${SUPABASE_BIN}" db push --project-ref "${PRODUCTION_REF}"

cat > "${METADATA_FILE}" <<EOF
{
  "ts": "$(date -Iseconds)",
  "staging_ref": "${STAGING_REF}",
  "production_ref": "${PRODUCTION_REF}",
  "rls_tests": "${RLS_TEST_PATH}",
  "actor": "${GITHUB_ACTOR:-local}" }
EOF

log "Promotion complete. Metadata: ${METADATA_FILE}"
