# Research: CI/CD Hardening & Multicloud Release Readiness

## Decision 1 — Long-term CI/CD Evidence Storage
- **Decision**: Store all CI/CD logs, coverage, and metrics as GitHub Actions artifacts with extended retention policies.
- **Rationale**: GitHub-hosted artifacts align with the mandated `{ts, opId, code, duration_ms}` log schema and keep evidence within the existing CI chain for compliance sign-off.@specs/002-cicd-hardening/spec.md#12-85 @README.md#63-116 @refs/docs/CB-Instruction-v1.0.0-en-US.md#150-201
- **Alternatives Considered**:
  - Supabase storage buckets — rejected due to additional PDPA surface area and redundant retention management.
  - Google Cloud Storage — rejected because it adds IAM overhead outside the prescribed free-tier tooling stack.@refs/docs/CB-MiniOps-v1.0.0-en-US.md#13-218

## Decision 2 — Supabase Migration Promotion
- **Decision**: Run Supabase migrations in staging first, execute Supabase CLI RLS smoke tests, then promote identical scripts to production with audit logs preserved for ≥12 months.@specs/002-cicd-hardening/spec.md#72-83
- **Rationale**: Staged promotion enforces PDPA-safe data stewardship, validates RLS policies before customer traffic, and keeps rollback evidence within the ≤10 minute MTTR budget.@specs/002-cicd-hardening/spec.md#48-103 @refs/docs/CB-Instruction-v1.0.0-en-US.md#138-201
- **Alternatives Considered**:
  - Direct-to-production migrations with manual DBA gates — rejected because it risks inconsistent evidence capture and slows automated rollbacks.
  - Supabase change requests without staging — rejected since the spec requires deterministic rehearsal coverage for multicloud releases.

## Decision 3 — CI/CD Notification Channel
- **Decision**: Send success/failure/rollback notifications to the operations email distribution (GitHub notification emails) for audit visibility.@specs/002-cicd-hardening/spec.md#12-15 @specs/002-cicd-hardening/spec.md#70-85
- **Rationale**: Email satisfies PDPA logging requirements, keeps stakeholders within the mandated Org→Site→Admin→Operator visibility chain, and avoids introducing additional chat tooling beyond the Service Plan scope.@refs/docs/CB-Instruction-v1.0.0-en-US.md#94-117 @refs/docs/CB-Service-Plan-v1.0.0-en-US.md#21-112
- **Alternatives Considered**:
  - LINE Alert webhook — rejected for this feature because the spec explicitly scopes notifications to email while LINE remains future enhancement.
  - Slack integration — rejected as it is not part of the approved stack and would violate the free-tier infrastructure guardrails.
