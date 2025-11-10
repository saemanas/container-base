# Cost & Quota Guardrails

This document tracks the low-cost operating limits for Container Base services so that spending and free-tier allocations stay within budget. Monitor these metrics via Cloud Run, Supabase, and Vercel dashboards. Trigger remediation when thresholds are hit.

## Key Metrics & Thresholds

| Surface | Metric | Free Tier Budget | Guardrail Trigger (≥80%) | Monitoring Source |
|---------|--------|------------------|--------------------------|-------------------|
| Cloud Run API | Concurrent requests per instance | 5 | ≥4 concurrent requests sustained for 5 minutes | Cloud Run Metrics → `run.googleapis.com/container/concurrency` |
| Cloud Run API | Monthly CPU-seconds | 360,000 | ≥288,000 CPU-s | Cloud Billing Budget alert |
| Cloud Run OCR | Request latency (P95) | 3 s | ≥2.4 s sustained for 5 min | Cloud Run Metrics |
| Cloud Run OCR | Monthly requests | 2,000,000 | ≥1,600,000 requests | Cloud Run Metrics |
| Supabase | Row reads | 4,000,000 | ≥3,200,000 reads | Supabase Usage dashboard |
| Supabase | Storage (GB) | 8 | ≥6.4 GB | Supabase Storage dashboard |
| Vercel | Build minutes | 100 | ≥80 minutes | Vercel usage dashboard |

## Alerting Playbook

1. **Detect Trigger**
   - Alerts configured via Cloud Monitoring, Supabase email alerts, and Vercel usage notifications.
   - Guardrail thresholds are ≥80% of the monthly free-tier allocation.

2. **Acknowledge**
   - Log the incident in `docs/deployment/observability.md` with timestamp, metric, and operator.
   - Notify the Platform channel within 30 minutes.

3. **Mitigate**
   - **Cloud Run**
     - Scale concurrency down to 3 per instance via `gcloud run services update`.
     - Enable request queuing in Cloud Tasks if spikes persist.
     - Run `python scripts/measure-latency.py --append` to confirm recovery; investigate if P95 ≥ 2400 ms.
   - **Supabase**
     - Archive cold data to Cloud Storage; run retention job early if near 80%.
     - Optimize queries to lower read counts (add indexes, cache).
   - **Vercel**
     - Switch portal preview builds to manual approval during peak usage.
     - Cache heavy build steps or downgrade to static export.

4. **Rollback / Backoff**
   - If mitigation fails, execute the rollback plan:
     - Revert to prior container image tags (`scripts/rollback/<service>.sh` once implemented).
     - Temporarily disable non-critical endpoints via feature flags.

5. **Review**
   - After mitigation, record the outcome in `docs/deployment/observability.md` and open a follow-up ticket if structural changes are needed.

## Simulation Checklist

- [ ] Run `pytest tests/integration/test_cost_guardrails.py` to verify documentation still lists thresholds and rollback steps.
- [ ] Execute stg load test (k6 script) monthly to exercise Cloud Run guardrail alerting.
- [ ] Confirm Supabase and Vercel alert emails reach on-call distribution list each quarter.
- [ ] Capture latency snapshots with `python scripts/measure-latency.py --iterations 5 --append` before and after major releases; review appended tables in this document.
