# `promote-supabase.sh`

## Purpose
Automates Supabase migration promotion (staging → production) and RLS regression checks, capturing metadata per deployment for rollback/PDPA evidence.

## Behavior
- Requires Supabase CLI; promotes migrations to `${STG_REF}` then runs `supabase db test` against the same project.
- Promotes to `${PROD_REF}` after stg validation completes.
- Emits JSON metadata to `artifacts/supabase/promotion-<timestamp>.json` capturing timestamps, refs, RLS path, and actor (GH run or local).

## Inputs / Environment
- `STG_REF` (default `container-base-stg`), `PROD_REF` (default `container-base-prod`), `RLS_TEST_PATH` (migrates tests).
- `SUPABASE_BIN` resolved automatically.
- Artifacts stored in `artifacts/supabase`.

## Usage
```
STG_REF=container-base-stg PROD_REF=container-base-prod scripts/promote-supabase.sh
```

## Related Documentation
- Refer to `docs/deployment/rollback-playbook.md` and `docs/deployment/supabase-schema.md` for context on migration sequencing.

