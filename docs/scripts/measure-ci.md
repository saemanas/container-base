# `measure-ci.sh`

## Purpose
Simulates the mandated CI pipeline (Ruff → ESLint → Pytest → OpenAPI lint → Docker build) outside of GitHub Actions and publishes runtime metrics + structured logs for AGENTS/Test-First Observability evidence.

## Behavior
- Defines stage commands (ruff, portal ESLint, Pytest guardrail, Redocly lint, Docker build) and iterates through them.
- Logs start/fail events as JSON with `{ts, opId, code, message}`; stops on the first failure to avoid cascading errors.
- Appends a markdown timing table to `docs/deployment/ci-pipeline.md` and writes a JSON metrics file in `artifacts/ci/measure`.

## Inputs
- `MEASURE_CI_ARTIFACT_DIR`: optional override for the artifact directory (default `artifacts/ci/measure`).

## Notes
- Failure details include the exact command that failed for quicker debugging.
- Run after dependency changes to capture new baseline durations for pipeline evidence.

