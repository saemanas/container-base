# Contract Tests (`tests/contract`)

Focus on OpenAPI and CI pipeline ordering contracts enforced before code merges.

| Test | Purpose | Linked Docs |
| --- | --- | --- |
| `test_ci_pipeline_order.py` | Asserts GitHub Actions `ci.yml` jobs run in the mandated order (check_backend → check_portal → check_openapi → build → ghcr → tag_deploy). | Mirrors `refs/docs/CB-Instruction-v1.0.0-en-US.md` §4.7. |
| `test_health_contract.py` | Validates `specs/001-lowcost-cicd-infra/contracts/openapi.yaml` declares `/healthz` and `/readyz`, ensuring health probes stay part of the contract. | Supports OpenAPI lint stage described in `docs/deployment/ci-pipeline.md` and the `docker run tufin/oasdiff:latest diff/breaking` artifacts archived under `artifacts/ci/openapi_lint/`. |

Contract tests run as part of the CI gate when the `check_openapi` job executes Redocly + containerized `oasdiff` commands (`docker run tufin/oasdiff:latest ...`).
