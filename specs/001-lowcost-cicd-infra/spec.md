# Feature Specification: Low-cost CI/CD & Infra Skeleton

**Feature Branch**: `001-lowcost-cicd-infra`  
**Created**: 2025-11-09  
**Status**: Draft  
**Input**: User description: "최소한/저비용의 CI/CD, 인프라, 시스템, 스켈레톤 등 구성."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Spin up minimal CI/CD pipeline (Priority: P1)

Infrastructure engineer sets up the shared repository skeleton and GitHub Actions workflows so that API, OCR worker, and portal apps automatically lint, test, and package on every PR and deploy on main merges while staying inside free-tier limits.

**Why this priority**: Without a working CI/CD baseline, downstream teams cannot ship nor verify builds, blocking Sprint 0 success metrics and governance requirements.

**Independent Test**: Trigger a pull request on the new branch and verify all CI jobs (api, ocr, portal) execute and report status without manual intervention, producing tagged container images for API/OCR and a build artifact for the portal.

**Acceptance Scenarios**:

1. **Given** the repo on GitHub, **When** a PR is opened, **Then** Ruff/ESLint/Pytest/OpenAPI Lint tasks run per app and report success or actionable failures.  
2. **Given** a merge to `main`, **When** the pipeline finishes, **Then** Cloud Run receives updated API/OCR images and Vercel receives a portal build preview without exceeding free-tier quotas.

---

### User Story 2 - Deploy low-cost runtime surfaces (Priority: P2)

Platform lead provisions minimal environments for API, OCR worker, and portal using Cloud Run and Vercel so field teams can access staging endpoints with Supabase backing while respecting PDPA controls.

**Why this priority**: Lightweight hosting enables operations to validate LINE-first workflows before investing in higher-cost infrastructure.

**Independent Test**: Run scripted deploys that launch Cloud Run services and Vercel project, then confirm health endpoints, Supabase connectivity, and LINE Login callbacks respond as expected.

**Acceptance Scenarios**:

1. **Given** Cloud Run free quota, **When** deployment jobs run, **Then** API and OCR services expose `/healthz` and `/readyz` and pass smoke checks using Supabase credentials.  
2. **Given** Vercel Hobby plan, **When** the portal deploy completes, **Then** the portal loads with environment-derived API base URL and LINE redirect values.

---

### User Story 3 - Govern secrets and cost guardrails (Priority: P3)

Operations analyst documents and enforces where secrets live (GitHub, platform env vars) and sets monitoring guardrails so cold starts, missing secrets, or quota breaches trigger rapid remediation within MiniOps constraints.

**Why this priority**: Centralized credential management and guardrails are required to stay compliant with PDPA and avoid paid overages.

**Independent Test**: Review secrets catalog and cost guard checklist, simulate a missing secret or quota hit, and verify documented runbooks restore service within MTTR thresholds.

**Acceptance Scenarios**:

1. **Given** a new operator onboarding, **When** they follow the secrets catalog, **Then** required GitHub/Vercel/Cloud Run/Supabase variables are provisioned without exposing real credentials.  
2. **Given** Cloud Run logs report OCR concurrency spikes, **When** guardrails trigger, **Then** the runbook executes scaling or queueing actions before free-tier exhaustion.

---

### Edge Cases

- Cloud Run cold starts exceed acceptable latency during peak usage; document mitigation via minimum instances or queuing.
- GitHub Actions loses access to Supabase keys; pipeline must fail safely and point to remediation steps.
- Vercel build exceeds build minutes due to dependency cache misses; define fallback to manual static export or deferred build window.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Provide a monorepo directory skeleton (`src/apps/{api, ocr, portal, mobile}` and `.github/workflows/`) so each workload has an isolated build context while sharing governance assets.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#110-123
- **FR-002**: Implement a GitHub Actions CI workflow that executes checkout, language runtime setup (Python 3.12, Node 22), lint/tests, and Docker build steps for API/OCR, all triggered on PRs and `main` pushes.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#125-309 @refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#29-33
- **FR-003**: Deliver deployment workflows that push API and OCR containers to GHCR and deploy to Cloud Run, plus portal deploy to Vercel Hobby plan, ensuring domain mappings (`api`, `ocr`, `portal`) are documented for Cloudflare DNS setup.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#91-123 @refs/docs/CB-MiniOps-v1.0.0-en-US.md#131-135 @refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md#24-31
- **FR-004**: Publish `.env.example` templates and secrets catalog covering API_BASE_URL, SUPABASE keys, LINE Login, OCR limits, and logging configuration, with guidance to store real values only in GitHub/hosting secret stores.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#24-27 @refs/docs/CB-MiniOps-v1.0.0-en-US.md#45-63 @refs/docs/CB-MiniOps-v1.0.0-en-US.md#160-170
- **FR-005**: Document Supabase integration including free-tier usage, RLS enforcement, and key separation (anon vs service role) to satisfy PDPA data isolation requirements, using a single Supabase project with environment-specific tables/policies for staging and production.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#80-88 @AGENTS.md#55-58
- **FR-006**: Define health/ready endpoints, MAX_IMAGE_MB, TIMEOUT_MS guardrails, Cloud Run concurrency (target 5 per instance), and logging schema `{ts, opId, code, duration_ms}` for API and OCR services to support observability and SLA monitoring.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#37-63 @refs/docs/CB-MiniOps-v1.0.0-en-US.md#211-219 @AGENTS.md#37-40
- **FR-007**: Provide local development instructions enabling mobile, API, OCR, and portal services to run concurrently with Supabase remote connection and CORS configuration.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#140-155
- **FR-008**: Establish cost and scaling guardrails, including upgrade triggers for performance, load, stability, and cost, with runbooks for responding when thresholds are crossed.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#201-229
- **FR-009**: Create rollback and incident response playbooks that ensure deployments can revert to prior tags within 10 minutes and align with CI/CD governance flow (Ruff → ESLint → Pytest → OpenAPI Lint → Build → GHCR → Tag Deploy).@AGENTS.md#60-64

### Key Entities *(include if feature involves data)*

- **PipelineDefinition**: Describes CI/CD jobs, triggers, required runtimes, and artifact outputs for each workload, including success/failure handling and notification hooks.
- **DeploymentSurface**: Captures hosting targets (Cloud Run services, Vercel project, Supabase project) with associated URLs, scaling settings, and health-check expectations.
- **SecretCredentialSet**: Enumerates secrets per environment (GitHub, Cloud Run, Vercel, Supabase), ownership, rotation cadence, and masking policies.
- **GuardrailMetric**: Defines monitored metrics (API p95 latency, OCR failure rate, Cloud Run quota usage) and corresponding alert thresholds.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: PR pipelines complete Ruff, ESLint, Pytest, and OpenAPI Lint stages for API/OCR/portal within 12 minutes median and 100% success rate for green builds over rolling 14 days.
- **SC-002**: Deployments to Cloud Run and Vercel finish within 5 minutes per service and maintain API/OCR P95 latency ≤3s post-deploy with ≤10-minute rollback MTTR when failures occur.
- **SC-003**: Secrets catalog coverage reaches 100% of required keys before first deploy, with quarterly rotation reminders and zero leaked credentials in repository history.
- **SC-004**: Cloud Run, Supabase, and Vercel usage stays ≤80% of free-tier quotas in steady state, with documented actions ready when thresholds are exceeded.

## Compliance, UX, and Operational Requirements *(mandatory)*

### PDPA & Security

- Enforce consent → revoke → delete ≤48h workflow in API documentation before enabling mobile or portal access; block non-consented requests.
- Apply GPS rounding (3 decimals), email masking, and Supabase RLS scopes across API endpoints; ensure SERVICE_ROLE_KEY is restricted to internal calls.
- Store all secrets in GitHub/hosting environments with dummy placeholders committed; document rotation and incident response for compromised credentials.

### UX & Localization

- Ensure Capture → Review → Submit flows remain ≤3 taps by coordinating mobile and portal build scripts with API availability; define offline queue expectations (≥99% success) and states (Queued, Uploading, Failed, Approved) with EN/TH i18n keys.
- Document how Organization/Site/Admin/Operator/Viewer roles interact with deployment artifacts (e.g., portal dashboards vs. API tokens) and localization handling for operational dashboards.
- Provide guidance for Empty/Loading/Success/Error/Offline UI states in portal/mobile skeletons to align with shadcn/ui and Expo patterns.

### KPI & Observability Mapping

- Map the feature to KPIs: FPRR ≥90%, API P95 ≤3s, rollback MTTR ≤10m, retention ≥60%, MAU ≥1,000; specify which dashboards or alerts confirm each metric.
- Define log schema `{ts, opId, code, duration_ms}` for all services, enabling aggregation of API latency, OCR error rate, and deployment status.
- Outline monitoring setup: Cloud Run logs, Vercel metrics, Supabase usage dashboards, and optional Sentry/OpenTelemetry integrations for future expansion.

## Clarifications

### Session 2025-11-09

- Q: How should staging versus production deployment approval flow behave in the low-cost pipeline? → A: Staging auto deploys; production requires manual approval.
- Q: How should Supabase staging versus production environments be structured within the low-cost constraints? → A: Share one Supabase project with separate tables/RLS per environment.
- Q: What Cloud Run concurrency limit should we enforce for the low-cost API/OCR services? → A: Set concurrency to 5 requests per instance.
