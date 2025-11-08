# Data Model: Low-cost CI/CD & Infra Skeleton

## Entities

### PipelineDefinition
- **Purpose**: Describes CI/CD jobs and triggers for each workload.
- **Key Fields**:
  - `id` (string, unique)
  - `app` (enum: `api`, `ocr-worker`, `portal`, `mobile`)
  - `workflow_file` (string path)
  - `triggers` (list of git events)
  - `stages` (ordered list: Ruff, ESLint, Pytest, Spectral, Build, GHCR Push, Tag Deploy)
  - `approval_required` (boolean, production only)
  - `artifacts` (list of generated images/build outputs)
- **Relationships**: Linked to `DeploymentSurface` via `app`.

### DeploymentSurface
- **Purpose**: Captures hosting targets and deployment configuration.
- **Key Fields**:
  - `id` (string, unique)
  - `app` (enum: `api`, `ocr-worker`, `portal`, `mobile`)
  - `environment` (enum: `staging`, `production`)
  - `platform` (enum: `cloud-run`, `vercel`, `expo-eas`)
  - `endpoint_url` (string)
  - `health_check` (string path)
  - `ready_check` (string path or `null`)
  - `concurrency_limit` (integer, default 5 for Cloud Run)
  - `supabase_schema` (string schema name when applicable)
- **Relationships**: References `SecretCredentialSet` entries for required credentials.

### SecretCredentialSet
- **Purpose**: Maps secrets, owners, and storage locations per environment.
- **Key Fields**:
  - `id` (string, unique)
  - `environment` (enum: `staging`, `production`)
  - `service` (enum: `github`, `cloud-run`, `vercel`, `supabase`)
  - `key_name` (string)
  - `owner` (string role)
  - `rotation_cadence_days` (integer)
  - `status` (enum: `draft`, `active`, `rotating`)
- **Relationships**: Associated with `PipelineDefinition` (for CI access) and `DeploymentSurface` (for runtime usage).

### GuardrailMetric
- **Purpose**: Defines monitored metrics and alert thresholds.
- **Key Fields**:
  - `id` (string, unique)
  - `metric_name` (enum: `api_p95`, `ocr_failure_rate`, `cloud_run_quota`, `vercel_build_minutes`)
  - `threshold` (numeric or percentage)
  - `observability_source` (enum: `cloud-run-logs`, `vercel-analytics`, `supabase-dashboard`, `sentry`, `k6`)
  - `alert_channel` (string, e.g., LINE webhook)
  - `runbook_ref` (string path)
- **Relationships**: Links to `DeploymentSurface` to specify the monitored service.

### ClarificationLog
- **Purpose**: Tracks clarifications and resulting decisions.
- **Key Fields**:
  - `id` (string, unique)
  - `question` (string)
  - `answer` (string)
  - `session_date` (date)
  - `impact_area` (enum: `deployment`, `database`, `performance`)
- **Relationships**: Used by planning artifacts; references `PipelineDefinition` or `DeploymentSurface` when decisions affect them.

## State Transitions

- `PipelineDefinition.approval_required`: `false` → `true` when environment is production and manual approval is toggled; revert only via governance review.
- `SecretCredentialSet.status`: `draft` → `active` after validation; `active` → `rotating` during key rotation; `rotating` → `active` post verification.
- `GuardrailMetric.threshold`: updated when KPI budgets change; changes trigger notification to governance log.

## Data Volume & Scale Assumptions

- Expect ≤10 PipelineDefinition entries (one per workload/environment combo) and ≤20 DeploymentSurface entries for MVP.
- Guardrail metrics sampled every 5 minutes; stored as time-series in monitoring stack.
- Secrets catalog maintained via markdown/YAML, synchronized with GitHub environment variables.
