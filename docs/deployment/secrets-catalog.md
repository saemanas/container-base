# Secrets Catalog: Low-cost CI/CD & Infra Skeleton

| Secret Name | Location | Scope | Staging Value | Production Value | Rotation |
|-------------|----------|-------|---------------|------------------|----------|
| API_SUPABASE_URL | GitHub Actions secrets | API/OCR | `https://container-base-stg.supabase.co` | `https://container-base.supabase.co` | Quarterly |
| API_SUPABASE_SERVICE_ROLE | GitHub Actions secrets | API | `stg-service-role` | `prod-service-role` | Monthly |
| API_SUPABASE_ANON_KEY | GitHub Actions secrets | API/OCR/Portal/Mobile | `stg-anon-key` | `prod-anon-key` | Quarterly |
| API_JWT_SECRET | GitHub Actions secrets | API | `stg-jwt-secret` | `prod-jwt-secret` | Monthly |
| OCR_MAX_IMAGE_MB | Cloud Run env vars | OCR Worker | `15` | `20` | As needed |
| OCR_TIMEOUT_MS | Cloud Run env vars | OCR Worker | `15000` | `20000` | As needed |
| PORTAL_API_BASE_URL | Vercel env vars | Portal | `https://api-stg.container-base.com` | `https://api.container-base.com` | As needed |
| PORTAL_LINE_REDIRECT | Vercel env vars | Portal | `https://portal-stg.container-base.com/callback` | `https://portal.container-base.com/callback` | As needed |
| MOBILE_API_BASE_URL | Expo EAS secrets | Mobile | `https://api-stg.container-base.com` | `https://api.container-base.com` | Quarterly |
| MOBILE_LINE_CHANNEL_ID | Expo EAS secrets | Mobile | `LINE-STG-CHANNEL` | `LINE-PROD-CHANNEL` | Quarterly |
| CLOUD_RUN_REGION | GitHub Actions secrets | CI/CD | `asia-southeast1` | `asia-southeast1` | Annual |
| GCLOUD_SERVICE_ACCOUNT_JSON | GitHub Actions secrets | CI/CD | `gcp-service-account-stg.json` | `gcp-service-account-prod.json` | Monthly |

> All secrets must be injected via platform-specific secret managers. Never commit real values. Staging/production placeholders above are illustrative only.
