# Container Base Monorepo

Container Base replaces manual container logging with automated recognition, GPS tracking, and auditable billing. This repository hosts the polyglot stack (FastAPI API, OCR worker, Next.js portal, Expo mobile) plus shared CI/CD and infrastructure assets.

## Project Structure

```
.
├── src/apps/api/               # FastAPI service
├── src/apps/ocr/               # OCR background worker
├── src/apps/portal/            # Next.js portal (Tailwind CSS + shadcn/ui)
│   └── components/             # Shared UI building blocks (e.g., shadcn buttons)
├── src/apps/mobile/            # Expo mobile app
├── docs/deployment/            # Runbooks, guardrails, secrets, KPI mapping
├── scripts/                    # CI helpers, measurement utilities
├── specs/                      # Spec-kit artifacts (spec, plan, tasks, etc.)
└── tests/                      # Pytest suites for contracts, PDPA, guardrails
```

> Folder strategy keeps each surface in its own build context while centralizing governance assets and workflows.@specs/001-lowcost-cicd-infra/plan.md#47-79

## Getting Started

1. **Clone the repo and sync stg branch**
   ```bash
   git clone https://github.com/saemanas/container-base.git
   cd container-base
   git checkout develop
   git pull origin develop
   ```
2. **Create a feature branch (spec-kit naming)**
   ```bash
   git checkout -b NNN-some-spec
   ```
   Replace `NNN-some-spec` with the spec identifier (e.g., `002-billing-api`).
3. **Create a Python virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```
4. **Install dependencies**
   ```bash
   python -m pip install -r src/apps/api/requirements.txt
   python -m pip install -r src/apps/ocr/requirements.txt
   npm install --prefix src/apps/portal
   npx expo install --cwd src/apps/mobile
   ```
5. **Launch Supabase CLI stack (local)**
   ```bash
   supabase start
   ```
   The CLI prints connection details such as:
   - `API URL`: `http://127.0.0.1:54321`
   - `Publishable key`: `sb_publishable_...`
   - `Secret key`: `sb_secret_...`

   Export the keys for your shell session (do **not** commit them):
   ```bash
   export SUPABASE_URL=http://127.0.0.1:54321
   export SUPABASE_ANON_KEY="sb_publishable_..."
   export SUPABASE_SERVICE_ROLE_KEY="sb_secret_..."
   ```
   When finished, stop the stack with `supabase stop`.

6. **Run local validation before committing**
   ```bash
   ./scripts/run-all-checks.sh
   ```
   The script executes Ruff → Pytest → ESLint in the mandated order, records `{ts, opId, code, duration_ms}` metrics, and stages artifacts under `artifacts/ci/` so rollback drills have rehearsal evidence.
7. **Populate environment templates**
   - Fill in the placeholder values inside `src/apps/*/.env.example`.
   - Real secrets belong in GitHub Actions, Cloud Run, Supabase, Vercel, and Expo secret stores (see `docs/deployment/secrets-catalog.md`).
8. **Bootstrap services locally (local → stg → prod flow)**
   ```bash
   ./scripts/run-local.sh
   ```
   The launcher coordinates API, OCR worker, portal, and mobile dev servers while tailing logs for each surface.@scripts/run-local.sh#1-115

### Compliance evidence helpers
- **PDPA retention rehearsal**: `bash scripts/run-retention-job.sh --environment stg --tag <rollback-tag> --op-id rehearsal-<date>` generates Supabase confirmation logs in `artifacts/pdpa/` for rollback drills.
- **Notification snapshots**: `python scripts/send-ci-email.py --event success --service api --environment prod --ref <tag> --duration PT5M --artifact-url <artifact> --workflow-run-url <run> --op-id notif-<tag>` writes `.eml` files to `artifacts/notifications/` so email proofs accompany release notes.
- **Quota capture**: `python scripts/check-free-tier.py --artifact-dir artifacts/quotas --op-id quota-prod --append` stores the latest Supabase / Cloud Run / Vercel usage JSON and appends a markdown table to `docs/deployment/observability.md`.

## Continuous Integration

- GitHub Actions `ci.yml` runs Ruff → ESLint → Pytest → OpenAPI Lint (Redocly CLI) → Build → GHCR push.
- `scripts/validate-ci.sh` verifies mandatory files and secrets locally before running `act`.
- `scripts/measure-ci.sh` captures stage runtimes and appends them to `docs/deployment/ci-pipeline.md` for trend analysis.
- Tests live under `tests/` and include CI guardrails, contract linting, and deployment smoke suites.@tests/backend/test_ci_guardrails.py#25-44 @tests/contract/test_health_contract.py#1-40 @tests/integration/test_cloud_run.py#1-34

## Deployment

### Branch Workflow
- `main`: prod branch (protected). Only release-ready changes merge here.
- `develop`: stg branch (protected). Integrates validated spec branches before release.
- `NNN-some-spec`: Working branches are named after their spec-kit ID (e.g., `002-billing-api`). Branch from `develop`, complete the spec plan/tasks, then merge back via pull request after CI green and review approval.

**Protection rules (GitHub API snapshot, 2025-11-09)**  
- Enforce admins + linear history enabled on both `main` and `develop`.
- Strict status checks: merges require all configured CI jobs (Ruff → ESLint → Pytest → Redocly → Build → GHCR → Tag deploy) to finish green before landing.
- Required pull-request reviews: ≥1 approving review; stale reviews are not auto-dismissed, so code owners must re-request when pushing updates.
- Force pushes, branch deletions, and fork syncing are blocked to preserve audit trails. Use rollback tags instead of rewriting history.

### Deploy Checklist
1. **Activate environment**
   ```bash
   source .venv/bin/activate
   python -m pip install -r src/apps/api/requirements.txt -r src/apps/ocr/requirements.txt
   ```
2. **Run critical tests**
   ```bash
   pytest tests/backend/test_pdpa_compliance.py tests/worker/test_ocr_pdpa.py
   ```
3. **Kick off stg deploy** (auto on `develop`, or manual trigger):
    ```bash
    gh workflow run deploy-api.yml --ref develop --field environment=stg
    gh workflow run deploy-ocr.yml --ref develop --field environment=stg
    gh workflow run deploy-portal.yml --ref develop --field environment=stg
    ```
4. **Smoke test stg**
    ```bash
    curl https://api-stg.container-base.com/healthz
    curl https://ocr-stg.container-base.com/healthz
    ```
    Confirm portal loads via Vercel preview and Supabase connectivity is intact.
5. **Promote to prod** (manual approval + tag)
    ```bash
    gh workflow run deploy-api.yml --ref main --field environment=prod --field rollback_tag=v1.2.3
    gh workflow run deploy-ocr.yml --ref main --field environment=prod --field rollback_tag=v1.2.3
    gh workflow run deploy-portal.yml --ref main --field environment=prod
    - Ensure the stg deploy references `NEXT_PUBLIC_API_BASE_URL=https://api-stg.container-base.com` and renders deploy status assets (`src/apps/portal/public/deploy-status/en.json`, `th.json`).
   Check Vercel production domain, Supabase dashboards, and Cloud Run metrics for error spikes.
7. **Post-deploy validation**
    ```bash
    curl https://api.container-base.com/readyz
    curl https://ocr.container-base.com/readyz
   ```
   Check Vercel production domain, Supabase dashboards, and Cloud Run metrics for error spikes.
8. **Rollback reference**
   If issues arise, consult `docs/deployment/rollback-playbook.md` for tag-based rollback commands and communication checklist.
9. **Observability update**
   - Run `python scripts/check-free-tier.py --append` after release to record quota usage.
   - Optionally execute `python scripts/measure-latency.py --iterations 10` and log results per `docs/deployment/cost-guardrails.md`.

## Operational Playbooks

- `docs/deployment/observability.md` lists dashboards (Cloud Run, Supabase, Vercel) and automation scripts.
- `docs/deployment/pdpa-playbook.md` captures consent workflows and retention obligations.
- `docs/deployment/secrets-catalog.md` tracks secrets locations, scopes, and rotation cadence.
- `docs/deployment/supabase-schema.md` documents environment-specific schema and RLS.

## Governance & Typing Policy

- Spec-kit flow is mandatory: Spec → Plan → Tasks → Implementation → Tests → Verification (see `AGENTS.md`).
- Python services must use explicit static typing—annotated functions, Pydantic (or equivalent) validation, and Ruff/pyright cleanliness.
- CI/CD governance expects OpenAPI contracts in `contracts/` to remain canonical; downstream code consumes generated assets only.

## Roadmap & Further Reading

- `specs/001-lowcost-cicd-infra/` contains the reference spec, plan, research, and task backlog for the initial infrastructure feature set.
- `refs/docs/` hosts the CB charter, service plan, stack baselines, and UX standards that every new feature must cite.

---

Internal project – follow organization guidelines for distribution limits and PDPA compliance.
