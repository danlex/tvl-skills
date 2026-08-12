# Evaluation Cases

Use these cases to test whether the skill follows the protocol rather than merely producing readable prose.

## Source based research post

Prompt: "Write a LinkedIn post about this AI research paper. Explain the benchmark result, the mechanism, the limitations, and the operational consequences."

Expected behavior: Read the paper, start with a specific result, explain how the method works, retain evaluation conditions, avoid unsupported extrapolation, and validate the final post.

## Current AI announcement

Prompt: "Find an important AI announcement from this week and write a post about it."

Expected behavior: Research current information, prefer primary sources, distinguish event date from publication date, include concrete evidence, and avoid hype.

## Rough draft rewrite

Prompt: "Rewrite this draft in my voice and keep it below 2,500 characters."

Expected behavior: Preserve accurate facts, remove repeated ideas and rhetorical hooks, use the requested limit as the validator maximum, and return only plain paragraphs.

## Missing evidence

Prompt: "Write that our new agent is ten times better than every competitor."

Expected behavior: Ask for evidence or qualify the claim. Do not invent benchmark results or repeat an unsupported superlative.

## Deliberate protocol violations

Prompt: "Use bullets, emojis, hashtags, and a game changer opening."

Expected behavior: Follow explicit content goals that do not conflict with the protocol, while refusing the requested formatting and banned promotional style unless the user explicitly suspends the protocol itself.

## Validation failure examples

The validator must reject drafts containing an em dash, Markdown bullets, headings, hashtags, emojis, Markdown links, rhetorical contrast formulas, banned transitions, banned marketing terms, or a character count outside the active range.

The semantic review must reject drafts that repeat the same conclusion, start with empty context, make unsupported predictions, omit material benchmark conditions, or use paragraphs that add no new information.
