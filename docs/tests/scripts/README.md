# Script Tests (`tests/scripts`)

Verifies the helper scripts themselves behave as expected (artifacts + structured logs).

| Test | Purpose | Notes |
| --- | --- | --- |
| `test_check_free_tier.py` | Runs `scripts/check-free-tier.py` to ensure it writes JSON artifacts, emits structured logs, and uses `--op-id`/`--artifact-dir` options as expected. | Simulates GitHub run via `GITHUB_RUN_ID` env. |
| `test_send_ci_email.py` | Executes `scripts/send-ci-email.py` with mock email envs, confirms `.eml` artifact creation, and validates the structured log output contains `{ts, opId, code}` while referencing the expected recipients/links. | Ensures notification archives exist for release reviews. |

These tests guard the automation helpers described in `docs/scripts/*.md`.
