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

## Rollback Drill Evidence Matrix
| Measure | Target | Collection Method | Artifact Location |
|---------|--------|-------------------|-------------------|
| Rollback MTTR | ≤ 10 minutes | GitHub Actions `deploy-*.yml` production jobs (`timeout-minutes: 10`) | Actions run summary + `tests/integration/test_rollback_drill.py` evidence |
| Structured Logs | `{ts, opId, code, duration_ms}` per stage | `printf` step in deploy workflows | Workflow logs exported to Actions artifacts |
| PDPA Retention Confirmation | Supabase audit log within 48 h | `scripts/run-retention-job.sh --environment production --op-id <id>` | `artifacts/pdpa/<op-id>-<run>.json` |
| Notification Archive | Success / Failure / Rollback emails | `scripts/send-ci-email.py --event <type>` | `artifacts/notifications/<op-id>-<event>.eml` |

### Rollback Drill Procedure Checklist
1. Trigger rollback workflows with `rollback_tag` input (see quickstart).
2. Monitor GitHub Actions duration; ensure completion ≤ 10 minutes and export log bundle.
3. After the retention job step runs, upload the generated JSON from `artifacts/pdpa/` to the compliance folder.
4. Verify the notification `.eml` artifact exists and forward to the operations distribution list.
5. Update ReleaseChecklist entry with artifact links and attach to incident ticket if applicable.
