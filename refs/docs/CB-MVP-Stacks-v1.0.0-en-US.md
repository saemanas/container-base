# MVP Stacks (Essential + Simplified + Free)

## Runtime Baselines (LTS first)
- **Python**: 3.12.x (LTS) – confirmed compatible with FastAPI 0.121.0, Pydantic 2.12.4, SQLModel 0.0.27, Supabase 2.23.2, Ultralytics 8.3.225, paddlepaddle 3.2.1, paddlepaddle-gpu 2.6.2, paddleocr 3.3.1 (paddleocr ships `py3-none-any`).
- **Node.js**: 22.21.1 LTS “Jod” – officially supported by Next.js 16.x (`>=18.17`), shadcn/ui, TanStack Query 5.x, Expo CLI 54.x. Node 24.11.0 LTS “Krypton” exists but Expo/Next.js have not yet declared formal support; revisit after vendor release notes update.

## Stack Components
- **Mobile (Expo SDK 52)**
  - Expo `54.0.22`, React Native `0.76.3`, React `18.3.1`.
  - State/Data: `@tanstack/react-query 5.90.7`, `react-native-mmkv 2.13.x`.
  - Auth: LINE Login via `expo-auth-session 5.4.x`.
- **API**
  - FastAPI `0.121.0`, Pydantic `2.12.4`, SQLModel `0.0.27`.
  - ASGI stack: `uvicorn[standard] 0.32.x`, `httpx 0.27.x`.
  - Supabase client `supabase 2.23.2`, JWT handling via `python-jose`.
- **Vision Worker**
  - YOLOv8 with `ultralytics 8.3.225` (bundles PyTorch 2.9.0 wheels for Python 3.12).
  - PaddleOCR `3.3.1` with `paddlepaddle 3.2.1` (CPU) or `paddlepaddle-gpu 2.6.2` (GPU, ensure CUDA match).
  - Served via FastAPI worker sharing tooling with core API.
- **Portal**
  - Next.js `16.0.1` (App Router), React `19.0.0`, React DOM `19.0.0`.
  - UI kit: `shadcn/ui` (Radix UI `1.1.x`), Tailwind CSS `3.4.x`, data layer `@tanstack/react-query 5.90.7`.
  - Tooling: TypeScript `5.6.x`, ESLint `9.x`, Prettier `3.x`.
- **Infra & Delivery**
  - GitHub (public repo), GHCR for container images.
  - Deployment targets: Cloudflare (DNS/edge), Cloud Run / Render / Fly.io (choose per workload).
  - Docker Engine ≥26 with Compose v2.29+ to leverage BuildKit and bake workflows.

## CI/CD Expectations
- GitHub Actions (Free tier) with runners on Python 3.12 & Node 22 LTS.
- Pipelines: Ruff `0.7.x`, ESLint `9.x`, Pytest, Redocly CLI `2.11.x` (OpenAPI lint), Docker smoke tests, tag-triggered deploy.
- Auto OpenAPI client generation via `scripts/generate-client.sh` on schema diff.

## Later (post-MVP hardening)
- Playwright E2E suites, k6 performance tests, Trivy fail-gate, SBOM/Cosign signing, Dark mode, Email reset flows.
