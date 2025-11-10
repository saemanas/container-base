# Secrets Catalog: Low-cost CI/CD & Infra Skeleton

> Reference: `refs/docs/CB-Service-Plan-v1.0.0-en-US.md` §§6, 11 for stack, PDPA, and CI/CD guardrails.

## 1. Secret Inventory Overview

### GitHub Actions Environment Variable vs Secret Mapping

| Environment | Environment Variables | Secrets |
|-------------|------------------------|---------|
| **local** | `SUPABASE_PROJECT_REF`, `SUPABASE_URL`, `CLOUD_RUN_REGION`, `GCP_PROJECT_ID`, `API_READY_URL_STG`, `API_READY_URL_PROD`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ZONE_ID_API`, `CLOUDFLARE_ZONE_ID_PORTAL` | `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`, `SUPABASE_STORAGE_SIGNING_KEY`, `API_JWT_SECRET`, `GCLOUD_SERVICE_ACCOUNT_JSON`, `PROJECT_TOKEN`, `CLOUDFLARE_API_TOKEN` |
| **stg** | `SUPABASE_PROJECT_REF`, `SUPABASE_URL`, `CLOUD_RUN_REGION`, `GCP_PROJECT_ID`, `API_READY_URL_STG`, `API_READY_URL_PROD`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ZONE_ID_API`, `CLOUDFLARE_ZONE_ID_PORTAL` | `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`, `SUPABASE_STORAGE_SIGNING_KEY`, `API_JWT_SECRET`, `GCLOUD_SERVICE_ACCOUNT_JSON`, `PROJECT_TOKEN`, `CLOUDFLARE_API_TOKEN` |
| **prod** | `SUPABASE_PROJECT_REF`, `SUPABASE_URL`, `CLOUD_RUN_REGION`, `GCP_PROJECT_ID`, `API_READY_URL_STG`, `API_READY_URL_PROD`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ZONE_ID_API`, `CLOUDFLARE_ZONE_ID_PORTAL` | `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`, `SUPABASE_STORAGE_SIGNING_KEY`, `API_JWT_SECRET`, `GCLOUD_SERVICE_ACCOUNT_JSON`, `PROJECT_TOKEN`, `CLOUDFLARE_API_TOKEN` |

| Secret Name | Manager (Location) | Component Scope | Local Source | Staging Binding | Production Binding | Rotation |
|-------------|--------------------|-----------------|--------------|-----------------|--------------------|----------|
| SUPABASE_PROJECT_REF | GitHub Actions secrets (`SUPABASE_PROJECT_REF`) | API/OCR/Portal/Mobile | `src/apps/api/.env.example` (`SUPABASE_PROJECT_REF=local-project-ref`) | `container-base-stg` | `container-base-prod` | Annual |
| SUPABASE_URL | GitHub Actions secrets (`API_SUPABASE_URL`) | API/OCR | `src/apps/api/.env.example` (`SUPABASE_URL=http://127.0.0.1:54321`) | `https://container-base-stg.supabase.co` | `https://container-base.supabase.co` | Quarterly |
| SUPABASE_SERVICE_ROLE_KEY | GitHub Actions secrets (`API_SUPABASE_SERVICE_ROLE`) | API | `src/apps/api/.env.example` (`SUPABASE_SERVICE_ROLE_KEY=local-service-role`) | `projects/cb-supabase-stg/secrets/SUPABASE_SERVICE_ROLE` | `projects/cb-supabase-prod/secrets/SUPABASE_SERVICE_ROLE` | Monthly |
| SUPABASE_ANON_KEY | GitHub Actions secrets (`API_SUPABASE_ANON_KEY`) | API/OCR/Portal/Mobile | `src/apps/api/.env.example` (`SUPABASE_ANON_KEY=local-anon-key`) | `Supabase dashboard → API settings (stg)` | `Supabase dashboard → API settings (prod)` | Quarterly |
| SUPABASE_STORAGE_SIGNING_KEY | GitHub Actions secrets (`SUPABASE_STORAGE_SIGNING_KEY`) | API/OCR | `src/apps/api/.env.example` | `projects/cb-supabase-stg/secrets/STORAGE_SIGNING_KEY` | `projects/cb-supabase-prod/secrets/STORAGE_SIGNING_KEY` | Quarterly |
| API_JWT_SECRET | GitHub Actions secrets (`API_JWT_SECRET`) | API | `src/apps/api/.env.example` (`API_JWT_SECRET=local-dev`) | `Secret Manager: cb-api-stg/API_JWT_SECRET` | `Secret Manager: cb-api-prod/API_JWT_SECRET` | Monthly |
| CLOUD_RUN_REGION | GitHub Actions secrets (`CLOUD_RUN_REGION`) | CI/CD | `.github/workflows/ci.yml` default | `asia-southeast1` | `asia-southeast1` | Annual |
| GCP_PROJECT_ID | GitHub Actions secrets (`GCP_PROJECT_ID`) | CI/CD | `scripts/measure-ci.sh` (`gcp_project_id`) | `cb-api-stg` | `cb-api-prod` | Annual |
| GCLOUD_SERVICE_ACCOUNT_JSON | GitHub Actions secrets (`GCLOUD_SERVICE_ACCOUNT_JSON`) | CI/CD | Local dev uses ADC via `gcloud auth application-default login` | `projects/cb-platform-stg/secrets/gha-deployer.json` | `projects/cb-platform-prod/secrets/gha-deployer.json` | Monthly |
| GHCR_PAT | GitHub Actions secrets (`PROJECT_TOKEN`) | CI/CD | `~/.docker/config.json` (developer PAT) | `GitHub → org secrets → PROJECT_TOKEN` | `GitHub → org secrets → PROJECT_TOKEN` | Rotate on PAT regeneration |
| PORTAL_API_BASE_URL | Vercel environment secrets (`NEXT_PUBLIC_API_BASE_URL`) | Portal | `src/apps/portal/.env.example` (`NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api`) | `https://api-stg.container-base.com` | `https://api.container-base.com` | As needed |
| PORTAL_SUPABASE_URL | Vercel environment secrets (`NEXT_PUBLIC_SUPABASE_URL`) | Portal | `src/apps/portal/.env.example` (`NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321`) | `https://container-base-stg.supabase.co` | `https://container-base.supabase.co` | Quarterly |
| PORTAL_SUPABASE_ANON_KEY | Vercel environment secrets (`NEXT_PUBLIC_SUPABASE_ANON_KEY`) | Portal | `src/apps/portal/.env.example` | `Supabase dashboard anon key (stg)` | `Supabase dashboard anon key (prod)` | Quarterly |
| PORTAL_LINE_REDIRECT | Vercel environment secrets (`NEXT_PUBLIC_LINE_REDIRECT`) | Portal | `src/apps/portal/.env.example` (`http://localhost:3000/callback`) | `https://portal-stg.container-base.com/callback` | `https://portal.container-base.com/callback` | As needed |
| API_READY_URL_STG | GitHub Actions environment secrets (`API_READY_URL_STG`) | Portal smoke tests | `.env.example` comment (`READY_URL_STG=http://localhost:8000/readyz`) | `https://api-stg.container-base.com/readyz` | N/A | As needed |
| API_READY_URL_PROD | GitHub Actions environment secrets (`API_READY_URL_PROD`) | Portal smoke tests | `.env.example` comment (`READY_URL_PROD=http://localhost:8000/readyz`) | N/A | `https://api.container-base.com/readyz` | As needed |
| OCR_MAX_IMAGE_MB | Cloud Run service vars (`MAX_IMAGE_MB`) | OCR Worker | `src/apps/ocr-worker/.env.example` (`MAX_IMAGE_MB=15`) | `15` | `20` | As needed |
| OCR_TIMEOUT_MS | Cloud Run service vars (`OCR_TIMEOUT_MS`) | OCR Worker | `src/apps/ocr-worker/.env.example` (`OCR_TIMEOUT_MS=15000`) | `15000` | `20000` | As needed |
| OCR_SUPABASE_URL | Cloud Run service vars | OCR Worker | `src/apps/ocr-worker/.env.example` (`SUPABASE_URL=http://127.0.0.1:54321`) | `https://container-base-stg.supabase.co` | `https://container-base.supabase.co` | Quarterly |
| MOBILE_API_BASE_URL | Expo EAS secrets (`API_BASE_URL`) | Mobile | `src/apps/mobile/.env.example` (`API_BASE_URL=http://10.0.2.2:8000`) | `https://api-stg.container-base.com` | `https://api.container-base.com` | Quarterly |
| MOBILE_SUPABASE_URL | Expo EAS secrets (`SUPABASE_URL`) | Mobile | `src/apps/mobile/.env.example` | `https://container-base-stg.supabase.co` | `https://container-base.supabase.co` | Quarterly |
| MOBILE_SUPABASE_ANON_KEY | Expo EAS secrets (`SUPABASE_ANON_KEY`) | Mobile | `src/apps/mobile/.env.example` | `Supabase dashboard anon key (stg)` | `Supabase dashboard anon key (prod)` | Quarterly |
| MOBILE_LINE_CHANNEL_ID | Expo EAS secrets (`LINE_CHANNEL_ID`) | Mobile | `src/apps/mobile/.env.example` (`LINE_CHANNEL_ID=LINE-LOCAL-CHANNEL`) | `LINE-STG-CHANNEL` | `LINE-PROD-CHANNEL` | Quarterly |
| CLOUDFLARE_API_TOKEN | GitHub Actions environment secrets (`CLOUDFLARE_API_TOKEN`) | Domain/DNS | Local `.env.cloudflare` stored in 1Password | `Cloudflare token scoped to stg zones (grey cloud)` | `Cloudflare token scoped to prod zones (orange cloud)` | Quarterly |
| CLOUDFLARE_ACCOUNT_ID | GitHub Actions environment vars (`CLOUDFLARE_ACCOUNT_ID`) | Domain/DNS | `.env.cloudflare` | `cf-account-stg` | `cf-account-prod` | Annual |
| CLOUDFLARE_ZONE_ID_API | GitHub Actions environment vars (`CLOUDFLARE_ZONE_ID_API`) | Domain/DNS | `.env.cloudflare` | `api-stg.container-base.com zone` | `api.container-base.com zone` | Annual |
| CLOUDFLARE_ZONE_ID_PORTAL | GitHub Actions environment vars (`CLOUDFLARE_ZONE_ID_PORTAL`) | Domain/DNS | `.env.cloudflare` | `portal-stg.container-base.com zone` | `portal.container-base.com zone` | Annual |

> All secrets must be injected via platform-specific secret managers. Never commit real values. Local placeholders above mirror `.env.example` defaults to simplify onboarding.

## 2. Environment Artifacts & Provisioning Notes

- **Local** — Developers load `.env.local` files per app, run Supabase CLI sandbox, and authenticate with `gcloud auth application-default login`. Cloudflare tokens stay in personal vaults and are never written to disk in plaintext.
- **Stg** — GitHub Actions `environment: stg` gates Cloud Run deploys (`cb-api-stg`, `cb-ocr-stg`) and Vercel preview promotions. Secrets originate from Google Secret Manager, Supabase dashboard (project `container-base-stg`), and Vercel environment variable sets.
- **Prod** — GitHub Actions `environment: prod` enforces manual approval before releasing to `cb-api-prod`, `cb-ocr-prod`, and Vercel prod. Secrets reside in isolated projects with Cloudflare tokens scoped to prod zones and Supabase project `container-base-prod`.

## 3. Rotation & Ownership

| Secret Group | Rotation Owner | Rotation Cadence | Notes |
|--------------|----------------|------------------|-------|
| Supabase keys (`SUPABASE_*`) | Platform Lead | Quarterly | Rotate via Supabase dashboard, update GitHub Actions envs, Vercel, Expo EAS. Align with PDPA consent enforcement (@CB Service Plan §11). |
| JWT & API crypto (`API_JWT_SECRET`) | Backend Lead | Monthly | Coordinate with FastAPI deployment window; ensure canary window (≤10m) validated per Service Plan rollback budget. |
| Cloud Run deployer (`GCLOUD_SERVICE_ACCOUNT_JSON`, `GCP_PROJECT_ID`, `CLOUD_RUN_REGION`) | Infra Lead | Monthly | Regenerate service account keys, upload to GitHub Actions environments, confirm IAM least privilege. |
| Cloudflare tokens (`CLOUDFLARE_*`) | Infra Lead | Quarterly | Validate stg (grey cloud) before prod (orange cloud) switch; log DNS changes for compliance. |
| Expo / Mobile credentials (`MOBILE_*`, `LINE_CHANNEL_ID`) | Mobile Lead | Quarterly | Rotate LINE channel secrets and Expo tokens; update Supabase anon keys in EAS projects. |
| GHCR_PAT (`PROJECT_TOKEN`) | DevOps Lead | On-demand | Required for CI/CD container pushes; rotate when PAT holder leaves or PAT scope changes. |

### Cloud Run Runtime Configuration

| Service | Environment Variables | Secrets |
|---------|------------------------|---------|
| `cb-api-<env>` | `SUPABASE_URL`, `SUPABASE_PROJECT_REF`, `MAX_CONCURRENCY` (if configured) | `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`, `SUPABASE_STORAGE_SIGNING_KEY`, `API_JWT_SECRET` |
| `cb-ocr-<env>` | `SUPABASE_URL`, `MAX_IMAGE_MB`, `OCR_TIMEOUT_MS` | `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY` |

### Vercel (Portal) Configuration

| Type | Keys |
|------|------|
| Environment Variables | `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_LINE_REDIRECT` |
| Secrets (Sensitive values) | `NEXT_PUBLIC_SUPABASE_ANON_KEY` *(store as Secret despite `NEXT_PUBLIC` prefix to avoid accidental leakage)* |

### Expo EAS (Mobile) Configuration

| Type | Keys |
|------|------|
| Environment Variables | `API_BASE_URL`, `SUPABASE_URL` |
| Secrets | `SUPABASE_ANON_KEY`, `LINE_CHANNEL_ID` |

## 4. Audit Notes (2025-11-10)

- `.env.example` files across API, OCR worker, portal, and mobile now document per-environment placeholders that match this catalog, unlocking automated validation of missing bindings during CI/CD hardening.
- `cd-api.yml`, `cd-ocr.yml`, and `cd-portal.yml` reference GitHub Actions environments (`stg`, `prod`) whose secrets map 1:1 with the entries above; promotion flows align with the Service Plan’s ≤10 minute rollback mandate.
- Cloud Run and Vercel deployments enforce post-deploy smoke tests (healthz/readyz + Supabase connectivity). Logs and PDPA artifacts are archived per CB Service Plan §11 to satisfy consent and retention obligations.
