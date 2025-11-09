# Data Model — CI/CD Hardening & Multicloud Release Readiness

## PipelineStageRecord
- **Purpose**: Captures every CI/CD stage execution for audit and observability dashboards.
- **Fields**:
  - `id` (UUID) — unique stage identifier.
  - `pipeline_run_id` (UUID) — aggregation key per CI/CD run.
  - `component` (enum: `api`, `ocr_worker`, `portal`, `shared`) — surface the stage applies to.
  - `stage_name` (string) — e.g., `ruff`, `pytest`, `deploy_cloud_run`.
  - `status` (enum: `success`, `failure`, `skipped`, `retrying`).
  - `started_at` / `finished_at` (timestamp with tz) — duration tracking.
  - `duration_ms` (integer) — direct measurement to back the `{ts, opId, code, duration_ms}` schema.
  - `artifact_url` (string) — GitHub Actions artifact link for evidence.
  - `log_digest` (string) — checksum of structured log payload.
  - `op_id` (string) — mirrors structured log opId.
  - `branch` (string) — branch or tag associated with the run.
  - `triggered_by` (string) — GitHub actor or automation ID.
  - `environment` (enum: `staging`, `production`).
  - `metadata` (JSONB) — supplementary details (coverage %, release notes reference).
- **Relationships**:
  - Many PipelineStageRecords belong to one PipelineRun aggregate (not yet modeled here).
- **Constraints**:
  - `artifact_url` must point to GitHub Actions artifact domain.
  - `op_id` required for observability; unique per stage instance.

## DeploymentEnvironment
- **Purpose**: Defines each target environment (staging, production) and the services deployed within it.
- **Fields**:
  - `id` (UUID).
  - `name` (enum: `staging`, `production`).
  - `cloud_provider` (enum: `cloud_run`, `vercel`, `cloudflare`, `supabase`).
  - `service_name` (string) — e.g., `api`, `ocr-worker`, `portal`, `dns`.
  - `gh_environment` (string) — GitHub environment name for secrets.
  - `secrets_bundle_ref` (string) — reference to secrets catalog entry.
  - `success_criteria` (JSONB) — thresholds (latency P95, MTTR, propagation time).
  - `rollback_tag` (string) — last known good tag for emergency redeploys.
  - `monitoring_dashboard_url` (string) — Grafana/Sentry links.
  - `last_validated_at` (timestamp with tz) — last time health checks & policies validated.
- **Constraints**:
  - `name` + `service_name` unique.
  - `cloud_provider` must map to allowed providers per spec.

## ReleaseChecklist
- **Purpose**: Human-in-the-loop gate capturing PDPA, UX, rollback preparedness, and approval metadata.
- **Fields**:
  - `id` (UUID).
  - `tag` (string) — semantic version candidate (vX.Y.Z).
  - `environment` (enum: `staging`, `production`).
  - `pdpa_confirmed` (boolean) — PDPA consent gating verified.
  - `ux_states_demoed` (boolean) — portal displays Empty/Loading/Success/Error/Offline states.
  - `rollback_rehearsed_at` (timestamp with tz) — last rollback drill time.
  - `approver_role` (enum: `admin`, `operator`).
  - `approver_email` (string) — masked email (***@domain).
  - `notes` (text) — summary of manual checks or blocking issues.
  - `artifacts` (JSONB) — references to GitHub artifacts or Supabase evidence.
- **Constraints**:
  - `tag` must correspond to a git tag existing in repository history.
  - `approver_email` must be masked per PDPA requirements.

## CredentialBundle
- **Purpose**: Represents GitHub Environment secret bundles tied to deployment automation.
- **Fields**:
  - `id` (UUID).
  - `name` (string) — e.g., `staging-api`, `prod-portal`.
  - `service_account` (string) — Cloud Run or Cloudflare account identifier.
  - `supabase_key_ref` (string) — reference to Supabase key storage.
  - `vercel_token_ref` (string) — optional when portal deploys needed.
  - `cloudflare_api_token_ref` (string).
  - `rotation_cadence_days` (integer).
  - `last_rotated_at` (timestamp with tz).
  - `owner` (string) — responsible role or team.
- **Constraints**:
  - Secrets themselves never stored; only references.
  - Rotation cadence must be ≤90 days to satisfy compliance playbook.

## Relationships Overview
- `DeploymentEnvironment` references `CredentialBundle` via `secrets_bundle_ref`.
- `ReleaseChecklist` consumes `PipelineStageRecord` artifact URLs to validate evidence.
- Future `PipelineRun` aggregate will link to `PipelineStageRecord` and `ReleaseChecklist` for reporting.
