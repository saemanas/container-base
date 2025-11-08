#!/usr/bin/env bash
# Launch API, OCR worker, and optional portal/mobile dev servers for a concurrent local run.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_PORT="${API_PORT:-8000}"
PORTAL_PORT="${PORTAL_PORT:-3000}"
MOBILE_TUNNEL_PORT="${MOBILE_TUNNEL_PORT:-8081}"
SUPABASE_URL="${SUPABASE_URL:-}"
SUPABASE_ANON_KEY="${SUPABASE_ANON_KEY:-}"

pids=()

cleanup() {
  if [[ ${#pids[@]} -gt 0 ]]; then
    echo "Shutting down background services..."
    for pid in "${pids[@]}"; do
      if kill -0 "$pid" 2>/dev/null; then
        kill "$pid" || true
      fi
    done
  fi
}
trap cleanup EXIT

require_env() {
  local name=$1
  local value=$2
  if [[ -z "$value" ]]; then
    echo "Missing required environment variable: ${name}" >&2
    exit 1
  fi
}

require_env "SUPABASE_URL" "$SUPABASE_URL"
require_env "SUPABASE_ANON_KEY" "$SUPABASE_ANON_KEY"

echo "Using Supabase endpoint: ${SUPABASE_URL}"

start_api() {
  echo "Starting API service on port ${API_PORT}..."
  (\
    cd "${ROOT_DIR}/src/apps/api" && \
    python -m uvicorn service.main:app --reload --port "${API_PORT}" --log-level info \
      > "${ROOT_DIR}/.logs/api.log" 2>&1 &
  )
  pids+=("$!")
}

start_ocr() {
  echo "Starting OCR worker..."
  (\
    cd "${ROOT_DIR}/src/apps/ocr-worker" && \
    python -m ocr \
      > "${ROOT_DIR}/.logs/ocr.log" 2>&1 &
  )
  pids+=("$!")
}

start_portal() {
  if [[ -f "${ROOT_DIR}/src/apps/portal/package.json" ]]; then
    echo "Starting portal dev server on port ${PORTAL_PORT}..."
    (\
      cd "${ROOT_DIR}/src/apps/portal" && \
      if [[ ! -d node_modules ]]; then
        npm install >/dev/null 2>&1
      fi && \
      npm run dev -- --port "${PORTAL_PORT}" \
        > "${ROOT_DIR}/.logs/portal.log" 2>&1 &
    )
    pids+=("$!")
  else
    echo "Portal app not initialized (package.json missing). Skipping portal startup."
  fi
}

start_mobile() {
  if [[ -f "${ROOT_DIR}/src/apps/mobile/app.config.ts" ]]; then
    echo "Starting Expo mobile bundler (tunnel port ${MOBILE_TUNNEL_PORT})..."
    (\
      cd "${ROOT_DIR}/src/apps/mobile" && \
      if [[ ! -d node_modules ]]; then
        npm install >/dev/null 2>&1
      fi && \
      npx expo start --tunnel --port "${MOBILE_TUNNEL_PORT}" \
        > "${ROOT_DIR}/.logs/mobile.log" 2>&1 &
    )
    pids+=("$!")
  else
    echo "Mobile app not initialized (app.config.ts missing). Skipping Expo startup."
  fi
}

mkdir -p "${ROOT_DIR}/.logs"

start_api
start_ocr
start_portal
start_mobile

wait_for_endpoint() {
  local name=$1
  local url=$2
  echo "Waiting for ${name} to become available at ${url}..."
  for attempt in {1..10}; do
    if curl --silent --fail --max-time 2 "$url" >/dev/null; then
      echo "${name} is responding."
      return 0
    fi
    sleep 2
  done
  echo "Timed out waiting for ${name} at ${url}" >&2
  return 1
}

wait_for_endpoint "API healthz" "http://localhost:${API_PORT}/healthz"
wait_for_endpoint "API readyz" "http://localhost:${API_PORT}/readyz"

if [[ -f "${ROOT_DIR}/src/apps/portal/package.json" ]]; then
  wait_for_endpoint "Portal" "http://localhost:${PORTAL_PORT}"
fi

echo "All requested services started. Press Ctrl+C to stop."
wait
