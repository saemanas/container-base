# Workflow Secrets & Environment Variables

This document records the secrets and environment variables that must be configured before running the repository's CI/CD workflows (`.github/workflows/ci.yml`, `cd-api.yml`, `cd-ocr.yml`, `cd-portal.yml`). Values are placeholders—replace them with project-specific credentials in GitHub Environments or organization secrets.

| Secret / Variable | Purpose | Example | Workflow / Script |
| --- | --- | --- | --- |
| `GCP_PROJECT_ID` | Google Cloud project containing Cloud Run services | `container-base-dev` | `cd-api.yml`, `cd-ocr.yml` |
| `CLOUD_RUN_REGION` | Region to deploy the API/OCR services | `asia-northeast3` | `cd-api.yml`, `cd-ocr.yml` |
| `GCLOUD_SERVICE_ACCOUNT_JSON` | Base64-encoded service account key for gcloud auth | `{"type":"service_account",...}` | `cd-api.yml`, `cd-ocr.yml` |
| `PROJECT_TOKEN` | GHCR auth token with `read:packages` and `write:packages` | `ghp_xxx` | `cd-api.yml`, `cd-ocr.yml` |
| `SUPABASE_PROJECT_REF` | Supabase project identifier for PDPA scripts | `prod-abcd1234` | `cd-api.yml`, `cd-ocr.yml`, `scripts/run-retention-job.sh` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key that can run retention jobs | `eyJhbGciOiJIUzI1NiIs...` | `cd-api.yml`, `cd-ocr.yml` |
| `CLOUDFLARE_API_TOKEN` | Token with cache purge permissions for the API domain | `cfpt_abcd1234` | `cd-api.yml`, `cd-ocr.yml` |
| `CLOUDFLARE_ZONE_ID_API` | Cloudflare zone ID for `api.container-base.com` | `abcdef1234567890` | `cd-api.yml` |
| `CLOUDFLARE_ZONE_ID_OCR` | Cloudflare zone ID for `ocr.container-base.com` | `1234567890abcdef` | `cd-ocr.yml` |
| `VERCEL_TOKEN` | Token used by `cd-portal.yml` to trigger portal deployments | `vercel_abcdef` | `cd-portal.yml` |
| `VERCEL_PROJECT_ID` | Vercel project that hosts the portal | `container-base-portal` | `cd-portal.yml` |
| `VERCEL_ORG_ID` | Vercel organization owning the portal | `container-base` | `cd-portal.yml` |
| `VERCEL_ENVIRONMENT` | Target Vercel environment for the portal deploy (stg/prod) | `production` | `cd-portal.yml` |
| `CI_GIT_REF` / `RUN_ALL_CHECKS_ARTIFACT_DIR` | Optional overrides used by `scripts/run-all-checks.sh` during CI proofs | `refs/stg` / `/tmp/artifacts` | `scripts/run-all-checks.sh` |

## Local environment variables

- All local variables are defined in `.env.example` at the repository root. Copy the file to `.env` before running Docker Compose targets (for example, `make build`) so every service shares the same configuration.
- Docker Compose automatically loads `.env`, so API, OCR, Portal, and Mobile containers inherit consistent Supabase credentials and logging settings.

| Variable | Used by | Purpose |
| --- | --- | --- |
| `SUPABASE_URL`, `SUPABASE_PROJECT_REF`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_STORAGE_SIGNING_KEY` | API, OCR, Portal, Mobile | Shared Supabase connection, service role jobs, and storage signing for uploads. `SUPABASE_ANON_KEY` is the publishable key exported from the Supabase CLI. |
| `API_JWT_SECRET`, `JWT_SECRET`, `OCR_URL`, `ALLOW_ORIGINS`, `MAX_IMAGE_MB`, `TIMEOUT_MS`, `LOG_LEVEL` | API | FastAPI settings, CORS/size limits, worker logging, and health endpoints. |
| `API_BASE_URL`, `MAX_IMAGE_MB`, `OCR_TIMEOUT_MS`, `OCR_BATCH_SIZE`, `LOG_LEVEL` | OCR | OCR worker tuning, retry limits, and structured logging controls. Reuses `MAX_IMAGE_MB`/`LOG_LEVEL` from the API section. |
| `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_LINE_REDIRECT`, `NEXT_PUBLIC_OPERATIONS_EMAIL`, `LOG_LEVEL` | Portal | Portal runtime values, LINE redirect, and operations email for help links. `LOG_LEVEL` aligns with the API and OCR logging level. |
| `EXPO_PUBLIC_API_BASE_URL`, `EXPO_PUBLIC_SUPABASE_URL`, `EXPO_PUBLIC_SUPABASE_ANON_KEY`, `EXPO_PUBLIC_LINE_CHANNEL_ID` | Mobile | Expo config, LINE channel ID for login, and local API/Supabase endpoints. |

## Local simulation helpers

- `PDPA_FORCE_FAILURE=1` – forces `scripts/run-all-checks.sh` to fail immediately so the PDPA compliance gate can be tested (scripts already log the failure and exit before lint/test stages).
- `SUPPRESS_CONSENT_CHECK=1` – CI scripts skip PDPA consent enforcement; tests may rely on toggling this key so intentionally failing scenarios can be isolated.
- `PDPA_RETENTION_FORCE_FAILURE=1` – instructs `scripts/run-retention-job.sh` to log a simulated retention gate failure, emit structured `status: failure`, record the artifact, and exit 1 so workflows can prove rollback/alerting behavior without touching real Supabase events.

## Placement guidance

1. Add the secrets to the GitHub repository's **Environments** (`stg` and `prod`) to scope them by branch/target.
2. Mirror each key in the deployment target (Cloud Run, Vercel, Supabase) to keep rollout scripts consistent; `SUPABASE_*` keys typically live in Supabase's in-project secret store.
3. When simulating PDPA failures locally, export the toggle variables before running `make test` or `scripts/run-all-checks.sh`. Remember to remove them (or set to `0`) before committing to avoid accidental CI gate failures.
