#!/usr/bin/env python3
"""Assess free-tier quota usage for Cloud Run, Supabase, and Vercel.

The script accepts an optional JSON file describing current usage metrics:
[
  {"service": "Cloud Run", "metric": "API CPU seconds", "used": 120000, "limit": 360000},
  {"service": "Supabase", "metric": "Row reads", "used": 3200000, "limit": 4000000}
]

If no file is supplied, baseline sample data is used. The script prints a JSON
summary to stdout and, when `--append` is provided, appends a markdown table to
`docs/deployment/observability.md`.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
OBS_DOC = ROOT_DIR / "docs" / "deployment" / "observability.md"


@dataclass(frozen=True)
class Quota:
    """Represents a single quota metric."""

    service: str
    metric: str
    used: float
    limit: float

    @property
    def percent(self) -> float:
        if self.limit == 0:
            return 0.0
        return round((self.used / self.limit) * 100, 2)

    @property
    def status(self) -> str:
        if self.percent >= 100:
            return "exceeded"
        if self.percent >= 90:
            return "critical"
        if self.percent >= 80:
            return "warning"
        return "ok"

    def to_dict(self) -> dict[str, float | str]:
        return {
            "service": self.service,
            "metric": self.metric,
            "used": self.used,
            "limit": self.limit,
            "percent": self.percent,
            "status": self.status,
        }


DEFAULT_DATA: Sequence[dict[str, float | str]] = (
    {"service": "Cloud Run", "metric": "API CPU seconds", "used": 0, "limit": 360000},
    {"service": "Cloud Run", "metric": "OCR CPU seconds", "used": 0, "limit": 360000},
    {"service": "Supabase", "metric": "Row reads", "used": 0, "limit": 4000000},
    {"service": "Supabase", "metric": "Storage GB", "used": 0, "limit": 8},
    {"service": "Vercel", "metric": "Build minutes", "used": 0, "limit": 100},
)


def load_usage(path: Path | None) -> List[Quota]:
    data: Iterable[dict[str, float | str]]
    if path is None:
        data = DEFAULT_DATA
    else:
        with path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        if not isinstance(raw, list):
            raise ValueError("Usage file must contain a JSON array")
        data = raw

    quotas: List[Quota] = []
    for item in data:
        try:
            quota = Quota(
                service=str(item["service"]),
                metric=str(item["metric"]),
                used=float(item["used"]),
                limit=float(item["limit"]),
            )
        except (KeyError, TypeError, ValueError) as exc:  # pragma: no cover - defensive
            raise ValueError(f"Invalid quota entry: {item}") from exc
        quotas.append(quota)
    return quotas


def append_markdown(quotas: Sequence[Quota]) -> None:
    timestamp = datetime.utcnow().isoformat()
    rows = ["| Service | Metric | Used | Limit | % | Status |", "| --- | --- | --- | --- | --- | --- |"]
    for quota in quotas:
        rows.append(
            f"| {quota.service} | {quota.metric} | {quota.used:.2f} | {quota.limit:.2f} | {quota.percent:.2f}% | {quota.status} |"
        )

    OBS_DOC.parent.mkdir(parents=True, exist_ok=True)
    with OBS_DOC.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## Free-tier Check ({timestamp})\n\n")
        handle.write("\n".join(rows))
        handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize free-tier quota usage")
    parser.add_argument("--source", type=Path, default=None, help="JSON file containing quota usage data")
    parser.add_argument("--append", action="store_true", help="Append a markdown summary to observability doc")
    args = parser.parse_args()

    quotas = load_usage(args.source)
    summary = [quota.to_dict() for quota in quotas]
    json.dump({"generated_at": datetime.utcnow().isoformat(), "quotas": summary}, fp=sys.stdout)
    sys.stdout.write("\n")

    if args.append:
        append_markdown(quotas)


if __name__ == "__main__":
    main()
