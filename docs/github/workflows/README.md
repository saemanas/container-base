# GitHub Workflows Overview

This document summarizes `.github/workflows/` entries so contributors know which CI/CD gates enforce the constitution, PDPA controls, and portal stack policies.

| Workflow | Responsibility | Key Artifacts | Compliance Notes |
| --- | --- | --- | --- |
| `ci.yml` | Repository-wide CI gate covering API, OCR, OpenAPI, portal lint/build, Docker image build, GHCR push, and tag evidence stages | `artifacts/ci/{ruff,eslint,pytest,openapi_lint,build,ghcr,tag_deploy}` plus `artifacts/ci/openapi_lint/*` diffs | Enforces Ruff → ESLint → Pytest → Redocly → Build → GHCR → Tag order; runs `scripts/check-portal-stack.py`, records `{ts,opId,code,duration_ms}`, and archives PDPA regression test logs |
| `cd-api.yml` | Staged & prod Cloud Run deploys for API including digest capture, rollback guard (`timeout-minutes: 10`), retention job, Cloudflare purge, structured logs | `artifacts/digests/api-*.txt`, `artifacts/pdpa/`, Cloud Run deploy steps | Requires `PROJECT_TOKEN`, `GCLOUD_SERVICE_ACCOUNT_JSON`, Cloudflare/Supabase secrets; documents in `docs/deployment/rollback-playbook.md`, `observability.md` |
| `cd-ocr.yml` | Same as `cd-api` but targeting OCR worker Cloud Run services; retains digest artifacts and PDPA retention logs | `artifacts/digests/ocr-*.txt`, `artifacts/pdpa/` | Shares secrets catalog, enforces rollback MTTR, Cloudflare purge (OCR zone), PDPA retention job |
| `cd-portal.yml` | Vercel portal deployments with backend readiness probe, EN/TH status asset validation, Cloudflare purge, and post-deploy reminders | none | Uses `API_READY_URL_*`, `CLOUDFLARE_ZONE_ID_PORTAL`, `VERCEL_*` secrets; ensures Next.js 16/React 19 build outputs and portal UX status |

## Maintenance pointers
- Update this page whenever any workflow adds/removes jobs, changes artifact paths, or changes secret requirements.
- Each workflow's dedicated `docs/github/workflows/*.md` should be edited alongside this overview to keep fine-grained details matched.
- Align any new workflow descriptions with AGENTS/constitution checkpoints (spec-to-verification order, structured logs, PDPA retention, rollback ≤10m).
