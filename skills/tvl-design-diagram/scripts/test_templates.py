#!/usr/bin/env python3
"""Structural checks for tvl-design-diagram templates."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "templates.md"
ETHICAL_CHECK = ROOT / "references" / "ethical-ai-check.md"
SKILL = ROOT / "SKILL.md"


def test_templates_reference_three_named_templates() -> None:
    text = TEMPLATES.read_text(encoding="utf-8")
    for name in ("system-map", "workflow", "decision-flow"):
        assert f"## {name}" in text


def test_each_template_has_mermaid_starter() -> None:
    text = TEMPLATES.read_text(encoding="utf-8")
    assert text.count("```mermaid") == 3
    assert text.count("Quality check:") == 3


def test_skill_points_to_template_reference() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "references/templates.md" in text
    assert "references/ethical-ai-check.md" in text
    assert "PASS" in text
    assert "FLAG" in text
    assert "BLOCK" in text


def test_ethical_check_covers_required_failure_modes() -> None:
    text = ETHICAL_CHECK.read_text(encoding="utf-8").lower()
    for mode in (
        "hallucination",
        "confabulation",
        "sycophancy",
        "confirmation bias",
        "source fabrication",
        "prompt injection",
        "selective evidence",
        "anchoring",
        "overconfidence",
    ):
        assert mode in text


if __name__ == "__main__":
    tests = [
        test_templates_reference_three_named_templates,
        test_each_template_has_mermaid_starter,
        test_skill_points_to_template_reference,
        test_ethical_check_covers_required_failure_modes,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} template checks passed")
