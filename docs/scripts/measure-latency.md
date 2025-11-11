# `measure-latency.py`

## Purpose
Probe Container Base HTTP endpoints, capture latency percentiles, and optionally append the results to `docs/deployment/cost-guardrails.md` for SLA monitoring (backend P95 ≤3s budget).

## Behavior
- Iterates each endpoint for the configured number of `--iterations`, tracking successes/failures, latency list, and error messages.
- Prints a JSON report with summary stats such as min/avg/p95/max and error notes.
- With `--append`, appends a markdown table describing each endpoint to `docs/deployment/cost-guardrails.md`.

## Inputs
- `--url`: can be provided multiple times; defaults to `https://api.container-base.com/readyz` and `https://ocr.container-base.com/readyz`.
- `--iterations`: number of requests per endpoint (default 3).
- `--timeout`: request timeout seconds (default 5.0).
- `--append`: append findings to the cost guardrail doc.

## Notes
- Useful before releases or after observing CI latency regressions; the appended sections include timestamped headings for traceability.

