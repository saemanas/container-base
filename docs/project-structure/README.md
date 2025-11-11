# Root Structure Summary

This repo relies on a layered layout. Most directories already have focused documentation (`docs/src/apps`, `docs/scripts`, `docs/tests`, `docs/github/workflows`). The remaining root-level artifacts below are summarized here to keep governance consistent and signal where to look for key configuration:

| Path | Content | Notes |
| --- | --- | --- |
| `AGENTS.md` | Operational playbook covering personas, MVP hypotheses, KPIs, CI/CD, PDPA, UX, and delivery standards. | Always cite when drafting specs/PRs. |
| `refs/docs/` | Canonical docs (Instruction, Service Plan, MiniOps, MVP Stacks, UX Design) that every spec must reference. | Used to validate stack/CI/UX/PDPA compliance. |
| `.specify/` | Spec-kit engine memory (constitution, tasks, workflows) driving Spec→Plan→Tasks automation. | Keep constitution aligned with AGENTS.md and update whenever governance rules change. |
| `specs/` | Spec kit per feature (`spec.md`, `plan.md`, `tasks.md`, data models, research). | Follow Spec→Plan→Tasks→Implementation workflow. |
| `docs/` | Deployment runbooks, workflow secrets catalog, observability, PDPA playbook, etc.; now includes `docs/tests`, `docs/scripts`, `docs/src/apps`, `docs/github/workflows`. | Always align docs with actual CI behavior; refer to `docs/project-structure/README.md` first when adding new folders. |
| `docker-compose.yml` | Local dev stack orchestrating API/OCR/portal/mobile; uses root `.env`. | Complemented by `Makefile` targets (`build`, `down`, `logs`, `check`). |
| `Makefile` | Convenience commands (`install`, `check`, `healthz`, `build`, `rebuild`, `down`, `logs`, `clean`, `prune`); wraps `scripts/run-all-checks.sh`, Docker Compose, log tailing, and curl health probes. | Help text mirrors `make help`; log filtering uses positional targets (`make logs api|ocr|portal`) with guards that warn when services are stopped; `make prune` now calls `docker compose down --rmi local --volumes` to wipe project images/volumes and prints ANSI `[OK]/[FAIL]` status markers. |
| `package.json` / `package-lock.json` | Monorepo workspace for portal/mobile builds. | Portal uses Next.js 16, mobile relies on Expo CLI; npm install runs in `scripts/run-all-checks.sh` and CI jobs. |
| `pytest.ini`, `.ruff.toml`, `.prettierrc`, `eslint.config.mjs` | Tooling configurations ensuring uniform lint/test behavior. | Update these whenever the stack versions shift (per refs docs). |
| `.eslintrc.cjs` | Root ESLint configuration for portal/front-end and scripts to stay within shared conventions (flat config). | Keep synchronized with `eslint.config.mjs` and CI lint jobs described in `docs/deployment/ci-pipeline.md`. |
| `.gitignore`, `.dockerignore` | Rules preventing caches, secrets, logs, and artifacts from entering source control or Docker contexts. | Align with `.env` guidance in `docs/deployment/workflow-secrets.md` and rerun `git status` after adding new generated files. |
| `.eslintignore`, `.prettierignore` | Additional ignore lists for ESLint/Prettier so generated artifacts (`node_modules`, `.next`, coverage, artifacts) remain outside linters. | Keep them in sync with folder creations mentioned in `docs/project-structure/README.md`. |
| `artifacts/` | CI-generated logs/metrics (`artifacts/ci`, `artifacts/pdpa`, etc.). | Already gitignored; used in docs for rollback & observability evidence. |
| `logs/` | Local service logs (`api.log`, `ocr.log`, `portal.log`) emitted by `make logs <service>` and `scripts/run-local.sh`. | Captures structured `{ts,opId,code,duration_ms}` entries and complements CI artifacts; not committed. |
| `supabase/` | Supabase CLI config (config.toml). | Mirrors Supabase project referenced by scripts. |
| `.env.example` | Centralized placeholder keys referenced in README/workflow secrets. | Copy to `.env` locally; never commit real secrets. |

Keep this document updated when you introduce or reorganize top-level directories/files so reviewers understand how they interact with the documented governance path. If new root folders (e.g., `tools/`) are added later, append them here with their obligations.
