# Backend Tests (`tests/backend`)

Focuses on contract and PDPA guardrails for the FastAPI/OCR services and supporting documentation.

| Test | Purpose | Notes |
| --- | --- | --- |
| `test_ci_guardrails.py` | Confirms `.github/workflows/ci.yml` defines the mandated job order (check_backend, check_portal, check_openapi, build, ghcr, tag_deploy) so CI honor the constitution. | Uses `pyyaml` to parse the workflow YAML. |
| `test_ocr_pdpa.py` | Verifies the OCR PDPA helper rejects service-role keys and accepts only anon keys, ensuring the worker cannot escalate privileges. | Relocated from `tests/worker` to keep PDPA guardrails co-located with other backend tests. |
| `test_pdpa_compliance.py` | Exercises the API PDPA helpers: missing consent raises, email masking hides local part, and GPS rounding keeps three decimals. | References `src/apps/api/app/pdpa.py`. |
| `test_pdpa_retention_job.py` | Ensures `cd-api.yml`/`cd-ocr.yml` production jobs invoke `scripts/run-retention-job.sh` with PDPA metadata and Supabase env tokens. | Validates presence of `SUPABASE`/`PDPA` tokens in the workflow steps. |
| `test_secrets_catalog.py` | Guards that `docs/deployment/secrets-catalog.md` documents required environment variables (`API_SUPABASE_*`, `API_JWT_SECRET`, etc.) with rotation cadence. | References the governance catalog for compliance. |

Maintain these tests as the first line of defense for backend compliance; update this README whenever new backend guardrails appear.
