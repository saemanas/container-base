# CI Workflow (`.github/workflows/ci.yml`)

## Overview
- Named `CI` and enforces the constitution‑mandated gate order: Ruff → ESLint → Pytest → OpenAPI Lint (Redocly) → Build → GHCR push → Tag Deploy.
- Provides artifact retention, PDPA evidence, and structured `{ts, opId, code, duration_ms}` logging per stage so compliance reviewers can trace the pipeline within the 90‑day audit window referenced in AGENTS.md and the constitution.

## Triggers & Environment
- Runs on pushes to feature branches (excluding `main`/`develop`) and pull requests. The job names mirror the CI ordering and remain linear to satisfy Spec-to-Verification Discipline.
- Shared env: `PYTHON_VERSION=3.12`, `NODE_VERSION=22.21.1`, `GHCR_IMAGE_PREFIX=ghcr.io/${{ github.repository }}`, `ARTIFACT_RETENTION_DAYS=90`.

## Jobs
1. **check_backend** – installs Python tooling, runs Ruff against API/OCR, uploads artifact logs, executes PDPA regression (`tests/backend/test_pdpa_compliance.py`), and performs the Pytest suite with artifact capture. Structured logs are appended via `scripts/measure-ci.sh`, so metrics referencing `{ts, opId, code, duration_ms}` are always retained.
2. **check_portal** – sets up Node 22.21.1 (Next.js 16 target), caches `.next`, runs ESLint, executes `scripts/check-portal-stack.py` (enforcing Next.js 16.0.1 / React 19.0.0), and builds/tests the portal. ESLint and stack guard logs are uploaded as artifacts for PDPA/UX evidence. 
3. **check_openapi** – installs Redocly CLI, lints `specs/001-lowcost-cicd-infra/contracts/openapi.yaml`, stores lint output/diff logs, and runs `oasdiff` to detect breaking schema changes. Both lint output and diffs remain archived to honor the constitution’s OpenAPI single‑source‑of‑truth requirements.
4. **build** – Docker Buildx builds API/OCR containers, tagging them with `ci-${{ github.run_id }}` and storing build logs for rollback drills.
5. **ghcr** – Logs into GHCR (needs `PROJECT_TOKEN` secret), pushes the new images with `latest` tags, records stage statuses in JSON artifacts, and retains them for auditing.
6. **tag_deploy** – Summarizes the pipeline completion and uploads a `pipeline-summary.txt` artifact documenting the run ID, commit, and full stage sequence for governance review.

## Secrets & Compliance hooks
- Requires `PROJECT_TOKEN` (GHCR) and ensures Supabase/Cloud Run secrets are validated via tests.
- Artifacts include PDPA evidence (consent tests, structured logs), propagate to `artifacts/ci/<stage>` to demonstrate rollback ≤10m and PDPA retention automation.
- Gate enforcer script `scripts/measure-ci.sh` writes to `docs/deployment/ci-pipeline.md`, bridging CI evidence with governance documentation.

## Notes for doc maintenance
- Update this document if any new job, artifact retention window, or PDPA log schema changes occur.
- Keep references to AGENTS/Constitution metrics (P95 ≤3s, PDPA retention ≤48h, rollback ≤10m) current as GitHub artifacts evolve.
