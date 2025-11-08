# Cloudflare Routing Playbook

This playbook documents how to connect the Container Base surfaces to Cloudflare-managed DNS while staying inside the free-tier quotas.

## Prerequisites

- Cloudflare account with access to the target zone (e.g., `example.com`).
- Subdomain ownership for:
  - `api.example.com` → Cloud Run (API service)
  - `ocr.example.com` → Cloud Run (OCR worker)
  - `portal.example.com` → Vercel (Portal web app)
- Cloud Run services created (`cb-api-stg`, `cb-api-prod`, `cb-ocr-stg`, `cb-ocr-prod`).
- Vercel project created with staging/production domains.

## DNS Records

| Surface | Type | Name | Target | TTL |
|---------|------|------|--------|-----|
| API (staging) | CNAME | `api-stg` | `cb-api-stg-<hash>.run.app` | Auto |
| API (production) | CNAME | `api` | `cb-api-prod-<hash>.run.app` | Auto |
| OCR (staging) | CNAME | `ocr-stg` | `cb-ocr-stg-<hash>.run.app` | Auto |
| OCR (production) | CNAME | `ocr` | `cb-ocr-prod-<hash>.run.app` | Auto |
| Portal (staging) | CNAME | `portal-stg` | `<staging>.vercel.app` | Auto |
| Portal (production) | CNAME | `portal` | `<production>.vercel.app` | Auto |

> Replace `<hash>` with the Cloud Run managed domain suffix generated per revision. For production, pin the CNAME to the custom domain bound via `gcloud run domain-mappings`.

## TLS & Security

1. **Cloud Run mappings**
   ```bash
   gcloud run domain-mappings create --service cb-api-prod \
     --domain api.example.com --project $GCP_PROJECT_ID --region $REGION
   gcloud run domain-mappings create --service cb-ocr-prod \
     --domain ocr.example.com --project $GCP_PROJECT_ID --region $REGION
   ```
2. **Vercel custom domains**
   ```bash
   vercel domains add portal.example.com
   vercel domains add portal-stg.example.com --env=preview
   ```
3. Cloudflare will issue Universal SSL certificates automatically. Confirm status under **SSL/TLS → Edge Certificates**.

## Verification Checklist

- [ ] `curl https://api.example.com/healthz` returns HTTP 200 with `{ "status": "ok" }`.
- [ ] `curl https://ocr.example.com/healthz` returns HTTP 200 with `{ "status": "ok" }`.
- [ ] Portal domain resolves and loads with the expected environment banner (staging vs production).
- [ ] Cloudflare analytics confirm traffic is proxied (orange cloud enabled) and free-tier bandwidth is within quota.

## Incident Response

- If Cloud Run certificates fail to validate, re-run `gcloud run domain-mappings describe` and check SSL provisioning logs.
- If DNS propagation is slow, flush cached entries using `dig +trace api.example.com` to verify authoritative records.
- Rollback by pointing CNAME back to previous service URL or disabling proxy mode (grey cloud) temporarily.
