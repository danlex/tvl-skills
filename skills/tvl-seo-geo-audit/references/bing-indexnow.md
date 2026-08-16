# Bing and IndexNow Checks

Use these checks when the user asks about Bing, Microsoft search experiences, Copilot-style visibility, faster discovery, or broader search ecosystem coverage.

Verified as of: 2026-08-16

## Bing Visibility

Evidence to collect when available:

- Bingbot crawl permission in `robots.txt`.
- Indexability basics: status, canonical, noindex, `X-Robots-Tag`, sitemap.
- Bing Webmaster Tools export or screenshots, if user-provided.
- Whether the page is publicly accessible and not blocked by authentication or governance policy.

Rules:

- Do not claim Copilot visibility from a generic SEO audit.
- If Bing evidence is unavailable, label it `NOT_TESTED`.
- Treat Bing indexing as a separate ecosystem from Google indexing.
- Keep IndexNow as discovery/submission support, not a ranking guarantee.

## IndexNow

Evidence to collect when relevant:

- Whether the site declares or documents IndexNow usage.
- Whether an IndexNow key file is hosted when submission evidence is provided.
- Whether the URL was submitted through IndexNow, if the user provides logs or API output.
- Whether submitted URLs are canonical and indexable.

Report as:

- `PASS`: IndexNow setup/submission evidence is present and URLs are canonical/indexable.
- `REVISE`: IndexNow is useful for freshness but missing, unverifiable, or not connected to sitemap/canonical policy.
- `BLOCK`: submitted URLs are private, noncanonical, noindexed, or misleading.

Do not submit URLs automatically unless the user explicitly asks and the skill has safe authenticated access.
