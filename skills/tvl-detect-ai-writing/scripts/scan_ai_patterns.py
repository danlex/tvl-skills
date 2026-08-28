#!/usr/bin/env python3
"""Deterministic pre-scan for regex-detectable AI writing tells.

This is an evidence-gathering aid for the tvl-detect-ai-writing skill, not the
verdict. It flags only the patterns that can be matched mechanically: negative
correction structures, em-dash density, hashtags, discourse-marker openers,
focal-word lexicon hits, and tricolon density. The semantic patterns (bridge
phrases, slogan closers, scene-painting, authority insertion, unsupported claims)
still need human-grade judgment from the skill.

Usage:
    python3 scripts/scan_ai_patterns.py draft.txt
    python3 scripts/scan_ai_patterns.py reply.txt --mode reply

Exit code is 0 when no tell fires, 1 when at least one does. In reply mode the
register rules invert, so lowercase and a missing final period are never flagged.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FOCAL_WORDS = (
    "delve", "delves", "delved", "delving", "surpassing", "surpasses",
    "intricate", "intricacies", "underscore", "underscores", "underscoring",
    "advancements", "showcasing", "showcases", "boasts", "garnered",
    "emphasizing", "realm", "groundbreaking", "aligns", "comprehending",
    "tapestry", "unlocking", "meticulous", "commendable",
)

DISCOURSE_OPENERS = (
    "however", "moreover", "additionally", "furthermore", "in conclusion",
    "it is important to note", "it's worth noting", "it is worth noting",
    "remember",
)

MARKETING = (
    "game changer", "game-changer", "mind blowing", "mind-blowing",
    "revolutionary", "transformative", "next generation", "next-generation",
    "ai powered", "ai-powered", "seamless", "unlock potential",
    "this changes everything",
)

NEG_CORRECTION = (
    r"\bnot just\b.*\bbut\b",
    r"\bit'?s not\b.*\bit'?s\b",
    r"\bnot only\b.*\bbut also\b",
    r"\bnot a\b[^.]*\bbut a\b",
    r"\bnot about\b[^.]*\babout\b",
    r"\bis not\b[^.]*\bit is\b",
)

STATE_FLIP = (
    r"\b(is|are|was|were)\s+no\s+longer\b",
    r"\bused\s+to\s+(be|flag|call|describe|treat)\b[^.]*\b(now|today)\b",
    r"\b(isn'?t|aren'?t|wasn'?t)\s+\w+\s+anymore\b",
)

PARADIGM_OPENER = (
    r"^\s*most\s+\w+.*\bstill\b",
    r"^\s*until\s+\d{4}\b",
    r"\bthe way we\b.*\bis broken\b",
    r"\bhas been getting\b.*\bwrong\b",
)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def sentence_count(text: str) -> int:
    parts = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    return max(1, len(parts))


class Finding:
    def __init__(self, name: str, detail: str, severity: str) -> None:
        self.name = name
        self.detail = detail
        self.severity = severity


def scan(text: str, mode: str) -> list[Finding]:
    findings: list[Finding] = []
    lower = text.lower()
    words = word_count(text)
    sentences = sentence_count(text)

    # Negative correction (pure-negation)
    for pat in NEG_CORRECTION:
        if re.search(pat, lower):
            findings.append(Finding(
                "Negative correction (pure-negation)",
                f"matched /{pat}/", "High"))
            break

    # Negative correction (state-flip)
    for pat in STATE_FLIP:
        if re.search(pat, lower):
            findings.append(Finding(
                "Negative correction (state-flip)",
                f"matched /{pat}/", "High"))
            break

    # Generic-paradigm opener (check first line)
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    for pat in PARADIGM_OPENER:
        if re.search(pat, first_line.lower()):
            findings.append(Finding(
                "Generic-paradigm opener",
                f"lead sentence matched /{pat}/", "High"))
            break

    # Em-dash density
    em = text.count("—")
    if em:
        dense = (words and em / words > 1 / 75) or (words < 250 and em >= 3)
        if dense:
            findings.append(Finding(
                "Em-dash density",
                f"{em} em dashes in {words} words", "Medium"))

    # Hashtags
    tags = re.findall(r"(?<!\w)#\w+", text)
    if tags:
        findings.append(Finding(
            "Hashtags", f"{len(tags)} hashtag(s): {' '.join(tags[:5])}", "Medium"))

    # Discourse-marker openers (sentence-initial), density > 1 per 5 sentences
    opener_hits = 0
    for seg in re.split(r"(?<=[.!?])\s+|\n+", text):
        seg_l = seg.strip().lower()
        for marker in DISCOURSE_OPENERS:
            if seg_l.startswith(marker):
                opener_hits += 1
                break
    if opener_hits and opener_hits / sentences > 1 / 5:
        findings.append(Finding(
            "Discourse-marker opener density",
            f"{opener_hits} openers in {sentences} sentences", "Medium"))

    # Focal-word lexicon
    hits = sorted({w for w in FOCAL_WORDS if re.search(rf"\b{w}\b", lower)})
    if hits:
        sev = "High" if any(h.startswith("delv") for h in hits) and len(findings) else "Medium"
        findings.append(Finding(
            "Focal-word lexicon", ", ".join(hits), sev))

    # Marketing residue
    mk = sorted({m for m in MARKETING if m in lower})
    if mk:
        findings.append(Finding("Marketing residue", ", ".join(mk), "Medium"))

    # Tricolon density: rough proxy — "a, b, and c" or "a, b, c." runs
    tricolons = re.findall(r"\b[\w'-]+,\s+[\w'-]+,\s+(?:and\s+)?[\w'-]+", text)
    if tricolons and words and len(tricolons) / words > 1 / 100:
        findings.append(Finding(
            "Tricolon density",
            f"{len(tricolons)} list-of-three run(s) in {words} words", "Low"))

    # Reply-mode extra: affirmation opener
    if mode == "reply":
        aff = (
            "this is so true", "absolutely", "couldn't agree more", "great point",
            "great post", "well said", "100%", "so true",
        )
        head = lower.strip()[:40]
        if any(head.startswith(a) for a in aff) or head.startswith("this.") or head == "this":
            findings.append(Finding(
                "Affirmation opener (reply)",
                "reply opens with a canonical bot affirmation", "High"))

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-scan text for regex-detectable AI tells.")
    ap.add_argument("path", help="path to a UTF-8 text file")
    ap.add_argument("--mode", choices=("post", "reply"), default="post",
                    help="reply inverts register rules and adds reply checks")
    args = ap.parse_args()

    text = Path(args.path).read_text(encoding="utf-8")
    findings = scan(text, args.mode)

    words = word_count(text)
    print(f"Scanned {words} words, mode={args.mode}")
    if words < 50:
        print("NOTE: under ~50 words, detectors degrade. Require converging tells.")

    if not findings:
        print("No regex-detectable tell fired. Run the full semantic review next.")
        return 0

    print(f"\n{len(findings)} deterministic tell(s) fired:\n")
    for f in findings:
        print(f"  [{f.severity:<6}] {f.name}: {f.detail}")
    print("\nThese are evidence, not the verdict. Apply combination-required "
          "scoring and the semantic patterns before reading the score.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
