# Tests Directory Map

`tests/` organizes all pytest suites guarding the container-base CI/CD, PDPA, and deployment guarantees. Below is a high-level map of each subdirectory and the files they contain, followed by references to the per-category summaries stored under `docs/tests/`.

- `tests/backend/`
  - Files: `test_ci_guardrails.py`, `test_ocr_pdpa.py`, `test_pdpa_compliance.py`, `test_pdpa_retention_job.py`, `test_secrets_catalog.py`
  - Focus: API/OCR PDPA helpers, CI workflow ordering, retention job invocation, and secrets catalog coverage.
  - See `docs/tests/backend/README.md` for per-file details.
- `tests/contract/`
  - Files: `test_ci_pipeline_order.py`, `test_health_contract.py`
  - Focus: OpenAPI contract coverage and GitHub Actions job order validation before merge.
  - See `docs/tests/contract/README.md`.
- `tests/integration/`
  - Files: `test_ci_pdpa_failure.py`, `test_cloud_run.py`, `test_cost_guardrails.py`, `test_multicloud_deploy.py`, `test_portal_build.py`, `test_rollback_drill.py`, `test_supabase_promotion.py`
  - Focus: Multi-service scenarios (PDPA gate, Cloud Run readiness, rollback drills, Supabase promotion, portal & quota probes).
  - See `docs/tests/integration/README.md`.
- `tests/scripts/`
  - Files: `test_check_free_tier.py`, `test_send_ci_email.py`
  - Focus: Validating helper scripts emit structured logs and artifacts.
  - See `docs/tests/scripts/README.md`.

Keep this overview synced with the actual `tests/` tree; if you add/remove test files or directories, update both this map and the matching `docs/tests/<subdir>/README.md`.
