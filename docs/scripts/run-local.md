# `run-local.sh`

## Purpose
Bootstrap the local Docker Compose stack (`docker compose up --build -d`) after loading the consolidated `.env` so all surfaces share consistent Supabase, portal, and logging configuration.

## Behavior
- Sources `.env` (requires root `.env` copy of `.env.example`) and validates critical keys such as `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_API_BASE_URL`, and `API_JWT_SECRET`.
- Emits an explicit error message when `.env` or required keys are missing.
- Calls `docker compose up --build -d` so API, OCR, portal, and mobile containers start with the same environment used in CI/C documentation.

## Usage
```
cp .env.example .env
# fill secrets and publishable keys
./scripts/run-local.sh
```

## Notes
- Since `docker compose` is required, this script is primarily for local QA/integration (not CI).
- Keep the `.env` copy out of version control (per `.gitignore` and PDPA policies).

