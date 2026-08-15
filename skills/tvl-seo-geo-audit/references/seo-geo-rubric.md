# SEO GEO Rubric

Use this rubric to audit whether a page is technically discoverable, understandable, trustworthy, and suitable for citation or synthesis by search and AI answer systems.

## Source Basis

- Google Search Central, "Guide to optimizing for generative AI features": there is no special schema.org markup required for generative AI search; continue using normal SEO fundamentals, helpful content, and structured data where appropriate.
- Google Search Central, "SEO Starter Guide": help search engines crawl, index, understand, and present content; use descriptive titles, useful snippets, links, images, and structured data where eligible.
- Google Search Central, "Creating helpful, reliable, people-first content": SEO is useful when applied to people-first content rather than search-engine-first content.
- Google Search Central, "Introduction to structured data": structured data helps Google understand page content and can make pages eligible for rich results.
- Google Search Central, robots documentation: `robots.txt` controls crawling, not indexing; use `noindex` or access control to keep a page out of search.
- OpenAI crawler documentation: `OAI-SearchBot`, `GPTBot`, and `ChatGPT-User` serve different purposes and can be controlled separately where applicable.
- Perplexity crawler documentation: `PerplexityBot` is used to surface and link websites in Perplexity search results; visibility depends on crawl permission and source quality.
- Anthropic crawler guidance: Anthropic bots honor robots directives and separate crawling/fetching purposes; blocking relevant bots can affect visibility in user-directed retrieval.

## Evidence Labels

- `CONFIRMED`: directly verified in page HTML, HTTP response, robots file, sitemap, search result, source, or tool output.
- `REFUTED`: evidence contradicts the claim or intended configuration.
- `NOT-FOUND`: expected element is absent.
- `UNVERIFIABLE`: cannot be checked with available evidence or tools.
- `MISLEADING`: exists but misrepresents the visible page, source, entity, language, or offer.

## Audit Checks

| Check | PASS | FLAG | BLOCK |
| --- | --- | --- | --- |
| HTTP and indexability | Page returns `200`, intended redirects are clean, and robots meta allows indexing when intended. | Minor redirect or header issue; indexability intent is unclear. | Page intended for search is blocked, noindexed, broken, or hidden behind inaccessible rendering. |
| Canonical | Canonical is present when useful and points to the correct indexable URL. | Canonical is missing on a page where duplication risk exists. | Canonical points to wrong language, wrong domain, non-indexable URL, or conflicts with hreflang. |
| Sitemap | URL appears in sitemap with plausible `lastmod`. | URL is missing or `lastmod` is stale but page is otherwise discoverable. | Sitemap misleads crawlers with wrong canonical URLs, invalid XML, or stale critical changes. |
| Robots.txt | Relevant crawlers can fetch intended public pages; sitemap is declared when useful. | AI crawler policy is implicit or undocumented. | Search or AI visibility is desired but relevant paths or bots are disallowed. |
| Title | Title is unique, accurate, intent-aligned, and usually within a readable search-result length. | Title is too long, generic, duplicated, or weakly differentiated. | Title is misleading, stuffed, or contradicts page content. |
| Meta description | Description summarizes the page clearly and supports click understanding. | Description is too long, too short, generic, duplicated, or omits the value. | Description is misleading or promises unsupported content. |
| Headings | One primary H1; H2/H3 structure matches the page topic and sections. | Headings are present but generic, skipped, or weakly organized. | Missing H1, multiple conflicting H1s, or headings hide/misstate the page topic. |
| Content quality | Page answers the search intent with specific, useful, current, people-first content. | Content is thin, overly generic, stale, or missing examples/evidence. | Content is misleading, automatically inflated, copied, or not useful for the stated intent. |
| Entity clarity | Page clearly identifies brand, product/service, audience, location/language, and differentiators. | Some entities are implied but not explicit. | Key entity is ambiguous or conflicts across title, schema, content, and metadata. |
| Source and trust signals | Claims are supported by sources, examples, dates, author/org identity, or verifiable product facts. | Some important claims need sources or clearer attribution. | Fabricated citations, fake metrics, unsupported rankings, or false authority claims. |
| Structured data | JSON-LD is valid, relevant, and matches visible content. | Schema is valid but minimal, incomplete, or could be more specific. | Schema is invalid, deceptive, or marks up invisible/unsupported claims. |
| Social metadata | Open Graph/Twitter metadata exists and matches the page. | Preview text or image is weak, missing, too generic, or wrong language. | Social preview misrepresents the page or uses broken assets. |
| Multilingual SEO | `lang`, canonical, hreflang, translated metadata, and language-specific content are consistent. | One language has weaker metadata or missing alternate link. | Hreflang/canonical sends users or crawlers to wrong language or wrong URL. |
| Internal linking | Page is reachable from navigation or relevant internal pages with descriptive anchors. | Page is reachable but weakly linked. | Orphaned page or conflicting navigation prevents discovery. |
| AI answer visibility | Page has clear answer blocks, factual atoms, source-backed claims, crawlable HTML, and concise summaries. | Page is crawlable but lacks direct answers, freshness, or citation-worthy statements. | Page relies on vague marketing copy, blocked crawlers, fabricated facts, or inaccessible content. |
| Measurement | Search Console, analytics, UTM/referral review, or AI visibility checks are defined. | Measurement exists but misses AI referrals, index coverage, or query tracking. | No measurement while claiming SEO/GEO impact. |

## AI Answer Visibility Signals

Positive signals:

- Clear, direct answers near the relevant section.
- Short definitions for important terms.
- Tables or lists that expose factual comparisons without burying the conclusion.
- Consistent entity names across title, headings, schema, links, and body copy.
- Checkable claims with sources, dates, product names, or first-party evidence.
- Fresh `lastmod` and visible update date when freshness matters.
- Crawlable HTML for core content, not only client-rendered text.
- Useful structured data that matches visible content.
- Public robots policy that allows the search/indexing bots the site wants to reach.

Risk signals:

- "Best", "number one", "guaranteed", or ranking claims without evidence.
- AI-specific promises such as "will appear in ChatGPT" without measurement.
- Vague page copy with no concrete nouns, facts, examples, or sourceable claims.
- Mismatch between schema, visible content, canonical, and language.
- Important content hidden in images, video, scripts, accordions that are not crawlable, or gated files.
- Thin pages that exist only to target an AI/search phrase.

## Recommended Fix Patterns

Technical fixes:

- Fix noindex/robots/canonical conflicts.
- Add or update sitemap URL and `lastmod`.
- Add reciprocal hreflang for language alternates.
- Ensure page returns `200` and important content is available in initial HTML.
- Validate JSON-LD and remove unsupported schema fields.

Editorial fixes:

- Shorten titles and descriptions while preserving intent.
- Add a direct answer paragraph after the H1 or before a complex section.
- Add factual tables for repeated entities, skills, tools, products, or service options.
- Add sources, dates, authorship, organization identity, and examples for load-bearing claims.
- Replace broad marketing claims with precise, verifiable statements.

AI visibility fixes:

- Add concise definitions and answer blocks that can be cited accurately.
- Separate facts from opinion, recommendation, and implementation steps.
- Include named entities and canonical terms users are likely to ask AI systems about.
- Document crawler policy for `OAI-SearchBot`, `GPTBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot`, `Claude-SearchBot`, and similar bots only when relevant to the site's governance.
- Set a measurement plan: Search Console queries, analytics referrals, UTM patterns where available, manual AI answer checks, and citation screenshots with dates.

## Decision Guidance

Use `BLOCK` when:

- The page cannot be indexed but the goal is search visibility.
- Canonical/hreflang can send users or crawlers to the wrong language or wrong page.
- Structured data or metadata is materially misleading.
- The page makes unsupported claims about rankings, AI citations, traffic, legal/compliance status, or product capabilities.

Use `REVISE` when:

- The page is indexable but metadata, structure, content, schema, or AI visibility can be materially improved.
- GEO claims need hedging or measurement.
- Content is useful but lacks direct answer sections, sources, or entity clarity.

Use `PASS` when:

- The page is crawlable, indexable, well structured, accurate, language-consistent, supported by evidence, and has a clear measurement path.
