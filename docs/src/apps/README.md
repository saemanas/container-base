# Applications Overview (`src/apps`)

This directory hosts the production surfaces covered by the Container Base stack: API, OCR worker, portal, and the Expo mobile client. Each surface has associated governance in AGENTS/refs/docs along with dedicated CI/CD scripts and deployment docs. The per-component docs (`docs/src/apps/api.md`, `ocr.md`, `portal.md`, `mobile.md`) provide deeper insights, while this README summarizes the overall architecture and responsibilities.

| Component | Responsibility | Delivery & Governance |
| --- | --- | --- |
| `api` | FastAPI backend providing health/readiness probes, PDPA consent middleware, structured logging, and contract-backed guardrails. | Dockerized for Cloud Run, linted via Ruff/ESLint, referenced by `docs/deployment/ci-pipeline.md`, `docs/deployment/pdpa-playbook.md`, and `docs/deployment/observability.md`. |
| `ocr` | OCR worker service running background loops, emitting heartbeats, and enforcing Supabase anon-only credentials for PDPA compliance. | Deployed via `cd-ocr.yml`, retention jobs documented in `docs/deployment/rollback-playbook.md`, and tests live under `tests/integration` + `tests/backend`. |
| `portal` | Next.js 16 / React 19 admin portal with shadcn/ui, release status assets, and UX triad states for EN/TH audiences. | Builds on Vercel, validated by `scripts/check-portal-stack.py`, and tied into `docs/deployment/ci-pipeline.md` + `docs/deployment/observability.md`. |
| `mobile` | Expo application scaffolding for the capture/queue experience (GPS tagging, LINE login, MMKV sync). | Expo dependencies in `package-lock.json`; future feature documentation should follow AGENTS UX mandates and local `.env` secrets guidance. |

## Shared expectations
- Structured logging (`{ ts, opId, code, duration_ms }`) must be produced by every surface and aggregated via CI artifacts or `artifacts/`.
- PDPA consent/retention guardrails are enforced through middleware (`api`), credential inhibitors (`ocr`), and retention scripts (`scripts/run-retention-job.sh`).
- CI/CD docs (`docs/deployment/*`) and `refs/docs/CB-*` act as single sources for compliance; update these references when app-level behavior changes (e.g., new endpoints, logging tweaks, or stack upgrades).

## Next steps
- Keep `docs/src/apps/*.md` in lock-step with code changes; add links from new features to this README and the relevant component doc.
- When adding new services, mirror this table with the same three columns so SCM reviewers can quickly understand responsibilities, delivery, and governance dependencies.
