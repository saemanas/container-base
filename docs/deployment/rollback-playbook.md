# Deployment Rollback Playbook

This playbook documents how to revert Container Base services within the mandated ≤10 minutes MTTR. Follow the steps in order. All commands assume the repository root and authenticated CLI sessions.

## Preconditions
- GHCR images are tagged with semantic versions (`vX.Y.Z`) during successful deploys.
- GitHub Actions CD workflows (`cd-api.yml`, `cd-ocr.yml`) accept manual inputs for rollback tags.
- Cloud Run services are named `cb-api-stg`, `cb-api-prod`, `cb-ocr-stg`, `cb-ocr-prod`.

## Rollback Steps

1. **Identify Failing Revision**
   - Check Cloud Run dashboard or `gcloud run services describe` for the current revision and error logs.
   - Record failing revision ID and timestamp in `docs/deployment/observability.md`.

2. **Select Prior Artifact**
   - List GHCR images:
     ```bash
     gh api /user/packages/container/package/container-base-api/versions | jq '.[].metadata.container.tags'
     ```
   - Choose the most recent known-good tag (e.g., `v1.2.3`).
   - Retrieve the digests captured by staging deploys (stored under `artifacts/digests/*.txt` by the CI workflows) to ensure production rollbacks use immutable references.

3. **Trigger Rollback Workflow**
   - API: `gh workflow run cd-api.yml --ref main --field environment=production --field rollback_tag=v1.2.3`
   - OCR: `gh workflow run cd-ocr.yml --ref main --field environment=production --field rollback_tag=v1.2.3`
   - Portal: `gh workflow run cd-portal.yml --ref main --field environment=production --field backend_ready_url=<readyz-url>` or use `vercel rollback <deployment-id>` if necessary.
   - Ensure Supabase migrations are not re-run; consult `scripts/promote-supabase.sh` metadata JSON in `artifacts/supabase/` to confirm most recent RLS smoke-test evidence.

4. **Verify Health**
   - `curl https://api.container-base.com/healthz`
   - `curl https://ocr.container-base.com/healthz`
   - `curl https://portal.container-base.com` (ensure expected version banner).
   - Confirm Cloudflare propagation by running `dig +short api.container-base.com` and `dig +short portal.container-base.com`; if stale, invoke the Cloudflare purge step manually as described in `cd-api.yml`.

5. **Communicate Status**
   - Post incident update in Platform channel with timelines and remaining risks.
   - Update `docs/deployment/observability.md` incident log.

## Post-Rollback Actions
- Create follow-up issue outlining root cause and mitigation plan.
- Schedule regression test run (`pytest && npm test --prefix src/apps/portal`).
- Re-enable automated deploys only after fix is merged and validated in staging.
