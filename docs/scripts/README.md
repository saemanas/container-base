# Scripts Directory Reference

Each file under `scripts/` implements a discrete automation step referenced from AGENTS, the constitution, or the deployment docs. The table below maps scripts to their “why,” what inputs they require, and where their outputs land so the peel-back of CI/CD governance stays traceable.

| Script | Purpose | Inputs / Outputs |
| --- | --- | --- |
| `check-free-tier.py` | Validates Cloud Run/Supabase/Vercel quota usage, emits JSON summary, and optionally appends a table to `docs/deployment/observability.md`. | CLI flags: `--source`, `--append`, `--artifact-dir`, `--op-id`; writes `artifacts/quotas/<op-id>-<run>.json` and structured log with `{ts,opId,code,duration_ms}`. |
| `check-portal-stack.py` | Enforces Next.js 16 / React 19 dependency majors in `src/apps/portal/package.json` (runs after portal ESLint). | No args; fails CI when majors drift, matching refs/docs stack requirements. |
| `measure-ci.sh` | Runs Ruff → ESLint → Pytest → OpenAPI lint → Docker build locally, captures durations, and appends tables to `docs/deployment/ci-pipeline.md`. | Depends on Python/npm/docker; respects `MEASURE_CI_ARTIFACT_DIR`. |
| `measure-latency.py` | Probes readyz endpoints, summarizes min/avg/p95/max latencies, and (with `--append`) records results in `docs/deployment/cost-guardrails.md`. | Flags: `--url`, `--iterations`, `--timeout`, `--append`. |
| `promote-supabase.sh` | Pushes migrations to staging, runs RLS tests, then promotes to production while writing metadata for rollback/PDPA audits in `artifacts/supabase`. | Requires Supabase CLI + `STG_REF`, `PROD_REF`, `RLS_TEST_PATH`; writes JSON metadata per run. |
| `run-all-checks.sh` | Enforces Ruff → Pytest → ESLint pre-commit order, emitting stage timing summaries under `artifacts/ci/local-summary-*.md`. | Needs `.venv`, Ruff/Pytest installed; respects `PDPA_FORCE_FAILURE` toggle. |
| `run-local.sh` | Loads `.env`, validates Supabase/portal keys, and brings up `docker compose` so all services share one config. | Relies on populated `.env` and Docker Compose; exits with guidance if key missing. |
| `run-retention-job.sh` | Logs PDPA retention triggers, writes JSON artifacts to `artifacts/pdpa/`, and supports forced failures via `PDPA_RETENTION_FORCE_FAILURE`. | Requires `--environment`, `--tag`, `--op-id`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_PROJECT_REF`. |
| `send-ci-email.py` | Renders success/failure/rollback email templates, archives `.eml` artifacts, and prints structured logs referenced in notification docs. | Accepts `--event`, `--service`, `--environment`, `--ref`, `--duration`, `--artifact-url`, `--workflow-run-url`, `--op-id`; needs `OPS_EMAIL_TO`, `OPS_EMAIL_FROM`, optional `OPS_EMAIL_CC`. |
| `supabase-smoke-test.sh` | Pulls staging schema, applies it to a local reference, executes Supabase RLS smoke tests, and logs the run for release checklists. | Needs Supabase CLI + `SUPABASE_STG_REF`; logs to `artifacts/supabase/rls-smoke-*.log`. |
| `validate-ci.sh` | Pre-flight gate ensuring required files, commands, env vars exist before running CI locally; logs JSON outcomes for each check. | Verifies `.ruff.toml`, `.github/workflows`, `python3`, `npm`, `docker`, and envs like `API_SUPABASE_URL`/`OCR_TIMEOUT_MS`. |

Refer to the accompanying per-script docs (`docs/scripts/<script>.md`) for detailed options, sample commands, and ties to AGENTS/constitution principles.
