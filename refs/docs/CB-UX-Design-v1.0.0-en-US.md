# **CB MVP UX Wireframe Specification**

**Version:** v1.0.0 (Aligned with CB MVP Specs & MiniOps)

**Purpose:** Define core user flows and screen layout hierarchy for MVP implementation (Android-first).

---

## **1. UX Philosophy — “Three Taps and Done.”**

| **Principle** | **Definition** | **UX Enforcement** |
| --- | --- | --- |
| **Instantness** | A record is created the moment the photo is taken. | One-tap capture + auto OCR + inline preview. |
| **Resilience** | Works offline, syncs automatically later. | Local queue module, sync badge on Timeline. |
| **Clarity** | User always knows task state. | Unified chips: queued, under_review, approved, rejected. |

---

## **2. Information Architecture**

```
src/
 ├─ apps/
 │   ├─ mobile/
 │   │   ├─ screens/
 │   │   │   ├─ Auth/
 │   │   │   ├─ Capture/
 │   │   │   ├─ Review/
 │   │   │   ├─ Timeline/
 │   │   │   ├─ TaskDetail/
 │   │   │   └─ Settings/
 │   │   ├─ components/
 │   │   │   ├─ StatusChip.tsx
 │   │   │   ├─ PDPAConsent.tsx
 │   │   │   ├─ QueueBadge.tsx
 │   │   │   └─ OfflineBanner.tsx
 │   │   └─ hooks/
 │   │       └─ useOfflineQueue.ts
```

Each screen must map **1:1** to a **User Story** in the spec.

---

## **3. Wireframe Overview**

### **A. Operator App (Expo / Android)**

### **1️⃣ Auth Screen**

**Purpose:** PDPA consent + SSO login.

**Elements:**

- Logo + App Title
- PDPA modal (scrollable)
- “Agree & Continue” button (primary)
- SSO button (generic: *“Sign in with SSO”*)
- Legal links: Privacy Policy / Terms

**Interactions:**

- Tapping “Agree” → enables login.
- Login success → routes to /capture.

---

### **2️⃣ Capture Screen**

**Purpose:** Take or pick photo, attach GPS automatically.

**Elements:**

- Camera viewport (live feed)
- Shutter button (center bottom)
- Gallery pick icon (bottom left)
- GPS indicator (bottom right)
- Toast feedback: “Saved offline / Uploaded successfully.”

**States:**

- Online: instant upload → status = under_review.
- Offline: save locally → badge queued.

---

### **3️⃣ Review Screen**

**Purpose:** Review recognized text before submission.

**Elements:**

- Image thumbnail
- OCR extracted fields:
    - Container number
    - Check digit
- “Confirm” (primary) / “Retry OCR” (secondary)
- Toast: “Processing OCR…”

**Interactions:**

- Retry triggers local OCR pipeline or remote call.

---

### **4️⃣ Timeline Screen**

**Purpose:** Show all tasks in order of capture.

**Elements:**

- Tabs or filters: All / Failed / Synced
- Cards: thumbnail + number + status chip
- Status chips:
    - 🟡 queued
    - 🔵 under_review
    - 🟢 approved
    - 🔴 rejected
- Pull-to-refresh + infinite scroll.

**Interactions:**

- Tap card → /task/:id.
- Swipe left → “Retry upload.”

---

### **5️⃣ Task Detail Screen**

**Purpose:** View metadata for one job.

**Elements:**

- Full-size image
- OCR results
- GPS map pin (static)
- History timeline
- Buttons: “Retry OCR” (if rejected), “Close”

---

### **6️⃣ Settings Screen**

**Purpose:** Manage language, PDPA, and offline queue.

**Elements:**

- Language toggle (EN/TH)
- Offline queue list + “Sync now” button
- PDPA consent record
- Logout

---

### **B. Admin Portal (Next.js / Web)**

### **1️⃣ Login Screen**

**Purpose:** PDPA consent + SSO (same flow as Operator).

**Elements:**

- App logo + title
- PDPA checkbox
- SSO Login button
- “Proceed to Portal”

---

### **2️⃣ Review Dashboard**

**Purpose:** Central review interface.

**Elements:**

- Top nav: Filters (status, date range)
- List table: thumbnail | container ID | check digit | status | date | reviewer
- Row actions: Approve / Reject
- Status color map identical to mobile chips.

---

### **3️⃣ Task Detail Modal**

**Purpose:** Review and validate a single entry.

**Elements:**

- Large image viewer
- OCR text fields
- Approve / Reject buttons
- Metadata sidebar (timestamp, GPS, uploader)

---

### **4️⃣ Export View**

**Purpose:** Download CSV reports.

**Elements:**

- Date filter, Status filter
- Button: “Export CSV”
- Confirmation toast: “File generated.”
- Headers: container_id, check_digit, status, captured_at, location

---

### **5️⃣ Dashboard (Summary View)**

**Purpose:** Show KPI cards and trend chart.

**Elements:**

- KPI cards: Total Tasks, Approval Rate, Failure Rate
- Bar chart (by date range)
- Export button → CSV

---

## **4. Shared Components**

| **Component** | **Used In** | **Function** |
| --- | --- | --- |
| **StatusChip** | Timeline / Admin table | Visual indicator for canonical status |
| **OfflineBanner** | All mobile screens | Warns user of offline mode |
| **QueueBadge** | Capture / Timeline | Displays queued count |
| **PDPAConsent** | Auth / Settings | Handles PDPA modal interaction |

---

## **5. Color & Style System**

| **Element** | **Color** | **Note** |
| --- | --- | --- |
| Primary (Action) | #007AFF | Buttons, chips |
| Secondary | #E0E0E0 | Neutral elements |
| Status – queued | #F9A825 (amber) | Waiting to sync |
| Status – under_review | #1E88E5 (blue) | Processing |
| Status – approved | #43A047 (green) | Success |
| Status – rejected | #E53935 (red) | Failed |
| Background | #FAFAFA | App body |
| Font | Roboto / Noto Sans Thai | Consistent across locales |

---

## **6. Interaction Map**

```
[Auth] → [Capture]
        ↓
     [Review] → [Timeline]
        ↓            ↓
  (Offline?) ───────> [Queue Sync]
        ↓
     [Task Detail]
        ↓
   [Settings / Logout]
```

---

## **7. Accessibility & PDPA UX Rules**

- Minimum tap target: 48×48px
- Font size ≥ 16px
- Status colors must pass WCAG AA contrast ratio
- PDPA consent required before accessing /capture
- Mask personal identifiers in logs and exports

---

## **8. UX Metrics**

| **Metric** | **Target** | **Description** |
| --- | --- | --- |
| Capture → Upload latency | ≤ 30s | average time from photo to server record |
| Offline queue recovery | ≥ 99% | successful retries |
| Review action delay | ≤ 10min | mean admin response time |
| PDPA compliance | 100% | all users must consent before login |

---

## **9. Wireframe Deliverables (Figma Layers)**

| **Frame Name** | **Type** | **Linked Spec** |
| --- | --- | --- |
| 01_Auth | Mobile / Portal | US-OP-001 / US-AD-001 |
| 02_Capture | Mobile | US-OP-002 |
| 03_Review | Mobile | US-OP-002 / US-OP-005 |
| 04_Timeline | Mobile | US-OP-004 |
| 05_TaskDetail | Mobile | US-OP-005 |
| 06_Settings | Mobile | US-OP-006 |
| 07_Admin_Review | Web | US-AD-002 |
| 08_Admin_Export | Web | US-AD-003 |
| 09_Admin_Dashboard | Web | US-AD-004 |

Each frame should include **status chips**, **toast feedback**, and **offline states** matching the canonical status design.