# SEO GEO Rubric

Use this rubric to audit whether a page is technically discoverable, understandable, trustworthy, accessible, and suitable for accurate extraction by search and AI answer systems. It checks prerequisites and evidence quality, not guaranteed rankings or citations.

## Scope Gates

| Mode | Applies to | Must not claim |
| --- | --- | --- |
| `PAGE` | One URL plus directly related assets such as canonical target, robots.txt, and declared sitemap. | Sitewide internal linking, Search Console performance, backlinks, Core Web Vitals field data, or full sitemap coverage. |
| `MULTILINGUAL_PAIR` | Two or more language URLs and their relationships. | Complete international SEO health beyond the supplied pair or sample. |
| `SITE_SAMPLE` | Declared sample of homepage, templates, navigation, robots, and sitemaps. | Exhaustive crawl conclusions outside the sample. |
| `CONTENT_BRIEF` | Unpublished content, metadata, outline, or source notes. | HTTP status, indexability, sitemap membership, crawler access, or live schema validation. |

For inaccessible URLs, offer a labelled framework-only audit and mark unfetched checks `NOT_TESTED` or `MISSING_TEST`.

## Audit Checks

| Check | Evidence needed | PASS | FLAG / REVISE | BLOCK |
| --- | --- | --- | --- | --- |
| HTTP and indexability | Status, final URL, redirect chain, robots meta, `X-Robots-Tag`, indexation intent. | Intended public URL resolves cleanly and allows indexing/snippets. | Redirects or intent need clarification; `nosnippet`, `max-snippet`, image-preview, or video-preview directives limit desired snippets. | Intended public page is broken, noindexed, disallowed in a way that prevents useful discovery, hidden behind auth, or blocked by header/meta conflict. |
| Canonical | Canonical URL, target status, target indexability, redirect chain, language and content similarity. | Canonical points to the correct indexable equivalent. | Canonical absent where duplication risk is real, or target should be validated. | Canonical points to wrong language, wrong domain, non-indexable URL, redirect loop, or materially different content. |
| Sitemap | Sitemap declaration, sitemap XML, URL membership, `lastmod`, canonical match. | URL membership and `lastmod` are accurate when sitemap evidence is in scope. | Missing from sitemap or `lastmod` unclear but page remains discoverable. | Sitemap misleads with wrong canonical URLs, invalid XML, or false significant-update signals. |
| Robots.txt | Robots file, relevant user-agent rules, sitemap declarations, intended crawler policy. | Relevant search crawlers can fetch intended public resources. | AI crawler policy is implicit or not tied to governance goals. | Desired search/AI discovery is impossible because relevant discovery bots are blocked, or private content is exposed contrary to intent. |
| Raw HTML versus rendered DOM | Initial HTML text, rendered DOM text when available, key content comparison. | Core content and JSON-LD needed for discovery are present or confirmed renderable. | Important content may depend on JavaScript and rendering was not available. | Core content is inaccessible to crawlers for the intended search/AI use case. |
| Title | Title text, uniqueness where evidence exists, intent match, display clarity. | Accurate, descriptive, concise enough for useful display. | Verbose, generic, duplicated, or weakly differentiated. | Misleading, stuffed, or contradicts visible content. |
| Meta description | Description text and consistency with page content. | Accurate summary that supports user understanding. | Missing, generic, duplicated, verbose, or underspecified. | Misleading or promises unsupported content. |
| Headings | H1-H3 hierarchy and visible content structure. | One clear primary topic and logical sections. | Generic, skipped, weakly organized, or multiple H1s without clear reason. | Headings hide or misstate the page topic. Missing H1 alone is not a blocker unless it materially misleads or breaks usability. |
| Content quality | Visible content, sources, dates, originality, examples, people-first usefulness. | Specific, useful, current, source-backed where needed. | Thin, stale, generic, missing examples, or missing important evidence. | Misleading, copied, automatically inflated, fabricated, or not useful for stated intent. |
| Entity clarity | Brand, product/service, person/org, location/language, audience, differentiators. | Key entities are explicit and consistent across page elements. | Some entities are implied but not explicit. | Key entity conflicts across title, schema, content, metadata, or language. |
| Source and trust signals | Citations, author/org identity, first-party facts, dates, evidence for claims. | Load-bearing claims are supported or framed as opinion. | Important claims need source, date, owner, or attribution. | Fabricated citations, fake metrics, unsupported rankings, false authority, or unverified AI citation guarantees. |
| Structured data | JSON-LD blocks, parser result, types, eligibility policy, visible-content consistency. | Valid, relevant, and consistent with visible content. | Valid but minimal, incomplete, or not eligible for the intended rich result. | Invalid, deceptive, or marks up invisible/unsupported claims. |
| Social metadata | Open Graph/Twitter metadata, image availability, language match. | Preview accurately represents the page. | Preview is missing, weak, wrong size, generic, or incomplete. | Preview misrepresents page or uses broken/misleading assets. |
| Multilingual SEO | `lang`, canonical, reciprocal hreflang, translated metadata, language-specific content. | Language and alternate relationships are reciprocal and consistent. | One language has weaker metadata or incomplete alternate declarations. | Canonical/hreflang sends crawlers or users to wrong language, wrong URL, or wrong region. |
| Internal linking | Navigation, anchors, same-site links in collected page or declared sample. | Page is reachable with descriptive anchors within the audited scope. | Reachable but weakly linked. | Orphaning or conflicting navigation prevents intended discovery, when site-sample evidence supports that conclusion. |
| Accessibility basics | Semantic landmarks, meaningful links, alt text for informative images, contrast/focus signals where inspectable. | Page is usable by people and machines in the checked areas. | Missing alt text, vague links, weak semantics, or likely contrast/focus issue needing browser/tool verification. | Accessibility issue materially prevents access to core content or task completion. |
| Lighthouse lab audit | Lighthouse JSON, Chrome DevTools Lighthouse report, or `scripts/run_lighthouse_audit.py` output for `performance`, `accessibility`, and `seo`. | Categories are measured and no material Lighthouse issue contradicts the audit. | Low score or material diagnostic in Performance, Accessibility, or SEO needs review; unavailable Lighthouse is `NOT_TESTED`. | A Lighthouse-confirmed issue materially prevents access, indexing, or task completion. Lighthouse score alone is not a blocker. |
| Core Web Vitals field data | CrUX, PageSpeed Insights field data, or Search Console evidence for LCP, INP, and CLS. | Field data meets current thresholds or no field data is applicable/available and labelled honestly. | Lab and field data diverge, field data is missing for a performance claim, or one metric needs improvement. | Severe field-data issue materially prevents access or task completion; score alone is not a blocker. |
| Bing and IndexNow | Bingbot policy, Bing Webmaster Tools export, IndexNow key/submission evidence, canonical/indexability of submitted URLs. | Bing visibility evidence is collected and aligned with intended policy. | Bing/IndexNow is useful but unverified, incomplete, or disconnected from canonical/sitemap policy. | Private, noindexed, noncanonical, or misleading URLs are submitted or optimized for Bing visibility against intent. |
| WCAG 2.2 accessibility mapping | WCAG 2.2 principle mapping, Lighthouse/axe/manual evidence, rendered DOM, keyboard/focus review when available. | Checked evidence supports Perceivable, Operable, Understandable, and Robust basics. | Automation finds issues or full conformance is unverified. | Core content or task completion is inaccessible in a way that materially blocks users. |
| Spam and abuse policy | Content purpose, originality, scaled/automated content patterns, doorway behavior, expired-domain/site-reputation signals, cloaking evidence. | No evidence of spam-policy risk in the audited scope. | Content pattern or governance needs review for people-first quality. | Evidence indicates scaled content abuse, cloaking, doorway behavior, fake reputation borrowing, or other serious policy violation. |
| Rich result eligibility by page type | Page type, structured-data profile, required/recommended fields, visible-content match, rich-result validation where available. | Schema profile is eligible, valid, and content-consistent. | Schema is incomplete, generic, or validation is unavailable. | Schema profile is deceptive, ineligible for the visible page, or marks up unsupported claims. |
| Image SEO deep check | Image purpose, alt text, filenames, captions/surrounding text, dimensions, compression, lazy loading, image structured data or sitemap when important. | Important images are discoverable, accessible, and performance-aware. | Image metadata, compression, dimensions, or lazy-loading behavior need improvement. | Core content exists only in inaccessible images or images materially block performance/accessibility. |
| Video SEO deep check | Video accessibility, public fetchability, transcript/captions, thumbnail, `VideoObject`, key moments, `max-video-preview`, video file access. | Important videos are discoverable and have sufficient text alternatives. | Video metadata, captions, transcript, thumbnails, or structured data need improvement. | Core content exists only in inaccessible video or crawler/user access is blocked against intent. |
| External citation and source-link integrity | Outbound source URLs, status, relevance, claim-to-source match, date/freshness, source authority for the claim. | Load-bearing external citations are reachable and support the claims. | Source is stale, weak, indirect, broken, or does not fully support the claim. | Fabricated, broken, irrelevant, or contradictory source supports a material claim. |
| SERP or cited-source comparison | Search/citation sample, target query, sources currently ranking/cited, passage comparison, source dates. | Optional comparison is measured and scoped to the query/source sample. | Comparison is unavailable or shows structural/evidence gaps. | Report claims competitive/citation superiority without measured evidence. |
| Log-based crawler verification | Server/CDN logs, verified bot requests, user-agent/IP verification, timestamp, URL, status. | Relevant crawlers are observed as intended in logs. | Logs unavailable, incomplete, or show crawl gaps. | Logs prove relevant crawlers are blocked or receiving wrong status for intended public pages. |
| AI answer visibility | Crawlable text, direct answers, definitions, factual atoms, source-backed claims, freshness, engine target. | Content is understandable and extractable, with no unsupported AI-visibility claims. | Readability/extractability can improve through definitions, tables, examples, and source-backed statements. | Page relies on vague marketing, fabricated facts, blocked relevant discovery bots, or inaccessible core content. |
| Measurement | Search Console, analytics, AI referral review, dated manual checks, or user-provided exports. | Measurement plan or evidence matches the claims made. | Measurement exists but misses index coverage, query tracking, AI referrals, or date/source. | SEO/GEO impact, ranking, traffic, or AI citation claims are made with no measurement. |
| `llms.txt` and RSL | `llms.txt`, `/.well-known/rsl.json`, `/RSL.txt`, or explicit absence. | Presence or absence is documented without ranking claims. | File exists but its purpose, freshness, or governance stance is unclear. | File is presented as required for Google rankings or AI citations, or conflicts with governance intent. |

## Evidence Coverage

Core checks for URL audits:

1. HTTP/final URL.
2. Robots meta.
3. `X-Robots-Tag`.
4. Canonical.
5. Indexation intent.

`PASS` requires all applicable core checks to be `CONFIRMED` or explicitly not applicable for the declared mode. Missing core evidence rolls up to `REVISE`, not `PASS`.

## Blocker Categories

- `INDEXING_BLOCKER`: status, noindex, X-Robots-Tag, robots/crawl policy, canonical, rendering, or snippet control prevents intended discovery.
- `TRUST_BLOCKER`: fabricated citations, false authority, fake metrics, unsupported rankings, or misleading claims.
- `MULTILINGUAL_BLOCKER`: hreflang/canonical/language conflict that sends users or crawlers to the wrong page.
- `STRUCTURED_DATA_BLOCKER`: deceptive or invalid structured data that misrepresents visible content.
- `PUBLICATION_BLOCKER`: private, regulated, pre-launch, or non-indexed content being optimized for public visibility against intent.

Do not classify a missing H1, long title, missing optional schema property, or weak social preview as a blocker by itself.

## AI Answer Visibility Signals

Positive signals:

- Complete answer passages in one to three sentences.
- The passage answers the question implied by its parent heading.
- Named entities, dates, numbers, product names, methods, or concrete examples.
- Clear freshness signal where freshness matters.
- Source-backed factual claims and visible organization identity.
- Core content available as text.

Risk signals:

- "Best", "number one", "guaranteed", "will appear in ChatGPT", or similar claims without evidence.
- Vague marketing copy with no concrete nouns, examples, or sourceable claims.
- Important content hidden only in media, scripts, inaccessible widgets, or gated files.
- Schema, metadata, canonical, language, and visible content mismatch.

Engine targeting:

- Google AI features follow Google Search fundamentals; there is no special AI markup requirement.
- ChatGPT, Claude, and Perplexity have separate crawler/fetcher policies. Use [crawler-policy.md](crawler-policy.md).
- Comparative citation analysis is optional and requires search/citation evidence. Without that access, label competitor/cited-source comparisons `NOT_TESTED`.

## Tool Fallbacks

When a check cannot be performed, name the tool or evidence that can assess it:

- Rendered DOM: browser automation, Playwright, Chrome DevTools, or a rendering crawler.
- Lighthouse lab checks: `scripts/run_lighthouse_audit.py`, Chrome DevTools Lighthouse panel, Lighthouse CLI, Lighthouse CI, or PageSpeed Insights. Use categories `performance`, `accessibility`, and `seo`.
- Core Web Vitals field data: PageSpeed Insights, CrUX, or Search Console.
- Bing and IndexNow: Bing Webmaster Tools, Bingbot logs, IndexNow key/submission logs, or API output.
- Search performance: Search Console export or verified property access.
- WCAG 2.2: Lighthouse, axe, manual keyboard review, accessibility tree, screen-reader/manual QA.
- Backlinks/off-page mentions: backlink index or search/citation sample. Off-page is out of default scope unless explicitly requested.
- Structured data eligibility: Google Rich Results Test or Schema.org validator, plus visible-content review.
- Accessibility: Lighthouse, axe, manual keyboard check, contrast tool.
- Crawler logs: server logs, CDN logs, verified bot IP/user-agent checks.

## Recommended Fix Patterns

Technical:

- Resolve noindex, `X-Robots-Tag`, canonical, hreflang, and robots conflicts.
- Compare raw HTML and rendered DOM for JavaScript-heavy pages.
- Separate Lighthouse lab results from Core Web Vitals field data.
- Validate Bing/IndexNow discovery only when Bing-specific evidence exists.
- Make core content available in initial HTML or verified rendered output.
- Validate JSON-LD and remove unsupported fields.
- Use sitemap `lastmod` only for significant content, structured-data, or link changes.

Editorial:

- Make titles and descriptions accurate, concise, and differentiated without fixed character rules.
- Add direct definitions, examples, tables, and answer passages when they improve user comprehension.
- Add sources, dates, authorship, organization identity, and examples for load-bearing claims.
- Verify source links and ensure each source actually supports the claim it is attached to.
- Replace broad marketing claims with precise, verifiable statements.

Governance:

- Decide crawler policy by search visibility, model-training, user-triggered retrieval, privacy, and ownership goals.
- Do not recommend allowing every AI crawler by default.
- Check spam-policy risk for scaled pages, third-party hosted content, expired-domain reuse, doorway pages, and cloaking when signals are present.
- Document measurement rather than promising outcomes.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Auditing from the user's description as if it were verified page evidence. | Fetch the page or label the check `USER_PROVIDED` / `NOT_TESTED`. |
| Reporting metadata improvements before checking indexability. | Run core indexability first. |
| Treating self-reported facts as verification. | Keep `USER_PROVIDED` provenance. |
| Declaring schema absent from raw HTML on a JS-rendered site. | Check rendered DOM or label `NOT_TESTED`. |
| Making sitewide claims from one URL. | Use `SITE_SAMPLE` or limit the conclusion to `PAGE`. |
| Recommending `llms.txt` as a Google ranking factor. | State that Google does not require it and ignores it for Search visibility. |
| Manufacturing issues on a healthy page. | Preserve useful uncertainty and return `PASS` when evidence supports it. |
