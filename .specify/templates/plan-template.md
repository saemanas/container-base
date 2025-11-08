# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-to-Verification Discipline**: Link to the approved `/specs/<feature>/spec.md` and confirm the Spec → Plan → Tasks → Implementation → Tests → Verification sequence is scheduled, with Context7 MCP availability (or outage log + risks) recorded.
- **Test-First Observability**: Outline planned tests (success + failure), coverage targets (≥70% overall, 100% for auth/upload/recognition), JSON logging, and how Docker Compose services plus `/reports/vision-bench.json` will surface KPIs (API P95 ≤3s, upload success ≥99%, rollback ≤10m).
- **PDPA-Safe Data Stewardship**: Describe consent gating, GPS rounding, email masking, Supabase RLS scopes, retention/ deletion workflows (≤48h), and secrets handling (GitHub environments + `.env.example` placeholders).
- **Instant, Resilient, Clear UX**: Declare Capture → Review → Submit ≤3 taps, offline queue design, required UI states (Empty/Loading/Success/Error/Offline), localization approach (EN/TH keys only), and role visibility (Org → Site → Admin → Operator → Viewer).
- **Automated CI/CD & Versioned Releases**: Confirm branch/commit strategy, CI order (Ruff → ESLint → Pytest → Spectral → Build → GHCR Push → Tag Deploy), rollback plan (≤10m), and ownership of OpenAPI contracts, `/billing/*` schemas, and `/models/<version>/model.yaml`.
- **Stack & Infrastructure Alignment**: State targeted runtimes (Python 3.12, Node 22.21.1, Expo/Next.js/FastAPI/Supabase), deployment targets (Cloud Run/Render/Fly + Cloudflare), monitoring (Grafana/Sentry), and payment/logistics integrations impacted.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
