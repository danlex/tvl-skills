#!/usr/bin/env python3
"""Structural checks for tvl-ethical-ai-judge."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RUBRIC = ROOT / "references" / "ethicalai-rubric.md"
OPENAI = ROOT / "agents" / "openai.yaml"

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


def test_skill_frontmatter_and_reference() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\nname: tvl-ethical-ai-judge\n")
    assert "references/ethicalai-rubric.md" in text
    assert "PASS | REVISE | BLOCK" in text


def test_skill_mentions_required_modes() -> None:
    text = SKILL.read_text(encoding="utf-8").lower()
    for mode in REQUIRED_MODES:
        assert mode in text


def test_rubric_defines_required_modes() -> None:
    text = RUBRIC.read_text(encoding="utf-8").lower()
    for mode in REQUIRED_MODES:
        assert f"| {mode}" in text


def test_rubric_defines_evidence_labels() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    for label in ("CONFIRMED", "REFUTED", "NOT-FOUND", "UNVERIFIABLE"):
        assert label in text


def test_openai_metadata_matches_skill() -> None:
    text = OPENAI.read_text(encoding="utf-8")
    assert "TVL Ethical AI Judge" in text
    assert "$tvl-ethical-ai-judge" in text


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_reference,
        test_skill_mentions_required_modes,
        test_rubric_defines_required_modes,
        test_rubric_defines_evidence_labels,
        test_openai_metadata_matches_skill,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} ethical AI judge checks passed")
