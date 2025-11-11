# OCR Worker (`src/apps/ocr`)

## Summary
FastAPI-powered background worker (deployed to Cloud Run) that maintains a heartbeat loop, exports `/healthz` & `/readyz`, enforces PDPA-safe Supabase credentials, and produces structured telemetry for rollback/observability requirements.

## Structure
- `app/main.py`: Lifespan context that validates `SupabaseCredentials`, ensures service roles are forbidden, starts the background `_run_worker` task reporting heartbeats, and defines the readiness probes.
- `app/pdpa.py`: Ensures the worker only accepts Supabase anon keys; raises `ServiceRoleForbiddenError` if a service role key is present.
- `app/logging.py`: Mirror of the API logger emitting JSON lines so the OCR loop’s start/stop/heartbeat events can be aggregated in `artifacts/ci`/Sentry.

## Governance touchpoints
- The service validates every credential set before launching to comply with PDPA credential isolation.
- Structured logs satisfy the Test-First Observability principle and feed dashboards described in `docs/deployment/observability.md`.
- CI/CD workflows (`ci.yml`, `cd-ocr.yml`) build/push this service as part of the mandated pipeline.

## Local & CI usage
- Dockerfile packages the worker for Cloud Run deployments; `cd-ocr.yml` captures image digests, executes PDPA retention jobs (`scripts/run-retention-job.sh`), and purges Cloudflare caches per zone.
- Integration tests such as `tests/integration/test_ci_pdpa_failure.py` interact with this worker as part of PDPA gate validations.

## Related docs
- `docs/deployment/rollback-playbook.md` (rollback & retention)
- `docs/deployment/ci-pipeline.md` (CI gating)
- `docs/deployment/observability.md` (heartbeat logs, PDPA artifacts)
