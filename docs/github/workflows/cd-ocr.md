# CD - OCR Workflow (`.github/workflows/cd-ocr.yml`)

## Purpose
- Mirrors `cd-api` but targets the OCR worker running on Cloud Run, ensuring multicloud readiness and PDPA retention logs per the constitution’s Automated CI/CD & Versioned Releases rules.
- The workflow ensures staged digest capture and structured rollback logs, allowing audit reviewers to trace OCR deployments in artifacts/CI evidence.

## Triggers & Inputs
- Fires on pushes to `develop` or `workflow_dispatch` requests with `environment`, `rollback_tag`, or `image_digest` like `cd-api` for predictable deploy gates.

## Jobs
1. **deploy-stg**
   - Same structure as API staging: caches pip wheels, authenticates GCP via `GCLOUD_SERVICE_ACCOUNT_JSON`, deploys `cb-ocr-stg`, pushes GHCR login entries, captures `artifacts/digests/ocr-stg.txt`, and uploads it for prod jobs.
2. **deploy (prod)**
   - Resolves image references; deploys `cb-ocr-prod` Cloud Run service with `timeout-minutes: 10`; emits structured rollback log (`{ts, opId, code, duration_ms}`), runs `scripts/run-retention-job.sh`, prints verification reminders, purges Cloudflare cache (OCR-specific zone ID) and polls DNS.

## Secrets & artifacts
- Shares GHCR, Supabase (`SUPABASE_*`), Cloud Run (`GCP_PROJECT_ID`, `CLOUD_RUN_REGION`, `GCLOUD_SERVICE_ACCOUNT_JSON`), and Cloudflare (`CLOUDFLARE_*_OCR`) secrets with `cd-api`, requiring consistent updates in `docs/deployment/workflow-secrets.md`.
- Artifacts (`artifacts/digests`, `artifacts/pdpa`) appear in `docs/deployment/observability.md` roller tables.

## Compliance notes
- PDPA retention job is invoked under `scripts/run-retention-job.sh`, guaranteeing consent evidence even on rollback drils (matching the Observability playbook’s Rollback Drill Evidence Matrix).
- Cloudflare purge step includes conditional warnings when credentials missing, ensuring the workflow fails loudly to preserve DNS consistency.
