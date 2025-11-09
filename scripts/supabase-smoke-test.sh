#!/usr/bin/env bash
# Supabase staging smoke-test runner for RLS and migration parity validation.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${ROOT_DIR}/artifacts/supabase"
SUPABASE_BIN="$(command -v supabase || true)"
SUPABASE_STAGING_REF="${SUPABASE_STAGING_REF:-}" # e.g., container-base-stg
SUPABASE_LOCAL_REF="${SUPABASE_LOCAL_REF:-local-ci}" # local sandbox ref for rehearsal
RLS_TEST_PATH="${RLS_TEST_PATH:-supabase/tests/rls}"

log() {
  printf '[supabase-smoke-test] %s\n' "$1"
}

fail() {
  log "ERROR: $1"
  exit 1
}

[[ -n "${SUPABASE_BIN}" ]] || fail "Supabase CLI not found. Install via 'npm install -g supabase'."
[[ -n "${SUPABASE_STAGING_REF}" ]] || fail "SUPABASE_STAGING_REF environment variable is required (staging project ref)."

mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/rls-smoke-$(date -u +"%Y%m%dT%H%M%SZ").log"

{
  log "Pulling staging schema snapshot (${SUPABASE_STAGING_REF})"
  "${SUPABASE_BIN}" db pull --project-ref "${SUPABASE_STAGING_REF}" --schema public

  log "Applying migrations to local rehearsal project (${SUPABASE_LOCAL_REF})"
  "${SUPABASE_BIN}" db push --project-ref "${SUPABASE_LOCAL_REF}" --db-url "postgresql://postgres:postgres@127.0.0.1:54322/postgres"

  log "Executing Supabase RLS smoke tests (${RLS_TEST_PATH})"
  "${SUPABASE_BIN}" db test --project-ref "${SUPABASE_STAGING_REF}" --tests "${RLS_TEST_PATH}"

  log "Diffing staging vs production migrations for parity"
  "${SUPABASE_BIN}" db diff --project-ref "${SUPABASE_STAGING_REF}" --schema public --linked || log "WARNING: Non-zero diff detected; review before production promotion."

  log "Supabase smoke test completed successfully."
} | tee "${LOG_FILE}"

log "Artifacts stored at ${LOG_FILE}"
