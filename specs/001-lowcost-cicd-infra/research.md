# Phase 0 Research: Low-cost CI/CD & Infra Skeleton

## Decisions & Rationale

### Deployment approvals
- **Decision**: Staging auto deploys; production requires manual approval.
- **Rationale**: Keeps experimentation fast on staging while preventing accidental production releases.
- **Alternatives**: Fully automated prod deploys (rejected due to risk); manual gating for both environments (rejected for slowing feedback).

### Supabase environment strategy
- **Decision**: Single Supabase project with environment-specific tables and RLS policies.
- **Rationale**: Minimizes cost and operational overhead while satisfying PDPA isolation via policy-level controls.
- **Alternatives**: Separate Supabase projects per environment (higher cost, duplicated setup); defer environment separation decision (delays compliance).

### Cloud Run concurrency
- **Decision**: Concurrency capped at 5 requests per instance for API and OCR services.
- **Rationale**: Balances cold-start latency, throughput, and free-tier CPU allocation, simplifying cost forecasts.
- **Alternatives**: Concurrency 1 (high latency), 10+ (risk of CPU throttling, unstable response times).

## Best Practices

- GitHub Actions pipeline order remains Ruff → ESLint → Pytest → Spectral → Build → GHCR push → Tag deploy.
- Secrets managed exclusively via GitHub/Vercel/Cloud Run environment variables with `.env.example` placeholders.
- Health checks: `/healthz` for liveness, `/readyz` for DB/model readiness; enforce MAX_IMAGE_MB, TIMEOUT_MS.
- Logging schema `{ts, opId, code, duration_ms}` across services; capture metrics for API p95, OCR failure rate, Cloud Run quota usage.
- Cost guardrails monitored via Cloud Run usage dashboards, Supabase quotas, and Vercel build minutes.
