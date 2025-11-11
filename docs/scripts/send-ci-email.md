# `send-ci-email.py`

## Purpose
Render CI/CD success/failure/rollback notification emails, archive them as `.eml` artifacts, and emit structured logs used for post-release alerting.

## Behavior
- Accepts details such as `--event`, `--service`, `--environment`, `--ref`, `--duration`, `--artifact-url`, `--workflow-run-url`, and `--op-id`.
- Requires environment variables `OPS_EMAIL_TO`, `OPS_EMAIL_FROM`, and optional `OPS_EMAIL_CC`.
- Writes the email body (including headers) to `artifacts/notifications/<op-id>-<event>.eml` and prints a JSON log capturing `{ts, opId, code, duration_ms}` referencing the artifact path.

## Usage (CI example)
```
export OPS_EMAIL_TO=ops@example.com
export OPS_EMAIL_FROM=noreply@example.com
python scripts/send-ci-email.py \
  --event success \
  --service api \
  --environment prod \
  --ref v1.2.3 \
  --duration PT3M \
  --artifact-url https://github.com/.../artifacts/ci-tag-deploy \
  --workflow-run-url https://github.com/.../actions/runs/xxx \
  --op-id api-prod-success
```

## Notes
- Template choices (`success`, `failure`, `rollback`) determine the subject/body structure.
- `docs/deployment/ci-cd-notifications.md` references this script for artifact archiving.
