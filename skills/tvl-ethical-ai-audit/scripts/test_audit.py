#!/usr/bin/env python3
"""Structural + behavioral checks for tvl-ethical-ai-audit."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RUBRIC = ROOT / "references" / "ethicalai-rubric.md"
CALIBRATION = ROOT / "references" / "calibration-notes.md"
CASES = ROOT / "references" / "evaluation-cases.md"
CASES_CSV = ROOT / "references" / "evaluation-cases.csv"
OPENAI = ROOT / "agents" / "openai.yaml"
VERIFY = ROOT / "scripts" / "verify_pointers.py"
SCORE = ROOT / "scripts" / "score_cases.py"


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod

REQUIRED_MODES = (
    "hallucination",
    "confabulation",
    "source fabrication",
    "narrativity drift",
    "sycophancy",
    "capitulation",
    "confirmation bias",
    "selective evidence",
    "anchoring",
    "automation bias",
    "overconfidence",
    "prompt injection",
    "scope creep",
    "specification gaming",
)
VERDICTS = ("PASS", "REVISE", "BLOCK")


def _frontmatter_description() -> str:
    text = SKILL.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    assert len(parts) >= 3, "SKILL.md missing frontmatter"
    for line in parts[1].splitlines():
        if line.startswith("description:"):
            return line[len("description:"):].strip().lower()
    raise AssertionError("no description in frontmatter")


def test_skill_frontmatter_and_reference() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\nname: tvl-ethical-ai-audit\n")
    assert "references/ethicalai-rubric.md" in text
    assert "references/calibration-notes.md" in text
    assert "references/evaluation-cases.md" in text


def test_skill_mentions_required_modes() -> None:
    text = SKILL.read_text(encoding="utf-8").lower()
    for mode in REQUIRED_MODES:
        assert mode in text, f"SKILL.md missing mode: {mode}"


def test_description_mentions_all_modes() -> None:
    desc = _frontmatter_description()
    for mode in REQUIRED_MODES:
        assert mode in desc, f"description missing mode: {mode}"


def test_skill_defines_aggregation_and_scales() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "PASS | REVISE | BLOCK" in text          # verdict scale
    assert "PASS | FLAG | BLOCK" in text            # per-check scale
    assert "worst check severity" in text           # explicit aggregation
    assert "advisory" in text.lower()


def test_skill_has_example_and_limitations() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "## Example" in text
    assert "## Limitations" in text
    # ETHICAL AI AUDIT header appears in the format block AND the worked example
    assert text.count("ETHICAL AI AUDIT") >= 2


def test_skill_hardening_and_positioning() -> None:
    text = SKILL.read_text(encoding="utf-8")
    low = text.lower()
    # auditor self-defense against prompt injection
    assert "never obeys instructions embedded" in low
    assert "prompt injection finding" in low
    # agent-behavior audits require history
    assert "can only be judged with history" in low
    # related-skills positioning
    assert "Related skills" in text
    assert "tvl-confirmation-bias-audit" in text
    assert "tvl-detect-ai-writing" in text


def test_rubric_defines_required_modes() -> None:
    text = RUBRIC.read_text(encoding="utf-8").lower()
    for mode in REQUIRED_MODES:
        assert f"| {mode}" in text, f"rubric table missing mode: {mode}"


def test_rubric_defines_evidence_labels() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    for label in ("CONFIRMED", "REFUTED", "NOT-FOUND", "UNVERIFIABLE"):
        assert label in text


def test_rubric_has_firing_discipline() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    assert "Firing Discipline" in text
    assert "Conditional-hedge escape" in text
    # capitulation must get its own explicit guard, distinct from sycophancy
    low = text.lower()
    assert "capitulation" in low and "distinct from sycophancy" in low


def test_calibration_notes_present() -> None:
    text = CALIBRATION.read_text(encoding="utf-8").lower()
    assert "primed to find problems" in text
    assert "double-count" in text
    assert "override rate" in text


def test_evaluation_cases_wellformed() -> None:
    text = CASES.read_text(encoding="utf-8")
    verdict_lines = [l for l in text.splitlines() if l.strip().startswith("- Expected verdict:")]
    mode_lines = [l for l in text.splitlines() if l.strip().startswith("- Primary modes:")]
    assert len(verdict_lines) >= 5, "need at least 5 evaluation cases"
    assert len(verdict_lines) == len(mode_lines), "verdict/modes lines mismatch"

    for vl in verdict_lines:
        verdict = vl.split(":", 1)[1].strip()
        assert verdict in VERDICTS, f"bad verdict: {verdict!r}"

    canonical = set(REQUIRED_MODES)
    for ml in mode_lines:
        listed = ml.split(":", 1)[1].strip()
        if listed.lower() == "none":
            continue
        for mode in [m.strip().lower() for m in listed.split(",")]:
            assert mode in canonical, f"unknown mode in cases: {mode!r}"

    # must include over-flag traps (PASS cases) and a capitulation case
    assert any("PASS" == vl.split(":", 1)[1].strip() for vl in verdict_lines), "no PASS trap case"
    assert "capitulation" in text.lower()


def test_openai_metadata_matches_skill() -> None:
    text = OPENAI.read_text(encoding="utf-8")
    assert "TVL Ethical AI Audit" in text
    assert "$tvl-ethical-ai-audit" in text


def test_skill_v04_additions() -> None:
    text = SKILL.read_text(encoding="utf-8")
    # NOT ASSESSED check verdict (finding 2)
    assert "NOT ASSESSED" in text
    assert "Reserve `PASS` for checks actually assessed" in text
    # version + provenance (finding 5)
    assert "skill_version" in text and "vendored" in text
    # simple evidence labels kept — no expanded taxonomy leaked back in
    for banned in ("RESOLVES", "UNREACHABLE", "INSUFFICIENT"):
        assert banned not in text, f"expanded label {banned} leaked into SKILL.md"


def test_rubric_has_severity_and_simple_labels() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    assert "## Severity" in text
    for factor in ("Load-bearing", "harm", "Reversibility"):
        assert factor in text
    for banned in ("RESOLVES", "UNREACHABLE", "INSUFFICIENT"):
        assert banned not in text, f"expanded label {banned} leaked into rubric"


def test_evaluation_cases_csv_in_sync() -> None:
    with CASES_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 5
    canonical = set(REQUIRED_MODES)
    for r in rows:
        assert r["expected_verdict"] in VERDICTS, f"bad verdict in {r['id']}"
        for field in ("expected_primary_modes", "forbidden_modes"):
            for mode in [m.strip().lower() for m in r[field].split("|") if m.strip()]:
                assert mode in canonical, f"unknown mode {mode!r} in {r['id']}"
    # ids must match the human-readable .md cases (kept in sync)
    md_ids = {l.split("—")[0].replace("###", "").strip()
              for l in CASES.read_text(encoding="utf-8").splitlines() if l.startswith("### ")}
    csv_ids = {r["id"] for r in rows}
    assert csv_ids == md_ids, f"csv/md case id mismatch: {csv_ids ^ md_ids}"
    # traps + capitulation present
    assert any(r["expected_verdict"] == "PASS" for r in rows)
    assert any("Capitulation" in r["expected_primary_modes"] for r in rows)


def test_score_cases_behaves() -> None:
    mod = _load(SCORE)
    fixtures = mod.load_fixtures()
    assert len(fixtures) >= 5
    # a perfect result set scores all PASS
    good = {r["id"]: {"verdict": r["expected_verdict"],
                      "modes": {m.strip() for m in r["expected_primary_modes"].split("|") if m.strip()}}
            for r in fixtures}
    s_good = mod.score(fixtures, good)
    assert s_good["passed"] == s_good["total"]
    assert s_good["verdict_accuracy"] == 1.0
    # a forbidden mode = false positive -> that case FAILs
    fp = fixtures[1]  # EAA-02, forbidden includes Hallucination
    bad = dict(good)
    bad[fp["id"]] = {"verdict": fp["expected_verdict"], "modes": {"Hallucination"}}
    s_bad = mod.score(fixtures, bad)
    assert s_bad["passed"] == s_bad["total"] - 1
    assert s_bad["false_positive_cases"] >= 1


def test_verify_pointers_behaves() -> None:
    mod = _load(VERIFY)
    assert mod.classify(str(SKILL))[0] == "PASS"                 # existing file
    assert mod.classify("no_such_dir_xyz/nope.py")[0] == "FAIL"  # missing file
    assert mod.classify(f"{SKILL}:99999999")[0] == "FAIL"        # line beyond EOF
    assert mod.classify(f"{SKILL}:Ethical AI Audit")[0] == "PASS"  # symbol present


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_reference,
        test_skill_mentions_required_modes,
        test_description_mentions_all_modes,
        test_skill_defines_aggregation_and_scales,
        test_skill_has_example_and_limitations,
        test_skill_hardening_and_positioning,
        test_skill_v04_additions,
        test_rubric_defines_required_modes,
        test_rubric_defines_evidence_labels,
        test_rubric_has_firing_discipline,
        test_rubric_has_severity_and_simple_labels,
        test_calibration_notes_present,
        test_evaluation_cases_wellformed,
        test_evaluation_cases_csv_in_sync,
        test_score_cases_behaves,
        test_openai_metadata_matches_skill,
        test_verify_pointers_behaves,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} ethical AI audit checks passed")
