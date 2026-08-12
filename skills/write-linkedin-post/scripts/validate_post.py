#!/usr/bin/env python3
"""Validate deterministic rules from LinkedIn Writing Protocol v3."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    detail: str


BANNED_PATTERNS = {
    "rhetorical contrast 'not X but Y'": r"\bnot\b[^.!?\n]{0,100}\bbut\b",
    "rhetorical contrast 'less X more Y'": r"\bless\b[^.!?\n]{0,100}\bmore\b",
    "rhetorical phrase 'instead of'": r"\binstead of\b",
    "rhetorical phrase 'forget X'": r"\bforget\b",
    "rhetorical phrase 'the real story is'": r"\bthe real story is\b",
    "rhetorical phrase 'X is dead'": r"\bis dead\b",
    "rhetorical phrase 'X no longer matters'": r"\bno longer matters\b",
    "editorial transition 'another important trend'": r"\banother important trend\b",
    "editorial transition 'looking ahead'": r"\blooking ahead\b",
    "editorial transition 'this matters because'": r"\bthis matters because\b",
    "editorial transition 'the challenge is'": r"\bthe challenge is\b",
    "editorial transition 'it is worth noting'": r"\bit is worth noting\b",
    "editorial transition 'the practical idea is simple'": r"\bthe practical idea is simple\b",
    "editorial transition 'in conclusion'": r"\bin conclusion\b",
    "marketing phrase 'this changes everything'": r"\bthis changes everything\b",
    "marketing phrase 'game changer'": r"\bgame[ -]?changer\b",
    "marketing phrase 'mind blowing'": r"\bmind[ -]?blowing\b",
    "marketing word 'huge'": r"\bhuge\b",
    "marketing word 'revolutionary'": r"\brevolutionary\b",
    "marketing word 'transformative'": r"\btransformative\b",
}

EMOJI_RE = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "]"
)
WORD_RE = re.compile(r"\b[\w’']+\b", flags=re.UNICODE)
URL_RE = re.compile(r"^https?://\S+$", flags=re.IGNORECASE)


def split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def split_sentences(paragraph: str) -> list[str]:
    return [
        part.strip()
        for part in re.split(r"(?<=[.!?])(?:[\"'”’)]*)\s+", paragraph.strip())
        if part.strip()
    ]


def validate_text(text: str, min_chars: int = 2700, max_chars: int = 2900) -> list[Finding]:
    findings: list[Finding] = []
    stripped = text.strip()
    char_count = len(stripped)

    if not stripped:
        return [Finding("error", "content", "The post is empty.")]

    if char_count < min_chars or char_count > max_chars:
        findings.append(
            Finding(
                "error",
                "character-count",
                f"Found {char_count} characters, expected {min_chars} to {max_chars}.",
            )
        )

    lines = stripped.splitlines()
    for number, line in enumerate(lines, start=1):
        if re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line):
            findings.append(Finding("error", "plain-paragraphs", f"List marker on line {number}."))
        if re.match(r"^\s*#{1,6}\s+", line):
            findings.append(Finding("error", "plain-paragraphs", f"Heading on line {number}."))
        if re.match(r"^\s*\|.*\|\s*$", line):
            findings.append(Finding("error", "plain-paragraphs", f"Table syntax on line {number}."))

    if "—" in stripped:
        findings.append(Finding("error", "em-dash", "Em dash found."))
    if re.search(r"(?<!\w)#[\w]+", stripped, flags=re.UNICODE):
        findings.append(Finding("error", "hashtags", "Hashtag found."))
    if EMOJI_RE.search(stripped):
        findings.append(Finding("error", "emojis", "Emoji or pictographic symbol found."))
    if re.search(r"\[[^\]]+\]\([^)]+\)", stripped):
        findings.append(Finding("error", "plain-paragraphs", "Markdown link found."))

    for label, pattern in BANNED_PATTERNS.items():
        match = re.search(pattern, stripped, flags=re.IGNORECASE)
        if match:
            findings.append(Finding("error", "banned-language", f"Found {label}: {match.group(0)!r}."))

    paragraphs = split_paragraphs(stripped)
    for index, paragraph in enumerate(paragraphs, start=1):
        length = len(paragraph)
        if length < 150 or length > 250:
            findings.append(
                Finding(
                    "warning",
                    "paragraph-length",
                    f"Paragraph {index} has {length} characters, preferred range is 150 to 250.",
                )
            )

        for sentence in split_sentences(paragraph):
            if URL_RE.fullmatch(sentence):
                continue
            word_count = len(WORD_RE.findall(sentence))
            if 0 < word_count < 10:
                excerpt = sentence if len(sentence) <= 90 else sentence[:87] + "..."
                findings.append(
                    Finding(
                        "warning",
                        "sentence-length",
                        f"Paragraph {index} has a {word_count} word sentence: {excerpt!r}.",
                    )
                )

    if re.search(r"(?<!https:)(?<!http:)\b[\w]+-[\w]+\b", stripped):
        findings.append(
            Finding(
                "warning",
                "hyphens",
                "A hyphenated expression was found. Rewrite it when a natural alternative exists.",
            )
        )

    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="UTF-8 text file. Reads stdin when omitted.")
    parser.add_argument("--min-chars", type=int, default=2700)
    parser.add_argument("--max-chars", type=int, default=2900)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.min_chars < 0 or args.max_chars < args.min_chars:
        print("Invalid character range.", file=sys.stderr)
        return 2

    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    findings = validate_text(text, args.min_chars, args.max_chars)
    errors = [finding for finding in findings if finding.severity == "error"]

    print(f"Characters: {len(text.strip())}")
    if not findings:
        print("PASS: deterministic checks found no issues.")
        return 0

    for finding in findings:
        print(f"{finding.severity.upper()}: {finding.rule}: {finding.detail}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(findings) - len(errors)} warning(s).")
        return 1

    print(f"PASS WITH WARNINGS: {len(findings)} warning(s) require editorial review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
