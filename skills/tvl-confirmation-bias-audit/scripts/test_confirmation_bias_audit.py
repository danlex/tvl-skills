#!/usr/bin/env python3
"""Structural checks for tvl-confirmation-bias-audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RUBRIC = ROOT / "references" / "confirmation-bias-rubric.md"
CHATBOT_CASES = ROOT / "references" / "chatbot-evaluation-cases.md"
OPENAI = ROOT / "agents" / "openai.yaml"

REQUIRED_TERMS = (
    "confirmation bias",
    "alternative hypothesis",
    "falsification",
    "one-sided",
    "PASS | REVISE | BLOCK",
    "SUPPORTING",
    "DISCONFIRMING",
    "MISSING-TEST",
    "AMBIGUOUS",
)

REQUIRED_SOURCES = (
    "EthicalAI",
    "Nickerson",
    "Wason",
    "Klayman",
    "Wan",
    "Jhaveri",
    "Mitropoulos",
    "Du",
    "Lopez-Lopez",
    "Cheng",
    "Shu",
    "Alessa",
    "Pilli",
    "Sharma",
    "Nehring",
    "Jacob",
    "de Jong",
    "Nicholls",
)

REQUIRED_CHATBOT_USE_CASES = (
    "Interpersonal advice",
    "Health information seeking",
    "Belief or delusion reinforcement",
    "Political or historical explanation",
    "Conversational search or factual lookup",
    "Shopping or product recommendation",
    "Conversational decision support",
    "Security or code-review chatbot",
    "Customer support or incident triage",
    "Legal, HR, or finance advice",
)


def test_skill_frontmatter_and_reference() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\nname: tvl-confirmation-bias-audit\n")
    assert "references/confirmation-bias-rubric.md" in text
    assert "references/chatbot-evaluation-cases.md" in text
    assert "$tvl-confirmation-bias-audit" in text


def test_skill_contains_audit_contract() -> None:
    text = SKILL.read_text(encoding="utf-8")
    for term in REQUIRED_TERMS:
        assert term in text


def test_rubric_contains_research_basis() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    for source in REQUIRED_SOURCES:
        assert source in text


def test_rubric_contains_required_checks() -> None:
    text = RUBRIC.read_text(encoding="utf-8").lower()
    for check in (
        "alternative stated",
        "alternative tested",
        "search direction balanced",
        "disconfirming evidence included",
        "ambiguous evidence interpreted fairly",
        "certainty calibrated",
        "framing resisted",
    ):
        assert check in text


def test_rubric_contains_chatbot_use_cases() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    assert "## Chatbot Use Cases" in text
    assert "## Chatbot-Specific Signals" in text
    assert "## Chatbot Audit Modes" in text
    assert "## Minimum Counter-Checks by Domain" in text
    for use_case in REQUIRED_CHATBOT_USE_CASES:
        assert use_case in text


def test_chatbot_evaluation_cases_cover_verdicts() -> None:
    text = CHATBOT_CASES.read_text(encoding="utf-8")
    for case in (
        "Interpersonal Advice Validation",
        "Health Self-Diagnosis",
        "Product Recommendation Summary",
        "Security Code Review Framing",
        "Political or Historical Framing",
        "Belief Reinforcement in Long Dialogue",
        "Customer Support Root Cause",
    ):
        assert case in text
    assert text.count("Verdict: `BLOCK`") >= 4
    assert "Verdict: `REVISE`" in text


def test_openai_metadata_matches_skill() -> None:
    text = OPENAI.read_text(encoding="utf-8")
    assert "TVL Confirmation Bias Audit" in text
    assert "$tvl-confirmation-bias-audit" in text


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_reference,
        test_skill_contains_audit_contract,
        test_rubric_contains_research_basis,
        test_rubric_contains_required_checks,
        test_rubric_contains_chatbot_use_cases,
        test_chatbot_evaluation_cases_cover_verdicts,
        test_openai_metadata_matches_skill,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} confirmation bias audit checks passed")
