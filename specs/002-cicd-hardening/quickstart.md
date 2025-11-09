# Quickstart — CI/CD Hardening & Multicloud Release Readiness

## Prerequisites
- Python 3.12.x with virtualenv support installed locally.@refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#66-128
- Node.js 22.21.1 LTS (`nvm use 22.21.1` recommended).@refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#66-128
- Docker Engine ≥26 with Compose v2.29+ for Cloud Run parity testing.@refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#66-128
- Auth to GitHub Actions, Cloud Run, Supabase, Vercel, and Cloudflare via GitHub environments per secrets catalog.@README.md#54-122 @docs/deployment/secrets-catalog.md#1-200

## Local Validation Flow
1. Activate the Python environment and install CI dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r src/apps/api/requirements.txt -r src/apps/ocr-worker/requirements.txt
   ```@README.md#36-82
2. Install frontend tooling (portal + shared scripts):
   ```bash
   npm install --prefix src/apps/portal
   ```@README.md#43-48
3. Run the consolidated checks to mirror CI sequencing:
   ```bash
   ./scripts/run-all-checks.sh
   ```
   This executes Ruff → ESLint → Pytest → OpenAPI Lint, matching FR-001 ordering before container builds and GHCR pushes.@README.md#49-61 @specs/002-cicd-hardening/spec.md#20-85
4. Generate CI evidence artifacts locally when needed:
   ```bash
   ./scripts/measure-ci.sh && ./scripts/validate-ci.sh
   ```
   Archive produced logs under `.artifacts/` to emulate GitHub Actions retention for audits.@README.md#63-116 @specs/002-cicd-hardening/spec.md#12-85

## Supabase Migration Rehearsal
1. Run the scripted Supabase smoke test (wraps pull → push → RLS test) to capture evidence locally:
   ```bash
   SUPABASE_STAGING_REF=<staging-ref> ./scripts/supabase-smoke-test.sh
   ```@specs/002-cicd-hardening/spec.md#72-85 @specs/002-cicd-hardening/tasks.md#33-41
   This script stores logs under `artifacts/supabase/` for later upload to GitHub artifacts.
2. Export the latest staging schema migrations and apply in a local sandbox when manual inspection is needed:
   ```bash
   supabase db pull --project-ref <staging-ref>
   supabase db push --project-ref <local-ref>
   ```
3. Execute Supabase CLI RLS smoke tests (if running manually outside the script):
   ```bash
   supabase db test --project-ref <staging-ref> --tests supabase/tests/rls
   ```@specs/002-cicd-hardening/spec.md#72-85
4. Once tests pass, commit migration scripts to the repo and prepare GitHub environment approvals referencing the captured logs.

## Deployment Dry Run
1. Use Docker Compose to build API and OCR worker containers with GHCR tags:
   ```bash
   docker compose -f deploy/docker-compose.ci.yml build api ocr-worker
   ```@refs/docs/CB-MiniOps-v1.0.0-en-US.md#140-218
2. Trigger staging workflows via GitHub CLI:
   ```bash
   gh workflow run ci.yml --ref develop
   gh workflow run deploy-api.yml --ref develop --field environment=staging
   gh workflow run deploy-ocr.yml --ref develop --field environment=staging
   gh workflow run deploy-portal.yml --ref develop --field environment=staging
   ```@README.md#87-104
3. Verify health endpoints and portal status once artifacts deploy:
   ```bash
   curl https://api-stg.container-base.com/readyz
   curl https://ocr-stg.container-base.com/readyz
   ```@README.md#93-110
4. Confirm notification emails land in the operations distribution list and archive them alongside GitHub Actions artifacts for compliance.

## Rollback Drill Checklist
1. Tag the previous production release locally:
   ```bash
   git fetch origin
   git checkout tags/<previous-tag>
   ```
2. Invoke rollback workflows with the `rollback_tag` input:
   ```bash
   gh workflow run deploy-api.yml --ref main --field environment=production --field rollback_tag=<previous-tag>
   gh workflow run deploy-ocr.yml --ref main --field environment=production --field rollback_tag=<previous-tag>
   ```@README.md#100-112
3. Ensure total execution completes ≤10 minutes and that structured logs include `{ts, opId, code, duration_ms}` for every stage; attach artifacts to the ReleaseChecklist entry.
