#!/usr/bin/env python3
"""Structural checks for tvl-build-free-website."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
RUBRIC = ROOT / "references" / "github-pages-rubric.md"
BLUEPRINTS = ROOT / "references" / "site-blueprints.md"
OPENAI = ROOT / "agents" / "openai.yaml"

REQUIRED_TERMS = (
    "GitHub Pages",
    "static website",
    "public",
    "index.html",
    ".nojekyll",
    "GitHub Actions",
    "PASS",
    "REVISE",
    "BLOCK",
)

REQUIRED_BLUEPRINTS = (
    "one-page-service",
    "portfolio-projects",
    "documentation-hub",
)

REQUIRED_OFFICIAL_SOURCES = (
    "docs.github.com/articles/creating-project-pages-manually",
    "configuring-a-publishing-source-for-your-github-pages-site",
    "github-pages-limits",
)


def test_skill_frontmatter_and_references() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\nname: tvl-build-free-website\n")
    assert "references/github-pages-rubric.md" in text
    assert "references/site-blueprints.md" in text
    assert "$tvl-build-free-website" in text


def test_skill_contains_deployment_contract() -> None:
    text = SKILL.read_text(encoding="utf-8")
    for term in REQUIRED_TERMS:
        assert term in text
    lower_text = text.lower()
    for phrase in (
        "HTTP `200`",
        "No secrets",
        "Repository is public",
        "asset paths",
    ):
        assert phrase.lower() in lower_text


def test_rubric_contains_github_pages_modes_and_limits() -> None:
    text = RUBRIC.read_text(encoding="utf-8")
    for source in REQUIRED_OFFICIAL_SOURCES:
        assert source in text
    for phrase in (
        "Branch deploy",
        "GitHub Actions deploy",
        "actions/configure-pages",
        "actions/upload-pages-artifact",
        "actions/deploy-pages",
        "1 GB",
        "10 minutes",
    ):
        assert phrase in text


def test_blueprints_cover_three_common_sites() -> None:
    text = BLUEPRINTS.read_text(encoding="utf-8")
    for blueprint in REQUIRED_BLUEPRINTS:
        assert f"## {blueprint}" in text
    assert text.count("Quality check:") == 3


def test_openai_metadata_matches_skill() -> None:
    text = OPENAI.read_text(encoding="utf-8")
    assert "TVL Build Free Website" in text
    assert "$tvl-build-free-website" in text


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_references,
        test_skill_contains_deployment_contract,
        test_rubric_contains_github_pages_modes_and_limits,
        test_blueprints_cover_three_common_sites,
        test_openai_metadata_matches_skill,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} free website skill checks passed")
