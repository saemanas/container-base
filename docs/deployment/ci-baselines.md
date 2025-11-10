# CI Baseline Metrics

This document captures baseline KPIs prior to CI/CD hardening changes. Update before major pipeline revisions and attach supporting artifacts.

## Current Snapshot
- **Captured At**: {{TIMESTAMP}}
- **API P95 Latency**: {{API_P95_MS}} ms (from `scripts/measure-latency.py`)
- **OCR Success Rate**: {{OCR_SUCCESS_RATE}} % (from latest stg workflow logs)
- **CI Duration (Ruff → GHCR)**: {{CI_DURATION_MS}} ms (from `scripts/run-all-checks.sh` summary)
- **Evidence Artifacts**: `artifacts/ci/local-summary-<timestamp>.md`, Supabase smoke test logs in `artifacts/supabase/`

## Notes
- Re-run `scripts/run-all-checks.sh` and `scripts/measure-ci.sh` to refresh values.
- Archive raw outputs in GitHub Actions artifacts for compliance review.
