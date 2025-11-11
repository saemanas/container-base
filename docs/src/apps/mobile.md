# Mobile App (`src/apps/mobile`)

## Summary
Expo + React Native surface that implements the three-tap capture flow, MMKV-backed offline queue, GPS tagging, and LINE Login/credit top-up UX referenced in AGENTS. While the current repo contains only package metadata, the doc notes the intended feature set and required dependencies.

## Structure
- `package-lock.json`: Captures Expo dependency tree; actual app code lives in the mobile directory (currently stubbed for future Expo work).
- `README.md`: Placeholder for mobile-specific guidance (to be filled as features ship).

## Governance touchpoints
- Mobile features must honor the Instant, Resilient, Clear UX triad and i18n requirements (EN/TH states per AGENTS).
- PDPA consent storage, GPS rounding, and XR logging must align with backend/vision guardrails when offline data sync occurs, with offline queue success ≥99%.

## Related docs
- `docs/deployment/workflow-secrets.md` for shared Supabase keys used by mobile builds.
- `docs/deployment/ci-pipeline.md` for CI gating to ensure backend compatibility before mobile releases.
