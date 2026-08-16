#!/usr/bin/env python3
"""Structural and behavioral checks for tvl-seo-geo-audit."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCES = ROOT / "references"
EVALS = ROOT / "evals" / "cases.jsonl"
OPENAI = ROOT / "agents" / "openai.yaml"
sys.path.insert(0, str(ROOT / "scripts"))

from check_reference_freshness import check as check_reference_freshness  # noqa: E402
from collect_seo_evidence import UnsafeUrlError, parse_html, validate_public_http_url  # noqa: E402
from render_audit_report import render_report  # noqa: E402
from run_lighthouse_audit import not_tested as lighthouse_not_tested  # noqa: E402
from verify_findings import verify_findings  # noqa: E402


REQUIRED_REFERENCES = (
    "references/evidence-contract.md",
    "references/seo-geo-rubric.md",
    "references/crawler-policy.md",
    "references/bing-indexnow.md",
    "references/wcag-accessibility.md",
    "references/structured-data-profiles.md",
    "references/source-register.md",
    "references/evaluation-cases.md",
)

REQUIRED_SCRIPTS = (
    "scripts/collect_seo_evidence.py",
    "scripts/verify_findings.py",
    "scripts/render_audit_report.py",
    "scripts/check_reference_freshness.py",
    "scripts/run_lighthouse_audit.py",
)

REQUIRED_STATES = (
    "CONFIRMED",
    "REFUTED",
    "NOT_FOUND",
    "NOT_TESTED",
    "MISSING_TEST",
    "UNVERIFIABLE",
    "MISLEADING",
)

REQUIRED_AGENTS = (
    "OAI-SearchBot",
    "GPTBot",
    "ChatGPT-User",
    "Claude-SearchBot",
    "ClaudeBot",
    "Claude-User",
    "PerplexityBot",
    "Perplexity-User",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_frontmatter_and_references() -> None:
    text = read(SKILL)
    assert text.startswith("---\nname: tvl-seo-geo-audit\n")
    assert "description:" in text.split("---", 2)[1]
    for reference in REQUIRED_REFERENCES:
        assert reference in text
        assert (ROOT / reference).exists()
    for script in REQUIRED_SCRIPTS:
        assert script in text or script.endswith("check_reference_freshness.py")
        assert (ROOT / script).exists()


def test_skill_uses_evidence_states_and_no_false_pass() -> None:
    text = read(SKILL)
    for state in REQUIRED_STATES:
        assert state in text
    assert "Other checks: PASS" not in text
    assert "Never report `PASS`" in text
    assert "Evidence coverage" in text
    assert "X-Robots-Tag" in text
    assert "Lighthouse" in text
    assert "performance`, `accessibility`, and `seo`" in text


def test_references_have_resolvable_relative_links() -> None:
    markdown_files = [SKILL, *REFERENCES.glob("*.md")]
    for path in markdown_files:
        text = read(path)
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            href = match.group(1)
            if href.startswith(("http://", "https://", "#")):
                continue
            assert (path.parent / href).exists(), f"{path} -> {href}"


def test_rubric_rows_are_populated_and_current() -> None:
    text = read(REFERENCES / "seo-geo-rubric.md")
    assert "under 60" not in text
    assert "under 160" not in text
    assert "no fixed character" in text or "fixed character" in text
    for required in (
        "HTTP and indexability",
        "X-Robots-Tag",
        "Raw HTML versus rendered DOM",
        "`llms.txt` and RSL",
        "Accessibility basics",
        "Lighthouse lab audit",
        "Core Web Vitals field data",
        "Bing and IndexNow",
        "WCAG 2.2 accessibility mapping",
        "Spam and abuse policy",
        "Rich result eligibility by page type",
        "Image SEO deep check",
        "Video SEO deep check",
        "External citation and source-link integrity",
        "SERP or cited-source comparison",
        "Log-based crawler verification",
        "Measurement",
    ):
        assert required in text
    rows = [line for line in text.splitlines() if line.startswith("| ") and " | " in line]
    audit_rows = [row for row in rows if not set(row.replace("|", "").strip()) <= {"-", " "}]
    assert len(audit_rows) >= 20
    for row in audit_rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        assert all(cells), row


def test_crawler_policy_separates_agent_purposes() -> None:
    text = read(REFERENCES / "crawler-policy.md")
    for agent in REQUIRED_AGENTS:
        assert agent in text
    assert "Model-training" in text or "model-training" in text
    assert "Search discovery" in text
    assert "user-triggered" in text
    assert "Do not recommend allowing every AI bot" in text


def test_source_register_has_official_urls_and_fresh_dates() -> None:
    errors = check_reference_freshness(max_age_days=180, today=date(2026, 8, 16))
    assert errors == []
    text = read(REFERENCES / "source-register.md")
    assert "developer.chrome.com/docs/lighthouse/overview" in text
    assert "developer.chrome.com/docs/devtools/lighthouse" in text
    assert "developers.google.com/search/docs/appearance/core-web-vitals" in text
    assert "www.bing.com/webmasters/help/webmaster-guidelines" in text
    assert "www.bing.com/indexnow/getstarted" in text
    assert "www.w3.org/TR/WCAG22" in text
    assert "developers.google.com/search/docs/essentials/spam-policies" in text


def test_evaluation_cases_are_behavioral() -> None:
    cases = [json.loads(line) for line in read(EVALS).splitlines() if line.strip()]
    assert len(cases) >= 10
    assert any(case["should_activate"] is False for case in cases)
    assert {case["expected_mode"] for case in cases if case["expected_mode"]} >= {
        "PAGE",
        "MULTILINGUAL_PAIR",
        "SITE_SAMPLE",
        "CONTENT_BRIEF",
    }
    joined = "\n".join(read(REFERENCES / "evaluation-cases.md").splitlines())
    for required in (
        "X-Robots-Tag Noindex",
        "JavaScript-Only Core Content",
        "GPTBot Blocked, OAI-SearchBot Allowed",
        "Prompt Injection in HTML",
        "Private Documentation",
        "Browser and Lighthouse Available",
        "Browser Access Unavailable",
        "Core Web Vitals Field Data Missing",
        "Bing and IndexNow Evidence Needed",
        "WCAG 2.2 Manual Conformance Not Verified",
        "Scaled Content Abuse Risk",
        "Rich Result Profile Mismatch",
        "Source Link Does Not Support Claim",
    ):
        assert required in joined
    assert any(case["id"] == "browser_lighthouse_available" for case in cases)
    assert any(case["id"] == "core_web_vitals_field" for case in cases)
    assert any(case["id"] == "bing_indexnow" for case in cases)


def test_collector_parser_extracts_core_observations() -> None:
    html = """
    <html lang="en"><head>
      <title>Clear title</title>
      <meta name="description" content="Useful description">
      <meta name="robots" content="index, follow">
      <link rel="canonical" href="/canonical">
      <link rel="alternate" hreflang="ro" href="/ro/">
      <meta property="og:title" content="OG title">
      <script type="application/ld+json">{"@type":"WebPage","name":"Page"}</script>
    </head><body><h1>Main</h1><h2>Section</h2><img src="a.png" alt="Diagram"><a href="/next">Next</a></body></html>
    """
    parsed = parse_html(html, "https://example.com/page")
    assert parsed["title"] == "Clear title"
    assert parsed["meta_description"] == "Useful description"
    assert parsed["robots_meta"] == "index, follow"
    assert parsed["canonical"] == "https://example.com/canonical"
    assert parsed["hreflang"][0]["hreflang"] == "ro"
    assert parsed["json_ld"][0]["valid"] is True
    assert parsed["headings"][0]["level"] == "h1"


def test_new_references_cover_p0_p1_contracts() -> None:
    bing = read(REFERENCES / "bing-indexnow.md")
    wcag = read(REFERENCES / "wcag-accessibility.md")
    profiles = read(REFERENCES / "structured-data-profiles.md")
    assert "IndexNow" in bing and "Bing Webmaster Tools" in bing
    for principle in ("Perceivable", "Operable", "Understandable", "Robust"):
        assert principle in wcag
    for schema_type in ("Article", "Product", "LocalBusiness", "VideoObject", "FAQPage"):
        assert schema_type in profiles


def test_collector_refuses_unsafe_urls() -> None:
    for url in ("file:///tmp/a.html", "http://127.0.0.1/test", "http://localhost/test"):
        try:
            validate_public_http_url(url)
        except UnsafeUrlError:
            pass
        else:
            raise AssertionError(f"unsafe URL accepted: {url}")


def test_lighthouse_not_tested_shape() -> None:
    result = lighthouse_not_tested("Lighthouse CLI is unavailable")
    assert result["state"] == "NOT_TESTED"
    for category in ("performance", "accessibility", "seo"):
        assert result["categories"][category]["state"] == "NOT_TESTED"


def sample_payload() -> dict:
    return {
        "manifest": {"audit_mode": "PAGE", "requested_url": "https://example.com", "final_url": "https://example.com"},
        "evidence_records": [
            {"id": "http.status", "state": "CONFIRMED", "origin": "MEASURED", "value": 200},
            {"id": "robots_meta", "state": "CONFIRMED", "origin": "MEASURED", "value": "index,follow"},
            {"id": "x_robots_tag", "state": "NOT_FOUND", "origin": "MEASURED", "value": None},
            {"id": "canonical", "state": "CONFIRMED", "origin": "MEASURED", "value": "https://example.com"},
            {"id": "indexation_intent", "state": "CONFIRMED", "origin": "USER_PROVIDED", "value": "public"},
            {"id": "core_web_vitals_field", "state": "NOT_TESTED", "origin": "MEASURED", "value": None},
            {"id": "bing_indexnow", "state": "NOT_TESTED", "origin": "MEASURED", "value": None},
            {"id": "crawler_logs", "state": "NOT_TESTED", "origin": "MEASURED", "value": None},
        ],
        "findings": [],
    }


def finding(**overrides: object) -> dict:
    base = {
        "id": "F-001",
        "check_id": "metadata.title",
        "priority": "P1",
        "area": "Metadata",
        "result": "REVISE",
        "evidence_state": "CONFIRMED",
        "origin": "MEASURED",
        "evidence_refs": ["http.status"],
        "location": "https://example.com",
        "evidence": "Title is vague.",
        "impact": "Weak snippet clarity.",
        "fix": "Rewrite title for clarity.",
        "verification": "Fetch title again and inspect SERP preview.",
        "effort": "S",
        "root_cause": "weak-title",
    }
    base.update(overrides)
    return base


def test_verifier_rollup_and_suppression() -> None:
    payload = sample_payload()
    payload["findings"] = [
        finding(),
        finding(id="F-002"),
        finding(id="F-003", evidence_refs=["missing"]),
        finding(id="F-004", result="PASS", evidence_state="NOT_TESTED"),
        finding(id="F-005", scope="sitewide", root_cause="sitewide-linking"),
    ]
    result = verify_findings(payload)
    assert result["verdict"] == "REVISE"
    assert len(result["verified_findings"]) == 1
    reasons = " ".join(item["reason"] for item in result["suppressed_findings"])
    assert "duplicate root cause" in reasons
    assert "evidence refs not found" in reasons
    assert "cannot PASS" in reasons
    assert "sitewide conclusion" in reasons


def test_verifier_blocks_p0_and_renderer_uses_verified_json() -> None:
    payload = sample_payload()
    payload["findings"] = [
        finding(
            priority="P0",
            result="BLOCK",
            blocker_category="INDEXING_BLOCKER",
            check_id="x_robots_tag",
            evidence_refs=["x_robots_tag"],
            evidence="X-Robots-Tag noindex blocks intended indexing.",
            root_cause="x-robots-noindex",
        )
    ]
    result = verify_findings(payload)
    assert result["verdict"] == "BLOCK"
    report = render_report(result)
    assert "SEO GEO AUDIT" in report
    assert "Evidence coverage" in report
    assert "INDEXING_BLOCKER" in report


def test_openai_metadata_neutral_prompt() -> None:
    text = read(OPENAI)
    assert "TVL SEO GEO Audit" in text
    assert "$tvl-seo-geo-audit" not in text
    assert "Report evidence, limitations, and prioritized fixes." in text


if __name__ == "__main__":
    tests = [
        test_skill_frontmatter_and_references,
        test_skill_uses_evidence_states_and_no_false_pass,
        test_references_have_resolvable_relative_links,
        test_rubric_rows_are_populated_and_current,
        test_crawler_policy_separates_agent_purposes,
        test_source_register_has_official_urls_and_fresh_dates,
        test_evaluation_cases_are_behavioral,
        test_collector_parser_extracts_core_observations,
        test_new_references_cover_p0_p1_contracts,
        test_collector_refuses_unsafe_urls,
        test_lighthouse_not_tested_shape,
        test_verifier_rollup_and_suppression,
        test_verifier_blocks_p0_and_renderer_uses_verified_json,
        test_openai_metadata_neutral_prompt,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} SEO GEO audit checks passed")
