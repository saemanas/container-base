# Tasks: CI/CD Hardening & Multicloud Release Readiness

**Input**: Design documents from `/specs/002-cicd-hardening/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are MANDATORY per the constitution. Add success + failure coverage for each user story, ensure ≥70% overall and 100% for auth/upload/recognition, and write them before implementation so they fail first.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- Each story must contain: PDPA compliance tasks (consent, RLS, masking), UX state coverage (Empty/Loading/Success/Error/Offline), observability/logging updates, and CI/CD validation steps (Ruff → ESLint → Pytest → OpenAPI Lint → Build → GHCR → Tag Deploy).

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Align branch and directory naming to `002-cicd-hardening` lifecycle@specs/002-cicd-hardening/plan.md#1-24
- [x] T002 Review Context7 references for CB Instruction, MiniOps, and MVP Stacks docs@refs/docs/CB-Instruction-v1.0.0-en-US.md#1-235 @refs/docs/CB-MiniOps-v1.0.0-en-US.md#1-324 @refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#1-200
- [x] T003 [P] Verify GitHub Actions access to Cloud Run, Vercel, Supabase, Cloudflare environments per secrets catalog@docs/deployment/secrets-catalog.md#1-200

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create GitHub Actions artifact retention policy for CI evidence (`.github/workflows/ci.yml`, new retention docs)@specs/002-cicd-hardening/spec.md#12-85 @specs/002-cicd-hardening/plan.md#6-20
- [x] T005 [P] Define Supabase CLI staging smoke-test script in `scripts/` for RLS validation@specs/002-cicd-hardening/spec.md#72-85 @specs/002-cicd-hardening/quickstart.md#19-35
- [x] T006 [P] Document operations email distribution and notification template in `docs/deployment/ci-cd-notifications.md`@specs/002-cicd-hardening/spec.md#12-85 @specs/002-cicd-hardening/research.md#17-36
- [x] T007 Update `.github/workflows/deploy-*.yml` inputs to accept `rollback_tag` and environment parameters consistently@specs/002-cicd-hardening/spec.md#33-86 @README.md#87-112
- [x] T008 Ensure Supabase migrations directory contains staging + production promotion notes (`docs/deployment/supabase-schema.md`)@specs/002-cicd-hardening/spec.md#72-85 @specs/002-cicd-hardening/research.md#6-17
- [x] T009 Harden secrets mapping in `.env.example` across API, OCR worker, portal, ensuring placeholders for new tokens@specs/002-cicd-hardening/spec.md#96-111 @README.md#54-122
- [x] T010 [P] Extend `scripts/run-all-checks.sh` to surface GitHub artifact upload step locally@README.md#49-63 @specs/002-cicd-hardening/spec.md#70-85
- [x] T011 [P] Capture baseline metrics (API P95, OCR success) before changes, store in `docs/deployment/ci-baselines.md`@specs/002-cicd-hardening/spec.md#87-103 @README.md#63-116
- [x] T012 Update `.github/workflows/deploy-*.yml` to enforce GitHub Environment manual approval gates before production deploys@specs/002-cicd-hardening/spec.md#74-85 @specs/002-cicd-hardening/plan.md#6-28

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - DevOps verifies gated CI for API & vision services (Priority: P1) 🎯 MVP

**Goal**: Guarantee every API/OCR PR runs Ruff → ESLint → Pytest → Redocly → Build → GHCR push → tag simulation with artifact retention and PDPA evidence@specs/002-cicd-hardening/spec.md#18-30

**Independent Test**: Trigger CI on a feature branch touching backend or vision code and confirm merge is blocked unless all stages pass with GitHub artifacts stored and PDPA tests enforced within 5 minutes@specs/002-cicd-hardening/spec.md#18-30

### Tests for User Story 1 (write first, ensure they fail initially)

- [x] T013 [P] [US1] Add CI pipeline contract test ensuring stage order in `tests/contract/test_ci_pipeline_order.py`@specs/002-cicd-hardening/spec.md#20-30
- [x] T014 [P] [US1] Add integration test simulating PDPA failure to ensure Pytest stage stops pipeline in `tests/integration/test_ci_pdpa_failure.py`@specs/002-cicd-hardening/spec.md#20-30

### Implementation for User Story 1

- [x] T015 [P] [US1] Update `.github/workflows/ci.yml` to enforce seven-stage sequence with explicit job dependencies@specs/002-cicd-hardening/spec.md#20-30 @specs/002-cicd-hardening/plan.md#6-20
- [x] T016 [P] [US1] Configure GitHub Actions artifact upload step after each CI stage to store structured logs under `artifacts/ci/<stage>`@specs/002-cicd-hardening/spec.md#12-30
- [x] T017 [P] [US1] Add PDPA consent regression suite execution in Pytest stage (`tests/backend/test_pdpa_compliance.py`) with fail-fast behavior@specs/002-cicd-hardening/spec.md#20-30 @README.md#83-87
- [x] T018 [US1] Implement CI guard to fail when portal dependencies deviate from Next.js16/React19 (package.json/version check)@specs/002-cicd-hardening/spec.md#74-85
- [x] T019 [US1] Document CI stage order, artifact retention, and PDPA evidence expectations in `docs/deployment/ci-pipeline.md`@specs/002-cicd-hardening/spec.md#20-30 @README.md#63-116
- [x] T020 [US1] Update `scripts/measure-ci.sh` to capture stage durations and upload digests mirroring `{ts, opId, code, duration_ms}` schema@README.md#63-116 @specs/002-cicd-hardening/spec.md#70-85

**Checkpoint**: User Story 1 fully functional and testable independently

---

## Phase 4: User Story 2 - Release manager rehearses multicloud CD (Priority: P2)

**Goal**: Automate tagged release deployment across Cloud Run, Vercel, Cloudflare, Supabase with rollback metadata and staged Supabase promotion@specs/002-cicd-hardening/spec.md#33-45

**Independent Test**: Run CD workflow from staging tag and confirm Cloud Run, Vercel, Cloudflare, Supabase receive updates, rollback metadata captured, and staging Supabase migrations validated@specs/002-cicd-hardening/spec.md#33-45

### Tests for User Story 2

- [ ] T021 [P] [US2] Add integration test for Supabase staging promotion script in `tests/integration/test_supabase_promotion.py`@specs/002-cicd-hardening/spec.md#72-85
- [ ] T022 [P] [US2] Add deploy workflow smoke test for Cloud Run/Vercel/Cloudflare in `tests/integration/test_multicloud_deploy.py`@specs/002-cicd-hardening/spec.md#33-45

### Implementation for User Story 2

- [ ] T023 [P] [US2] Update `deploy-api.yml` and `deploy-ocr.yml` to use immutable GHCR digests and enforce staging-before-production Supabase promotion@specs/002-cicd-hardening/spec.md#33-86
- [ ] T024 [P] [US2] Extend `deploy-portal.yml` to wait for backend success and run portal status checks for EN/TH UI states@specs/002-cicd-hardening/spec.md#35-117
- [ ] T025 [US2] Implement Supabase CLI automation script `scripts/promote-supabase.sh` with RLS smoke test hook@specs/002-cicd-hardening/spec.md#72-85
- [ ] T026 [US2] Document multicloud deployment sequence and rollback metadata requirements in `docs/deployment/rollback-playbook.md`@specs/002-cicd-hardening/spec.md#33-60 @README.md#107-112
- [ ] T027 [P] [US2] Configure Cloudflare deployment verification step (DNS cache purge and propagation check) in `deploy-api.yml`@specs/002-cicd-hardening/spec.md#33-60

**Checkpoint**: User Stories 1 and 2 operational independently

---

## Phase 5: User Story 3 - Compliance lead validates rollback + observability proofs (Priority: P3)

**Goal**: Capture rollback drill evidence, ensure structured logs `{ts, opId, code, duration_ms}`, PDPA retention jobs, and email notifications are archived@specs/002-cicd-hardening/spec.md#40-60

**Independent Test**: Execute rollback drill redeploying previous tag within 10 minutes, confirm structured logs recorded, PDPA retention jobs triggered, and notifications archived@specs/002-cicd-hardening/spec.md#46-60

### Tests for User Story 3

- [ ] T026 [P] [US3] Add automated rollback drill test in `tests/integration/test_rollback_drill.py` verifying ≤10 minute completion@specs/002-cicd-hardening/spec.md#46-60
- [ ] T027 [P] [US3] Add unit test for PDPA retention job triggers in `tests/backend/test_pdpa_retention_job.py`@specs/002-cicd-hardening/spec.md#46-60

### Implementation for User Story 3

- [ ] T028 [US3] Update rollback workflow (`deploy-api.yml`, `deploy-ocr.yml`) to enforce ≤10 minute timer and capture structured logs@specs/002-cicd-hardening/spec.md#46-60
- [ ] T029 [P] [US3] Integrate PDPA retention job trigger into CD pipeline with Supabase confirmation logging (`scripts/run-retention-job.sh`)@specs/002-cicd-hardening/spec.md#50-60 @specs/002-cicd-hardening/spec.md#96-111
- [ ] T030 [P] [US3] Implement email notification sender (`scripts/send-ci-email.py`) that archives notifications to GitHub artifacts@specs/002-cicd-hardening/spec.md#12-15 @specs/002-cicd-hardening/spec.md#70-85
- [ ] T031 [US3] Update observability documentation (`docs/deployment/observability.md`) with rollback drill metrics and artifact references@specs/002-cicd-hardening/spec.md#46-103
- [ ] T032 [US3] Configure `scripts/check-free-tier.py` to append post-deploy quota metrics into artifacts@README.md#114-116 @specs/002-cicd-hardening/spec.md#87-103

**Checkpoint**: All user stories independently validated with compliance evidence

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements impacting multiple stories

- [ ] T033 [P] Refresh `docs/deployment/ci-pipeline.md` diagrams and include notification email samples@specs/002-cicd-hardening/spec.md#12-85
- [ ] T034 Document mobile out-of-scope handoff in `docs/deployment/ci-pipeline.md#mobile-ready` per FR-011@specs/002-cicd-hardening/spec.md#74-85
- [ ] T035 Refine README quickstart section to reflect updated scripts and notification flow@README.md#49-117 @specs/002-cicd-hardening/quickstart.md#1-82
- [ ] T036 [P] Add monitoring dashboard links for new metrics in `docs/deployment/observability.md`@specs/002-cicd-hardening/spec.md#87-103
- [ ] T037 Conduct security review of GitHub environments and confirm `.env.example` parity@specs/002-cicd-hardening/spec.md#96-111
- [ ] T038 [P] Run quickstart validation end-to-end and log results in `docs/deployment/release-checklist.md`@specs/002-cicd-hardening/quickstart.md#1-82

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion; then execute in priority order or parallel based on capacity
- **Polish (Phase 6)**: Depends on all targeted user stories being complete

### User Story Dependencies
- **US1 (P1)**: Start after Foundational; independent
- **US2 (P2)**: Start after Foundational; depends on artifact upload + Supabase promotion scripts from US1
- **US3 (P3)**: Start after Foundational; depends on artifact retention and multicloud deployment steps from US1 & US2

### Within Each User Story
- Tests written first, fail before implementation
- Artifacts/logging configured before rollout documentation
- Rollback drills validated after deployment scripts updated

### Parallel Opportunities
- Setup and Foundational tasks flagged [P] can run concurrently when they touch separate files
- After Foundational, US1/US2/US3 implementation can proceed in parallel by different contributors once their prerequisites are ready
- Notifications, Supabase scripts, and documentation updates marked [P] can run simultaneously across stories

---

## Parallel Example: User Story 1

```bash
# Run CI contract + PDPA failure tests in parallel (after authoring)
pytest tests/contract/test_ci_pipeline_order.py
pytest tests/integration/test_ci_pdpa_failure.py

# Update GitHub workflow logic while documenting metrics in parallel
code .github/workflows/ci.yml docs/deployment/ci-pipeline.md
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 & 2 to harden pipeline prerequisites
2. Deliver US1 to guarantee CI ordering and PDPA compliance evidence
3. Validate artifacts and PDPA tests, then greenlight limited rollout

### Incremental Delivery
1. US1 → Harden CI gates and artifact retention
2. US2 → Automate multicloud deployments with staged Supabase promotion
3. US3 → Formalize rollback drills, notifications, and PDPA retention evidence

### Parallel Team Strategy
- Developer A: CI pipeline ordering & artifacts (US1)
- Developer B: Supabase promotion + multicloud deploy (US2)
- Developer C: Rollback drills, observability, notifications (US3)

Each developer references common Foundational outputs and shares documentation updates in Phase 6.
