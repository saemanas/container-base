# Container Base Monorepo

Container Base replaces manual container logging with automated recognition, GPS tracking, and auditable billing. This repository hosts the polyglot stack (FastAPI API, OCR worker, Next.js portal, Expo mobile) plus shared CI/CD and infrastructure assets.

## Project Structure

```
.
├── src/apps/api/               # FastAPI service
├── src/apps/ocr-worker/        # OCR background worker
├── src/apps/portal/            # Next.js portal
├── src/apps/mobile/            # Expo mobile app
├── docs/deployment/            # Runbooks, guardrails, secrets, KPI mapping
├── scripts/                    # CI helpers, measurement utilities
├── specs/                      # Spec-kit artifacts (spec, plan, tasks, etc.)
└── tests/                      # Pytest suites for contracts, PDPA, guardrails
```

## Getting Started

1. **Clone the repo and switch to the feature branch**
   ```bash
   git clone https://github.com/saemanas/container-base.git
   cd container-base
   git checkout 001-lowcost-cicd-infra
   ```
2. **Create a Python virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```
3. **Install dependencies**
   ```bash
   python -m pip install -r src/apps/api/requirements.txt
   python -m pip install -r src/apps/ocr-worker/requirements.txt
   npm install --prefix src/apps/portal
   npx expo install --cwd src/apps/mobile
   ```
4. **Populate environment templates**
   - Fill in the placeholder values inside `src/apps/*/.env.example`.
   - Real secrets belong in GitHub Actions, Cloud Run, Supabase, Vercel, and Expo secret stores (see `docs/deployment/secrets-catalog.md`).

5. **Run services locally**
   ```bash
   export SUPABASE_URL=https://container-base-stg.supabase.co
   export SUPABASE_ANON_KEY=anon-key
   ./scripts/run-local.sh
   ```

## Deployment

### CI / CD Pipeline
- GitHub Actions `ci.yml` runs Ruff → ESLint → Pytest → Spectral → Build → GHCR push.
- Deployment workflows (`deploy-api.yml`, `deploy-ocr.yml`, `deploy-portal.yml`) publish Cloud Run/Vercel artifacts. Staging auto deploys on `develop`; production requires manual approval and tag selection.
- `scripts/validate-ci.sh` verifies mandatory files and secrets locally before running `act`.
- `scripts/measure-ci.sh` can be executed to capture stage runtimes and append them to `docs/deployment/ci-pipeline.md` for trend analysis.

### Deploy Checklist
1. **Activate environment**
   ```bash
   source .venv/bin/activate
   python -m pip install -r src/apps/api/requirements.txt -r src/apps/ocr-worker/requirements.txt
   ```
2. **Run critical tests**
   ```bash
   pytest tests/backend/test_pdpa_compliance.py tests/worker/test_ocr_pdpa.py
   ```
3. **Kick off staging deploy** (built-in auto deploy on `develop`, or manual trigger):
   ```bash
   gh workflow run deploy-api.yml --ref develop --field environment=staging
   gh workflow run deploy-ocr.yml --ref develop --field environment=staging
   gh workflow run deploy-portal.yml --ref develop --field environment=staging
   ```
4. **Smoke test staging**
   ```bash
   curl https://api-stg.container-base.com/healthz
   curl https://ocr-stg.container-base.com/healthz
   ```
   Confirm portal loads via Vercel preview and Supabase connectivity is intact.
5. **Promote to production** (manual approval + tag)
   ```bash
   gh workflow run deploy-api.yml --ref main --field environment=production --field rollback_tag=v1.2.3
   gh workflow run deploy-ocr.yml --ref main --field environment=production --field rollback_tag=v1.2.3
   gh workflow run deploy-portal.yml --ref main --field environment=production
   ```
6. **Post-deploy validation**
   ```bash
   curl https://api.container-base.com/readyz
   curl https://ocr.container-base.com/readyz
   ```
   Check Vercel production domain, Supabase dashboards, and Cloud Run metrics for error spikes.
7. **Rollback reference**
   If issues arise, consult `docs/deployment/rollback-playbook.md` for tag-based rollback commands and communication checklist.
8. **Observability update**
   - Run `python scripts/check-free-tier.py --append` after release to record quota usage.
   - Optionally execute `python scripts/measure-latency.py --iterations 10` and log results per `docs/deployment/cost-guardrails.md`.

## Observability & Guardrails
- `docs/deployment/observability.md` lists dashboards (Cloud Run, Supabase, Vercel) and automation scripts.
- `docs/deployment/cost-guardrails.md` documents quota triggers (≥80%) and the remediation playbook.
- `scripts/measure-ci.sh`, `scripts/measure-latency.py`, and `scripts/check-free-tier.py` assist with performance and quota tracking.

## Static Typing Policy
Per `AGENTS.md` and the constitution, **all Python services must use explicit static typing**:
- Function signatures annotated; no implicit `Any`.
- Data validation handled via Pydantic (or equivalent) models.
- Ruff/pyright must pass.

## License
Internal project – see organization guidelines for distribution limits.
