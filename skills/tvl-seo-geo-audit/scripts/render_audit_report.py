#!/usr/bin/env python3
"""Render a Markdown SEO/GEO audit report from verified findings JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def render_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return lines


def render_report(payload: dict[str, Any]) -> str:
    manifest = payload.get("manifest", {})
    coverage = payload.get("evidence_coverage", {})
    findings = payload.get("verified_findings", [])
    suppressed = payload.get("suppressed_findings", [])
    blocker_categories = sorted({f.get("blocker_category") for f in findings if f.get("blocker_category")}) or ["none"]

    lines = [
        "# SEO GEO AUDIT",
        "",
        "## Scope",
        f"- Mode: {manifest.get('audit_mode', 'unknown')}",
        f"- Requested URL: {manifest.get('requested_url', 'unknown')}",
        f"- Final URL: {manifest.get('final_url', 'unknown')}",
        f"- Audit timestamp: {manifest.get('retrieval_timestamp', 'unknown')}",
        f"- Sample selection: {manifest.get('selected_sample', [])}",
        f"- Environment limitations: {manifest.get('limitations', [])}",
        "",
        "## Verdict",
        f"- Result: {payload.get('verdict', 'unknown')}",
        f"- Confidence: {payload.get('confidence', 'unknown')}",
        f"- Evidence coverage: {coverage.get('verified', 0)} of {coverage.get('applicable', 0)} core checks verified",
        f"- Blocker categories: {', '.join(blocker_categories)}",
        "",
        "## Findings",
    ]
    if findings:
        rows = [
            [
                f.get("id"),
                f.get("priority"),
                f.get("area"),
                f.get("result"),
                f.get("evidence_state"),
                f.get("origin"),
                f.get("location"),
                f.get("evidence"),
                f.get("impact"),
                f.get("fix"),
                f.get("verification"),
                f.get("effort"),
            ]
            for f in findings
        ]
        lines.extend(render_table(["ID", "Priority", "Area", "Result", "Evidence state", "Origin", "Location", "Evidence", "Impact", "Fix", "Verification", "Effort"], rows))
    else:
        lines.append("No verified findings.")

    lines.extend(["", "## Suppressed Findings"])
    if suppressed:
        rows = [[item.get("reason"), item.get("finding", {}).get("id", "unknown")] for item in suppressed]
        lines.extend(render_table(["Reason", "Finding"], rows))
    else:
        lines.append("None.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render SEO/GEO audit report")
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = render_report(payload)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
