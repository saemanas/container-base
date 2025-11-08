# CI Pipeline Runbook

## Overview
The CI workflow (`.github/workflows/ci.yml`) enforces the mandated sequence Ruff → ESLint → Pytest → Spectral → Build → GHCR → Tag Deploy across all surfaces while staying within free-tier budgets.

## Stages
1. **Ruff** – Python lint for API and OCR worker using matrix jobs
2. **ESLint** – Portal lint with npm cache and Next.js build cache restore
3. **Pytest** – Test suite execution (future placeholder) for services
4. **Spectral** – OpenAPI contract lint
5. **Build** – Docker image builds for API/OCR via Buildx
6. **GHCR** – Build and push images to GitHub Container Registry (uses `GITHUB_TOKEN`)
7. **Tag Deploy** – Summary/notification step to close the loop

## Required Secrets (GitHub Actions)
- `GHCR_IMAGE_PREFIX` (derived) – uses `ghcr.io/${{ github.repository }}`
- `GITHUB_TOKEN` – default token grants push rights to GHCR
- Optional future secrets: `GCLOUD_SERVICE_ACCOUNT`, `VERCEL_TOKEN`, `SUPABASE_ANON_KEY`

## Common Operations
- **Dry run locally**: `act pull_request -W .github/workflows/ci.yml`
- **Investigate failure**: Inspect the failing job log; re-run selected jobs from GitHub UI if inputs unchanged
- **Upgrade dependencies**: Update `requirements.txt`, `package-lock.json`, re-run `npm install`, and adjust caches as needed

## Troubleshooting
- **Ruff/ESLint failures**: Fix lint issues locally; re-run `ruff check` or `npm run lint`
- **Pytest failures**: Ensure tests import correct modules; mimic pipeline environment with Python 3.12
- **Spectral failures**: Validate OpenAPI contract structure; run `spectral lint` manually
- **Docker build failures**: Confirm Dockerfile path and dependencies; leverage `docker build` locally
- **GHCR push issues**: Ensure repository has GHCR permissions; personal access token may be required for forks
