# `run-retention-job.sh`

## Purpose
Log PDPA retention job executions, capture structured metadata for rollback drills, and optionally fail to exercise alerting paths.

## Behavior
- Requires `--environment`, `--tag`, and `--op-id`.
- Verifies `SUPABASE_SERVICE_ROLE_KEY` and `SUPABASE_PROJECT_REF`, then records a JSON artifact under `artifacts/pdpa/<opId>-<run>.json` containing masked keys and structured fields `{ts, opId, code, duration_ms}`.
- Optionally runs `supabase events list` (noop in CI) and respects `PDPA_RETENTION_FORCE_FAILURE=1` to simulate failure.

## Usage
```
SUPABASE_SERVICE_ROLE_KEY=sb_secret ...
SUPABASE_PROJECT_REF=container-base-prod
scripts/run-retention-job.sh --environment prod --tag v1.2.3 --op-id api-prod-rollback
```

## Notes
- Used in `cd-api.yml` / `cd-ocr.yml` rollback phases to prove PDPA retention compliance before EMR communication.
- The resulting artifact is referenced via `docs/deployment/observability.md`/`rollback-playbook.md`.
