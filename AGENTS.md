# Container Base Expert Agents Playbook

This playbook supersedes prior drafts and folds in the `/refs/docs` canon that originated from the `/init` bootstrap package. Treat it as the single operational contract for every AI or human contributor.

---

## 1. Source Graph & Truth Hierarchy
- **Primary references** (must be cited in specs, PRDs, and tickets):
  - `refs/docs/CB-Instruction-v1.0.0-en-US.md` — execution charter & collaboration ritual.
  - `refs/docs/CB-Service-Plan-v1.0.0-en-US.md` — product/service blueprint for the Thai launch.
  - `refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md` — runtime + tooling baselines.
- **Operational guides**: `development.md`, `deployment.md`, `.github/workflows/*`, `scripts/*`, `docs/patterns/*`, `contracts/*`.
- **Spec-kit rule**: Before running `/specify`, `/clarify`, `/plan`, `/tasks`, `/analyze`, `/implement`, or writing code, ping the Context7 MCP endpoint. If reachable, pull the relevant doc section and cite it; if unavailable, log the outage, risks, and mitigation.
- **Language & CLI policy**: Repository artifacts stay English-only (keys, comments, logs). Localization values may include Thai. Any command output shared by agents must be described in Korean.
- **Comment discipline**: Every code submission MUST include concise English comments that explain intent, invariants, and edge cases. Contributions lacking explanatory comments are rejected during review.

---

## 2. Service North Star & KPIs
- Mission: Replace LINE/chat photo logging in Thai logistics sites with autonomous container recognition, GPS auto logging, and auditable billing.
- Hierarchy: Organization → Site → Admin → Operator → Viewer. Auth via LINE Login + Supabase Auth, scoped by RLS.
- MVP capabilities: photo/condition recognition, GPS timestamping, container timeline, org/site admin, stats, billing visibility, LINE alerts, CSV exports, AI model dashboard.
- Success metrics: FPRR ≥ 90%, backend P95 ≤ 3 s, rollback MTTR ≤ 10 min, ≥60% 30-day retention, ≥1,000 monthly active containers, PDPA compliance in <48 h.

---

## 3. Expert Agent Roster
| Component | Agent Persona | Non-Negotiable Outputs | Key Checkpoints |
| --- | --- | --- | --- |
| Mobile (Expo SDK 52) | Cross-Platform Engineer | 3-tap capture flow, offline queue + MMKV sync, GPS tagging, credit top-up UX, LINE Login bridge | Offline queue telemetry, queue retry policy, i18n coverage EN/TH |
| API / DB (FastAPI + Supabase) | Backend Engineer | Typed FastAPI services, SQLModel schemas, `/billing/usage` + `/billing/events` contracts, Supabase RLS policies, audit logging | OpenAPI diff gates, PDPA consent tables, k6/Sentry latency proofs |
| Vision Worker (YOLOv8n + PaddleOCR) | ML Engineer | `/models/<version>/model.yaml`, evaluation suite, rollback triggers, `/reports/vision-bench.json` accuracy evidence | Δ accuracy ≤3%, inference ≤2 s, version pinning + rollback instructions |
| Portal (Next.js 14 + shadcn/ui) | Frontend Engineer | App Router layouts, TanStack Query data layer, stateful admin UI, AI dashboard | Empty/Loading/Success/Error/Offline states, design tokens, Storybook demos |
| Infra & Delivery | Infrastructure Engineer | Supabase + Cloud Run/Render/Fly topology docs, Cloudflare routing, secrets catalog, incident runbooks | Docker Compose parity, rollback ≤10 min, cost ceiling doc |
| CI/CD | DevOps Engineer | GitHub Actions chain (Ruff → ESLint → Pytest → Spectral → Build → GHCR push → Tag deploy), release drafter, rollback workflow | Conventional Commit guard, tag gate, future hooks (Playwright/k6/Trivy/SBOM) scaffolded |

Agents operate as a single swarm: spec everything, cite sources, and treat OpenAPI contracts plus shared DTOs in `contracts/` as the system of record.

---

## 4. Operating Protocol
1. **Spec → Plan → Tasks → Implementation → Tests → Verification**. No code without a spec excerpt from `/refs/docs`.
2. Maintain weekly Product/Platform/Experience triads, bi-weekly ops review, monthly compliance audit.
3. Deliverables must: (a) run with Docker Compose, (b) pass Ruff + ESLint + Pytest + Spectral, (c) emit structured logs `{ ts, opId, code, duration_ms }`.
4. Git discipline: `main` (prod), `develop` (staging), `feature/<topic>` (task). Commits follow Conventional Commit ≤72 chars. Pre-push hooks block force pushes and invalid messages.
- Branch workflow: `main` and `develop` are protected; working branches follow the spec-kit naming convention (`NNN-some-spec`, e.g., `001-lowcost-cicd-infra`). Branch from `develop`, complete spec tasks, and merge back via reviewed PRs.
5. CLI & documentation outputs: code/comments English; CLI summaries Korean; tests and commands shared with teammates must be runnable verbatim.

---

## 5. Delivery Standards
### 5.1 Tooling Baselines (see `refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md`)
- Python 3.12.x, FastAPI 0.121.0 target, SQLModel 0.0.27, Supabase Python 2.23.x.
- Node.js 22.21.1 LTS “Jod” (upgrade React Vite starter to Next.js 14.2.33 + React 18.3.1).
- Expo CLI 54.x, React Native 0.76.3, TanStack Query 5.90.x, MMKV 2.13.x.
- Vision: Ultralytics 8.3.225, PaddleOCR 3.3.1 (paddlepaddle 3.2.1 / GPU 2.6.2).
- Tooling: Ruff 0.7.x, ESLint 9.x, Prettier 3.x, Biome 2.2.4 optional, Playwright 1.56.1 (hook stub).

### 5.2 Quality & Testing
- Tests precede implementation per feature; include success + failure cases.
- Coverage: ≥70% overall, 100% for auth/upload/recognition paths.
- Naming: `test_<module>_<behavior>.py` (backend) and `*.test.ts(x)` (frontend) with Given/When/Then comments.
- Mock Supabase, Cloudflare, LINE, payment rails. Runtime ≤60 s per module.
- Shared utilities require home-package tests; downstream callers mock interfaces.
- Python services MUST use explicit static typing—function signatures annotated, Pydantic (or equivalent) models for request/response/data validation, and Ruff/pyright-ready code with no implicit `Any` usage left unchecked.

### 5.3 UX & Localization
- Enforce CB UX triad: Instantness (≤3 taps), Resilience (offline-first ≥99% upload success), Clarity (Queued/Uploading/Failed/Approved states visible).
- Every screen/page implements Empty, Loading, Success, Error, Offline. Strings funnel through EN/TH dictionaries; never hardcode copy.

### 5.4 Performance & Reliability Budgets
| Metric | Target | Validation |
| --- | --- | --- |
| API latency (P95) | ≤3 s | k6, Sentry trace |
| Mobile cold start | ≤2.2 s | React Native profiler |
| Offline upload success | ≥99% | Queue metrics |
| Vision inference | <2 s, FPRR ≥90% | `/reports/vision-bench.json` |
| Rollback execution | ≤10 min | Tag redeploy workflow |

### 5.5 Security, PDPA & Compliance
- Block app until PDPA consent stored; support consent → revoke → delete within 48 h.
- GPS rounded to 3 decimals; emails masked to domain; Supabase RLS per org/site.
- Secrets only via GitHub environments; `.env.example` uses dummy placeholders; no hardcoded credentials.
- Retention: 12 months default, automated image lifecycle (14-day full, thumbnail after).

---

## 6. Domain Execution Guides
### 6.1 Mobile (Expo)
- Implement capture → review → submit in ≤3 taps with offline queue + retry telemetry.
- Store GPS + timestamp automatically; round before transmission.
- LINE Login via `expo-auth-session`. Mirror Supabase session tokens; handle guest/demo mode with local storage.
- Provide queue state indicators (Queued/Uploading/Failed/Approved) and surfaced top-up credits.
- Instrument React Native profiler traces for cold start budgets; provide instructions in PRs/tests.

### 6.2 API / DB
- Base on FastAPI 0.121.0, SQLModel 0.0.27, Supabase Postgres; treat Supabase RLS as first-class.
- `/billing/usage`, `/billing/events`, `/billing/audit` data contracts live in `contracts/`; generate clients from OpenAPI via `scripts/generate-client.sh`.
- Logging standard: `{ ts, opId, code, duration_ms }` JSON. Inline PDPA enforcement (consent locks, GPS rounding, email masking).
- Provide Docker Compose services + k6 scripts for latency evidence.

### 6.3 Vision Worker
- Model manifests: `/models/<version>/model.yaml` plus evaluation assets.
- YOLOv8n + PaddleOCR pipeline with inference under 2 s. Provide benchmarking notebooks/tests referencing `/refs/docs/CB-Service-Plan*`.
- Implement A/B validation hook and rollback triggers; publish `/reports/vision-bench.json`.

### 6.4 Portal (Next.js 14 App Router)
- Replace Vite starter with Next.js 14.2.33 + React 18.3.1, shadcn/ui tokens, TanStack Query.
- Every feature under `frontend/src/features/<domain>` with Storybook/Playground coverage for all states.
- Provide AI dashboard for model versions, billing visibility, and alerts.

### 6.5 Infra & Delivery
- Document Supabase + Cloud Run/Render/Fly topology, Cloudflare routing, secrets handoff, rollback playbooks.
- Compose-based local parity, GHCR image tagging, release drafter integration.
- Incident checklist aligning with monthly compliance audit; ensure PDPA logs stored.

### 6.6 CI/CD
- GitHub Actions pipeline order: Ruff → ESLint → Pytest → Spectral → Build → GHCR push → Tag deploy.
- Future hooks (Playwright, k6, Trivy, SBOM) stubbed but optional for MVP; ensure toggles exist.
- Automated tag deploy + rollback ≤10 min; missing tag triggers release checklist reminder.

---

## 7. Immediate Priorities (Sprint 0)
1. **Architecture alignment**: finalize Supabase + Cloud Run/Render/Fly topology, Vite → Next.js migration path with milestones.
2. **Spec bootstrapping**: write Product, API, Portal, Mobile, Vision, Billing specs referencing `/refs/docs`.
3. **Operational foundations**: stand up GitHub Actions (Ruff/ESLint/Pytest/Spectral), tag deployments, secrets catalog.
4. **Data & compliance prep**: PDPA consent flow, GPS rounding enforcement, automated image retention jobs.

---

## 8. Reuse & Knowledge Sharing
- Design components/hooks/services for ≥2 consumers; consolidate duplicates into shared utilities before merge.
- Backend modules live under `backend/app/<domain>`; frontend features under `frontend/src/features/<domain>`; adapters mediate cross-domain code.
- OpenAPI schemas, generated clients, and shared enums/DTOs in `contracts/` are the single source of truth—never redeclare.
- Version scripts/migrations under `tools/` or `scripts/` with SemVer + rollback notes in `release-notes.md`.
- PR template requires “reuse reviewed” checkbox; reviewers block merges when centralization is possible.
- Maintain `docs/patterns/` entries plus Storybook demos covering Empty/Loading/Success/Error/Offline states.

---

## 9. Recent Change Snapshot
- `001-align-project-structure`: upgraded Python 3.12.x (backend/vision) and mandated Node.js 22.21.1 LTS; FastAPI 0.114.2 (target 0.121.0), SQLModel 0.0.27, Supabase Python 2.7.1, React 19.1.1 + Vite 7.1.11, Biome 2.2.4, Playwright 1.56.1. Plan migration toward Next.js 14.2.33 + React 18.3.1 and Supabase enhancements per `/refs/docs`.

---

## 10. Definition of Done Checklist
- ✅ Ruff, ✅ ESLint, ✅ Pytest (coverage ≥70%, auth/upload/recognition =100%), ✅ Spectral.
- ✅ Docker Compose services boot + smoke tests documented.
- ✅ Performance proofs (k6/Sentry/Profiler) stored in PR artifacts.
- ✅ Logs follow `{ ts, opId, code, duration_ms }`.
- ✅ i18n states implemented; no hardcoded copy.
- ✅ PDPA consent + masking enforced; retention automation configured.
- ✅ Release drafter + tag deploy wired; rollback ≤10 min path verified.

Agents must self-audit against this list before surfacing work.