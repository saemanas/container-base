#!/usr/bin/env python3
"""Measure HTTP latency for Container Base services.

Example usage::

    python scripts/measure-latency.py \
        --url https://api.container-base.com/readyz \
        --url https://ocr.container-base.com/readyz \
        --iterations 5 --append

The script prints a JSON summary to stdout and, when ``--append`` is supplied,
adds a markdown table to ``docs/deployment/cost-guardrails.md``.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT_DIR = Path(__file__).resolve().parents[1]
COST_DOC = ROOT_DIR / "docs" / "deployment" / "cost-guardrails.md"
DEFAULT_ENDPOINTS = (
    "https://api.container-base.com/readyz",
    "https://ocr.container-base.com/readyz",
)


@dataclass(slots=True)
class ProbeStats:
    url: str
    iterations: int
    successes: int
    failures: int
    latency_ms: List[float] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)

    def summary(self) -> dict[str, Any]:
        percentiles = self._percentiles(self.latency_ms)
        return {
            "url": self.url,
            "iterations": self.iterations,
            "successes": self.successes,
            "failures": self.failures,
            "min_ms": percentiles.get("min"),
            "avg_ms": percentiles.get("avg"),
            "p95_ms": percentiles.get("p95"),
            "max_ms": percentiles.get("max"),
            "errors": self.error_messages,
        }

    @staticmethod
    def _percentiles(latencies: Sequence[float]) -> dict[str, Optional[float]]:
        if not latencies:
            return {key: None for key in ("min", "avg", "p95", "max")}

        sorted_data = sorted(latencies)
        p95_index = int(round(0.95 * (len(sorted_data) - 1)))
        return {
            "min": round(sorted_data[0], 2),
            "avg": round(statistics.mean(sorted_data), 2),
            "p95": round(sorted_data[p95_index], 2),
            "max": round(sorted_data[-1], 2),
        }


def probe(url: str, iterations: int, timeout: float) -> ProbeStats:
    stats = ProbeStats(url=url, iterations=iterations, successes=0, failures=0)

    for _ in range(iterations):
        start_ns = time.perf_counter_ns()
        request = Request(url, method="GET")
        try:
            with urlopen(request, timeout=timeout) as response:
                response.read()
                status_code = response.status
        except HTTPError as exc:  # pragma: no cover - network error depends on env
            stats.failures += 1
            stats.error_messages.append(f"HTTPError {exc.code}: {exc.reason}")
            continue
        except URLError as exc:  # pragma: no cover - network error depends on env
            stats.failures += 1
            stats.error_messages.append(f"URLError: {exc.reason}")
            continue
        except Exception as exc:  # pragma: no cover - defensive
            stats.failures += 1
            stats.error_messages.append(f"Unexpected error: {exc!r}")
            continue

        end_ns = time.perf_counter_ns()
        elapsed_ms = (end_ns - start_ns) / 1_000_000
        stats.successes += 1
        stats.latency_ms.append(elapsed_ms)
        if status_code >= 400:
            stats.error_messages.append(f"Status {status_code}")
    return stats


def append_markdown(results: Iterable[ProbeStats]) -> None:
    timestamp = datetime.utcnow().isoformat()
    rows = ["| Endpoint | Iterations | Success | P95 (ms) | Max (ms) | Notes |", "| --- | --- | --- | --- | --- | --- |"]
    for result in results:
        summary = result.summary()
        notes = ", ".join(result.error_messages) if result.error_messages else "-"
        rows.append(
            "| {url} | {iters} | {succ}/{iters} | {p95} | {max} | {notes} |".format(
                url=summary["url"],
                iters=summary["iterations"],
                succ=summary["successes"],
                p95=summary["p95_ms"] if summary["p95_ms"] is not None else "n/a",
                max=summary["max_ms"] if summary["max_ms"] is not None else "n/a",
                notes=notes,
            )
        )

    COST_DOC.parent.mkdir(parents=True, exist_ok=True)
    with COST_DOC.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## Latency Probe ({timestamp})\n\n")
        handle.write("\n".join(rows))
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure HTTP latency for Container Base services")
    parser.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="Endpoint to probe (may be supplied multiple times). Defaults to readyz endpoints.",
    )
    parser.add_argument("--iterations", type=int, default=3, help="Number of requests per URL (default: 3)")
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds (default: 5.0)")
    parser.add_argument("--append", action="store_true", help="Append markdown summary to cost-guardrails doc")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    urls: Sequence[str] = tuple(args.urls) if args.urls else DEFAULT_ENDPOINTS

    results: List[ProbeStats] = []
    for url in urls:
        stats = probe(url=url, iterations=args.iterations, timeout=args.timeout)
        results.append(stats)

    payload = {
        "generated_at": datetime.utcnow().isoformat(),
        "iterations": args.iterations,
        "timeout": args.timeout,
        "results": [result.summary() for result in results],
    }
    json.dump(payload, fp=sys.stdout)
    sys.stdout.write("\n")

    if args.append:
        append_markdown(results)


if __name__ == "main__":  # pragma: no cover - sanity guard
    raise SystemExit("Use `python scripts/measure-latency.py` to run the probe")

if __name__ == "__main__":
    main()
