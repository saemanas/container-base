# Implementation Plan: CI/CD Hardening & Multicloud Release Readiness

**Branch**: `002-cicd-hardening` | **Date**: 2025-11-09 | **Spec**: [`spec.md`](./spec.md)
**Input**: Feature specification from `/specs/002-cicd-hardening/spec.md`

## Summary

We will harden CI/CD so that API and OCR worker pulls always pass the mandated Ruff → ESLint → Pytest → Redocly → Build → GHCR push → tag-gate order, coordinate multicloud deployments (Cloud Run, Vercel, Cloudflare, Supabase), enforce manual approval gates before production, guard portal stack versions in CI, and preserve compliance evidence through long-retained GitHub Actions artifacts, staged Supabase migrations, and audited notification flows.@specs/002-cicd-hardening/spec.md#33-86 @specs/002-cicd-hardening/spec.md#12-85

## Technical Context

**Language/Version**: Python 3.12.x for API/OCR services; Node.js 22.21.1 for portal workflows as mandated stack baselines.@refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#66-128 @specs/002-cicd-hardening/spec.md#72-83  
**Primary Dependencies**: FastAPI + SQLModel (API), GitHub Actions + Redocly CLI, Docker/Cloud Run, Supabase CLI, Vercel, Cloudflare per spec scope.@specs/002-cicd-hardening/spec.md#33-85 @refs/docs/CB-MiniOps-v1.0.0-en-US.md#106-218  
**Storage**: Supabase Postgres with RLS and PDPA retention workflows.@specs/002-cicd-hardening/spec.md#33-60 @specs/002-cicd-hardening/spec.md#96-117  
**Testing**: Pytest (backend/worker), k6 latency checks, CI artifact verification, and Supabase CLI RLS smoke tests before production promotion.@specs/002-cicd-hardening/spec.md#20-59 @specs/002-cicd-hardening/spec.md#72-85  
**Target Platform**: GitHub Actions CI, Google Cloud Run (API/OCR), Vercel (portal), Cloudflare DNS, Supabase managed services.@specs/002-cicd-hardening/spec.md#33-45 @specs/002-cicd-hardening/spec.md#118-130  
**Project Type**: Multisurface infrastructure (CI/CD automation touching backend, worker, and portal surfaces).@specs/002-cicd-hardening/spec.md#33-85  
**Performance Goals**: API P95 ≤3s, rollback ≤10m, OCR availability ≥99%, PDPA evidence within 48h, artifact pipeline <15m avg runtime.@specs/002-cicd-hardening/spec.md#87-103  
**Constraints**: PDPA consent enforcement, GPS/email masking, secrets via GitHub environments, zero-downtime DNS, immutable GHCR digests, email notifications for every run.@specs/002-cicd-hardening/spec.md#63-116 @specs/002-cicd-hardening/spec.md#70-85  
**Scale/Scope**: Applies to all non-mobile repos; targets production parity across multicloud topology and ensures ≥95% automated release success rate.@specs/002-cicd-hardening/spec.md#33-103

## Constitution Check

- **Spec-to-Verification Discipline**: Spec is ratified and clarifications recorded; plan → tasks → implementation cadence will follow constitution, with Context7 docs consulted (refs/ docs cited) and explicit manual approval gates scheduled before production deploys.@specs/002-cicd-hardening/spec.md#1-85 @.specify/memory/constitution.md#24-41
- **Test-First Observability**: CI will add success/failure Pytest, Supabase smoke tests, k6 latency sampling, and structured logs `{ts, opId, code, duration_ms}` stored as GitHub artifacts to preserve ≥70% coverage and KPI traces.@specs/002-cicd-hardening/spec.md#20-85 @.specify/memory/constitution.md#32-40
- **PDPA-Safe Data Stewardship**: Pipelines block deploys on PDPA consent tests, enforce GPS/email masking, run staging-first Supabase migrations, and manage secrets via GitHub environments per policy.@specs/002-cicd-hardening/spec.md#54-85 @specs/002-cicd-hardening/spec.md#96-111 @.specify/memory/constitution.md#42-48
- **Instant, Resilient, Clear UX**: Portal deployment flow must present all five UX states with EN/TH keys so operators track releases while offline queue transparency remains documented, while mobile remains out of scope with documented handoff for future integration.@specs/002-cicd-hardening/spec.md#104-117 @.specify/memory/constitution.md#50-56
- **Automated CI/CD & Versioned Releases**: Workflow enforces Ruff → ESLint → Pytest → Redocly → Build → GHCR → Tag deploy, manual approvals, and ≤10m rollback backed by artifact evidence.@specs/002-cicd-hardening/spec.md#20-85 @specs/002-cicd-hardening/spec.md#87-103 @.specify/memory/constitution.md#58-64
- **Stack & Infrastructure Alignment**: Plan adheres to mandated stack (Python 3.12/Node 22.21.1, FastAPI, Next.js 16, Supabase, Cloud Run, Cloudflare) and aligns with MiniOps topology and KPI budgets.@refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#66-128 @refs/docs/CB-MiniOps-v1.0.0-en-US.md#13-218 @.specify/memory/constitution.md#66-74

## Project Structure

### Documentation (this feature)

```text
specs/002-cicd-hardening/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md            # created by /speckit.tasks
```

### Source Code (repository root)

```text
repo/
├── .github/workflows/          # CI/CD pipelines (ci.yml, deploy-*.yml)
├── docs/deployment/            # PDPA, rollout, rollback playbooks
├── scripts/                    # run-all-checks.sh, measure-ci.sh helpers
├── src/apps/api/               # FastAPI service aligning with CI stages
├── src/apps/ocr/               # Worker service built/deployed via CI
├── src/apps/portal/            # Next.js portal with release status UI
└── tests/                      # Contract, integration, PDPA guardrail suites
```

**Structure Decision**: Feature spans shared CI/CD assets under `.github/workflows`, deployment runbooks in `docs/deployment`, automation scripts, and service directories to guarantee coordinated releases.@README.md#5-116 @specs/002-cicd-hardening/spec.md#33-117

## Progress Tracker

| Phase / Story | Status | Evidence | Next Steps |
|---------------|--------|----------|------------|
| Phase 5 / US3 (Rollback + Observability) | Completed | `tests/integration/test_rollback_drill.py` and `tests/backend/test_pdpa_retention_job.py` enforce rollback MTTR ≤10m and PDPA retention tracing; `docs/deployment/observability.md` now documents rollout metrics, structured `{ts, opId, code, duration_ms}` logging, retention job artifacts, and notification archives. | Monitor production rollback runs to ensure artifacts land in `artifacts/pdpa/`, `artifacts/notifications/`, and `artifacts/quotas/` as described in the rollback drill checklist. |
| Phase 6 / Polish | Nearing completion | `docs/deployment/ci-pipeline.md` describes the full CI sequence, Redocly lint/diff, and portal stack guard; README/quickstart highlight shared scripts; `scripts/check-free-tier.py` and `scripts/run-retention-job.sh` produce artefacts referenced in observability guidance. | Finalize release checklist entries (`docs/deployment/release-checklist.md`) with links to structured-log artifacts and confirm GitHub environments contain the documented PDPA secrets. |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _None_ | — | — |
