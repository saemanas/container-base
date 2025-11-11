# Container Base Monorepo

Container Base replaces manual container logging with automated recognition, GPS tracking, and auditable billing. This repository hosts the polyglot stack (FastAPI API, OCR worker, Next.js portal, Expo mobile) alongside CI/CD, PDPA, and governance tooling documented across `docs/`.

## Architecture Map

```
.
├── src/apps/                  # Applications (api, ocr, portal, mobile)
├── scripts/                   # Automation helpers (run-all-checks, retention, CI probes)
├── tests/                     # Backend/contract/integration/script suites
├── .github/workflows/         # GitHub Actions CI & CD flows
├── docs/                      # Runbooks, workflow guides, scripts/tests/app docs
│   ├── deployment/            # CI/CD, PDPA, secrets, observability, rollback
│   ├── scripts/               # Documentation for every helper script
│   ├── src/apps/              # Component-specific explanations
│   ├── tests/                 # Summary of each test directory
│   ├── .github/workflows/     # Workflow-specific runbooks + overview
│   └── project-structure/     # Maps remaining root artifacts
├── refs/docs/                 # Canonical instructions/stack/plan documents (CB-Instruction, CB-Service-Plan, CB-MVP-Stacks, CB-UX-Design, CB-MiniOps)
├── .specify/                  # Spec-kit engine memory (constitution, tasks, workflows) powering Spec→Plan→Tasks automation
├── Makefile                   # Targets for install/check/healthz/build/etc.
├── docker-compose.yml         # Local stack orchestration
├── .env.example               # Shared placeholder keys for Supabase/API/portal/mobile
└── specs/                     # Spec-kit artifacts per feature (spec/plan/tasks/data)
```

## Quick Start

1. **Clone & branch**
   ```bash
   git clone https://github.com/saemanas/container-base.git
   cd container-base
   git checkout develop
   git pull origin develop
   git checkout -b NNN-spec-name
   ```

2. **Prep environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```

3. **Install dependencies** (Makefile target)
   ```bash
   make install
   ```
   Installs API/OCR Python deps, portal packages, and Expo native modules. Indicates success/failure via ANSI `[OK]/[FAIL]` markers.

4. **Populate `.env`**
   ```bash
   cp .env.example .env
   ```
   Fill Supabase, portal (`PORTAL_PORT=8888` by default), and mobile values per `docs/deployment/workflow-secrets.md`. Never commit the populated `.env`.

5. **Validate locally** (lint + tests)
   ```bash
   make check
   ```
   Wraps `scripts/run-all-checks.sh` to run Ruff → Pytest → ESLint with structured `{ts, opId, code, duration_ms}` logs stored under `artifacts/ci/`.

6. **Check health**
   ```bash
   make healthz
   ```
   Curls API (8000), OCR (8080), and portal (8888) health endpoints with colored pass/fail output.

7. **Bootstrap stack**
   ```bash
   make build
   ```
   Starts Docker Compose; follow logs via `make logs` or target a service (`make logs api|ocr|portal`).

8. **Rebuild / restart**
   ```bash
   make rebuild
   ```
   Forces container recreation when dependencies or env vars change.

9. **Clean up**
   ```bash
   make down
   ```

> ℹ️ Need the stack plus environment sourced in one step? Run `./scripts/run-local.sh` (documented in `docs/scripts/run-local.md`) after copying `.env`.

## Frequently used Make targets

| Target | Purpose | Notes |
| --- | --- | --- |
| `make install` | Install Python/Node dependencies and Expo native modules. | Emits ANSI `[OK]/[FAIL]` statuses; rerun after dependency updates. |
| `make check` | Run Ruff → Pytest → ESLint via `scripts/run-all-checks.sh`. | Produces structured logs under `artifacts/ci/`. |
| `make healthz` | Curl API (`:8000`), OCR (`:8080`), portal (`:8888`). | Failures exit non-zero to guard PRs. |
| `make build` | `docker compose up --build -d` for API/OCR/portal. | Companion to `make logs` and `make down`. |
| `make rebuild` | Force container recreation. | Use after environment or dependency changes. |
| `make logs [api|ocr|portal]` | Follow service logs. | Omit suffix for all logs. |
| `make clean` | `docker compose down --remove-orphans`. | Removes stopped containers. |
| `make prune` | Tear down + remove orphans and dangling images. | Destructive—use with caution. |

## Documentation Tour

- `docs/project-structure/README.md` maps every remaining root-level artifact (AGENTS, refs, specs, configs, ignore files, etc.).
- `docs/deployment/` holds runbooks for CI/CD sequences (`ci-pipeline.md`), secrets (`workflow-secrets.md`, `secrets-catalog.md`), rollback, observability, PDPA, Supabase schema, and cost guardrails.
- `docs/github/workflows/` now summarizes every workflow; each `.md` matches a GitHub Actions file, ensuring the documented steps match the actual jobs.
- `docs/scripts/`, `docs/src/apps/`, and `docs/tests/` cover every helper, app surface, and test directory so nothing is left undocumented.

## Operational Highlights

- Structured logs `{ts, opId, code, duration_ms}` are emitted by services (see `docs/deployment/observability.md` for dashboards).
- PDPA retention scripts/logs live under `scripts/run-retention-job.sh` and the matching docs/tests.
- CI guardrails (Ruff, ESLint, Pytest, Redocly, Docker, GHCR, Tag) and portal stack checks (`scripts/check-portal-stack.py`) are enforced via `docs/github/workflows/ci.md` and `docs/deployment/ci-pipeline.md`.
- Tag-based deployments, Supabase promotion scripts, and rollback drills are described in `docs/deployment/rollback-playbook.md` and tested via `tests/integration/test_rollback_drill.py`.

## CI/CD & Testing

- GitHub Actions pipeline (`ci.yml`) runs per `docs/github/workflows/ci.md`.
- `cd-api.yml`, `cd-ocr.yml`, `cd-portal.yml` deploy to Cloud Run/Vercel with artifact retention, structured logs, and PDPA retention jobs; see `docs/github/workflows/cd-*.md`.
- Tests live under `tests/backend`, `tests/contract`, `tests/integration`, and `tests/scripts`; each directory has a README in `docs/tests/`.

## Governance

- High-level mandates come from `AGENTS.md` and `refs/docs/CB-*` (Instruction, MiniOps, MVP Stacks, Service Plan); each now mentions the executable `docs/` runbooks in their “Documentation Alignment” sections.
- Feature work follows Spec → Plan → Tasks → Implementation → Tests → Verification; each spec directory contains the required docs.

## Compliance Aids

- `docs/deployment/pdpa-playbook.md` explains consent retention and `PDPA_FORCE_FAILURE` toggles.
- Supabase promotion/retention scripts under `scripts/` are described in `docs/scripts/`.
- `docs/deployment/workflow-secrets.md` plus `.gitignore`/`.dockerignore`/`.eslintignore` ensure secrets and artifacts stay out of source control.

## Need More?

- Before editing code, review the matching doc under `docs/` (apps, scripts, tests, workflows, project-structure) to keep documentation in sync.
- Use `docs/deployment/ci-pipeline.md` and `docs/github/workflows/README.md` to understand the expected pipeline order before adjusting any workflow.

---

Internal project – follow organization guidelines for PDPA compliance and release approvals.
