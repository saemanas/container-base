# CD - API Workflow (`.github/workflows/cd-api.yml`)

## Purpose
- Manages staged and production deployments of the FastAPI service to Cloud Run and ensures rollback/replay guardrails (≤10min) that the constitution enforces.
- Connects to GHCR (image digest management), Cloud Run, Cloudflare, and PDPA retention automation so the API surface stays traceable per `docs/deployment/rollback-playbook.md` and `docs/deployment/ci-pipeline.md`.

## Triggers & Inputs
- Pushes to `develop` or manual `workflow_dispatch` (with `environment`, `rollback_tag`, `image_digest`).
- Inputs allow you to force a digest (for production immutability) or reuse a rollback tag. Manual approval gates exist via GitHub Environments before the `deploy` job (prod) runs.

## Jobs
1. **deploy-stg**
   - Timeout 15 minutes, caches pip wheels, authenticates `GCLOUD_SERVICE_ACCOUNT_JSON`, deploys to Staging Cloud Run (`cb-api-stg`), logs GHCR authentication, captures image digests in `artifacts/digests/api-stg.txt`, and uploads the chunk for future digest resolution.
2. **deploy (prod)**
   - Depends on staging; resolves image references using provided digest/rollback tag/stg digest; deploys Cloud Run `cb-api-prod`, emits structured rollback logs (`printf` with `{ts, opId, code, duration_ms}`), runs `scripts/run-retention-job.sh` (guarded by `SUPABASE_SERVICE_ROLE_KEY` + `SUPABASE_PROJECT_REF`), prompts for PDPA retention evidence, purges Cloudflare cache, and posts deployment reminders.

## Secrets & values tracked
- Cloud Run: `GCP_PROJECT_ID`, `CLOUD_RUN_REGION`, `GCLOUD_SERVICE_ACCOUNT_JSON` (documented in `docs/deployment/workflow-secrets.md`).
- GHCR: `PROJECT_TOKEN` for pushing the image digest.
- PDPA: `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_PROJECT_REF` feed the retention script; PDPA logs land in `artifacts/pdpa/` for ≤48h evidence.
- Cloudflare: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ZONE_ID` (api-specific) and `TARGET_DOMAIN` for propagation/ cache purge.

## Compliance annotations
- Timeout `timeout-minutes: 10` ensures rollback jobs finish within MTTR budgets.
- Structured logs emitted by the rollback step make downstream dashboards ingestable (per constitution’s PDPA-Safe Data Stewardship and Test-First Observability). 
- Documentation should mention artifacts referenced from `docs/deployment/observability.md` and `docs/deployment/rollback-playbook.md`.
