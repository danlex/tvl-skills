#!/usr/bin/env python3
"""Structural and behavioral checks for tvl-detect-ai-writing."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
PATTERNS = ROOT / "references" / "ai-writing-patterns.md"
CALIBRATION = ROOT / "references" / "calibration-notes.md"
CASES = ROOT / "references" / "evaluation-cases.md"
OPENAI = ROOT / "agents" / "openai.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
import scan_ai_patterns as scanner  # noqa: E402

REQUIRED_TERMS = (
    "Pattern Score",
    "Negative correction",
    "Focal-word lexicon",
    "reply mode",
    "combination",
    "0-2",
    "9-10",
    "Highlighted Text",
    "Validation Check",
)


def test_skill_frontmatter_and_references() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\nname: tvl-detect-ai-writing\n")
    assert "references/ai-writing-patterns.md" in text
    assert "references/calibration-notes.md" in text
    assert "references/evaluation-cases.md" in text
    assert "$tvl-detect-ai-writing" in text
    assert "scripts/scan_ai_patterns.py" in text


def test_skill_contains_report_contract() -> None:
    text = SKILL.read_text(encoding="utf-8")
    for term in REQUIRED_TERMS:
        assert term in text, f"missing required term: {term}"


def test_references_present() -> None:
    for path in (PATTERNS, CALIBRATION, CASES):
        assert path.exists(), f"missing reference: {path.name}"
    patterns = PATTERNS.read_text(encoding="utf-8")
    assert "Detection taxonomy" in patterns
    assert "Reply-mode patterns" in patterns
    calibration = CALIBRATION.read_text(encoding="utf-8")
    assert "Combination-required scoring" in calibration
    assert "Length gate" in calibration


def test_openai_metadata_matches_skill() -> None:
    text = OPENAI.read_text(encoding="utf-8")
    assert "TVL Detect AI Writing" in text
    assert "$tvl-detect-ai-writing" in text


def test_scanner_flags_templated_post() -> None:
    sample = (
        "Most teams still treat evaluation as an afterthought.\n"
        "It is not about speed, it is about trust. Moreover, this delves into "
        "the intricate realm of governance. #AI #Leadership"
    )
    findings = {f.name for f in scanner.scan(sample, "post")}
    assert "Generic-paradigm opener" in findings
    assert "Negative correction (pure-negation)" in findings
    assert "Focal-word lexicon" in findings
    assert "Hashtags" in findings


def test_scanner_passes_clean_post() -> None:
    sample = (
        "The model reached 71.2 on GSM8K after we removed contaminated splits. "
        "In my experience the gain shrinks once you control for leakage, so I "
        "read the headline number with some caution."
    )
    findings = scanner.scan(sample, "post")
    assert findings == [], f"unexpected findings: {[f.name for f in findings]}"


def test_scanner_reply_affirmation() -> None:
    sample = "Absolutely, great point. This really underscores the shift."
    findings = {f.name for f in scanner.scan(sample, "reply")}
    assert "Affirmation opener (reply)" in findings


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_references,
        test_skill_contains_report_contract,
        test_references_present,
        test_openai_metadata_matches_skill,
        test_scanner_flags_templated_post,
        test_scanner_passes_clean_post,
        test_scanner_reply_affirmation,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} detect-ai-writing checks passed")
