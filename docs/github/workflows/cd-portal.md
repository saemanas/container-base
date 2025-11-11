# CD - Portal Workflow (`.github/workflows/cd-portal.yml`)

## Purpose
- Deploys the Next.js 16 / React 19 portal via Vercel with readiness, stack guard, and PDPA/UX observability guardrails, satisfying AGENTS.md portal expectations and the constitution’s Instant, Resilient, Clear UX principle.
- It depends on backend readiness before building to keep release status assets (`public/deploy-status/en.json`/`th.json`) accurate.

## Triggers & Inputs
- Runs on pushes to `develop` and manual dispatches (`environment`, `backend_ready_url`).
- Grants `NODE_VERSION=22.21.1`, `PORTAL_DIR=src/apps/portal`, `STATUS_ASSET_DIR=src/apps/portal/public/deploy-status` to ensure environment alignment with mandated stack baselines.

## Jobs
**deploy** job** (timeout 20m)
- Prod approval: prints reminder that GitHub environment approvals gate the job when `$TARGET_ENV == 'prod'`.
- Backend readiness: polls `API_READY_URL_STG/PROD` secrets or the override `backend_ready_url` (up to five attempts). Failing readiness fails the job, preserving UX clarity.
- Node setup + npm install/build: runs `npm install`/`npm run build` inside the portal directory, then validates EN/TH deploy status assets exist to satisfy portal UX triad states.
- Vercel deploy placeholder: logs simulation commands for prod/stg; actual team should replace with `vercel deploy` using `VERCEL_TOKEN` + `VERCEL_PROJECT_ID/ORG` stored in GitHub Environments.
- Cloudflare purge (prod only): uses `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ZONE_ID_PORTAL` to purge `portal.container-base.com`, waits for DNS propagation, and logs warnings when tokens missing.
- Post-deploy reminder: prompts manual verification of portal status assets.

## Secrets & Observability
- While Vercel tokens live in Secrets (`VERCEL_TOKEN`, `VERCEL_PROJECT_ID`, `VERCEL_ORG_ID`), the workflow also references `API_READY_URL_*` to compute staging/prod readiness.
- Cloudflare purge and propagation rely on `CLOUDFLARE_ZONE_ID_PORTAL`; log lines must include structured tokens for `{ts, opId, code}` to stay consistent with structured logging requirements.
- Documented in `docs/deployment/observability.md` under Portal readiness, so any change to the cleanup or readiness step must trigger doc updates.

## Notes
- This document must be revisited if the portal instrumentation extends to real Vercel deploy commands or if additional UX states/logging steps are introduced.
