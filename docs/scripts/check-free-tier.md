# `check-free-tier.py`

## Purpose
Assess free-tier quotas across Cloud Run, Supabase, and Vercel to ensure the CI/CD budget guardrails from `docs/deployment/cost-guardrails.md` remain intact.

## What it does
- Reads optional JSON usage data (or uses built-in defaults) and computes percent/ status (ok/warning/critical/exceeded).
- Emits a structured JSON summary to stdout plus a `logs`-style record describing `{ts, opId, code, duration_ms}` for the given `--op-id`.
- When `--append` is provided, inserts a markdown table into `docs/deployment/observability.md` under a timestamped heading.
- Persists artifacts under `artifacts/quotas/<op-id>-<run>.json` for release retros.

## Inputs
- `--source PATH`: custom JSON file describing `service`, `metric`, `used`, `limit`.
- `--append`: append table to observability doc.
- `--artifact-dir`: where to store JSON artifacts (default `artifacts/quotas`).
- `--op-id`: operational identifier for structured log (defaults to `quota-summary`).

## Related Gov Docs
- `docs/deployment/observability.md` (records appended tables).
- `docs/deployment/cost-guardrails.md` (context for thresholds).

