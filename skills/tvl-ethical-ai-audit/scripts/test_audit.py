#!/usr/bin/env python3
"""Structural + behavioral checks for tvl-ethical-ai-audit."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RUBRIC = ROOT / "references" / "ethicalai-rubric.md"
CALIBRATION = ROOT / "references" / "calibration-notes.md"
CASES = ROOT / "references" / "evaluation-cases.md"
OPENAI = ROOT / "agents" / "openai.yaml"
VERIFY = ROOT / "scripts" / "verify_pointers.py"

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


def test_verify_pointers_behaves() -> None:
    spec = importlib.util.spec_from_file_location("verify_pointers", VERIFY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    # existing file -> CONFIRMED
    assert mod.classify(str(SKILL))[0] == "CONFIRMED"
    # missing file -> NOT-FOUND
    assert mod.classify("no_such_dir_xyz/nope.py")[0] == "NOT-FOUND"
    # line beyond EOF -> NOT-FOUND
    assert mod.classify(f"{SKILL}:99999999")[0] == "NOT-FOUND"
    # symbol present -> CONFIRMED
    assert mod.classify(f"{SKILL}:Ethical AI Audit")[0] == "CONFIRMED"


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_reference,
        test_skill_mentions_required_modes,
        test_description_mentions_all_modes,
        test_skill_defines_aggregation_and_scales,
        test_skill_has_example_and_limitations,
        test_skill_hardening_and_positioning,
        test_rubric_defines_required_modes,
        test_rubric_defines_evidence_labels,
        test_rubric_has_firing_discipline,
        test_calibration_notes_present,
        test_evaluation_cases_wellformed,
        test_openai_metadata_matches_skill,
        test_verify_pointers_behaves,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} ethical AI audit checks passed")
