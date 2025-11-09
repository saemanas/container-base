#!/usr/bin/env python3
"""Render CI/CD notification emails and archive them as artifacts."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

TEMPLATES: Final[dict[str, str]] = {
    "success": """Subject: [CI/CD][SUCCESS] {service} {environment} run {workflow_run_url}\n"
    "Body:\n"
    "- Service: {service}\n"
    "- Environment: {environment}\n"
    "- Tag/Commit: {ref}\n"
    "- Duration: {duration}\n"
    "- Evidence: {artifact_url}\n""",
    "failure": """Subject: [CI/CD][FAILURE] {service} {environment} run {workflow_run_url}\n"
    "Body:\n"
    "- Failed Stage: {stage_name}\n"
    "- Error Summary: {error_excerpt}\n"
    "- Next Steps: {next_steps}\n"
    "- Evidence: {artifact_url}\n""",
    "rollback": """Subject: [CI/CD][ROLLBACK] {service} {environment} triggered for {rollback_tag}\n"
    "Body:\n"
    "- Triggered By: {initiator}\n"
    "- Rollback Tag: {rollback_tag}\n"
    "- ETA to Completion: ≤10 minutes\n"
    "- Logs: {artifact_url}\n""",
}

DEFAULT_NEXT_STEPS = "Retry job or open incident"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", choices=TEMPLATES.keys(), required=True)
    parser.add_argument("--service", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--duration", required=True)
    parser.add_argument("--artifact-url", required=True, dest="artifact_url")
    parser.add_argument("--workflow-run-url", required=True, dest="workflow_run_url")
    parser.add_argument("--artifact-dir", default="artifacts/notifications", dest="artifact_dir")
    parser.add_argument("--op-id", required=True, dest="op_id")

    parser.add_argument("--stage-name", default="unknown", dest="stage_name")
    parser.add_argument("--error-excerpt", default="See artifact for details", dest="error_excerpt")
    parser.add_argument("--next-steps", default=DEFAULT_NEXT_STEPS, dest="next_steps")
    parser.add_argument("--rollback-tag", default="", dest="rollback_tag")
    parser.add_argument("--initiator", default="automation", dest="initiator")

    return parser.parse_args()


def _load_env() -> tuple[str, str, list[str]]:
    to_addr = os.environ.get("OPS_EMAIL_TO")
    from_addr = os.environ.get("OPS_EMAIL_FROM")
    cc_raw = os.environ.get("OPS_EMAIL_CC", "")

    if not to_addr or not from_addr:
        raise SystemExit("OPS_EMAIL_TO and OPS_EMAIL_FROM environment variables are required")

    cc_addresses = [addr.strip() for addr in cc_raw.split(",") if addr.strip()]
    return to_addr, from_addr, cc_addresses


def _render_email(event: str, context: dict[str, str]) -> str:
    template = TEMPLATES[event]
    return template.format(**context)


def _write_artifact(directory: Path, filename: str, content: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    artifact_path = directory / filename
    artifact_path.write_text(content, encoding="utf-8")
    return artifact_path


def main() -> int:
    args = _parse_args()
    to_addr, from_addr, cc_addresses = _load_env()

    context = {
        "service": args.service,
        "environment": args.environment,
        "ref": args.ref,
        "duration": args.duration,
        "artifact_url": args.artifact_url,
        "workflow_run_url": args.workflow_run_url,
        "stage_name": args.stage_name,
        "error_excerpt": args.error_excerpt,
        "next_steps": args.next_steps,
        "rollback_tag": args.rollback_tag or args.ref,
        "initiator": args.initiator,
    }

    email_body = _render_email(args.event, context)
    headers = [f"From: {from_addr}", f"To: {to_addr}"]
    if cc_addresses:
        headers.append(f"Cc: {', '.join(cc_addresses)}")

    final_content = "\n".join(headers + ["", email_body])

    artifact_dir = Path(args.artifact_dir)
    artifact_filename = f"{args.op_id}-{args.event}.eml"
    artifact_path = _write_artifact(artifact_dir, artifact_filename, final_content)

    now = datetime.now(timezone.utc)
    payload = {
        "ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "opId": args.op_id,
        "code": "ci-email",
        "duration_ms": 0,
        "message": "Notification artifact archived",
        "event": args.event,
        "service": args.service,
        "environment": args.environment,
        "artifact_path": str(artifact_path),
        "workflow_run_url": args.workflow_run_url,
        "to": to_addr,
    }

    print(json.dumps(payload))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    sys.exit(main())
