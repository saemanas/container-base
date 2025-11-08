# **CB Plan: Photo Recognition–Based Container Management Service (Target: Thailand Market)**

**Version:** v1.0.0

## **1. Core Concept**

> “A smart on-site solution that automatically recognizes container numbers and conditions from photos.”
> 

In Thailand’s ports, factories, warehouses, and logistics companies,

many still share photos via LINE and manually record information.

**Container Base (CB)** replaces this inefficiency with AI-driven automation.

When users upload a photo, container numbers and conditions are automatically recognized, recorded, and searchable — with self-managed AI versioning, zero-ops CI/CD, and data-driven billing policies ensuring sustainable low-cost operation.

---

## **2. Why Target the Thai Market First**

| **Factor** | **Details** |
| --- | --- |
| 📍 **Geographic Hub** | Thailand is Southeast Asia’s logistics center — Laem Chabang, Bangkok Port, Songkhla, etc. |
| 🚚 **High Ground Logistics Demand** | Truck-based logistics, strong need for site-level tracking. |
| 🧾 **Low Digitalization** | Excel/LINE-based workflows → major efficiency gains from OCR automation. |
| 💬 **User Behavior** | Mobile + LINE oriented → accustomed to “app + notification” workflows. |
| 🏗️ **Operational Structure** | SMEs in logistics, warehouses, and factories → easier SaaS adoption. |
| 💵 **Cost Sensitivity** | Prefer pay-per-use (credit system) over monthly subscriptions. |

---

## **3. Thai Market Strategy**

**🇹🇭 Localization Factors**

| **Area** | **Localization Content** |
| --- | --- |
| **Language** | Thai / English bilingual support |
| **Payments** | PromptPay, LINE Pay |
| **Notification Channels** | LINE Notify + Webhooks |
| **Mapping Service** | OpenStreetMap + automatic GPS logging |
| **Timezone/Units** | UTC+7 (Asia/Bangkok) |
| **Legal Compliance** | PDPA (Thailand) adherence |
| **Server Location** | Supabase (Singapore Region) + Cloudflare Functions |

---

## **4. Organization-Based Structure (Including Access Control)**

| **Level** | **Role** | **Example** |
| --- | --- | --- |
| **Organization** | Logistics/factory-level entity | “Bangkok Logistics Co., Ltd.” |
| **Site** | Actual work site | “Laem Chabang Yard #1” |
| **Admin** | Site manager | Approvals / staff invitations / reporting |
| **Operator** | Worker uploading photos | Recognizes and logs container states |
| **Viewer** | Read-only user | Customer-facing portal access |

### **🔐 Login & Access Control**

- Supports LINE Login / Email Login (Supabase Auth)
- JWT + Refresh token management
- Guest mode (demo) using local storage
- RLS (Row-Level Security) limits access by Org/Site

---

## **5. Feature Summary (Thailand MVP Scope)**

| **Category** | **Feature** | **Description** |
| --- | --- | --- |
| Core | **📸 Photo Recognition** | Detect container number, check digit, and condition |
| Core | **📍 GPS Auto Logging** | Store location + timestamp on capture |
| Core | **🗂️ Container Timeline** | Track inbound/outbound, damage, and movement |
| Management | **👥 User/Org Management** | Admin approval, role-based access |
| Management | **📊 Statistics** | Daily throughput, damage frequency |
| Add-on | **🔔 LINE Alerts** | Push notifications for completion or anomalies |
| Add-on | **🧾 CSV/Excel Export** | Auto-generate reports for accounting |
| Add-on | **🧠 AI Model Versioning Dashboard** | Visualize and manage deployed AI model versions, accuracy metrics, and rollback triggers |

---

## **6. MVP Tech Stack (Thailand Infrastructure Focus)**

| **Area** | **Technology** | **Description** |
| --- | --- | --- |
| **Mobile App** | React Native (Expo) | Offline queue + AsyncStorage |
| **Backend API** | FastAPI (Python) | Serverless deployment on Supabase Functions |
| **Database** | Supabase (Postgres + RLS) | Integrated auth/storage/policy stack |
| **Storage** | Supabase Storage | Image buckets + lifecycle (14 days → thumbnail retention) |
| **AI Vision** | YOLOv8 + PaddleOCR | Detection + text recognition |
| **AI Lifecycle** | /models/<version>/model.yaml + /vision/config/ab.yaml | Self-versioning + A/B validation + rollback on degradation |
| **Infra** | Cloudflare Functions / Pages | Serverless API & Portal hosting |
| **CI/CD** | GitHub Actions + Release Drafter + Auto Rollback | Canary window (10m) → rollback ≤10m; full automation loop |
| **Monitoring** | Grafana Cloud + Sentry | SLA, latency, and AI accuracy tracing |
| **Payment** | PromptPay + LINE Pay | Thai payment standards |
| **Billing Contracts** | /billing/usage, /billing/events, /audit/logs | Event-based metering + API credits ledger |
| **Alerting** | LINE Notify / Email | Real-time admin alerts |

---

## **7. Business Model (Thailand)**

| **Tier** | **Description** |
| --- | --- |
| **Free Tier** | Up to 100 tasks/month free (with ads) |
| **Pro Tier** | 1,000 tasks/month for 990฿ |
| **Enterprise Tier** | API integration / unlimited / custom pricing |
| **Add-on** | Damage detection AI, automated alert workflows, and model analytics dashboard (paid add-ons) |

---

## **8. On-Site Scenarios (Thailand)**

| **Location** | **Scenario** |
| --- | --- |
| **Port (Laem Chabang)** | Capture at gate → auto recognition + record |
| **Warehouse (Samut Prakan)** | Workers capture photos via app → manager approves and commits data |
| **Carrier (Bang Na)** | Drivers capture during transit → auto location update |
| **Factory (Rayong)** | Internal container inspections for maintenance tracking |

---

## **9. KPI (Thailand Initial Validation)**

| **Metric** | **Target** |
| --- | --- |
| **Recognition Accuracy (FPRR)** | ≥ 90% |
| **Average Processing Time (P95)** | ≤ 3s |
| **1-Month Retention Rate** | ≥ 60% |
| **Manager Satisfaction** | ≥ 4.5 / 5 |
| **Monthly Active Containers** | ≥ 1,000 / month |
| **Model Accuracy Deviation (Δ%)** | ≤ 3% between versions |
| **Rollback MTTR** | ≤ 10m (auto rollback on degraded model performance) |

---

## **10. KPI & SLA Monitoring**

| **Metric** | **Target** | **Tool** |
| --- | --- | --- |
| **P95 Latency** | ≤ 3s | Grafana Dashboard |
| **AI Recognition Rate** | ≥ 90% | Sentry Trace + Metrics |
| **Error Rate** | ≤ 1% | JSON log-based |
| **Availability** | ≥ 99.5% | Uptime + Alert Webhook |
| **Backup Frequency** | 1/day | Supabase Scheduled Job |
| **Auto Rollback** | ≤ 10m | GitHub Actions Canary Monitor |
| **Billing Accuracy** | 100% | /billing/audit validation jobs |

---

## **11. Thailand PDPA & Billing Compliance**

| **Category** | **Policy** |
| --- | --- |
| **Consent for Personal Data** | /docs/SECURITY.md#consent-template |
| **Retention Period** | 12 months (auto deletion) |
| **Sensitive Data Masking** | Round GPS coordinates, keep email domain only |
| **Access Control** | RBAC + RLS, AuditLog tracking |
| **Data Contract for Billing** | Event-based metering contracts between /billing/events and /audit/logs |
| **Compliance Automation** | Auto flag PDPA violations via Sentry rule “SEC-PDPA-ALERT” |

---

## **12. Global Expansion Roadmap**

| **Phase** | **Region** | **Goal** |
| --- | --- | --- |
| Phase 1 | **🇹🇭 Thailand** | MVP commercialization, PoC with logistics firms/ports |
| Phase 2 | **🇻🇳 Vietnam / 🇮🇩 Indonesia** | Expansion to similar environments |
| Phase 3 | **🌏 Global** | English UI, AWS Global CDN |
| Phase 4 | **🧠 Global AI Ops** | Unified AI lifecycle + multilingual OCR model auto-training pipeline |

---

## **13. Summary**

| **Category** | **Details** |
| --- | --- |
| **Core Concept** | Photo recognition–based container management with self-managed AI lifecycle |
| **Market Focus** | 🇹🇭 Thailand (mobile/LINE-centric users) |
| **Tech Stack** | React Native · FastAPI · Supabase · YOLOv8/PaddleOCR |
| **Security/Auth** | RLS + JWT + LINE Login |
| **Automation Upgrades** | AI model version control, auto CI/CD rollback, event-based billing contracts |
| **Core Values** | Automation · Reliability · Self-healing Ops · Cost-efficiency |
| **Performance Goals** | FPRR ≥ 90% / P95 ≤ 3s / Rollback ≤ 10m |
| **Operational Strategy** | Zero-Server · Fully-Automated CI/CD · Billing Transparency |
| **Expansion Vision** | Southeast Asia → Global SaaS platform with autonomous AI lifecycle |
