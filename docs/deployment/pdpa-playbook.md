# PDPA Consent & Retention Playbook

## Consent Capture
- Collect explicit consent via LINE login handoff; store records in `app_stg.consent_records` / `app_prod.consent_records`.
- Log consent timestamp, channel (LINE, portal), and data scope in consent record.
- Block application access until consent record exists with `revoked_at IS NULL`.

## Revocation & Deletion
- Provide portal admin action to revoke consent, populating `revoked_at`.
- On revocation, queue deletion job to purge personal data within 48 hours.
- Maintain audit trail of revocation requests in `billing_ledger` notes for billing reconciliation.

## Retention Windows
- Full-resolution images retained 14 days, thumbnails retained 12 months.
- Billing and operational logs retained 12 months for PDPA compliance.
- Anonymize GPS data older than 12 months (round to 3 decimals before storage).

## Access Controls
- Enforce Supabase RLS policies by `org_id` and `site_id`.
- Mask emails to `*@domain` format in any structured log or export.
- Restrict service-role key usage to API/OCR Cloud Run services via secret managers.

## Incident Response
- Notify compliance lead within 1 hour of suspected PDPA breach.
- Freeze data exports and initiate audit log capture.
- Provide incident summary and remediation steps in `docs/deployment/rollback-playbook.md` within 24 hours.

## Remediation Workflow
- **Missing consent evidence**: Trigger API safeguard (`403`) and run `scripts/pdpa/backfill_consent.sh` to reconcile consent records; document outcome in `docs/deployment/observability.md`.
- **Revoked consent leakage**: Execute Supabase purge function `select pdpa.purge_user_data(user_id)` and confirm with audit log export.
- **Email/GPS masking regression**: Re-run `pytest tests/backend/test_pdpa_compliance.py` and redeploy only after passing; record fix in release notes.
- **OCR credential misuse**: Rotate Supabase anon key, redeploy OCR worker, and validate via `pytest tests/worker/test_ocr_pdpa.py`.
