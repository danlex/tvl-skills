# SEO GEO Evaluation Cases

Use these cases to test whether the skill produces practical, evidence-first audits. They are not templates for final answers.

## Case 1: Indexable But Overlong Metadata

Page evidence:

```text
Status: 200
Robots meta: index, follow
Canonical: https://example.com/en/skills/
Title length: 74 characters
Meta description length: 230 characters
H1 count: 1
JSON-LD: ItemList, valid
Sitemap lastmod: three days before the latest deployment
```

Expected audit:

- Verdict: `REVISE`
- Reason: no blocker, but metadata is too long and sitemap freshness is stale.
- Required fix: shorten title/description and update sitemap `lastmod`.

## Case 2: Wrong Canonical on Multilingual Page

Page evidence:

```text
URL: https://example.com/ro/servicii/
HTML lang: ro
Canonical: https://example.com/en/services/
Hreflang ro: https://example.com/ro/servicii/
Hreflang en: https://example.com/en/services/
```

Expected audit:

- Verdict: `BLOCK`
- Reason: Romanian page canonical points to English page, creating language and indexing conflict.
- Required fix: canonical must point to the Romanian URL; keep reciprocal hreflang.

## Case 3: GEO Claim Without Measurement

Draft claim:

```text
This page is optimized for ChatGPT and will appear in AI answers for "best B2B AI training".
```

Available evidence:

```text
The page is crawlable and has schema, but no AI answer checks, no referral data, no cited-source screenshots, and no query tracking.
```

Expected audit:

- Verdict: `REVISE`
- Reason: the page may be AI-readable, but the citation/ranking claim is unverified.
- Required fix: replace guarantee with a controllable statement and define measurement.

## Case 4: Deceptive Structured Data

Page evidence:

```text
Visible page: consulting service landing page
JSON-LD: Course with aggregateRating 5.0 and 240 reviews
Visible reviews: none
Review source: not provided
```

Expected audit:

- Verdict: `BLOCK`
- Reason: structured data marks up unsupported ratings and wrong content type.
- Required fix: remove unsupported rating and use schema that matches visible content.

## Case 5: AI Answer Visibility Improvement

Page evidence:

```text
Article explains "AI skills" in long paragraphs.
No direct definition near the top.
No comparison table for prompts, skills, workflows, and agents.
Sources are listed at the bottom.
Content is indexable and accurate.
```

Expected audit:

- Verdict: `REVISE`
- Reason: technically healthy but less extractable for AI answers.
- Required fix: add a short definition, comparison table, key takeaways, and source-backed factual atoms.

## Case 6: Good Page With Clear Limits

Page evidence:

```text
Status: 200
Robots: index, follow
Canonical and hreflang: correct
Title: clear and under 60 characters
Meta description: clear and under 160 characters
JSON-LD: valid WebPage + BreadcrumbList, matches visible content
Content: direct answer, examples, sources, update date
Robots.txt: allows general crawl and declares sitemap
Measurement: Search Console and AI referral review planned monthly
```

Expected audit:

- Verdict: `PASS`
- Reason: no material technical, content, structured data, or AI visibility issue found.
- Required fix: none; optional P2 improvements only.
