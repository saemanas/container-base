# Supabase Schema Blueprint: Low-cost CI/CD & Infra Skeleton

## Overview
- Single Supabase project with logical schemas `app_stg` and `app_prod`
- Shared auth, storage, and functions; environment separation handled via schema prefixes and RLS
- All timestamps stored in UTC; GPS coordinates rounded to 3 decimals before insert

## Schemas
### `app_stg`
| Table | Purpose | Key Columns | RLS Policy Summary |
|-------|---------|-------------|--------------------|
| container_events | Stores uploads, OCR results, and approvals | id (uuid), container_id, captured_at, status, uploader_id | Allow insert/update by uploader; org/site admins read all |
| billing_ledger | Tracks credit consumption | id (uuid), org_id, amount, reason, recorded_at | Org admins read/write own rows; auditors read all |
| consent_records | PDPA consent timeline | id (uuid), user_id, consent_given_at, revoked_at | User can read own; admins read scoped org |
| queue_metrics | Offline queue telemetry | id (uuid), device_id, event_type, occurred_at | Service role write; org admins read |

### `app_prod`
Schema mirrors `app_stg` with identical table definitions, policies, and indexes to keep parity.

## Roles & Keys
| Role | Usage | Notes |
|------|-------|-------|
| anon | Portal/mobile public access; read-only on non-sensitive views | Denied write; limited to read via security-definer functions |
| authenticated | Supabase auth sessions; read/write limited to org/site scope | Use for portal/mobile data mutations |
| service_role | Backend-only (API/OCR) elevated capabilities | Inject via Cloud Run secrets only |

## Row-Level Security (RLS)
- Enable RLS on every table listed above
- Use `org_id` and `site_id` columns to enforce scoping; call `auth.jwt()` claims for portal/mobile access
- Expose read-only materialized views (e.g., `container_events_public`) to anon role when necessary
- Consent evidence must be persisted in `consent_records` with `revoked_at` populated on withdrawal; API middleware relies on this field.
- Recommended policy snippet (adjust for schema):
  ```sql
  ALTER TABLE app_stg.container_events ENABLE ROW LEVEL SECURITY;
  CREATE POLICY container_events_org_isolation
    ON app_stg.container_events
    USING (org_id = auth.jwt()->>'org_id');
  ```
- Mirror policies to `app_prod` and include automated lint checks via `supabase db diff` in CI.

## Migrations & Tooling
- Track schema changes via SQL files in `supabase/migrations/`
- Use Supabase CLI for applying changes locally; CI should validate migrations with `supabase db diff`
- Document any RLS or consent table changes in `docs/deployment/pdpa-playbook.md` to keep legal traceability
- Staging-first rehearsal:
  - Run `SUPABASE_STAGING_REF=<ref> ./scripts/supabase-smoke-test.sh` to capture pull → push → RLS results
  - Store generated logs under `artifacts/supabase/` and upload to GitHub Actions artifacts for ≥90 day retention
  - Record promotion approvals and rollback readiness in `docs/deployment/rollback-playbook.md`

## Maintenance
- Run quarterly review to ensure stg/prod parity
- Document policy updates in `docs/deployment/pdpa-playbook.md`
