# CI Pipeline Runbook

## Overview
The CI workflow (`.github/workflows/ci.yml`) enforces the mandated sequence Ruff → ESLint → Pytest → OpenAPI Lint → Build → GHCR → Tag Deploy across all surfaces while staying within free-tier budgets.

### Trigger policy
- **Pull requests targeting protected branches (`main`, `develop`)** always execute the full CI pipeline before merge.
- **Feature branch pushes** (any branch except `main`/`develop`) run CI automatically, providing feedback prior to opening a PR.
- **Direct pushes to `main`/`develop`** rely on the resulting PR merge checks; the workflow ignores raw push events on these protected branches to prevent duplicate runs.

### Caching policy
- **pip (API/OCR + tests)**: cache `~/.cache/pip` using key `pip-${{ runner.os }}-${{ hashFiles('src/apps/**/requirements.txt', 'tests/requirements.txt') }}`. Restores across feature branches to reuse wheel downloads.
- **npm (Portal)**: rely on `actions/setup-node@v4` with `cache: npm` and `cache-dependency-path: package-lock.json` so the shared npm store is restored automatically. This works alongside the existing `.next/cache` artifact for faster Next.js builds.
- **Docker Buildx**: use GitHub Actions cache backend (`type=gha`) so CI and CD jobs share image layers. Key format `docker-${{ runner.os }}-${{ env.GHCR_IMAGE_PREFIX }}` with branch-specific restore keys.
- **Portal deploy assets**: reuse npm cache for CD workflows to avoid reinstalling dependencies before `vercel` bundle steps.
- **Capacity guardrail**: monitor Actions storage (default 10 GB for free tier). Old caches are removed via LRU, but periodically clear stale entries with `gh cache delete` if needed.

## Stages
1. **Lint (parallel)** – Ruff and ESLint execute concurrently. Ruff covers the API/OCR Python surfaces via matrix jobs, while ESLint validates the portal stack with cached dependencies. Both jobs must succeed before downstream stages proceed.
2. **Pytest** – Executes service test suite and applies PDPA regression checks (`tests/backend/test_pdpa_compliance.py`) for API. This job declares `needs: [ruff, eslint]` so failures in either lint job gate test execution.
3. **OpenAPI Lint & Diff** – Lint the contract with `@redocly/cli@2.11.0` and compare against the base branch using `openapi-diff@0.24.1`. Because the diff tool only understands OpenAPI 3.0.x, CI copies both the base and head specs into `artifacts/ci/openapi_lint/` and temporarily rewrites the document header from `openapi: 3.1.0` to `openapi: 3.0.3` prior to comparison. The original sources remain untouched; the normalization only happens inside the CI artifact directory before the diff runs.
4. **Build** – Docker image builds for API/OCR via Buildx
5. **GHCR** – Build and push images to GitHub Container Registry (authenticate with PAT secret `PROJECT_TOKEN`)
6. **Tag Deploy** – Summary/notification step to close the loop and upload `artifacts/ci/tag_deploy/pipeline-summary.txt` with a 90-day retention window for compliance evidence

### Rollback-aware Flow (US3)
```
┌────────┐    ┌─────┐    ┌────┐    ┌─────────────┐
│  CI PR │ -> │ Stg │ -> │Prod│ -> │ Rollback (≤10m)
└────────┘    └────────┘    └────────┘    └─────────────┘
     |              |              |            |
     |              |              |            └─▶ `scripts/run-retention-job.sh`
     |              |              └─▶ `scripts/send-ci-email.py`
     |              └─▶ GHCR digest capture
     └─▶ Tag summary artifact (`artifacts/ci/tag_deploy/`)
```
*Diagram describes the mandated promotion path: CI evidence → stg deploy → prod deploy with manual approval → automated rollback drill capturing Supabase retention logs and notification emails.*

## Required Secrets (GitHub Actions)
- `PROJECT_TOKEN` – GitHub PAT with `write:packages`, stored in repo secrets for GHCR pushes
- `GHCR_IMAGE_PREFIX` (derived) – uses `ghcr.io/${{ github.repository }}`
- Optional future secrets: `GCLOUD_SERVICE_ACCOUNT`, `VERCEL_TOKEN`, `SUPABASE_ANON_KEY`

## Common Operations
- **Dry run locally**: `act pull_request -W .github/workflows/ci.yml`
- **Spin up local stack**: `bash scripts/run-local.sh` boots API, OCR worker, and portal (when configured) with Supabase credentials from the environment. Use this when validating end-to-end flows before tagging a release.
- **Sanity-check CI prerequisites**: `bash scripts/validate-ci.sh` verifies required tooling/variables and emits structured JSON logs so missing dependencies are caught before pushing branches.
- **Investigate failure**: Inspect the failing job log; re-run selected jobs from GitHub UI if inputs unchanged
- **Upgrade dependencies**: Update `requirements.txt`, `package-lock.json`, re-run `npm install`, and adjust caches as needed
- **Retrieve CI evidence**: Download `ci-summary-<run_id>` artifact to attach audit-ready logs during release reviews (retained for 90 days)
- **Per-stage artifacts**: Each CI job writes logs beneath `artifacts/ci/<stage>/` (e.g., `ruff/service.log`, `pdpa/api.log`, `openapi_lint/lint.log`, `build/api.log`, `ghcr/api.json`) ensuring auditors can trace `{ts, opId, code, duration_ms}` from `scripts/measure-ci.sh`
- **Portal stack guard**: CI runs `python3 scripts/check-portal-stack.py` to enforce Next.js 16 / React 19 baseline before building
- **Notification archive**: Production deploys and rollbacks call `scripts/send-ci-email.py` which emits `.eml` artifacts in `artifacts/notifications/` and structured logs `{ts, opId, code, duration_ms}` for auditing.
- **Quota evidence**: Execute `python scripts/check-free-tier.py --artifact-dir artifacts/quotas --op-id quota-<env>` post-release to record Supabase/Cloud Run/Vercel usage snapshots alongside CI artifacts.

### Stg Deployment Verification
- **Digest capture**: After `cd-api`/`cd-ocr` stg runs, download `artifacts/digests/*.txt` to confirm immutable GHCR references exist before prod promotion.
- **Cloud Run health**: Run `scripts/measure-latency.py --url https://api-stg.container-base.com/readyz --op-id readyz-api-stg` (repeat for OCR) and attach logs to the release checklist.
- **Supabase smoke tests**: Execute `SUPABASE_STG_REF=container-base-stg bash scripts/supabase-smoke-test.sh`; store the resulting log in `artifacts/supabase/` and cross-reference PDPA consent enforcement (`refs/docs/CB-Service-Plan-v1.0.0-en-US.md §11`).
- **Portal readiness**: Validate that the Vercel preview uses `NEXT_PUBLIC_API_BASE_URL=https://api-stg.container-base.com` and renders EN/TH deploy status assets. Capture screenshots or logs under `artifacts/portal/`.
- **Cloudflare propagation**: `dig +short api-stg.container-base.com` and `portal-stg.container-base.com`; if stale, trigger the stg purge step using stg-scoped tokens outlined in `docs/deployment/secrets-catalog.md`.

### Script Reference
| Script | Purpose | Primary doc |
| --- | --- | --- |
| `scripts/run-all-checks.sh` | Run Ruff, Pytest, and portal ESLint before committing. | `docs/deployment/ci-baselines.md` |
| `scripts/run-local.sh` | Launch API, OCR worker, portal, and optional mobile dev servers for manual QA. | This document (Common Operations) |
| `scripts/validate-ci.sh` | Assert required tooling, config files, and env vars exist before CI. | This document (Common Operations) |
| `scripts/check-portal-stack.py` | Ensure portal dependencies stay on mandated Next.js/React majors. | This document (Stages & Common Operations) |
| `scripts/measure-ci.sh` | Capture local CI stage timing snapshots and append evidence tables. | `docs/deployment/ci-baselines.md` |
| `scripts/check-free-tier.py` | Track free-tier quota consumption and append observability notes. | `docs/deployment/observability.md` |
| `scripts/measure-latency.py` | Probe HTTP latency for readyz endpoints and log KPI evidence. | `docs/deployment/cost-guardrails.md` |
| `scripts/run-retention-job.sh` | Execute PDPA retention drill against Supabase with structured logs. | `docs/deployment/observability.md` & `docs/deployment/release-checklist.md` |
| `scripts/promote-supabase.sh` | Push Supabase migrations stg→prod with RLS smoke tests. | `docs/deployment/rollback-playbook.md` |
| `scripts/supabase-smoke-test.sh` | Validate Supabase schema and retention policies post-deploy. | `docs/deployment/supabase-schema.md` |
| `scripts/send-ci-email.py` | Emit structured email notifications for CI/CD events. | `docs/deployment/ci-cd-notifications.md` |

## Troubleshooting
- **Ruff/ESLint failures**: Fix lint issues locally; re-run `ruff check` or `npm run lint`
- **Pytest failures**: Ensure tests import correct modules; mimic pipeline environment with Python 3.12
- **OpenAPI lint/diff failures**: Validate OpenAPI contract structure (`npx @redocly/cli@2.11.0 lint <spec>`). For diff issues, replicate the CI behavior locally by copying the specs, rewriting the header to `openapi: 3.0.3`, and running `npx openapi-diff@0.24.1 <base> <head>` to inspect changes.
- **Docker build failures**: Confirm Dockerfile path and dependencies; leverage `docker build` locally
- **GHCR push issues**: Ensure `PROJECT_TOKEN` PAT exists with `write:packages` scope; rotate via GitHub settings if expired

## Notification Email Samples
- **Success** (`scripts/send-ci-email.py --event success ...`)
  ```text
  Subject: [CI/CD][SUCCESS] api production run https://github.com/org/repo/actions/runs/<id>
  Body:
  - Service: api
  - Environment: production
  - Tag/Commit: <ref>
  - Duration: PT5M
  - Evidence: https://github.com/org/repo/actions/artifacts/<id>
  ```
- **Rollback** (`--event rollback`)
  ```text
  Subject: [CI/CD][ROLLBACK] api production triggered for v1.3.2
  Body:
  - Triggered By: automation
  - Rollback Tag: v1.3.2
  - ETA to Completion: ≤10 minutes
  - Logs: https://github.com/org/repo/actions/artifacts/<id>
  ```

## Mobile-ready (Handoff Only)
Mobile capture/queue flows remain out of scope for this CI/CD hardening phase (per FR-011). When the Expo mobile client is onboarded:

1. **Entry Point**: Extend the CI workflow with a `mobile` matrix job after Portal lint/build to run Expo diagnostics and queue telemetry sync tests.
2. **Artifact Reuse**: Consume the existing notification (`scripts/send-ci-email.py`) and quota snapshots so mobile deploys share the same audit trail.
3. **Rollback Path**: Reference the rollback drill evidence matrix in `docs/deployment/observability.md` to ensure mobile deploys document `{ts, opId, code, duration_ms}` metrics and Supabase retention execution.
4. **Scope Guard**: Until mobile automation is live, document any manual mobile validation in ReleaseChecklist entries and tag incidents with `mobile-handoff` for traceability.
