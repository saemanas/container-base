# Container Base Infrastructure Skeleton

Container Base is a low-cost CI/CD and infrastructure scaffold supporting API, OCR worker, web portal, and mobile clients for autonomous container tracking in Thailand.@refs/docs/CB-Instruction-v1.0.0-en-US.md#21-63

## Repository Layout

```
src/
  apps/
    api/
      Dockerfile
      service/
    ocr-worker/
      Dockerfile
    portal/
      package.json
    mobile/
      app.config.ts
.github/workflows/
  ci.yml
  deploy-api.yml
  deploy-ocr.yml
  deploy-portal.yml
docs/deployment/
  ci-pipeline.md
  pdpa-playbook.md
  secrets-catalog.md
  supabase-schema.md
specs/001-lowcost-cicd-infra/
  spec.md
  plan.md
  tasks.md
scripts/
  run-local.sh
```

> Folder strategy keeps each surface in its own build context while centralizing governance assets and workflows.@specs/001-lowcost-cicd-infra/plan.md#47-79

## Getting Started

1. **Prerequisites**
   - Docker, Docker Compose, Node.js 22, Python 3.12, and Supabase access tokens as described in the secrets catalog.@docs/deployment/secrets-catalog.md#1-57
2. **Bootstrap services locally**
   ```bash
   ./scripts/run-local.sh
   ```
   The launcher coordinates API, OCR worker, portal, and mobile dev servers while tailing logs for each surface.@scripts/run-local.sh#1-115
3. **Configuration**
   - Copy each `.env.example` to `.env` and populate credentials in your secret manager (never commit real values).@specs/001-lowcost-cicd-infra/spec.md#65-74

## Continuous Integration

GitHub Actions enforces a shared pipeline running Ruff, ESLint, Pytest, Spectral, container builds, and GHCR pushes before deployment steps.@specs/001-lowcost-cicd-infra/spec.md#65-74 @.github/workflows/ci.yml#1-183

- Run `./scripts/validate-ci.sh` locally to emulate the contract checks with structured JSON logging.@scripts/validate-ci.sh#1-35
- Tests live under `tests/` and include CI guardrails, contract linting, and deployment smoke suites.@tests/backend/test_ci_guardrails.py#1-19 @tests/contract/test_health_contract.py#1-31 @tests/integration/test_cloud_run.py#1-38

## Deployment Workflows

Phase 4 introduces GitHub Actions deploy pipelines for each surface:

- **API**: `deploy-api.yml` promotes images to Cloud Run. Staging auto-deploys on `develop`; production requires a manual dispatch with approval gates.@.github/workflows/deploy-api.yml#1-74
- **OCR Worker**: `deploy-ocr.yml` mirrors the Cloud Run strategy (to be implemented next).
- **Portal**: `deploy-portal.yml` targets Vercel hobby environments (to be implemented next).

Health and readiness endpoints (`/healthz`, `/readyz`) are defined in the API to satisfy Cloud Run probes and smoke tests.@src/apps/api/service/main.py#15-24 @tests/integration/test_cloud_run.py#1-38

## Operational Playbooks

Operational guides live under `docs/deployment/` and cover PDPA consent, Supabase schema isolation, CI pipeline expectations, and secrets governance.@docs/deployment/pdpa-playbook.md#1-27 @docs/deployment/supabase-schema.md#1-49 @docs/deployment/ci-pipeline.md#1-25

## Roadmap

Implementation proceeds per `specs/001-lowcost-cicd-infra/tasks.md`, progressing from foundational setup through deployment automation and cost guardrails.@specs/001-lowcost-cicd-infra/tasks.md#1-104

---

For detailed requirements, architecture decisions, and open tasks, consult `spec.md`, `plan.md`, and `tasks.md` within the feature directory.@specs/001-lowcost-cicd-infra/spec.md#61-118 @specs/001-lowcost-cicd-infra/plan.md#47-79
