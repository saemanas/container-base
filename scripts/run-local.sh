#!/usr/bin/env bash
# Orchestrates the local Docker Compose stack after the shared `.env` file is sourced.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  cat <<'EOF' >&2
Missing .env configuration.
Copy the template and populate it with your Supabase + portal/local values:
  cp .env.example .env
  # edit the values, keeping `SUPABASE_ANON_KEY` as the publishable key
EOF
  exit 1
fi

# Load the consolidated environment so Compose, scripts, and npm commands share the same values.
set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

required_vars=(
  SUPABASE_URL
  SUPABASE_PROJECT_REF
  SUPABASE_ANON_KEY
  SUPABASE_SERVICE_ROLE_KEY
  NEXT_PUBLIC_API_BASE_URL
  API_JWT_SECRET
)

missing=()
for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    missing+=("${var}")
  fi
done

if (( ${#missing[@]} > 0 )); then
  printf 'Missing required environment variables: %s\n' "${missing[*]}" >&2
  exit 1
fi

printf 'Sourced %s and launching Docker Compose stack...\n' "${ENV_FILE}"
docker compose up --build -d
