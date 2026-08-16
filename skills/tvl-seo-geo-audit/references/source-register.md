# Source Register

Prefer official platform guidance. Review this register when crawler names, robot behavior, Search documentation, or GEO guidance may have changed.

Review window: 180 days

| Source | URL | Topic supported | Last verified | Notes |
| --- | --- | --- | --- | --- |
| Google Search Central: AI optimization guide | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | No special AI markup, no Google need for `llms.txt`, no artificial chunking requirement, people-first content. | 2026-08-16 | Google says regular SEO fundamentals apply and special machine-readable files are not required for Google Search. |
| Google Search Central: AI features and your website | https://developers.google.com/search/docs/appearance/ai-features | AI features eligibility, snippet controls, Search Console measurement. | 2026-08-16 | AI features use Search fundamentals; no additional technical requirements. |
| Google Search Central: title links | https://developers.google.com/search/docs/appearance/title-link | Title display and no fixed title length limit. | 2026-08-16 | Titles may be truncated by device/display width; use concise descriptive titles. |
| Google Search Central: build and submit a sitemap | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap | Sitemap `lastmod` significant update guidance. | 2026-08-16 | `lastmod` should reflect significant page updates, not arbitrary deployment timestamps. |
| Google Search Central: robots meta tag and X-Robots-Tag | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | Robots meta, `X-Robots-Tag`, noindex, nosnippet, max-snippet, preview directives. | 2026-08-16 | Header directives can apply to non-HTML resources and page responses. |
| Google Search Central: robots.txt introduction | https://developers.google.com/search/docs/crawling-indexing/robots/intro | Robots.txt controls crawling, not guaranteed indexing. | 2026-08-16 | Use noindex or access control to keep a page out of Search. |
| OpenAI crawler documentation | https://developers.openai.com/api/docs/bots | `OAI-SearchBot`, `GPTBot`, `ChatGPT-User` purposes and independence. | 2026-08-16 | Search discovery and model-training crawlers can be controlled separately. |
| Anthropic crawler guidance | https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler | `Claude-SearchBot`, `ClaudeBot`, `Claude-User` crawler/fetcher purposes. | 2026-08-16 | Anthropic documents separate bots for search, model improvement, and user-triggered retrieval. |
| Perplexity crawler documentation | https://docs.perplexity.ai/docs/resources/perplexity-crawlers | `PerplexityBot`, `Perplexity-User` purposes and robots behavior. | 2026-08-16 | `PerplexityBot` is for search discovery; `Perplexity-User` is user-triggered retrieval. |
