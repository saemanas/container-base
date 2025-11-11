# Integration Tests (`tests/integration`)

Count multiple-system scenarios (CI gate, Cloud Run readiness, release drills) ensuring deployments stay compliant before merging to protected branches.

| Test | Purpose | Notes |
| --- | --- | --- |
| `test_ci_pdpa_failure.py` | Runs `scripts/run-all-checks.sh` with `PDPA_FORCE_FAILURE=1` to confirm the PDPA gate halts the pipeline, aligned with AGENTS PDPA-Safe Data Stewardship. | Marked `@pytest.mark.slow`/`integration`. |
| `test_cloud_run.py` | Loads `specs/.../openapi.yaml` and asserts `/healthz` & `/readyz` entries exist, ensuring Cloud Run health contracts stay part of the API spec. | Supports `docs/deployment/ci-pipeline.md`. |
| `test_cost_guardrails.py` | Validates `docs/deployment/cost-guardrails.md` documents 80% thresholds for Cloud Run, Supabase, Vercel, plus rollback remediation text. | Helps trace quota metrics referenced by `check-free-tier.py`. |
| `test_multicloud_deploy.py` | Asserts `cd-api.yml`/`cd-ocr.yml` expose stg/prod workflow_dispatch options and include prod approval messaging so manual gates are enforced. | Works with `docs/deployment/ci-pipeline.md` & `docs/deployment/rollback-playbook.md`. |
| `test_portal_build.py` | Smoke tests portal setup: checks `package.json` exists and `.env.example` contains key portal placeholders (NEXT_PUBLIC_*). | Node install prerequisites verified before watchers. |
| `test_rollback_drill.py` | Ensures `cd-api.yml` & `cd-ocr.yml` declare `timeout-minutes ≤ 10` and that rollback steps emit `{ts, opId, code, duration_ms}` telemetry. | Aligns with rollback MTTR KPI. |
| `test_supabase_promotion.py` | Confirms `scripts/promote-supabase.sh` exists, logs staging before prod, runs RLS tests, and pushes production migrations after stage validation. | Tied to Supabase promotion docs in `docs/deployment/supabase-schema.md`. |

Integration suites complement the guardrails by executing or examining the same workflows/scripts described in deployment docs.
