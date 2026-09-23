#!/usr/bin/env python3
"""score_cases.py — score audit runs against the evaluation fixtures.

The fixtures (references/evaluation-cases.csv) are labeled cases with an
expected verdict and expected/forbidden modes. Behavioral scoring needs an LLM
to actually run the skill, so this harness is run in the loop:

  1. An agent/human audits each case's `draft` with the skill.
  2. Record results as CSV: `id,verdict,modes` (modes pipe-separated), e.g.
        EAA-01,BLOCK,Source fabrication|Overconfidence
  3. Run:  python3 score_cases.py results.csv
     -> per-case PASS/FAIL + accuracy, false-positive rate, missed-mode count.

With no results file it just prints the fixtures and these instructions.

A case scores PASS when: verdict matches, every expected primary mode is
present, and no forbidden mode appears (a forbidden mode = a false positive).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "references" / "evaluation-cases.csv"


def _modes(field: str) -> set[str]:
    return {m.strip() for m in field.split("|") if m.strip()}


def load_fixtures(path: Path = FIXTURES) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_results(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[row["id"]] = {"verdict": row.get("verdict", "").strip(), "modes": _modes(row.get("modes", ""))}
    return out


def score(fixtures: list[dict], results: dict[str, dict]) -> dict:
    """Return a summary dict. Each case is PASS or FAIL."""
    cases = []
    for fx in fixtures:
        cid = fx["id"]
        res = results.get(cid)
        expected = fx["expected_verdict"].strip()
        primary = _modes(fx["expected_primary_modes"])
        forbidden = _modes(fx["forbidden_modes"])
        if res is None:
            cases.append({"id": cid, "result": "FAIL", "reasons": ["no result supplied"]})
            continue
        reasons = []
        if res["verdict"] != expected:
            reasons.append(f"verdict {res['verdict'] or '∅'} != {expected}")
        missing = primary - res["modes"]
        if missing:
            reasons.append("missing primary: " + ", ".join(sorted(missing)))
        false_pos = forbidden & res["modes"]
        if false_pos:
            reasons.append("false positive: " + ", ".join(sorted(false_pos)))
        cases.append({"id": cid, "result": "PASS" if not reasons else "FAIL", "reasons": reasons})

    passed = sum(1 for c in cases if c["result"] == "PASS")
    verdict_ok = sum(
        1 for fx in fixtures
        if (r := results.get(fx["id"])) and r["verdict"] == fx["expected_verdict"].strip()
    )
    false_pos_cases = sum(
        1 for fx in fixtures
        if (r := results.get(fx["id"])) and (_modes(fx["forbidden_modes"]) & r["modes"])
    )
    n = len(fixtures)
    return {
        "total": n,
        "passed": passed,
        "verdict_accuracy": round(verdict_ok / n, 3) if n else 0.0,
        "false_positive_cases": false_pos_cases,
        "cases": cases,
    }


def main(argv: list[str]) -> int:
    fixtures = load_fixtures()
    if not argv:
        print(__doc__)
        print(f"\n{len(fixtures)} fixtures in {FIXTURES.name}:")
        for fx in fixtures:
            print(f"  {fx['id']}: expect {fx['expected_verdict']:<6} "
                  f"primary=[{fx['expected_primary_modes']}] forbidden=[{fx['forbidden_modes']}]")
        print("\nProduce results.csv (id,verdict,modes) then: python3 score_cases.py results.csv")
        return 0

    summary = score(fixtures, load_results(Path(argv[0])))
    for c in summary["cases"]:
        tail = "" if c["result"] == "PASS" else "  — " + "; ".join(c["reasons"])
        print(f"  {c['id']}: {c['result']}{tail}")
    print(f"\n{summary['passed']}/{summary['total']} cases PASS | "
          f"verdict accuracy {summary['verdict_accuracy']:.0%} | "
          f"false-positive cases {summary['false_positive_cases']}")
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
