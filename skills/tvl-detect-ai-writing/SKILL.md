---
name: tvl-detect-ai-writing
description: Detect formulaic AI writing patterns in LinkedIn posts, short-form blog articles, professional web content, and X/Twitter replies or short comments (reply mode). Use when the user pastes a post, draft, article, or reply and asks to "detect AI patterns", "check if this is AI-written", "score this text", "find AI tells", or "audit my post for AI slop". Returns a strict Markdown report with a Pattern Score (0-10), highlighted text, detected patterns, main diagnosis, and a validation checklist. Does not rewrite. For academic or research papers, use a paper-specific detector instead.
---

# Detect AI Writing

Analyze short-form professional writing for formulaic AI-generated patterns and return a strict Markdown report. Do not rewrite. Do not produce alternative full versions. Do not judge whether the idea is good or bad. The report is advisory: the human decides what to change.

Tuned for calm, direct, factual professional content (LinkedIn posts and business writing on AI, agentic systems, security, governance, research, applied technology). If another author uses it, adapt the audience and tone notes only.

For academic or research papers, use a paper-specific detector: the patterns, banned phrases, and validation criteria differ.

## When to invoke

- The user pastes a LinkedIn post, blog excerpt, draft, or web-copy sample and asks to *"detect AI patterns"*, *"check if this is AI-written"*, *"score this text"*, *"find AI tells"*, or *"audit my post for AI slop"*.
- The user provides a URL to a blog post or article and asks to analyze its writing patterns. Fetch the article body with `WebFetch` and skip nav, footer, ads, and comments.
- The user pastes an **X/Twitter reply or short comment** and asks to check it for AI slop before sending. Run in reply mode.
- The user explicitly types `$tvl-detect-ai-writing`.

Skip for trivial conversational turns and non-writing tasks.

If no text is supplied, output exactly this line and stop:

> Paste the text you want me to analyze. I will highlight the AI-like patterns, explain what triggers them, score the text, and return a Markdown report with the findings.

## What you preserve

- The author's meaning and factual claims.
- Examples, names, numbers, tools, and technical details.
- Domain logic. Do not flag a specific term the user asked you to preserve.

## Workflow

1. Capture the text. Inline text is used directly. For a URL, fetch and extract only the article body. For a reply, treat it as reply mode.
2. Optionally run the deterministic pre-scan for the regex-detectable tells. Save the text to a file and run:

   ```bash
   python3 scripts/scan_ai_patterns.py draft.txt
   ```

   For reply mode:

   ```bash
   python3 scripts/scan_ai_patterns.py reply.txt --mode reply
   ```

   The scan flags negative-correction structures, em-dash density, hashtags, discourse-marker openers, focal-word lexicon hits, and tricolon density. Treat its output as evidence, not as the verdict. The semantic patterns below still need human-grade judgment.
3. Read the text against the full pattern taxonomy below. Mark the exact phrase that creates each pattern. Do not paraphrase.
4. Apply combination-required scoring. A single isolated tell is unreliable. Require at least two distinct tell categories before any non-PASS reading, and be conservative below about 50 words.
5. Return the strict Markdown report. Do not summarize, soften, or rewrite. If a pattern is absent, write **Pass**. Pattern Score 0 is a valid, correct result.

The full pattern reference lives in [references/ai-writing-patterns.md](references/ai-writing-patterns.md). Calibration thresholds and the research basis live in [references/calibration-notes.md](references/calibration-notes.md). Use [references/evaluation-cases.md](references/evaluation-cases.md) when testing or modifying this skill.

## What you detect

### Banned patterns (flag when present)

- **Negative correction / parallelism.** "It is not X, it is Y" / "Not just X, but Y" / "Not only X, but also Y" / "Not about X, about Y". Also the state-flip variant: "X is no longer Y. It is Z." / "X used to be Y. Now it is Z." The single most-identified AI tell. When any variant opens two or more body paragraphs in the same post, escalate to High as a cumulative structural tell, even when each instance is grounded.
- **Artificial tension.** "But here is the part nobody talks about" / "This is where it gets interesting" / "The real shift is" / "This changes everything" / "That is the unlock" / "Read that again" / "Let that sink in" / "Full stop". Engagement bait disguised as insight.
- **Generic bridge phrases.** "The point is" / "What this means in practice" / "That matters because" / "One thing is clear" / "My reading is" / "For me, this means" / "The bigger story is". Structure without new information.
- **Content-less announcement sentences.** A short sentence whose whole job is to promise what comes next: "Three things matter here." then an enumeration. Test: does it survive without the next sentence? If not, flag, and suggest merging with a comma.
- **Content-less callback / echo.** "X breaks similarly" / "The same applies to Y" / "Z follows the same pattern". Asserts equivalence instead of stating the mechanism for the current item. Strip it: if the substantive claim remains, it was filler.
- **Metaphorical-scaffolding verbs.** "rests on" / "hinges on" / "is grounded in" / "is rooted in" / "is built on" / "is anchored in" / "predicates on", where a direct verb (assumes, depends on, comes from, uses, requires) is available. A register signal, not a deterministic tell.
- **Scene-painting clause stacks.** Two or more short parallel subject-verb-modifier clauses describing one scene through accumulation: "The methodology reads cleanly, the figures are tight, the conclusions are confident." Pick the one observation that carries the weight.
- **Generic-paradigm openers.** "Most teams still run X at the Y level" / "Until 2024, X did Y. Now..." / "The way we X is broken" / "Industry has been getting X wrong". A textbook thought-leader hook. High severity as the lead sentence.
- **Short imperative-fragment introducers.** Two-to-four-word standalone openers: "Take X." / "Consider Y." / "Think about Z." / "Here's the thing." / "Picture this." The cadence is the tell. High when two or more appear.
- **Topic-marker colon openers.** Short topic phrase plus colon plus the claim, as a paragraph opener: "On scope-creep:" / "Bottom line:" / "In short:" / "TL;DR:". A longer prepositional phrase joined by a comma to a main clause does not flag.

### Detection taxonomy (score against all)

1. Rhetorical-question opening whose answer is supplied immediately.
2. List stacking: short fragments placed in a row for rhythm.
3. Negative correction / parallelism (pure-negation and state-flip variants; cumulative paragraph-opener escalation).
4. Artificial contrast: polished opposition for effect, not clarity.
5. Slogan closer: a short final line engineered to sound memorable.
6. Generic bridge phrase.
7. Authority insertion: a person, company, or title dropped in for credibility without context.
8. Compression claim: a strong number or operational claim with no grounding.
9. Over-neat symmetry: sentences shaped for rhythm over clarity.
10. Vague abstraction: "unlock", "shift", "transformation", "control layer", "new operating model", "future ready".
11. Marketing residue: "game changer", "powerful", "revolutionary", "seamless", "next generation", "AI powered".
12. False tension: drama around something that needs none.
13. Uniform paragraph rhythm: same length and cadence throughout.
14. Em-dash density: flag at more than one per 75 words, or three or more in a post under 250 words. A single em dash does not flag.
15. Hashtags: signal a creator template, not professional content.
16. Unsupported claim or invented fact.
17. Discourse-marker opener density: "However", "Moreover", "Additionally", "In conclusion", "It is worth noting". Flag at more than one per five sentences.
18. Focal-word lexicon hit: words empirically overused by alignment-trained models — *delve*, *delves*, *delving*, *surpassing*, *intricate*, *intricacies*, *underscore*, *underscores*, *advancements*, *showcasing*, *boasts*, *garnered*, *realm*, *groundbreaking*, *tapestry*, *meticulous*, *commendable*, *aligns*. Treat *delve* as near-deterministic when paired with another tell.
19. Epistemic flatness: in a personal-claim post of 150+ words, absence of any first-person uncertainty marker ("I think", "I'm not sure", "maybe", "in my experience").
20. Tricolon density: lists of three; flag at more than one per 100 words.

### Reply-mode patterns (X/Twitter replies and short comments)

Apply in addition to the above only when the text is a reply, and **invert the register rules**: lowercase, fragments, contractions, and a missing final period are normal human texture and must not be flagged. Over-polish is the tell. A strong reply carries a concrete payload (a number, a named paper or standard, a specific failure mode, or a genuinely specific question) and takes a stance; the absence of both is the core slop signal.

- **Affirmation opener.** "This is so true" / "Absolutely" / "Great point" / "Well said" / "100%" / "This." as a lead. The canonical bot opener. High.
- **Restating the parent** before responding, which signals generation from the tweet text, not from knowledge. High.
- **Vague takeaway / platitude** that could attach to any tweet. Medium.
- **Hollow question** with no specific hook. A genuinely specific question is a strength, not a tell. Medium.
- **No-stance corporate-neutral:** agreeable, polished, risk-free, forgettable. High when the whole reply is stance-free.
- **Tell-vocabulary in short form:** even one of *delve / underscore / intricate / crucial / fascinating / "it's worth noting"* in a 1-3 sentence reply. Medium-High.

A strong human reply is usually one or two sentences. A three-plus-sentence, fully structured reply reads as generated; note it should be a quote-tweet instead.

## Score scale (0-10)

| Score | Reading |
| --- | --- |
| 0-2 | Natural, specific, human writing. |
| 3-4 | Mostly natural with isolated formulaic elements. |
| 5-6 | Noticeable patterns; readers may sense templating. |
| 7-8 | Heavily templated; multiple AI tells stacked. |
| 9-10 | Strongly AI-patterned across structure, phrasing, and rhythm. |

## Output format (STRICT)

```
# AI Pattern Report

## Pattern Score

X out of 10

## Highlighted Text

<full original text reproduced verbatim, with suspicious phrases marked using
double equals signs: ==exact phrase==. Mark only the exact words that create
the pattern; do not paraphrase.>

## Detected Patterns

### Pattern 1

**Pattern name:** <name from the taxonomy>

**Exact phrase:** "<exact phrase from text>"

**Why it was flagged:** <the mechanism, not a vague "this sounds AI">

**Severity:** Low | Medium | High

**Suggested direction:** <short editorial guidance, not a rewrite>

### Pattern 2
...

## Main Diagnosis

<3 to 5 sentences. Explain the mechanism behind the artificial feeling. Be
specific.>

## Validation Check

- **Em-dash density (>1 per 75 words OR >=3 in <250 words):** Pass | Issue found
- **Hashtags:** Pass | Issue found
- **Generic-paradigm opener:** Pass | Issue found
- **Short imperative-fragment introducer:** Pass | Issue found
- **Topic-marker colon opener:** Pass | Issue found
- **Slogan ending:** Pass | Issue found
- **Generic bridge phrase:** Pass | Issue found
- **Content-less announcement sentence:** Pass | Issue found
- **Content-less callback / echo phrase:** Pass | Issue found
- **Metaphorical-scaffolding verb:** Pass | Issue found
- **Scene-painting clause stack:** Pass | Issue found
- **Artificial contrast:** Pass | Issue found
- **Negative correction (pure-negation variant):** Pass | Issue found
- **Negative correction (state-flip variant):** Pass | Issue found
- **Cumulative parallelism as paragraph-opener (>=2 body paragraphs):** Pass | Issue found
- **Marketing language:** Pass | Issue found
- **Unsupported claim / invented fact:** Pass | Issue found
- **Robotic paragraph rhythm:** Pass | Issue found
- **Discourse-marker opener density:** Pass | Issue found
- **Focal-word lexicon hits:** Pass | Issue found (list which words)
- **Tricolon density (>1 per 100 words):** Pass | Issue found
- **Epistemic flatness (personal-claim post):** Pass | Issue found
- **[reply mode] Affirmation / restating parent / vague takeaway / hollow question / no-stance:** Pass | Issue found
- **[reply mode] Carries a concrete payload AND a stance:** Pass | Issue found

## Summary of Priority Fixes

<Top 3 to 5 issues, ranked by severity. Editorial direction only. Do not rewrite.>
```

## Rules

- No rewriting. No alternative full versions.
- No em dashes, hashtags, or marketing language in your own output.
- Preserve names, numbers, tools, and technical details from the original.
- Mark the exact phrase. Explain the pattern. Do not invent facts.
- Penalize combination and density, not isolated occurrences. Require at least two distinct tell categories before a non-PASS reading.
- If a banned pattern is absent, write **Pass**. Do not invent issues to justify yourself.
- Be strict but constructive. Keep the tone calm, direct, and factual.
- Return only the Markdown report when text is provided.

## Common triggers

- "Detect AI patterns in this LinkedIn post."
- "Check if this draft is AI-written."
- "Score this text for AI slop."
- "Find the AI tells in my post."
- "Audit my LinkedIn draft before I publish."
- "Check this reply for AI slop before I send it."
- "Use $tvl-detect-ai-writing on this text."
