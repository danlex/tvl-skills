# Crawler Policy

Use crawler policy to align the site owner's goals with search discovery, model-training, user-triggered retrieval, privacy, and governance. Do not recommend allowing every AI bot by default.

Verified as of: 2026-08-16

| Provider | Agent | Purpose | Robots behavior | Visibility implication | Default audit stance |
| --- | --- | --- | --- | --- | --- |
| OpenAI | `OAI-SearchBot` | Search discovery and linking in ChatGPT search experiences. | Uses robots policy. | Relevant to ChatGPT search visibility. | Allow only if ChatGPT search visibility is desired. |
| OpenAI | `GPTBot` | Model-training crawl. | Uses robots policy. | Independent from search visibility. | Governance decision; do not require for GEO. |
| OpenAI | `ChatGPT-User` | User-triggered retrieval. | Separate user-agent behavior for user requests. | Relevant to user-directed retrieval, not automatic indexing. | Allow only if user-triggered retrieval is desired. |
| Anthropic | `Claude-SearchBot` | Search discovery and result quality for Claude search responses. | Uses robots policy. | Relevant to Claude search visibility. | Allow only if Claude search visibility is desired. |
| Anthropic | `ClaudeBot` | Model-training or model-improvement crawl. | Uses robots policy and Anthropic crawler controls. | Independent from search visibility. | Governance decision; do not require for GEO. |
| Anthropic | `Claude-User` | User-triggered retrieval. | Provider-specific user request fetcher. | Relevant to user-directed retrieval. | Allow only if user-triggered retrieval is desired. |
| Perplexity | `PerplexityBot` | Search discovery and website surfacing in Perplexity. | Uses robots policy. | Relevant to Perplexity search visibility. | Allow only if Perplexity visibility is desired. |
| Perplexity | `Perplexity-User` | User-triggered retrieval. | Perplexity documents that it generally ignores robots.txt because the user requested the fetch. | Independent from automatic crawling; relevant to user-directed retrieval. | Treat as retrieval governance, not crawler discovery. |

## Decision Structure

Ask:

1. Should this page be public and indexed?
2. Should it be discoverable in AI search experiences?
3. Should it be available for model-training crawlers?
4. Should user-triggered fetchers be allowed to retrieve it?
5. Are there privacy, licensing, compliance, or customer-data restrictions?

Report crawler recommendations as policy choices, not universal SEO rules.
