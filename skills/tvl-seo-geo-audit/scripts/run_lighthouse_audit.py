#!/usr/bin/env python3
"""Run a Lighthouse audit when local browser tooling is available."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from collect_seo_evidence import UnsafeUrlError, validate_public_http_url


CATEGORIES = ("performance", "accessibility", "seo")


def not_tested(reason: str) -> dict[str, Any]:
    return {
        "tool": "lighthouse",
        "state": "NOT_TESTED",
        "reason": reason,
        "categories": {category: {"state": "NOT_TESTED", "score": None} for category in CATEGORIES},
    }


def command_for(url: str) -> list[str] | None:
    category_arg = ",".join(CATEGORIES)
    common = [
        url,
        f"--only-categories={category_arg}",
        "--output=json",
        "--quiet",
        "--chrome-flags=--headless=new --no-sandbox",
    ]
    if shutil.which("lighthouse"):
        return ["lighthouse", *common]
    if shutil.which("npx"):
        return ["npx", "--yes", "lighthouse", *common]
    return None


def normalize_report(raw: dict[str, Any]) -> dict[str, Any]:
    categories = {}
    raw_categories = raw.get("categories", {})
    for category in CATEGORIES:
        item = raw_categories.get(category) or {}
        categories[category] = {
            "state": "CONFIRMED" if "score" in item else "NOT_TESTED",
            "score": item.get("score"),
            "title": item.get("title"),
            "audit_refs": len(item.get("auditRefs", [])),
        }
    return {
        "tool": "lighthouse",
        "state": "CONFIRMED",
        "requested_url": raw.get("requestedUrl"),
        "final_url": raw.get("finalUrl"),
        "lighthouse_version": raw.get("lighthouseVersion"),
        "fetch_time": raw.get("fetchTime"),
        "categories": categories,
    }


def run(url: str, timeout: int = 180) -> dict[str, Any]:
    validate_public_http_url(url)
    command = command_for(url)
    if not command:
        return not_tested("Lighthouse CLI and npx are not available")
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return not_tested("Lighthouse timed out")
    if completed.returncode != 0:
        reason = completed.stderr.strip() or completed.stdout.strip() or f"Lighthouse exited with {completed.returncode}"
        return not_tested(reason[:1000])
    try:
        return normalize_report(json.loads(completed.stdout))
    except json.JSONDecodeError as exc:
        return not_tested(f"Lighthouse returned invalid JSON: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Lighthouse performance, accessibility, and SEO checks")
    parser.add_argument("url")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = run(args.url, args.timeout)
    except UnsafeUrlError as exc:
        print(f"Refused URL: {exc}", file=sys.stderr)
        return 2
    data = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(data + "\n", encoding="utf-8")
    else:
        print(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
