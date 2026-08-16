#!/usr/bin/env python3
"""Check source-register dates and required crawler names."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REGISTER = ROOT / "references" / "source-register.md"
CRAWLER_POLICY = ROOT / "references" / "crawler-policy.md"
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


def extract_dates(text: str) -> list[date]:
    values = []
    for match in re.finditer(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|", text):
        values.append(date.fromisoformat(match.group(1)))
    return values


def check(max_age_days: int = 180, today: date | None = None) -> list[str]:
    today = today or date.today()
    errors = []
    source_text = SOURCE_REGISTER.read_text(encoding="utf-8")
    crawler_text = CRAWLER_POLICY.read_text(encoding="utf-8")
    dates = extract_dates(source_text)
    if len(dates) < 5:
        errors.append("source register must include last verified dates")
    for item in dates:
        age = (today - item).days
        if age > max_age_days:
            errors.append(f"source register entry is stale: {item.isoformat()} is {age} days old")
    for agent in REQUIRED_AGENTS:
        if agent not in source_text and agent not in crawler_text:
            errors.append(f"required crawler agent missing: {agent}")
    for required_url in (
        "developers.google.com/search/docs/fundamentals/ai-optimization-guide",
        "developers.google.com/search/docs/appearance/core-web-vitals",
        "developers.google.com/search/docs/essentials/spam-policies",
        "developers.google.com/search/docs/appearance/google-images",
        "developers.google.com/search/docs/appearance/video",
        "developers.google.com/search/docs/appearance/structured-data/intro-structured-data",
        "developer.chrome.com/docs/lighthouse/overview",
        "bing.com/webmasters/help/webmaster-guidelines",
        "bing.com/indexnow/getstarted",
        "w3.org/TR/WCAG22",
        "developers.openai.com/api/docs/bots",
        "support.claude.com",
        "docs.perplexity.ai/docs/resources/perplexity-crawlers",
    ):
        if required_url not in source_text:
            errors.append(f"required official source missing: {required_url}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SEO/GEO source freshness")
    parser.add_argument("--max-age-days", type=int, default=180)
    args = parser.parse_args()
    errors = check(args.max_age_days)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("source register freshness passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
