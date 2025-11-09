# Implementation Plan: Low-cost CI/CD & Infra Skeleton

**Branch**: `001-lowcost-cicd-infra` | **Date**: 2025-11-09 | **Spec**: [/specs/001-lowcost-cicd-infra/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-lowcost-cicd-infra/spec.md`

## Summary

Stand up a monorepo skeleton and low-cost CI/CD topology so API, OCR worker, portal, and mobile apps lint, test, build, and deploy through GitHub Actions while staying within free-tier budgets. Deliver Cloud Run + Vercel deployment workflows, secrets catalog, and guardrails (manual prod approvals, shared Supabase project with segregated RLS, Cloud Run concurrency 5) to satisfy MiniOps principles.@specs/001-lowcost-cicd-infra/spec.md#10-118

## Technical Context

**Language/Version**: Python 3.12.x, Node.js 22.21.1 LTS, Expo SDK 54, React 19.0.0 (portal), React 18.3.1 (mobile).@refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#3-31  
**Primary Dependencies**: FastAPI 0.121.0, SQLModel 0.0.27, Supabase client 2.23.x, Next.js 16.0.1, React 19.0.0, shadcn/ui, TanStack Query 5, GitHub Actions, Cloud Run, Vercel.@specs/001-lowcost-cicd-infra/spec.md#63-89 @refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#17-34  
**Storage**: Supabase Postgres (single project with environment-specific tables/RLS).@specs/001-lowcost-cicd-infra/spec.md#65-117  
**Testing**: Pytest for API/OCR, Vitest/Playwright placeholders for portal, Expo test runners; Ruff + ESLint lint gates.@specs/001-lowcost-cicd-infra/spec.md#10-88  
**Target Platform**: Cloud Run (API/OCR), Vercel Hobby (portal), Expo-managed Android builds, Supabase hosted Postgres.@specs/001-lowcost-cicd-infra/spec.md#25-117  
**Project Type**: Polyrepo-in-monorepo (mobile, portal, API, worker) with shared CI/CD governance.@specs/001-lowcost-cicd-infra/spec.md#63-90  
**Performance Goals**: API/OCR P95 ≤3s, OCR inference <2s, rollback ≤10m, free-tier usage ≤80%, offline upload success ≥99%.@specs/001-lowcost-cicd-infra/spec.md#82-109  
**Constraints**: Cloud Run concurrency 5, MAX_IMAGE_MB + TIMEOUT_MS guardrails, manual prod approvals, PDPA enforcement, GitHub Actions free minutes.@specs/001-lowcost-cicd-infra/spec.md#55-118  
**Scale/Scope**: Support Sprint 0 MVP surfaces (API, OCR, portal, mobile) with secrets catalog, health checks, cost guardrails, and deployment playbooks.@specs/001-lowcost-cicd-infra/spec.md#10-118  
**PDPA Enforcement Deliverables**: GPS rounding + email masking logic in API/OCR middleware, Supabase RLS policies per org/site, consent evidence workflow, and rotation-ready secrets catalog updates mapped to docs/tests.@specs/001-lowcost-cicd-infra/spec.md#93-98 @.specify/memory/constitution.md#40-46  
**UX Triad Deliverables**: Mobile/portal build scripts must document ≤3-tap Capture → Review → Submit flow, MMKV offline queue states (Queued/Uploading/Failed/Approved), and EN/TH i18n coverage for Empty/Loading/Success/Error/Offline states tied to verification scripts.@specs/001-lowcost-cicd-infra/spec.md#99-104 @.specify/memory/constitution.md#48-55

## Constitution Check

*GATE: Passed (Context7 MCP verified 2025-11-09; docs cited in spec).*

- **Spec-to-Verification Discipline**: Spec is approved and cited; plan → tasks → implementation sequencing will follow Spec-kit outputs (research.md, plan.md, data-model.md, quickstart.md, contracts/, tasks.md).@specs/001-lowcost-cicd-infra/spec.md#1-118 @.specify/memory/constitution.md#24-39
- **Test-First Observability**: CI pipeline runs Ruff/ESLint/Pytest/OpenAPI Lint before build; health checks `/healthz` `/readyz`, structured logs, and k6/Sentry hooks maintain KPI visibility (API P95 ≤3s, rollback ≤10m).@specs/001-lowcost-cicd-infra/spec.md#10-109 @.specify/memory/constitution.md#32-39
- **PDPA-Safe Data Stewardship**: Supabase RLS, GPS rounding, consent gating, secrets via GitHub environments with `.env.example` placeholders, retention automation tracked in guardrails.@specs/001-lowcost-cicd-infra/spec.md#63-103 @.specify/memory/constitution.md#40-46
- **Instant, Resilient, Clear UX**: Ensure mobile/portal flows stay within 3 taps, maintain offline queue states, EN/TH i18n keys, and role-based visibility across admin surfaces.@specs/001-lowcost-cicd-infra/spec.md#99-104 @.specify/memory/constitution.md#48-55
- **Automated CI/CD & Versioned Releases**: Uphold Ruff → ESLint → Pytest → OpenAPI Lint → Build → GHCR → Tag Deploy order, enforce manual prod approvals, document rollback ≤10m, align contracts/models with single sources of truth.@specs/001-lowcost-cicd-infra/spec.md#63-118 @.specify/memory/constitution.md#56-63
- **Stack & Infrastructure Alignment**: Target Python 3.12, Node 22.21.1, Expo 54, Next.js 16, Supabase, Cloud Run, Vercel, Cloudflare; monitor via Cloud Run logs, Vercel metrics, Supabase dashboards, optional Sentry/Grafana.@specs/001-lowcost-cicd-infra/spec.md#25-109 @.specify/memory/constitution.md#64-79

## Project Structure

### Documentation (this feature)

```text
specs/001-lowcost-cicd-infra/
├── plan.md              # Implementation strategy (this file)
├── research.md          # Phase 0 decisions & rationale
├── data-model.md        # Entities and relationships
├── quickstart.md        # Setup & verification guide
├── contracts/           # OpenAPI excerpt for health/readiness endpoints
└── tasks.md             # Created by `/speckit.tasks`
```

### Source Code (repository root)

```text
repo/
├── .github/workflows/
│   ├── ci.yml
│   ├── deploy-api.yml
│   ├── deploy-ocr.yml
│   └── deploy-portal.yml
├── src/apps/api/
│   ├── Dockerfile
│   └── service/__main__.py
├── src/apps/ocr-worker/
│   ├── Dockerfile
│   └── ocr/__main__.py
├── src/apps/portal/
│   └── package.json
├── src/apps/mobile/
│   └── app.config.ts
└── docs/
    └── deployment/
        └── secrets-catalog.md

tests/
├── backend/
│   └── test_ci_guardrails.py
├── contract/
│   └── test_health_contract.py
└── integration/
    ├── test_cloud_run.py
    └── test_portal_build.py
```

**Structure Decision**: Maintain a single repository with `src/apps/<surface>` directories feeding shared CI/CD workflows under `.github/workflows/`, enabling per-surface build contexts while centralizing governance assets. Portal/mobile UX hooks depend on API/OCR PDPA filters being in place before Capture → Review → Submit flows are validated; DNS/RLS docs live under `docs/deployment/`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _None_ | — | — |
