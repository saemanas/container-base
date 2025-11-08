# Tasks: Low-cost CI/CD & Infra Skeleton

**Input**: Design documents from `/specs/001-lowcost-cicd-infra/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are MANDATORY per the constitution. Add success + failure coverage for each user story, ensure ≥70% overall and 100% for auth/upload/recognition, and write them before implementation so they fail first.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- Each story must contain: PDPA compliance tasks (consent, RLS, masking), UX state coverage (Empty/Loading/Success/Error/Offline), observability/logging updates, and CI/CD validation steps (Ruff → ESLint → Pytest → Spectral → Build → GHCR → Tag Deploy).

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize repository structure per plan in `src/apps/{api,ocr-worker,portal,mobile}` and `.github/workflows/`
- [X] T002 Create placeholder `.env.example` files for each surface under `src/apps/*/.env.example`
- [X] T003 [P] Document secrets catalog scaffold in `docs/deployment/secrets-catalog.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Configure shared Ruff/ESLint/Prettier settings in `.ruff.toml`, `.eslintrc.cjs`, and `.prettierrc`
- [X] T005 [P] Add Docker base images and runtime entrypoints in `src/apps/api/Dockerfile` and `src/apps/ocr-worker/Dockerfile`
- [X] T006 [P] Scaffold Supabase schema definitions for `app_stg` and `app_prod` in `docs/deployment/supabase-schema.md`
- [X] T007 Establish logging utility enforcing `{ts, opId, code, duration_ms}` format in `src/apps/api/service/logging.py`
- [X] T008 Define PDPA consent and retention policy notes in `docs/deployment/pdpa-playbook.md`
- [X] T009 Wire baseline quickstart validation script in `scripts/validate-ci.sh`
- [X] T010 Document concurrent local run workflow in `specs/001-lowcost-cicd-infra/quickstart.md`
- [X] T011 [P] Add multi-service launcher script in `scripts/run-local.sh` verifying supabase/API/OCR/portal availability

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Spin up minimal CI/CD pipeline (Priority: P1) 🎯 MVP

**Goal**: CI pipeline automatically lint/tests/builds all workloads and prepares deploy artifacts within free-tier limits.

**Independent Test**: Run GitHub Actions `ci.yml` on a PR and confirm Ruff/ESLint/Pytest/Spectral/Build/GHCR stages pass and publish artifacts.

### Tests for User Story 1 (MANDATORY — write before implementation) ⚠️

- [X] T012 [P] [US1] Author pipeline contract test in `tests/backend/test_ci_guardrails.py` validating workflow stages
- [X] T013 [P] [US1] Create Spectral lint test stub for OpenAPI contract in `tests/contract/test_health_contract.py`

### Implementation for User Story 1

- [X] T014 [P] [US1] Implement `.github/workflows/ci.yml` with matrix jobs for api/ocr/portal lint + tests
- [X] T015 [P] [US1] Add GHCR build and push steps for API/OCR images in `.github/workflows/ci.yml`
- [X] T016 [US1] Configure portal build artifact caching in `.github/workflows/ci.yml`
- [X] T017 [US1] Document CI runbook updates in `docs/deployment/ci-pipeline.md`
- [X] T018 [US1] Ensure structured logging emitted during pipeline smoke tests by updating `scripts/validate-ci.sh`

**Checkpoint**: User Story 1 functional and testable independently

---

## Phase 4: User Story 2 - Deploy low-cost runtime surfaces (Priority: P2)

**Goal**: Provision Cloud Run and Vercel deployments with health/readiness checks and Supabase connectivity.

**Independent Test**: Execute deployment workflows to staging and validate `/healthz` `/readyz` endpoints plus Vercel portal loading with Supabase data.

### Tests for User Story 2 (MANDATORY — write before implementation) ⚠️

- [X] T019 [P] [US2] Write deployment smoke test in `tests/integration/test_cloud_run.py` hitting `/healthz`
-- [X] T020 [P] [US2] Add portal availability test in `tests/integration/test_portal_build.py`

### Implementation for User Story 2

- [X] T021 [P] [US2] Create `.github/workflows/deploy-api.yml` with staging auto deploy and prod approval gates
- [X] T022 [P] [US2] Create `.github/workflows/deploy-ocr.yml` mirroring approval strategy
- [X] T023 [US2] Configure `.github/workflows/deploy-portal.yml` for Vercel hobby deploys with environment targets
- [X] T024 [US2] Implement health/readiness endpoints in `src/apps/api/service/main.py` and `src/apps/ocr-worker/ocr/main.py`
- [X] T025 [US2] Update `quickstart.md` deployment verification section with Cloud Run & Vercel steps
- [X] T041 [P] [US2] Implement structured logging for OCR worker in `src/apps/ocr-worker/ocr/logging.py` and wire into `ocr/main.py`
- [X] T042 [US2] Document Cloudflare DNS mapping steps for `api`, `ocr`, and `portal` in `docs/deployment/cloudflare-routing.md`

**Checkpoint**: User Stories 1 and 2 independently operational

---

## Phase 5: User Story 3 - Govern secrets and cost guardrails (Priority: P3)

**Goal**: Centralize secrets management, monitoring, and cost guardrails to react within MiniOps constraints.

**Independent Test**: Run guardrail simulation scripts to confirm alerts trigger when secrets missing or quotas near 80%.

### Tests for User Story 3 (MANDATORY — write before implementation) ⚠️

- [X] T026 [P] [US3] Implement quota alert simulation in `tests/integration/test_cost_guardrails.py`
- [X] T027 [P] [US3] Add secret presence test in `tests/backend/test_secrets_catalog.py`
- [X] T043 [P] [US3] Add PDPA consent and masking tests in `tests/backend/test_pdpa_compliance.py`
- [X] T044 [P] [US3] Add OCR credential isolation tests in `tests/worker/test_ocr_pdpa.py`

### Implementation for User Story 3

- [X] T028 [P] [US3] Populate `docs/deployment/secrets-catalog.md` with staging/prod mappings and rotation cadence
- [X] T029 [US3] Create guardrail monitoring doc in `docs/deployment/cost-guardrails.md`
- [X] T030 [US3] Add Supabase schema + RLS configuration instructions to `docs/deployment/supabase-schema.md`
- [X] T031 [US3] Update `scripts/validate-ci.sh` to check required environment variables before pipeline run
- [X] T032 [US3] Document runbook for manual approvals and rollback in `docs/deployment/rollback-playbook.md`
- [X] T045 [US3] Enforce consent gating, GPS rounding, and email masking in `src/apps/api/service/main.py`
- [X] T046 [P] [US3] Harden OCR worker credential usage in `src/apps/ocr-worker/ocr/main.py`
- [X] T047 [US3] Expand `docs/deployment/pdpa-playbook.md` with remediation steps for consent failures

**Checkpoint**: All user stories independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T033 [P] Consolidate observability dashboards references in `docs/deployment/observability.md`
- [X] T034 Refine README deployment section in `README.md`
- [ ] T035 [P] Run full quickstart validation checklist from `quickstart.md`
- [X] T036 Harden error handling for CI scripts in `scripts/validate-ci.sh`
- [X] T037 Publish final KPI alignment note in `docs/deployment/kpi-mapping.md`
- [X] T038 [P] Capture CI duration metrics via timed run in `scripts/measure-ci.sh` and append results to `docs/deployment/ci-pipeline.md`
- [X] T039 [P] Add Cloud Run latency probe in `scripts/measure-latency.py` and document thresholds in `docs/deployment/cost-guardrails.md`
- [X] T040 Automate quota usage check using `scripts/check-free-tier.py` with summary recorded in `docs/deployment/observability.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Each depends on Phase 2 completion; US1 (P1) should complete before US2 and US3 if delivering MVP sequentially
- **Polish (Phase 6)**: Depends on selected user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent after foundational work
- **User Story 2 (P2)**: May run in parallel with US1 post-foundation but should wait for CI artifacts if sharing pipelines
- **User Story 3 (P3)**: Can proceed after foundational work; depends on secrets placeholders from Phase 1 and docs from Phase 2

### Within Each User Story

- Tests (T012/T013, T019/T020/T041, T026/T027/T044/T045) must be written and fail before their paired implementation tasks
- Implementation tasks follow tests, ensuring structured logging and PDPA checks are in place before deployment verification
- Story completion requires independent verification per acceptance scenarios

- ### Parallel Opportunities

- Tasks marked [P] across phases can run concurrently (e.g., T003, T005, T006, T011, T012, T013, T014, T015, T019, T020, T021, T022, T026, T027, T028, T030, T033, T035, T038, T039, T041, T042, T044, T045, T047)
- After foundational completion, separate teams can pick up US1, US2, and US3 simultaneously if coordination on shared files is maintained
- Tests for each story can be developed in parallel before implementation begins

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (critical)
3. Execute Phase 3: User Story 1 tasks (tests first, then implementation)
4. Validate CI pipeline via T012–T018 and halt for review/demo

### Incremental Delivery

1. Deliver MVP (US1) following steps above
2. Add US2 to enable deployments; validate health endpoints and staging deploys
3. Add US3 to lock in governance, guardrails, and documentation
4. Finish with Phase 6 polish tasks

### Parallel Team Strategy

- Developer A: Focus on CI workflows (US1) once foundational stage done
- Developer B: Handle deployment workflows and health endpoints (US2)
- Developer C: Maintain secrets/guardrails documentation and validation scripts (US3)

---

## Notes

- [P] tasks address different files and have no blocking dependencies
- Story labels ensure traceability from tasks to user stories
- Tests precede implementation per constitution; ensure failing state before code changes
- Commit after each task or coherent group to ease code review
- Stop at story checkpoints to validate independent increments
- Maintain English code/comments while summarizing CLI outputs in Korean per AGENTS.md language policy
