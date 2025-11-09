<!--
Sync Impact Report
- Version: 0.0.0 → 1.0.0
- Modified Principles:
  - Placeholder Principle 1 → Spec-to-Verification Discipline
  - Placeholder Principle 2 → Test-First Observability
  - Placeholder Principle 3 → PDPA-Safe Data Stewardship
  - Placeholder Principle 4 → Instant, Resilient, Clear UX
  - Placeholder Principle 5 → Automated CI/CD & Versioned Releases
- Added Sections:
  - MVP Stack & Operational Constraints
  - Workflow & Quality Gates
- Removed Sections: None
- Templates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Container Base Constitution

## Core Principles

### Spec-to-Verification Discipline
Non-negotiable rules:
- Every effort begins with a `/specs/<feature>/spec.md` artifact that cites the Service North Star, KPIs, and compliance expectations set in AGENTS.md and refs/docs.
- Execution order is fixed: **Spec → Plan → Tasks → Implementation → Tests → Verification**. Each stage must be committed (research.md, plan.md, tasks.md, contracts/, quickstart.md) before code is authored or merged.
- Before running `/specify`, `/clarify`, `/plan`, `/tasks`, `/analyze`, `/implement`, or writing code, agents MUST verify Context7 MCP availability; if unreachable, log the outage and associated risks in the work product.
- All outputs (code, docs, commits, logs) stay English-only, include summaries, file paths, runnable commands, and respect repository i18n policies.
Rationale: Enforcing a shared cadence keeps solo agents aligned with the triad (Product, Platform, Experience) and preserves institutional memory.

### Test-First Observability
Non-negotiable rules:
- Write failing tests before implementation with success and failure cases; maintain ≥70% coverage overall and 100% for auth, upload, and recognition modules.
- Enforce Ruff for Python, ESLint for JS/TS, and repository Prettier hooks; reject dead/commented code and require typed signatures plus docstrings on public functions.
- Python services must employ explicit static typing with Pydantic (or equivalent) models and annotated signatures; no implicit `Any` may remain after linting.
- Every code change MUST include concise English comments capturing intent, invariants, and edge cases; reviewers reject submissions lacking explanatory comments.
- All services emit structured logs `{ ts, opId, code, duration_ms }` and expose metrics that prove API P95 ≤ 3 s, offline upload success ≥ 99%, vision accuracy ≥ 90%, and rollback ≤ 10 min (validated via k6, Sentry, Grafana, or equivalent traces).
- Deliverables ship with Docker Compose targets, health probes, `/reports/vision-bench.json`, and monitoring dashboards so regressions are observable.
Rationale: Only measurable systems can uphold the KPI and SLA budgets promised to Thai logistics customers.

### PDPA-Safe Data Stewardship
Non-negotiable rules:
- Block all user access until PDPA consent is stored; support consent → revoke → delete within 48 hours and document the evidence path.
- Round GPS coordinates to three decimals, mask emails to their domain, and enforce Supabase RLS per organization/site for every query and storage bucket.
- Secrets live exclusively in GitHub environment variables; `.env.example` contains dummy placeholders, never real credentials.
- Apply retention automation (images 12 months, metadata per policy), maintain `/billing/usage`, `/billing/events`, and `/audit/logs` contracts, and ensure audit logs can prove compliance at any time.
Rationale: Trust in PDPA handling is a prerequisite for operations in Thailand’s regulated logistics sector.

### Instant, Resilient, Clear UX
Non-negotiable rules:
- Uphold the CB UX triad: Capture → Review → Submit ≤ 3 taps, ≥99% offline upload success via MMKV-backed queues, and state visibility (Queued, Uploading, Failed, Approved).
- Every surface (Expo app, Next.js portal, admin dashboards) implements Empty, Loading, Success, Error, and Offline states with i18n keys for EN/TH; no hardcoded copy.
- Features must specify how GPS tagging, LINE Login bridge, and role hierarchy (Organization → Site → Admin → Operator → Viewer) surface instantly actionable information.
- Specs describe localized copy, error handling, and offline fallbacks before implementation; accessibility and clarity are blockers, not polish items.
Rationale: Frontline operators adopt CB only when the experience is instant, resilient, and transparent regardless of connectivity.

### Automated CI/CD & Versioned Releases
Non-negotiable rules:
- Branch policy: `main` (production), `develop` (staging), `feature/<topic>`; commits follow Conventional Commit ≤72 chars and cannot be force-pushed past pre-push hooks.
- CI pipeline order is immutable: Ruff → ESLint → Pytest → Spectral → Build → GHCR Push → Tag Deploy, with Playwright/k6/Trivy/SBOM hooks scaffolded for later enforcement.
- Release Drafter creates notes on every `main` merge; semantic tags (vX.Y.Z) trigger production deploys via Cloud Run/Render/Fly, and rollback by redeploying the previous tag must finish ≤10 minutes.
- OpenAPI schemas, `/billing/*` contracts, model manifests (`/models/<version>/model.yaml`), and shared DTOs in `contracts/` are the single source of truth; downstream code consumes generated clients only.
Rationale: Automation keeps the free-tier stack reliable, transparent, and ready for rollback without human toil.

## MVP Stack & Operational Constraints

- Mandated stack: Expo (React Native 0.76.3, React 18.3.1, TanStack Query 5, MMKV), Next.js 14.2.33 + shadcn/ui + TanStack Query 5 for the portal, FastAPI 0.121.0 + SQLModel 0.0.27 + Supabase 2.7.x for the API, YOLOv8n + PaddleOCR workers, GitHub + GHCR + Cloudflare + Cloud Run/Render/Fly for delivery.
- Runtime baselines: Python 3.12.x, Node.js 22.21.1 LTS, Docker Engine ≥26 with Compose v2.29+, Biome 2.2.4, Playwright 1.56.1. Deviations require written approval inside the plan.md Complexity Tracking table.
- Deployment artifacts must be runnable via Docker Compose, store environment configuration in GitHub environments, and describe secrets mapping per environment in deployment docs.
- KPI/SLA budgets: FPRR ≥ 90%, backend P95 ≤ 3 s, offline upload success ≥ 99%, retention ≥ 60%, monthly active containers ≥ 1,000, rollback MTTR ≤ 10 min. Every feature spec maps its success criteria to at least one KPI.
- Architecture defaults: Supabase (Singapore) for storage/auth, Cloudflare for DNS and routing, PromptPay/LINE Pay integrations for billing, and Grafana/Sentry for monitoring.
- PDPA & billing compliance assets live in `/docs/` and must stay synchronized with this constitution whenever policies change.

## Workflow & Quality Gates

- Spec kit directories anchor every feature: `research.md` (Phase 0), `plan.md` (Phase 1), `data-model.md`, `quickstart.md`, `contracts/`, and `tasks.md`. Missing artifacts block coding.
- Constitution Check in plan.md verifies: Context7 MCP status logged, KPI alignment, PDPA controls, UX state coverage, CI/CD + rollback readiness, and Docker Compose validation steps.
- Tests run before implementation work begins, include contract/integration coverage, mock Supabase/Cloudflare/LINE interactions, and keep per-module runtime ≤60 s.
- Reviews confirm JSON logging, i18n usage, KPI instrumentation, and that `/billing/*` contracts or `/models/<version>/` manifests remain canonical for any shared change.
- Weekly triad (Product, Platform, Experience) reviews backlog health; bi-weekly ops review audits release automation; monthly compliance audit validates PDPA evidence, billing accuracy, and rollback drills.
- All runtime guidance (AGENTS.md, refs/docs) is treated as normative; deviations must be recorded in plan.md Complexity Tracking and ratified via governance.

## Governance

- This constitution supersedes ad-hoc practices. Agents must reference it in PR templates, review checklists, and automated gates (CI, pre-push hooks, release drafter).
- Amendments require: (1) rationale tied to KPIs or compliance, (2) update to this file plus impacted templates/docs, (3) notification in release notes, and (4) confirmation during the next triad sync.
- Versioning follows SemVer: MAJOR for breaking/removing principles or governance processes, MINOR for adding or materially expanding sections/principles, PATCH for clarifications or wording fixes without behavioral change.
- Ratified changes automatically set `Last Amended` to the change date; `Ratified` records the first adoption date and never shifts retroactively.
- Compliance reviews enforce PDPA, KPI, and CI/CD gates monthly. Non-compliance pauses deployments until corrective actions (tests, docs, alerts) are merged.
- Context7 MCP availability must be verified before any `/specify` or related workflow runs; outages and risks are logged alongside specs to maintain traceability.

**Version**: 1.0.0 | **Ratified**: 2025-11-08 | **Last Amended**: 2025-11-08
