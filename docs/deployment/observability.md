# Observability Playbook

This document enumerates the dashboards, scripts, and alerting flows used to observe the Container Base platform.

## Dashboards

| Surface | Dashboard | Location | Purpose |
|---------|-----------|----------|---------|
| API (Cloud Run) | Cloud Run metrics board | Google Cloud Console → Cloud Run → `cb-api-*` | Monitor request latency (P50/P95), error rate, concurrency, CPU/memory usage |
| OCR Worker (Cloud Run) | Cloud Run metrics board | Google Cloud Console → Cloud Run → `cb-ocr-*` | Track worker loop heartbeat, queue depth, invocation failures |
| Supabase | Usage dashboard | Supabase Console → Project → Reports | Verify row read/write counts, storage utilization, function execution |
| Vercel Portal | Vercel Analytics | Vercel Dashboard → Project → Analytics | Observe build minutes, response latency, error rate |
| KPI Aggregation | Grafana (future) | TBD | Aggregate KPI mapping (FPRR, P95, retention) once data warehouse is online |

## Alert Sources
- **Cloud Run**: Create alert policies on latency (P95) ≥ 2.4 s, error rate ≥ 1%, CPU usage ≥ 80% for 5 min.
- **Supabase**: Configure email usage alerts for 80% of row-read quota and storage consumption.
- **Vercel**: Enable build-minute alerts at ≥ 80 minutes on the Hobby plan.

## Automation Scripts

| Script | Description | How to Run | Output |
|--------|-------------|------------|--------|
| `scripts/measure-ci.sh` | Times CI stages locally and appends results to `docs/deployment/ci-pipeline.md`. | `./scripts/measure-ci.sh` | JSON log + appended markdown table |
| `scripts/check-free-tier.py` | Checks Supabase / Cloud Run / Vercel quotas via API and prints summary. | `python scripts/check-free-tier.py` | stdout JSON summary and optional markdown note |
| `scripts/measure-latency.py` | Probes API/OCR endpoints and records latency percentiles into `docs/deployment/cost-guardrails.md`. | `python scripts/measure-latency.py --iterations 10` | stdout metrics + updated markdown |

## Runbook
1. Execute `scripts/check-free-tier.py` daily during peak season.
2. Run `scripts/measure-ci.sh` weekly to track pipeline regression.
3. Run `scripts/measure-latency.py` whenever Cloud Run alerts trigger or before major releases.
4. Log the results into this document and cross-link to incident reports in `docs/deployment/observability.md`.
