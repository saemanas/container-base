# `supabase-smoke-test.sh`

## Purpose
Validate Supabase staging schema, migration parity, and RLS guardrails before promoting to production, aligning with PDPA-Safe Data Stewardship.

## Behavior
- Requires Supabase CLI, `SUPABASE_STG_REF`, optional `SUPABASE_LOCAL_REF`, and `RLS_TEST_PATH`.
- Pulls the staging schema, applies it to the local rehearsal ref, executes RLS tests, and compares migrations via `supabase db diff`.
- Logs output to `artifacts/supabase/rls-smoke-<timestamp>.log`.

## Usage
```
SUPABASE_STG_REF=container-base-stg \
  SUPABASE_LOCAL_REF=local-ci \
  scripts/supabase-smoke-test.sh
```

## Notes
- Outputs warnings when diffs appear; recommended to review before production promotion.
- See `docs/deployment/supabase-schema.md` for migrations context and `docs/deployment/rollback-playbook.md` for rollback steps captured by the same log directories.
