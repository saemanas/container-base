# `check-portal-stack.py`

## Purpose
Prevent portal regressions to unsupported stacks by verifying `src/apps/portal/package.json` locks Next.js 16 / React 19 (as required in AGENTS portal stack section).

## Behavior
- Loads dependencies + devDependencies from the portal package and extracts numeric majors.
- Ensures `next`, `react`, and `react-dom` are present and their major versions equal `16`, `19`, `19` respectively.
- Prints GitHub Action-style `::error::` messages if versions drift and exits non-zero, failing the pipeline immediately.

## Usage
Run directly in CI (after ESLint) or locally when updating portal dependencies:

```
python scripts/check-portal-stack.py
```

## Compliance Linkage
- Documented as part of `docs/deployment/ci-pipeline.md` portal stack guard step.
- Supports `refs/docs/CB-MVP-Stacks-v1.0.0-en-US.md` requirement for Next.js 16.0.1 + React 19.0.0.

