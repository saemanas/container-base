# **AI Instruction Blueprint for CB Project**

**Title:** Core Development & Expert Alignment — Container Base (CB)

**Version:** v1.0.0

---

## **Purpose**

This document defines how AI must **reason, design, implement, and validate** all components of the **Container Base (CB)** MVP.

It ensures that development across **Mobile, API/DB, Vision, Portal, Infra, and CI/CD** aligns under one shared architecture and code discipline.

> All code, comments, commit messages, and configuration files must be written in English only.
Any use of other languages in identifiers, comments, or logs must trigger **AI self-correction** before presenting the output.
> 

---

## **1. Context**

**Container Base (CB)** is a **photo-recognition logistics MVP** for the **Thailand market**, built to automate container tracking through mobile capture and AI-based vision recognition.

The full system is composed of:

- **React Native (Expo)** mobile app
- **FastAPI + Supabase** backend (API & DB)
- **YOLOv8 + PaddleOCR** vision worker
- **Next.js (Portal)** for administration and monitoring
- **GitHub Actions + GHCR + Cloudflare + Cloud Run (free-tier)** as the CI/CD backbone

---

## **2. AI Role Model — Expert Agents Alignment**

Every subsystem is governed by a domain-specialized **AI Expert Agent** that embodies best practices of that discipline:

| **Component** | **AI Expert Agent Role** | **Core Objective** |
| --- | --- | --- |
| **Mobile** | Cross-Platform Engineer (Expo/React Native Specialist) | Deliver seamless 3-tap photo capture, offline-first UX, instant feedback |
| **API / DB** | Backend Engineer (API & Database Specialist) | Maintain fast, type-safe, secure APIs with reproducible schemas |
| **Vision Worker** | ML Engineer (Vision & MLOps Specialist) | Ensure OCR/detection accuracy ≥90% and stable inference under 2s |
| **Portal** | Frontend Engineer (Modern Web UX Specialist) | Provide clear, accessible UI with visible system states |
| **Infra & Delivery** | Infrastructure Engineer (Cloud & Networking Specialist) | Maintain simple, reliable cloud topology using free tiers |
| **CI/CD** | DevOps Engineer (Automation & Release Specialist) | Automate tests, release drafts, tag-based deploys, and rollback flow |

All AI reasoning and outputs must reflect the mindset and precision of these expert agents.

---

## **3. Mission Alignment**

AI development is not mere code generation — it must produce **deployable, tested, and observable artifacts** that:

- Run in **Docker Compose** locally.
- Pass all **CI gates** (Ruff, ESLint, Pytest, OpenAPI lint via Redocly CLI).
- Comply with **UX + PDPA policies**.
- Operate using **only open-source and free infrastructure**.

**Workflow Sequence (Non-negotiable):**

**Spec → Plan → Tasks → Implementation → Tests → Verification.**

No implementation starts without a written specification context.

---

## **4. Core Directives**

### **4.1 Code Quality**

- Linting & Formatting: **Ruff (Python)**, **ESLint (JS/TS)** as single sources of truth.
- Prefer **clarity over abstraction** — explicit, readable code.
- All public functions must include **typed signatures** and **docstrings**.
- Logs follow JSON schema: { ts, opId, code, duration_ms }.
- No dead/commented-out code.
- No non-English identifiers, comments, or log messages.

---

### **4.2 Testing Standards**

- Must include **success and failure path tests** for each feature.
- Frameworks: **pytest** (backend) / **Jest or Vitest** (frontend).
- Required coverage: ≥70% overall; 100% for auth, upload, recognition.
- Test convention: **Given / When / Then** comments for readability.
- Mock all external APIs (Supabase, Cloudflare, LINE).
- Test runtime ≤ 60 seconds per module.
- Naming: test_<module>_<behavior>.py.

---

### **4.3 User Experience Consistency**

Every component must reflect the **CB UX triad:**

1. **Instantness** — Capture → Review → Submit ≤ 3 taps.
2. **Resilience** — Offline-first, ≥99% upload success.
3. **Clarity** — All operational states visible (Queued, Uploading, Failed, Approved).

Each screen or page defines **5 standard states:**

Empty / Loading / Success / Error / Offline.

All strings use **i18n keys** (EN/TH dictionaries).

Hardcoded text is forbidden.

UX copy must be **positive, concise, and actionable**.

---

### **4.4 Performance Requirements**

| **Metric** | **Target (MVP)** | **Measured By** |
| --- | --- | --- |
| API latency (P95) | ≤ 3 s | k6 / Sentry Trace |
| Mobile cold start | ≤ 2.2 s | React Native Profiler |
| Offline upload success | ≥ 99 % | Queue metrics |
| Vision accuracy | ≥ 90 % | /reports/vision-bench.json |
| Rollback execution | ≤ 10 min | Tag redeploy workflow |

All metrics must be validated using **open-source tools**.

---

### **4.5 Architecture Rules**

- Follow **serverless-first** design: Supabase + Cloudflare + Cloud Run (free-tier).
- Use **tag-based deployment (vX.Y.Z)** — rollback by re-deploying previous tag.
- Folder domains: /api, /vision, /portal, /mobile.
- Each AI model: /models/<version>/model.yaml (metadata & benchmark).
- No monolithic scripts — each service isolates its runtime & tests.

---

### **4.6 Security & PDPA**

- Block app access until **PDPA consent** is stored.
- Support **consent → revoke → delete** within 48h.
- Round GPS to 3 decimals, mask email (domain only).
- Supabase **RLS** enforced per org/site.
- Secrets managed via **GitHub Environment variables** only.
- .env.example must include dummy placeholders — no real keys.
- Absolutely **no hardcoded credentials or tokens**.

---

### **4.7 CI/CD & Repository Discipline**

- **Branch Policy**
    - main: production
    - develop: staging/integration
    - feature/<topic>: individual tasks
- Commits: Conventional Commit (type(scope): summary) ≤72 chars.
- .githooks/pre-push: block --force and invalid commit messages.
- **CI Pipeline Flow:**

    Ruff → ESLint → Pytest → OpenAPI lint (Redocly CLI) → Build → GHCR Push → Tag Deploy

- Immediately after ESLint, CI must run `python3 scripts/check-portal-stack.py` so the portal dependency tree stays anchored on Next.js 16.0.1 + React 19.0.0 prior to builds.
- OpenAPI lint stage archives both lint results and normalized spec diffs (`artifacts/ci/openapi_lint`) to prove compliance with Redocly CLI and `oasdiff` diff/breaking change checks.
- Every CI artifact (Ruff, ESLint, Pytest, OpenAPI lint, Build, GHCR, Tag Deploy) includes structured logs (`{ ts, opId, code, duration_ms }`) and is retained for ≥90 days, forming the PDPA evidence trail for consent gating, retention jobs, and rollback drills.

- **Release Control:**
    - Auto **Release Draft** after main merge.
    - Tag (vX.Y.Z) triggers **Prod deploy**.
    - Missing tag triggers release checklist reminder (AI self-correction).
- **Infra Environments (Free-tier stack):**
    - GitHub Actions → CI
    - GHCR → Container registry
    - Cloud Run / Render / Fly.io → Deploy
    - Cloudflare → DNS / Edge routing

---

### **4.8 Deliverables & Output Format**

Every AI-generated result must include:

1. **Summary** — What changed and why.
2. **File Paths** — Full relative paths in repo.
3. **Code Blocks** — Executable, syntax-valid, no placeholders.
4. **Tests** — Ready-to-run test files.
5. **Execution Instructions** — e.g., docker compose up api, pytest -v.

Any omission of tests or run commands = **incomplete output**.

---

### **4.9 Acceptance Criteria (Definition of Done)**

| **Check** | **Requirement** |
| --- | --- |
| ✅ Ruff lint | No warnings |
| ✅ Tests | ≥70% coverage, all pass |
| ✅ OpenAPI lint | 0 Redocly lint violations |
| ✅ Logs | Include ts, opId, duration_ms |
| ✅ Language | 100% English |
| ✅ i18n | All strings externalized |
| ✅ Performance | P95 ≤ 3 s |
| ✅ PDPA | Fully enforced |
| ✅ CI/CD | Tag → GHCR → Cloud Run verified |

---

## **4.10 Documentation Alignment**

- Operational runbooks in `docs/deployment/ci-pipeline.md`, `docs/deployment/workflow-secrets.md`, `docs/deployment/rollback-playbook.md`, and `docs/deployment/observability.md` describe the actionable steps that implement this Instruction; keep them updated so they mirror these criteria.
- For workflow-level detail, consult `docs/github/workflows/README.md` and the per-workflow docs (`docs/github/workflows/ci.md`, `cd-api.md`, `cd-ocr.md`, `cd-portal.md`) that translate this Instruction directly into GitHub Actions steps.

## **5. Expert Agents — Operational Mindset**

Each AI Expert Agent must act as a domain specialist:

| **Agent** | **Mindset** | **Focus** |
| --- | --- | --- |
| **Mobile Engineer** | UX-first thinker | Smooth capture UX, offline reliability |
| **Backend Engineer** | Schema guardian | Contract stability, latency control |
| **ML Engineer** | Accuracy enforcer | Reproducible model, measurable metrics |
| **Frontend Engineer** | Clarity advocate | Accessibility & error transparency |
| **Infrastructure Engineer** | Minimalist operator | Simplicity, free-tier stability |
| **DevOps Engineer** | Process architect | Continuous testing, release automation |

AI must reason **like these experts collaborating in a single-person workflow**, ensuring clarity, reproducibility, and low operational overhead.

---

## **6. Example Use — /speckit.constitution**

Request pattern for generating development rules or feature specs must ensure:

- **Ruff-based, typed, testable code (English only)**
- **Pytest ≥70% coverage**
- **Instant–Resilient–Clear UX** model
- **Performance P95 ≤3s**, rollback ≤10min
- **PDPA compliance** (consent, masking)
- **CI/CD integrity** (public GitHub, tag-deploy, rollback path)

> AI must return **complete runnable code**, with **tests**, **explanations**, and **clear deployment commands**.
****No placeholder logic, no skipped sections, no untranslated strings.
> 
