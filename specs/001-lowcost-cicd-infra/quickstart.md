# Quickstart Guide: Low-cost CI/CD & Infra Skeleton

## Prerequisites
- Python 3.12.x and Node.js 22.21.1 installed.
- Docker Engine ≥26 with Compose v2.29+.
- Supabase project (single project for staging/prod) with anon/service role keys available.
- GitHub repository with Actions enabled and access to GHCR.

## Setup Steps
1. **Clone & checkout feature branch**
   ```bash
   git clone <repo-url>
   cd container-base
   git checkout 001-lowcost-cicd-infra
   ```
2. **Create Python virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```
3. **Install tooling**
   ```bash
   python -m pip install -r src/apps/api/requirements.txt
   python -m pip install -r src/apps/ocr/requirements.txt
   npm install --prefix src/apps/portal
   npx expo install --cwd src/apps/mobile
   ```
4. **Populate `.env.example` templates**
   - Update `src/apps/api/.env.example`, `src/apps/ocr/.env.example`, `src/apps/portal/.env.example`, and `src/apps/mobile/.env.example` with placeholder keys (no secrets).
   - Record live secrets in GitHub, Cloud Run, Vercel, and Supabase environments per `docs/deployment/secrets-catalog.md`.
5. **Configure Supabase schemas**
   - Create staging (`app_stg`) and production (`app_prod`) schemas.
   - Apply RLS policies for each table; ensure service role key restricted to backend workloads.
5. **Bootstrap Cloud Run & Vercel services**
   - Create Cloud Run services `cb-api-stg`, `cb-api-prod`, `cb-ocr-stg`, `cb-ocr-prod` with concurrency 5.
   - Provision Vercel project for the portal and set staging/production domains.
6. **Set GitHub secrets**
   - `API_SUPABASE_URL`, `API_SUPABASE_SERVICE_ROLE`, `OCR_TIMEOUT_MS`, `PORTAL_API_BASE_URL`, etc.
   - Add `CLOUD_RUN_REGION`, `GCLOUD_SERVICE_ACCOUNT`, `VERCEL_TOKEN`, `SUPABASE_ANON_KEY`.

## Local Concurrent Run Workflow
Follow this flow to run all services together while pointing to the shared Supabase project:

1. **Export shared environment variables**
   ```bash
   export SUPABASE_URL=https://example.supabase.co
   export SUPABASE_ANON_KEY=anon-key
   ```
2. **Start API service** (new shell)
   ```bash
   cd src/apps/api
   uvicorn api.main:app --reload --port 8000
   ```
3. **Start OCR worker** (new shell)
   ```bash
   cd src/apps/ocr
   python -m app.main
   ```
4. **Start portal** (new shell)
   ```bash
   cd src/apps/portal
   npm install
   npm run dev
   ```
5. **Start mobile app** (new shell)
   ```bash
   cd src/apps/mobile
   npx expo start
   ```
6. **Verify connectivity**
   - Hit `http://localhost:8000/healthz` and `http://localhost:8000/readyz`
   - Portal: open `http://localhost:3000`
   - Expo: check API calls resolve successfully using the exported Supabase variables

> Once `scripts/run-local.sh` is implemented (T011), it should orchestrate these commands automatically.

## Verification
1. **Run CI locally**
   ```bash
   source .venv/bin/activate  # if not already active
   act pull_request -W .github/workflows/ci.yml
   ```
   Expect Ruff/ESLint/Pytest/OpenAPI Lint stages to pass or fail with actionable errors.
2. **Execute health checks**
   ```bash
   curl https://cb-api-stg-<hash>.run.app/healthz
   curl https://cb-api-stg-<hash>.run.app/readyz
   ```
   Responses should return HTTP 200 with JSON payload `{ "status": "ok" }`.
3. **Trigger stg deployment**
   ```bash
   gh workflow run deploy-api.yml --ref main --field environment=stg
   ```
   Confirm GitHub Actions deploy job completes and Cloud Run revision becomes healthy.
4. **Manual prod approval test**
   - Open GitHub Actions run for `deploy-api.yml` targeting prod.
   - Ensure job pauses on “Manual approval required”; approve to complete rollout.
5. **Monitor guardrails**
   - Check Cloud Run dashboard for concurrency utilization ≤5 and quota usage <80%.
   - Inspect Supabase dashboards for row-level access events.
   - Review Vercel build minutes under the Hobby plan budget.

## Validation Log (2025-11-09)

| Step | Status | Notes |
|------|--------|-------|
| Clone & checkout feature branch | ✅ | Workspace already on `001-lowcost-cicd-infra`. |
| Create Python virtual environment | ✅ | `.venv` created with Python 3.13.7. |
| Install tooling | ✅ | `pip install` for API/OCR worker and npm dependencies executed earlier. |
| Populate `.env.example` templates | ⚠️ Pending | Placeholders reviewed; real secrets remain in platform secret stores. |
| Configure Supabase schemas | ⚠️ Pending | Requires Supabase access—documented steps only. |
| Bootstrap Cloud Run & Vercel services | ⚠️ Pending | Infra provisioning deferred until staging environment ready. |
| Set GitHub secrets | ⚠️ Pending | Secrets catalog verified; actual values reside in GitHub/Cloud Run/Vercel. |
| Local concurrent run workflow | ⚠️ Pending | Not executed (Supabase/demo services unavailable in local environment). |
| CI dry run via `act` | ⚠️ Pending | Requires Docker-in-Docker; skipped in current session. |
| Pytest critical suites (`pdpa`, `ocr_pdpa`) | ✅ | `pytest` run via `.venv/bin/python -m pytest ...` (9 passed). |
| Staging deployment workflow | ⚠️ Pending | Requires GitHub Actions trigger; not run. |
| Production approval simulation | ⚠️ Pending | Manual approval left for actual release window. |
| Guardrail monitoring | ⚠️ Pending | Dashboards documented; no live workload to inspect. |

## Rollback Procedure
1. Identify the previous GHCR image tag.
2. Run GitHub Actions workflow dispatch with `rollback_tag=<previous-tag>`.
3. Verify Cloud Run revision traffic shifts back within 10 minutes.
