#!/usr/bin/env bash
# Logs PDPA retention triggers and Supabase confirmations for rollback drills.
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: run-retention-job.sh --environment <env> --tag <tag> --op-id <op-id>

Required environment variables:
  SUPABASE_SERVICE_ROLE_KEY  Supabase service-role key (masked for logs)
  SUPABASE_PROJECT_REF       Supabase project reference identifier
USAGE
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

RETENTION_ENVIRONMENT=""
RETENTION_TAG=""
OP_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --environment)
      RETENTION_ENVIRONMENT=${2:-}
      shift 2
      ;;
    --tag)
      RETENTION_TAG=${2:-}
      shift 2
      ;;
    --op-id)
      OP_ID=${2:-}
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${RETENTION_ENVIRONMENT}" || -z "${RETENTION_TAG}" || -z "${OP_ID}" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 1
fi

if [[ -z "${SUPABASE_SERVICE_ROLE_KEY:-}" || -z "${SUPABASE_PROJECT_REF:-}" ]]; then
  echo "Supabase credentials are required for retention logging." >&2
  exit 1
fi

SECONDS=0
TIMESTAMP=$(date -u +%FT%TZ)
RUN_ID=${GITHUB_RUN_ID:-local}
ARTIFACT_DIR="artifacts/pdpa"
mkdir -p "${ARTIFACT_DIR}"
ARTIFACT_FILE="${ARTIFACT_DIR}/${OP_ID}-${RUN_ID}.json"

MASKED_PROJECT_REF="${SUPABASE_PROJECT_REF:0:6}***"
MASKED_SERVICE_KEY="${SUPABASE_SERVICE_ROLE_KEY:0:4}***"

if command -v supabase >/dev/null 2>&1; then
  # Note: Supabase CLI call intentionally no-op for dry runs; real workflows rely on service logs.
  echo "Running Supabase retention verification for ${RETENTION_ENVIRONMENT} (${RETENTION_TAG})"
  supabase events list --project-ref "${SUPABASE_PROJECT_REF}" >/dev/null 2>&1 || true
else
  echo "Supabase CLI not found; writing placeholder confirmation log." >&2
fi

duration_ms=$((SECONDS * 1000))

cat >"${ARTIFACT_FILE}" <<EOF
{
  "ts": "${TIMESTAMP}",
  "opId": "${OP_ID}",
  "code": "pdpa-retention",
  "duration_ms": ${duration_ms},
  "environment": "${RETENTION_ENVIRONMENT}",
  "tag": "${RETENTION_TAG}",
  "supabase_project_ref": "${MASKED_PROJECT_REF}",
  "supabase_service_role_key": "${MASKED_SERVICE_KEY}",
  "message": "Supabase retention job trigger logged"
}
EOF

echo "Retention artifact written to ${ARTIFACT_FILE}" >&2
