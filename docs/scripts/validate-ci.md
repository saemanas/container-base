# `validate-ci.sh`

## Purpose
Sanity-checks the local environment before running CI jobs, ensuring required configuration files, tools, and environment variables exist, then logs structured JSON for each guard clause.

## Behavior
- Verifies presence of `.ruff.toml`, `.eslintrc.cjs`, `.prettierrc`, and `.github/workflows`.
- Checks required commands (`python3`, `npm`, `docker`) and environment variables such as `API_SUPABASE_URL`, `API_SUPABASE_ANON_KEY`, `API_SUPABASE_SERVICE_ROLE`, `OCR_MAX_IMAGE_MB`, `OCR_TIMEOUT_MS`, and `API_JWT_SECRET`.
- Emits structured logs (e.g., `{"ts":"...","opId":"validate-ci","code":"MISSING_ENV",...}`) for each validation result.

## Usage
```
./scripts/validate-ci.sh
```

## Notes
- Designed as a pre-flight step before `act`/`make check` to catch missing secrets or dependencies earlier.
- Aligns with the constitution’s Spec-to-Verification discipline by documenting required baseline assets.
