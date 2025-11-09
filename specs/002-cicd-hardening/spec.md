# Feature Specification: CI/CD Hardening & Multicloud Release Readiness

**Feature Branch**: `002-cicd-hardening`  
**Created**: 2025-11-09  
**Status**: Draft  
**Input**: User description: "Harden CI/CD so every non-mobile component reaches CI pass gates and production CD readiness across Cloudflare domain, Cloud Run (API/OCR worker), Vercel (portal), and Supabase DB through main→production automation."

## Clarifications

### Session 2025-11-09

- Q: Where should long-term CI/CD evidence artifacts live for audit readiness? → A: Store them in GitHub Actions artifacts with extended retention windows.
- Q: What is the required Supabase migration promotion flow to keep RLS evidence intact? → A: Run migrations in staging with Supabase CLI RLS smoke tests, then promote the same scripts to production.
- Q: Which channel must receive CI/CD run notifications? → A: Deliver notifications via the designated operations email distribution.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - DevOps verifies gated CI for API & vision services (Priority: P1)

The DevOps engineer needs a single CI pipeline that automatically lint-checks, tests, lints OpenAPI specs with Redocly, builds containers, and pushes images for the FastAPI backend and OCR worker before any merge to `develop` or `main`, guaranteeing compliance with the order mandated in `refs/docs/CB-Instruction-v1.0.0-en-US.md §4.7`.

**Why this priority**: Without deterministic CI gates the organization cannot trust Cloud Run deployments nor prove PDPA compliance evidence; this is the baseline for every downstream deployment.

**Independent Test**: Trigger CI on a feature branch touching backend or vision code and confirm it blocks merge unless all seven stages (Ruff → ESLint → Pytest → OpenAPI lint → Build → GHCR push → Tag simulation) pass.

**Acceptance Scenarios**:

1. **Given** a backend pull request, **When** CI runs, **Then** Ruff, ESLint, Pytest, Redocly, Docker build, and GHCR push all pass before merge is unblocked.
2. **Given** a failed PDPA regression test, **When** the CI workflow reaches the Pytest stage, **Then** the pipeline stops and surfaces the PDPA failure log artifact within 5 minutes.

---

### User Story 2 - Release manager rehearses multicloud CD (Priority: P2)

The release manager needs scripted deployment steps that publish successful artifacts to Cloudflare (DNS & routing), Cloud Run (API + OCR worker), Supabase (migrations + policies), and Vercel (portal) upon tagged releases so that production mirrors the topology described in `refs/docs/CB-Service-Plan-v1.0.0-en-US.md §3`.

**Why this priority**: Coordinated releases across providers are mandatory to keep FPRR ≥90% and to maintain auditors’ trust that infra changes are reproducible.

**Independent Test**: From a staging tag, execute the CD workflow and confirm each provider receives the new version plus rollback metadata without manual patching.

**Acceptance Scenarios**:

1. **Given** a tag `vX.Y.Z` on `main`, **When** CD runs, **Then** Cloud Run updates API + OCR worker, Vercel publishes the portal preview to production, and Cloudflare routes traffic with zero downtime.
2. **Given** Supabase migration scripts, **When** CD executes against staging, **Then** migrations apply in order and RLS policies remain intact with evidence stored in logs.

---

### User Story 3 - Compliance lead validates rollback + observability proofs (Priority: P3)

The compliance lead needs the CI/CD system to capture evidence for rollback rehearsals and PDPA logging so that audits can confirm MTTR ≤10 minutes and consent enforcement is never bypassed, as mandated in `refs/docs/CB-Instruction-v1.0.0-en-US.md §4.6`.

**Why this priority**: Without formal rollback drills and telemetry, PDPA breaches or failed releases could go undetected and violate the constitution.

**Independent Test**: Execute a scheduled rollback drill where the latest production tag is reverted, observe structured logs `{ts, opId, code, duration_ms}`, and verify the drill completes within 10 minutes.

**Acceptance Scenarios**:

1. **Given** production is on `v1.4.0`, **When** an incident triggers rollback, **Then** the workflow redeploys `v1.3.2` within 10 minutes while logging opIds for every stage.
2. **Given** a consent revocation request, **When** CD pipelines run data retention jobs, **Then** Supabase confirmations are published to the PDPA audit log within 48 hours.

---

### Edge Cases

- Runner outage or rate limiting pauses CI mid-sequence; pipeline must retry failed stages without re-running successful ones while keeping artifacts immutable.
- Secrets rotation removes a Cloud Run service account key; deployment must fail fast with guidance to refresh GitHub environment variables instead of silently skipping the target.
- Vercel or Cloud Run deployment succeeds but Cloudflare DNS cache lags; monitoring must detect partial rollout and allow automated purge or rollback.
- Supabase migration fails halfway; workflow must halt downstream deploys and emit recovery steps before any production traffic flips.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: CI for API and OCR worker MUST execute the mandated order Ruff → ESLint → Pytest → Redocly → Build → GHCR push → Tag gate for every pull request touching non-mobile code (`refs/docs/CB-Instruction-v1.0.0-en-US.md §4.7`).
- **FR-002**: CI MUST publish structured artifacts (logs, coverage, k6/Profiler evidence) as long-retained GitHub Actions artifacts so release managers can attach them to compliance reviews before merging to `main`.
- **FR-003**: CD MUST promote Cloud Run services (API + OCR worker) using immutable GHCR image digests and must surface rollback commands within the same workflow run.
- **FR-004**: CD MUST configure Cloudflare DNS + zero-downtime rules referencing the latest deployment manifest and verify propagation before marking production complete.
- **FR-005**: CD MUST trigger Supabase migrations first in staging, execute Supabase CLI RLS smoke tests, and only then promote identical scripts to production while logging PDPA consent enforcement and storing evidence for ≥12 months (`refs/docs/CB-Instruction-v1.0.0-en-US.md §4.6`).
- **FR-006**: Vercel deployments MUST execute after successful backend promotions and confirm the portal build artifact renders Empty/Loading/Success/Error/Offline states using EN/TH keys (`refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md §Portal`).
- **FR-007**: Release workflows MUST require manual approval before pushing to production unless a tagged rollback is invoked, in which case automation must run immediately with notification hooks; manual approvals are enforced via GitHub Environment protection rules that require Admin/Operator review.
- **FR-008**: All secrets MUST be injected via GitHub Environments and mirrored in `.env.example` placeholders; workflows may not echo secret values.
- **FR-009**: Observability hooks MUST capture `{ts, opId, code, duration_ms}` for every CI/CD stage and forward them to the existing dashboards referenced in `refs/docs/CB-MiniOps-v1.0.0-en-US.md`.
- **FR-010**: Portal build validation MUST confirm compatibility with the officially mandated Next.js 16 / React 19 stack from `refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md`, and CI/CD must fail if artifacts regress to older baselines documented in prior AGENTS drafts through an automated stack version guard in CI.
- **FR-011**: CD MUST exclude the mobile client while still producing documentation about where mobile would hook in once coverage expands, with the current handoff captured in `docs/deployment/ci-pipeline.md#mobile-ready` so scope remains aligned to the user request.
- **FR-012**: CI/CD notifications MUST trigger email delivery to the designated operations distribution list (e.g., GitHub notification emails) for every success, failure, and rollback event.

### Key Entities *(include if feature involves data)*

- **PipelineStageRecord**: Describes each CI/CD stage name, status, timestamps, opId, duration, artifacts linked, and triggering commit/tag; used for audits and dashboards.
- **DeploymentEnvironment**: Captures Cloudflare, Cloud Run, Vercel, and Supabase targets (staging, main, production) with associated secrets bundle references and success criteria per environment.
- **ReleaseChecklist**: Human-reviewed checklist storing PDPA confirmation, UX triad validation, rollback rehearsal status, and approval metadata for each tag.
- **CredentialBundle**: Logical definition of GitHub environment variables (service account keys, Supabase tokens, Vercel tokens) plus rotation cadence and owner; no secrets stored inside the spec.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of API and OCR worker pull requests complete the seven-stage CI sequence in under 15 minutes on average with ≤2% flake rate.
- **SC-002**: 95% of tagged releases reach production across Cloud Run, Vercel, Cloudflare, and Supabase without manual intervention, with automated evidence attached to the release draft.
- **SC-003**: At least one rollback drill per sprint completes in ≤10 minutes from trigger to restored traffic, with logs proving `{ts, opId, code, duration_ms}` for each action.
- **SC-004**: Compliance reviews receive PDPA consent enforcement proof within 48 hours of each deploy, and zero unresolved PDPA tickets remain open beyond the SLA.
- **SC-005**: Observability dashboards show portal/API latency budgets (API P95 ≤3s) after each deployment with no more than 5% variance from pre-deploy baselines.

## Compliance, UX, and Operational Requirements *(mandatory)*

### PDPA & Security

- CI/CD workflows must block deploys until PDPA consent gating tests pass and rollback scripts for data deletion remain accessible, satisfying `.specify/memory/constitution.md` and `refs/docs/CB-Instruction-v1.0.0-en-US.md §4.6`.
- Deployment records must document GPS rounding (3 decimals), email masking, retention windows (14-day full images, 12-month thumbnail/metadata) and confirm Supabase RLS enforcement via automated checks.
- GitHub environment variables must include Cloud Run service accounts, Supabase keys, Vercel tokens, and Cloudflare API tokens with dummy entries mirrored in `.env.example`; secrets rotation procedures must be referenced in `docs/patterns/ci-cd.md`.

### UX & Localization

- Even though this feature focuses on infra, the portal release flow must demonstrate all five UI states (Empty, Loading, Success, Error, Offline) with EN/TH localization keys tied to deployment progress so operators can see progress (per `refs/docs/CB-Instruction-v1.0.0-en-US.md §4.3`).
- Notifications, dashboards, and release checklists must clarify how each role (Organization, Site, Admin, Operator, Viewer) accesses deployment status; only Admin/Operator roles approve production pushes.
- Offline/queued states for deployments (e.g., queued tag) must surface the CB UX triad language so that operations staff receive the same clarity as end-user flows.

### KPI & Observability Mapping

- Primary KPIs: rollback MTTR ≤10 min, API P95 ≤3 s, ≥60% 30-day retention supported by reliable billing/vision data after deploys, and FPRR ≥90% through stable releases (`refs/docs/CB-Service-Plan-v1.0.0-en-US.md §2`).
- Metrics to capture: stage duration histograms, deployment success/failure counters, PDPA job throughput, Cloudflare propagation time, Supabase migration duration, and portal build validation stats.
- Logs must use `{ts, opId, code, duration_ms}` and feed existing dashboards plus `/reports/vision-bench.json` updates when model deployments piggyback on the same workflow.
- CI/CD hooks must continue to follow Ruff → ESLint → Pytest → Redocly → Build → GHCR → Tag deploy order, with future expansions (Playwright, k6, Trivy, SBOM) stubbed but toggled off until ready (per `refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md §CI/CD Expectations`).

## Assumptions & Dependencies

1. Cloud Run remains the primary runtime for API and OCR worker; Render/Fly are fallback options referenced but not exercised unless Cloud Run quotas block deployment.
2. Portal builds officially target Next.js 16/React 19 per `refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md`, and AGENTS/constitution have been updated to reflect the same baseline so FR-010 now enforces a single canonical stack.
3. Mobile pipelines stay out of scope for this feature but future work must reference artifacts from this spec when they are onboarded.
4. GitHub Actions runners have network access to Cloudflare, Google Cloud, Vercel, and Supabase; if firewalls restrict access, mirrored self-hosted runners will be added through a separate infrastructure ticket.
