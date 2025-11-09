# CI Pipeline Runbook

## Overview
The CI workflow (`.github/workflows/ci.yml`) enforces the mandated sequence Ruff → ESLint → Pytest → OpenAPI Lint → Build → GHCR → Tag Deploy across all surfaces while staying within free-tier budgets.

### Trigger policy
- **Pull requests targeting protected branches (`main`, `develop`)** always execute the full CI pipeline before merge.
- **Feature branch pushes** (any branch except `main`/`develop`) run CI automatically, providing feedback prior to opening a PR.
- **Direct pushes to `main`/`develop`** rely on the resulting PR merge checks; the workflow ignores raw push events on these protected branches to prevent duplicate runs.

## Stages
1. **Lint (parallel)** – Ruff and ESLint execute concurrently. Ruff covers the API/OCR Python surfaces via matrix jobs, while ESLint validates the portal stack with cached dependencies. Both jobs must succeed before downstream stages proceed.
2. **Pytest** – Executes service test suite and applies PDPA regression checks (`tests/backend/test_pdpa_compliance.py`) for API. This job declares `needs: [ruff, eslint]` so failures in either lint job gate test execution.
3. **OpenAPI Lint (Redocly CLI)** – OpenAPI contract lint
4. **Build** – Docker image builds for API/OCR via Buildx
5. **GHCR** – Build and push images to GitHub Container Registry (authenticate with PAT secret `PROJECT_TOKEN`)
6. **Tag Deploy** – Summary/notification step to close the loop and upload `artifacts/ci/tag_deploy/pipeline-summary.txt` with a 90-day retention window for compliance evidence

### Rollback-aware Flow (US3)
```
┌────────┐    ┌────────┐    ┌────────┐    ┌─────────────┐
│  CI PR │ -> │ Staging│ -> │ Prod   │ -> │ Rollback (≤10m)
└────────┘    └────────┘    └────────┘    └─────────────┘
     |              |              |            |
     |              |              |            └─▶ `scripts/run-retention-job.sh`
     |              |              └─▶ `scripts/send-ci-email.py`
     |              └─▶ GHCR digest capture
     └─▶ Tag summary artifact (`artifacts/ci/tag_deploy/`)
```
*Diagram describes the mandated promotion path: CI evidence → staging deploy → production deploy with manual approval → automated rollback drill capturing Supabase retention logs and notification emails.*

## Required Secrets (GitHub Actions)
- `PROJECT_TOKEN` – GitHub PAT with `write:packages`, stored in repo secrets for GHCR pushes
- `GHCR_IMAGE_PREFIX` (derived) – uses `ghcr.io/${{ github.repository }}`
- Optional future secrets: `GCLOUD_SERVICE_ACCOUNT`, `VERCEL_TOKEN`, `SUPABASE_ANON_KEY`

## Common Operations
- **Dry run locally**: `act pull_request -W .github/workflows/ci.yml`
- **Investigate failure**: Inspect the failing job log; re-run selected jobs from GitHub UI if inputs unchanged
- **Upgrade dependencies**: Update `requirements.txt`, `package-lock.json`, re-run `npm install`, and adjust caches as needed
- **Retrieve CI evidence**: Download `ci-summary-<run_id>` artifact to attach audit-ready logs during release reviews (retained for 90 days)
- **Per-stage artifacts**: Each CI job writes logs beneath `artifacts/ci/<stage>/` (e.g., `ruff/service.log`, `pdpa/api.log`, `openapi_lint/lint.log`, `build/api.log`, `ghcr/api.json`) ensuring auditors can trace `{ts, opId, code, duration_ms}` from `scripts/measure-ci.sh`
- **Portal stack guard**: CI runs `python3 scripts/check-portal-stack.py` to enforce Next.js 16 / React 19 baseline before building
- **Notification archive**: Production deploys and rollbacks call `scripts/send-ci-email.py` which emits `.eml` artifacts in `artifacts/notifications/` and structured logs `{ts, opId, code, duration_ms}` for auditing.
- **Quota evidence**: Execute `python scripts/check-free-tier.py --artifact-dir artifacts/quotas --op-id quota-<env>` post-release to record Supabase/Cloud Run/Vercel usage snapshots alongside CI artifacts.

## Troubleshooting
- **Ruff/ESLint failures**: Fix lint issues locally; re-run `ruff check` or `npm run lint`
- **Pytest failures**: Ensure tests import correct modules; mimic pipeline environment with Python 3.12
- **OpenAPI lint failures**: Validate OpenAPI contract structure; run `redocly lint` manually
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
