#!/usr/bin/env python3
"""Verify SEO/GEO candidate findings against evidence records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID_STATES = {"CONFIRMED", "REFUTED", "NOT_FOUND", "NOT_TESTED", "MISSING_TEST", "UNVERIFIABLE", "MISLEADING"}
VALID_ORIGINS = {"MEASURED", "USER_PROVIDED", "INFERRED"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
CORE_CHECKS = {"http.status", "robots_meta", "x_robots_tag", "canonical", "indexation_intent"}


def evidence_index(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = payload.get("evidence_records") or payload.get("evidence", {}).get("evidence_records") or []
    return {record.get("id"): record for record in records if record.get("id")}


def suppress(reason: str, finding: dict[str, Any]) -> dict[str, Any]:
    return {"reason": reason, "finding": finding}


def verify_findings(payload: dict[str, Any]) -> dict[str, Any]:
    records = evidence_index(payload)
    mode = payload.get("manifest", {}).get("audit_mode") or payload.get("audit_mode", "PAGE")
    findings = payload.get("findings", [])
    verified: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []
    seen_root_causes: set[tuple[str, str, str]] = set()
    result_by_check_location: dict[tuple[str, str], set[str]] = {}

    required_fields = {
        "id",
        "check_id",
        "priority",
        "area",
        "result",
        "evidence_state",
        "origin",
        "evidence_refs",
        "location",
        "evidence",
        "impact",
        "fix",
        "verification",
        "effort",
    }

    for finding in findings:
        missing = sorted(field for field in required_fields if not finding.get(field))
        if missing:
            suppressed.append(suppress(f"missing required fields: {', '.join(missing)}", finding))
            continue
        if finding["priority"] not in VALID_PRIORITIES:
            suppressed.append(suppress("invalid priority", finding))
            continue
        if finding["evidence_state"] not in VALID_STATES:
            suppressed.append(suppress("invalid evidence state", finding))
            continue
        if finding["origin"] not in VALID_ORIGINS:
            suppressed.append(suppress("invalid evidence origin", finding))
            continue
        refs = finding.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            suppressed.append(suppress("missing evidence refs", finding))
            continue
        missing_refs = [ref for ref in refs if ref not in records]
        if missing_refs:
            suppressed.append(suppress(f"evidence refs not found: {', '.join(missing_refs)}", finding))
            continue
        if mode == "PAGE" and finding.get("scope") == "sitewide":
            suppressed.append(suppress("sitewide conclusion from PAGE mode", finding))
            continue
        if finding["evidence_state"] in {"NOT_TESTED", "MISSING_TEST", "UNVERIFIABLE"} and finding["result"] == "PASS":
            suppressed.append(suppress("cannot PASS an unverified check", finding))
            continue
        if not finding.get("verification"):
            suppressed.append(suppress("fix lacks verification method", finding))
            continue

        root_key = (
            finding.get("root_cause") or finding["check_id"],
            finding["location"],
            finding.get("blocker_category") or "",
        )
        if root_key in seen_root_causes:
            suppressed.append(suppress("duplicate root cause", finding))
            continue
        seen_root_causes.add(root_key)

        check_key = (finding["check_id"], finding["location"])
        result_by_check_location.setdefault(check_key, set()).add(finding["result"])
        verified.append(finding)

    contradictory_keys = {
        key for key, results in result_by_check_location.items() if "PASS" in results and ("BLOCK" in results or "REVISE" in results)
    }
    if contradictory_keys:
        next_verified = []
        for finding in verified:
            key = (finding["check_id"], finding["location"])
            if key in contradictory_keys:
                suppressed.append(suppress("contradictory result for same check and URL", finding))
            else:
                next_verified.append(finding)
        verified = next_verified

    core_verified = 0
    core_applicable = 0
    for check in CORE_CHECKS:
        record = records.get(check)
        if record:
            core_applicable += 1
            if record.get("state") in {"CONFIRMED", "NOT_FOUND"}:
                core_verified += 1

    any_p0 = any(f["priority"] == "P0" for f in verified)
    any_p1 = any(f["priority"] == "P1" for f in verified)
    missing_core = any(
        records.get(check, {}).get("state") in {"NOT_TESTED", "MISSING_TEST", "UNVERIFIABLE"} for check in CORE_CHECKS if records.get(check)
    )
    if any_p0:
        verdict = "BLOCK"
    elif any_p1 or missing_core:
        verdict = "REVISE"
    else:
        verdict = "PASS"

    confidence = "HIGH" if core_applicable and core_verified == core_applicable and not suppressed else "MEDIUM"
    if core_applicable and core_verified < max(1, core_applicable // 2):
        confidence = "LOW"

    return {
        "manifest": payload.get("manifest", {}),
        "verdict": verdict,
        "confidence": confidence,
        "evidence_coverage": {"verified": core_verified, "applicable": core_applicable},
        "verified_findings": verified,
        "suppressed_findings": suppressed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify SEO/GEO findings")
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = verify_findings(payload)
    data = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(data + "\n", encoding="utf-8")
    else:
        print(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
