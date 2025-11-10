# **CB MiniOps**

**Description:** API / OCR separation and optimized serverless deployment plan

- **Version:** v1.0.0
- **Target Platform:** Android first
- **Components:** Mobile App (React Native / Expo) + API (FastAPI) + OCR Worker (FastAPI + OCR) + Admin Portal (Next.js Web App)
- **Principles:** Simple · Low-cost · Serverless
- **Secrets/Environment Variables:** GitHub Secrets + Deployment Platform Environment Variables

---

## **1. Minimal Tech Stack by Role (Free or Low-cost Options)**

### **1) Mobile App (Android)**

- **Local Development**
    - Expo (free) + Android Emulator
    - Authentication: LINE Login (test channel)
    - API endpoint injected from .env → API_BASE_URL
- **Deployment**
    - Expo EAS Build (free plan) → .apk / .aab
    - Play Console release can be skipped during MVP phase
- **Required Files**
    - app.json, app.config.ts (per-environment API URL)
    - .env.example → API_BASE_URL, LINE_CHANNEL_ID

---

### **2) API Server (FastAPI)**

- **Local Development**
    - uvicorn api.main:app --reload --port 8080
    - Database: Supabase (Postgres free tier) → No local DB required
- **Serverless Deployment**
    - Cloud Run (free quota) → container auto-deployment
- **Endpoints**
    - /healthz (liveness)
    - /readyz (DB/Auth check)
    - /api/* (domain functions)
    - Internal → calls OCR Worker via OCR_URL
- **Required Files**
    - Dockerfile (Python 3.12 slim)
    - api/__main__.py (uvicorn entrypoint)
    - .env.example → JWT_SECRET, SUPABASE_*, ALLOW_ORIGINS, OCR_URL, MAX_IMAGE_MB, TIMEOUT_MS

---

### **3) OCR Worker (FastAPI + OCR)**

- **Local Development**
    - PaddleOCR or Tesseract OCR (+ check digit post-processing)
    - POST /ocr (image → text)
- **Serverless Deployment**
    - Cloud Run (free quota) → cold start allowed
- **Endpoints**
    - /healthz (liveness)
    - /readyz (model load check)
    - POST /ocr (body: base64/URL, MAX_IMAGE_MB, TIMEOUT_MS)
- **Required Files**
    - Dockerfile (model/weights cached in separate build layers)
    - .env.example → MAX_IMAGE_MB, TIMEOUT_MS, LOG_LEVEL

---

### **4) Portal (Next.js)**

- **Local Development**
    - next dev (App Router)
    - .env.local → inject API_BASE_URL
- **Serverless Deployment**
    - Vercel Hobby (free)
    - Domain strategy: portal.example.com (Portal) / api.example.com (API) / ocr.example.com (OCR)
- **Required Files**
    - next.config.ts, .env.example → API_BASE_URL, LINE_LOGIN_REDIRECT
    - public/health.html (optional health page)

---

### **5) Authentication / Database / Storage**

- **Supabase (Free Tier)**
    - Postgres + Auth + Storage + RLS
    - LINE OAuth → handled by API server (JWT issuance) or Supabase custom Auth
- **Required Setup**
    - SUPABASE_URL, ANON_KEY, SERVICE_ROLE_KEY
    - RLS: per-user row-level security; Admin role separated

---

### **6) DNS / CDN / Domains**

- **Cloudflare (Free)**
    - DNS hosting + CDN caching
    - Records: api, ocr, portal → respective deployments

---

### **7) Logging / Monitoring**

- **Default:** Cloud Run Logging, Vercel Logs
- **Optional:** Sentry (free), OpenTelemetry (future integration)

---

## **2. Common CI/CD (GitHub Actions + GHCR)**

### **1) Repository Structure**

```
repo/
  src/
    apps/
      api/
      ocr/
      portal/
      mobile/
  .github/workflows/
    ci.yml
    deploy-api.yml
    deploy-ocr.yml
    deploy-portal.yml
```

### **2) CI**

- Trigger: PR (build/test), main (image push/deploy)
- Image: ghcr.io/<org>/<app>:latest
- Steps: checkout → setup-{node|python} → test → build → docker push

### **3) CD**

- API / OCR: Cloud Run deployment (google-github-actions/deploy-cloudrun)
- Portal: automatic deployment via Vercel

---

## **3. Local Development**

### **1) Run Flow**

| **Service** | **Command** | **Note** |
| --- | --- | --- |
| Mobile | expo start | Android Emulator |
| API | uvicorn api.main:app --reload --port 8080 |  |
| OCR | uvicorn ocr.main:app --reload --port 8081 |  |
| Portal | next dev --port 3000 |  |
| DB | Supabase remote connection |  |
| CORS | ALLOW_ORIGINS=["http://localhost:3000","exp://*"] |  |

### **2) Docker Compose**

- Run api and ocr containers
- Portal and Mobile run locally with hot reload

---

## **4. Environment Variable Standards**

| **Key** | **Purpose** | **Used By** |
| --- | --- | --- |
| API_BASE_URL | Portal/Mobile → API endpoint | mobile, portal |
| OCR_URL | API → OCR Worker endpoint | api |
| JWT_SECRET | API JWT signing | api |
| SUPABASE_URL, ANON_KEY, SERVICE_ROLE_KEY | DB/Auth/Storage | api |
| LINE_CHANNEL_ID, SECRET, REDIRECT_URI | LINE Login | api, portal |
| ALLOW_ORIGINS | CORS allowed domains | api |
| MAX_IMAGE_MB, TIMEOUT_MS | OCR request limit / timeout | api, ocr |
| LOG_LEVEL | Logging level | api, ocr, portal |

> Values are stored in **GitHub Secrets** or platform environment settings.
> 
> 
> Only .env.example should be committed.
> 

---

## **5. Security / Permissions**

- RLS: per-user isolation; Admin separated
- SERVICE_ROLE_KEY: internal server use only
- CORS: strict whitelist by domain
- HTTPS: provided by platform defaults

---

## **6. Network Topology**

```
[Mobile/Android] ──HTTPS──▶ [API (Cloud Run)] ──HTTP──▶ [OCR Worker (Cloud Run)]
                                 │
                                 ▼
                           [Supabase (Auth/DB/Storage)]

[Portal (Next.js on Vercel)] ──HTTPS──▶ [API]
```

---

## **7. Cost and Operations Guide**

- Supabase: start on free tier
- Cloud Run: within free quota, cold start allowed
- Vercel Hobby: free portal hosting
- GitHub Actions / GHCR: free for public repositories
- On traffic growth: enable minimal instance (paid) for Cloud Run, or OCR only

---

## **8. Immediate Low-cost Optimizations**

- **Dual Health Checks:** separate /healthz (liveness) and /readyz (DB/Auth or model load)
- **Request Guardrails:** enforce MAX_IMAGE_MB, TIMEOUT_MS, and allowed file types
- **Docker Layer Optimization:** cache OCR runtime and weights separately
- **Least Privilege Keys:** SERVICE_ROLE_KEY used only internally + route-level ACL
- **Observability MVP:** 3 log-based metrics — API p95 / error rate / OCR failure rate
- **Cost Guard:** Cloud Run concurrency & QPS limits; Supabase storage/log quota alerts

---

## **9. Upgrade Triggers (Scaling or Separation)**

| **Category** | **Condition (7-day avg)** | **Recommended Action** |
| --- | --- | --- |
| Performance | API p95 > 1.0s or OCR p95 > 2.0s | Keep 1 minimum OCR instance (paid) or optimize model/image size |
| Load | 50+ concurrent or >30k OCR/day | Increase OCR autoscale and introduce Pub/Sub queue |
| Stability | /readyz fails ≥3 times/week | Add staging env, improve health policy, automate rollback |
| Cost | Free-tier usage >80% for 2 consecutive weeks | Early alert → prepare paid upgrade |

---

## **10. Operations Checklist**

- **Repo Init:** src/apps/{api, ocr, portal, mobile} + add .env.example
- **Local Run:** setup Supabase keys → run api, ocr → configure CORS & OCR_URL
- **CI/CD:** define ci.yml → deploy to Cloud Run (API/OCR) + Vercel (Portal) → connect Cloudflare DNS
- **Secrets:** register JWT_SECRET, SUPABASE_*, LINE_*, CLOUD_*
- **Ops/Security:** apply RLS, monitor /healthz & /readyz, review logs and metrics dashboards

---

## **11. File Examples (Summary)**

**src/apps/api/Dockerfile**

```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python","-m","api"]
```

**src/apps/ocr/Dockerfile**

```
FROM python:3.12-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y tesseract-ocr && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime
WORKDIR /app
COPY . .
EXPOSE 8080
CMD ["python","-m","ocr"]
```

**.github/workflows/ci.yml**

```
name: CI
on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  api:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: src/apps/api
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -q || true

  ocr:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: src/apps/ocr
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -q || true

  portal:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: src/apps/portal
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm ci
      - run: npm run build --if-present
```

*(Deployment workflows deploy-api.yml, deploy-ocr.yml, deploy-portal.yml should also match working-directory: src/apps/....)*