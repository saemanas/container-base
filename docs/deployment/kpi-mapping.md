# KPI Mapping: Low-cost CI/CD & Infra Skeleton

This document links the success criteria defined in `specs/001-lowcost-cicd-infra/spec.md` to the operational signals, dashboards, and owners responsible for tracking them.

| KPI | Target | Data Source / Dashboard | Measurement Cadence | Owner | Remediation Trigger |
|-----|--------|-------------------------|---------------------|-------|---------------------|
| False Positive Recognition Rate (FPRR) | ≥ 90% | Vision evaluation reports (`/reports/vision-bench.json`), Grafana (future) | Weekly during model updates | ML Engineer | If FPRR < 90%, roll back to previous model version and open incident per `docs/deployment/rollback-playbook.md`. |
| API latency (P95) | ≤ 3 s | Cloud Run metrics board (`cb-api-*`); `scripts/measure-latency.py` snapshots | Daily during active releases | Platform Engineer | If P95 ≥ 2.4 s for 5 min, scale concurrency or queue requests; if ≥3 s persist, trigger rollback. |
| Rollback MTTR | ≤ 10 min | GitHub Actions deploy logs, `docs/deployment/rollback-playbook.md` audit notes | After each release or rollback drill | DevOps Engineer | If rollback exceeds 10 min, update playbook with bottleneck fixes and schedule another drill. |
| Offline upload success | ≥ 99% | Mobile telemetry (`queue_metrics` table in Supabase), Grafana dashboard (planned) | Weekly | Mobile Engineer | If success < 99%, inspect queue failure reasons, patch retry policy, and document outcome in `docs/deployment/observability.md`. |
| 30-day retention | ≥ 60% | Supabase analytics / product analytics (future) | Monthly | Product Manager | If retention drops below 60%, run churn analysis, adjust onboarding, and capture actions in product roadmap notes. |
| Monthly active containers | ≥ 1,000 | Supabase `container_events` aggregate view | Monthly | Product Manager | If goal is missed for two consecutive months, revisit acquisition or rollout plan; log in quarterly review. |
| Cost guardrails (Cloud Run/Supabase/Vercel) | ≤ 80% free-tier usage steady state | `python scripts/check-free-tier.py --append` output; `docs/deployment/cost-guardrails.md` | Weekly | Platform Engineer | If usage ≥80%, execute mitigation from `cost-guardrails.md` (scale down, archive data, adjust build cadence). |

## Review Routine
- **Weekly Platform Sync:** Review latency, cost guardrails, and queue metrics.
- **Bi-weekly ML Review:** Confirm FPRR trends and plan model retraining if required.
- **Monthly Product Sync:** Check retention, active containers, and publish summary to leadership notes.

## Notes
- Dashboard URLs and access instructions live in `docs/deployment/observability.md`.
- Automation scripts should append evidence (CI timing, free-tier usage, latency probes) whenever executed to maintain audit trails.
