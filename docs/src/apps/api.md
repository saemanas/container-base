# API Service (`src/apps/api`)

## Summary
FastAPI 0.121.0 service acting as the central REST endpoint for Container Base backend workflows. It exposes health/ready probes, enforces PDPA consent semantics, masks emails, rounds GPS data, and emits the required structured logs (`{ ts, opId, code, duration_ms }` schema) described in the constitution.

## Structure
- `app/main.py`: FastAPI app with lifespan hooks that log startup/shutdown events, PDPA middleware, healthz/readyz endpoints, and placeholders for future business routes.
- `app/pdpa.py`: Pydantic-based helpers for normalizing consent metadata, masking email domains, and rounding GPS coordinates before any handler uses them.
- `app/logging.py`: JSON logger provider plus `log_event` helper so every stage (startup, probes, PDPA denials) writes structured telemetry that can feed `artifacts/ci/*` and Sentry/Grafana.

## Governance touchpoints
- PDPA-safe handling: requests lacking active consent raise `ConsentMissingError` and are rejected before any business logic.
- Structured logging ensures `{ ts, opId, code, duration_ms }` is available for CI evidence/rollback drills.
- Health endpoints used by `cd-api.yml` readiness checks and `docs/deployment/ci-pipeline.md`.

## Local & CI usage
- Dockerfile builds the FastAPI app for Cloud Run; CI uses `docker build` + GHCR push to produce immutable artifacts.
- Tests under `tests/backend/` rely on this service’s health endpoints for guardrails and coverage.

## Related docs
- `docs/deployment/ci-pipeline.md` (CI gating)
- `docs/deployment/pdpa-playbook.md` (consent handling)
- `docs/deployment/observability.md` (structured logs)
