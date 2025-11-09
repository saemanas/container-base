# **📘 CB MVP Specs (User Stories Only)**

**Version:** v1.0.0

**Actors:**

- **Operator (Field Staff)** – captures container images, performs recognition, uploads data, and retries failed tasks
- **Admin (Reviewer / Operator)** – reviews uploaded recognition results, approves or rejects tasks, and monitors progress

**Scope:** MVP (Minimum Viable Product)

**Languages:** English / Thai supported

**Note:** PDPA compliance required

**Canonical Statuses:** queued, under_review, approved, rejected

---

## **🧍‍♂️ Actor A: Operator (Field Staff)**

### **Epic A1 – Login and PDPA Consent**

**US-OP-001 (P1)**

- The Operator must agree to the PDPA (Personal Data Protection Act) consent before using the app for the first time.
    
    After giving consent, the user signs in through **SSO (e.g., LINE)** to obtain identity and authorization.
    
- **Why:** To ensure legal compliance and standardized user identification.
- **Acceptance Hints:**
    - Given a new user, When launching the app, Then the PDPA consent and “Agree” button are displayed.
    - When the user agrees and logs in, Then an authentication token is issued and automatic login is maintained thereafter.

---

### **Epic A2 – Container Capture and Auto Recognition**

**US-OP-002 (P1)**

- The Operator captures a photo of a container using a mobile device, and the system automatically recognizes and records the container number and check digit.
    
    The timestamp and GPS location at capture are stored together.
    
- **Why:** To reduce manual input errors and improve data accuracy.
- **Acceptance Hints:**
    - Given camera access granted, When a photo is taken, Then the number and check digit are automatically extracted and displayed on screen.
    - If recognition fails, the user receives immediate feedback (“Recognition failed – retry available”).

---

**US-OP-003 (P1)**

- The Operator can continue working in areas with poor network connectivity by saving photos and recognition data locally.
    
    When the connection is restored, the data is automatically synchronized with the server.
    
- **Why:** To ensure continuous operations in ports or yards with unstable networks.
- **Acceptance Hints:**
    - Given an offline state, When capturing and saving, Then data remains in a local queue.
    - When the connection is restored, Then the queue automatically syncs with the server and status changes from queued to under_review.

---

**US-OP-004 (P1)**

- The Operator can view the current status of captured, transmitted, and reviewed tasks in real time through the “My Timeline” screen.
- **Why:** To track progress and determine whether rework is needed.
- **Acceptance Hints:**
    - Given a logged-in user, When opening the timeline, Then tasks are listed in order of most recent capture.
    - Each task is clearly shown in one of the four statuses: queued, under_review, approved, or rejected.

---

### **Epic A3 – Recognition Failure Handling and Retry**

**US-OP-005 (P2)**

- The Operator can press a “Retry” button to resend a failed OCR recognition request or manually upload another image if necessary.
- **Why:** To reduce failed recognitions and allow field users to correct issues before review.
- **Acceptance Hints:**
    - Given a failed task (rejected), When “Retry” is clicked, Then a new OCR request is sent.
    - When a new image is uploaded, Then the previous task entry updates and its status changes to under_review.

---

### **Epic A4 – Reliability and Quality Tracking**

**US-OP-006 (P2)**

- The Operator app should minimize interruptions, upload failures, or crashes.
    
    The system automatically collects such event data and provides quality statistics.
    
- **Why:** To measure service reliability and identify improvement metrics.
- **Acceptance Hints:**
    - The app logs offline queue failure rates and crash events internally.
    - The management portal can later display summary metrics based on this data (for future integration).

---

## **🧑‍💼 Actor B: Admin (Reviewer / Operator)**

### **Epic B1 – Login and PDPA Consent**

**US-AD-001 (P1)**

- The Admin must agree to the PDPA consent before using the web portal.
    
    After giving consent, the user signs in through **SSO (e.g., LINE)** for authentication and authorization.
    
- **Why:** To ensure legal compliance and standardized user identification.
- **Acceptance Hints:**
    - Given a new user, When launching the portal, Then PDPA consent and “Agree” button are displayed.
    - When the user agrees and logs in, Then an authentication token is issued and automatic login is maintained thereafter.

---

### **Epic B2 – Review and Approval / Rejection Management**

**US-AD-002 (P1)**

- The Admin reviews the uploaded container recognition results in the web portal and can approve or reject each task.
- **Why:** To maintain data quality and return incorrect results for rework.
- **Acceptance Hints:**
    - Given a logged-in Admin, When opening the list, Then tasks are displayed by status (queued, under_review, approved, rejected).
    - When “Approve” is clicked, Then the status changes to approved and is reflected in the Operator’s timeline.

---

**US-AD-003 (P1)**

- The Admin can export all task records as a CSV file for use in external systems or client reports.
- **Why:** To support integrations with client systems and automate reporting.
- **Acceptance Hints:**
    - When “Export CSV” is clicked, Then a file is generated and downloaded according to the applied filters.
    - The CSV header must include consistent field names: container_id, check_digit, status, captured_at, location.

---

### **Epic B3 – Operational Dashboard**

**US-AD-004 (P2)**

- The Admin can view summary KPIs such as processed count, approval rate, and failure rate by time period in a dashboard.
- **Why:** To improve operational efficiency and quickly identify bottlenecks.
- **Acceptance Hints:**
    - Given a selected time range, When “Search” is clicked, Then main KPIs (completed count, failure rate, etc.) are displayed as cards.
    - Metrics shown in the dashboard must match the CSV export data exactly.

---

## **⚙️ Summary Table**

| **Actor** | **Epic** | **Story ID** | **Priority** | **Core Value** |
| --- | --- | --- | --- | --- |
| Operator | A1. Login/PDPA | US-OP-001 | P1 | Legal and secure authentication |
| Operator | A2. Capture/Recognition | US-OP-002 | P1 | Automated container number recognition |
| Operator | A3. Offline Handling | US-OP-003 | P1 | Offline save and auto-sync |
| Operator | A4. Timeline | US-OP-004 | P1 | Personal work tracking |
| Operator | A5. Retry | US-OP-005 | P2 | Failed task reprocessing |
| Operator | A6. Quality Stats | US-OP-006 | P2 | Service reliability metrics |
| Admin | B1. Login/PDPA | US-AD-001 | P1 | Legal and secure authentication |
| Admin | B2. Review | US-AD-002 | P1 | Approval/Rejection management |
| Admin | B3. Export | US-AD-003 | P1 | Data export to CSV |
| Admin | B4. Dashboard | US-AD-004 | P2 | Operational efficiency tracking |