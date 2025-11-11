# Portal Web App (`src/apps/portal`)

## Summary
Next.js 16 + React 19 administrative portal built with shadcn/ui and TanStack Query. It renders EN/TH status assets, mirrors the UX triad (Empty, Loading, Success, Error, Offline states), and surfaces release/observability information to operations users.

## Structure
- `package.json` / `node_modules`: Portal uses Next.js App Router, with dependencies pinned to the mandated stack to satisfy `check-portal-stack.py`.
- `components/`: Shared UI primitives, including status and telemetry cards, follow the shadcn/ui theming tokens described in AGENTS.
- `public/deploy-status/en.json` + `th.json`: Static assets populated during deployment to show release readiness per environment and used by `cd-portal.yml`.

## Governance touchpoints
- CI workflow runs `npm run lint` followed by `scripts/check-portal-stack.py` to ensure Next.js 16 / React 19 alignment.
- `docs/deployment/ci-pipeline.md` documents the portal job, including Node caching, stack guard, and build/test artifact upload.
- Observability docs reference this portal deployment path to track EN/TH deploy statuses and manual verification steps.

## Deployment
- Vercel deployment simulated in `cd-portal.yml`; actual `VERCEL_*` secrets and overrides live in `docs/deployment/workflow-secrets.md`.
- Cloudflare purge uses `CLOUDFLARE_ZONE_ID_PORTAL`, and readiness probes ensure backend is available before building.

## Related docs
- `docs/deployment/ci-pipeline.md` (CI steps)
- `docs/deployment/workflow-secrets.md` (portal secrets)
- `docs/deployment/observability.md` (portal readiness entry)
