#!/usr/bin/env python3
"""Structural checks for tvl-seo-geo-audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RUBRIC = ROOT / "references" / "seo-geo-rubric.md"
CASES = ROOT / "references" / "evaluation-cases.md"
OPENAI = ROOT / "agents" / "openai.yaml"

REQUIRED_TERMS = (
    "technical SEO",
    "generative engine optimization",
    "AI answer visibility",
    "structured data",
    "hreflang",
    "robots.txt",
    "sitemap",
    "canonical",
    "PASS | REVISE | BLOCK",
)

REQUIRED_CHECKS = (
    "HTTP and indexability",
    "Canonical",
    "Sitemap",
    "Robots.txt",
    "Title",
    "Meta description",
    "Structured data",
    "Multilingual SEO",
    "AI answer visibility",
    "Measurement",
)

REQUIRED_SOURCES = (
    "Google Search Central",
    "OpenAI crawler",
    "Perplexity crawler",
    "Anthropic crawler",
)


def test_skill_frontmatter_and_references() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\nname: tvl-seo-geo-audit\n")
    assert "references/seo-geo-rubric.md" in text
    assert "references/evaluation-cases.md" in text
    assert "$tvl-seo-geo-audit" in text


def test_skill_contains_required_terms() -> None:
    text = SKILL.read_text(encoding="utf-8")
    for term in REQUIRED_TERMS:
        assert term in text


def test_rubric_contains_sources_and_checks() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    for source in REQUIRED_SOURCES:
        assert source in text
    for check in REQUIRED_CHECKS:
        assert check in text


def test_rubric_contains_evidence_labels() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    for label in ("CONFIRMED", "REFUTED", "NOT-FOUND", "UNVERIFIABLE", "MISLEADING"):
        assert label in text


def test_evaluation_cases_cover_verdicts() -> None:
    text = CASES.read_text(encoding="utf-8")
    for case in (
        "Indexable But Overlong Metadata",
        "Wrong Canonical on Multilingual Page",
        "GEO Claim Without Measurement",
        "Deceptive Structured Data",
        "AI Answer Visibility Improvement",
        "Good Page With Clear Limits",
    ):
        assert case in text
    for verdict in ("Verdict: `PASS`", "Verdict: `REVISE`", "Verdict: `BLOCK`"):
        assert verdict in text


def test_openai_metadata_matches_skill() -> None:
    text = OPENAI.read_text(encoding="utf-8")
    assert "TVL SEO GEO Audit" in text
    assert "$tvl-seo-geo-audit" in text


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_references,
        test_skill_contains_required_terms,
        test_rubric_contains_sources_and_checks,
        test_rubric_contains_evidence_labels,
        test_evaluation_cases_cover_verdicts,
        test_openai_metadata_matches_skill,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} SEO GEO audit checks passed")
