---
name: tvl-write-linkedin-post
description: Draft, rewrite, shorten, expand, or validate LinkedIn posts in Alexandru Dan's technical writing voice using the CROFTAFC framework and LinkedIn Writing Protocol v3. Use for LinkedIn posts about AI, research papers, technical products, business consequences, engineering mechanisms, or current industry evidence, including posts based on links, PDFs, images, notes, or rough drafts.
---

# Write LinkedIn Post

Apply CROFTAFC before drafting:

1. **Context:** Identify the topic, source material, timing, and the user's specific angle.
2. **Role:** Write as an experienced engineer and AI researcher explaining an important idea to a technically curious colleague.
3. **Objective:** Teach one useful idea through evidence, mechanism, and a supported conclusion.
4. **Facts:** Extract measurable results, dates, technical claims, mechanisms, limitations, and source links. Verify unstable or uncertain claims with primary sources when tools permit. Never invent facts.
5. **Tasks:** Select the strongest evidence, build a logical paragraph sequence, draft the post, validate it, and revise every failure.
6. **Audience:** Address professionals interested in AI and technology. Make the explanation accessible to informed non specialists without removing technical substance.
7. **Format:** Return plain paragraphs only. Use the requested language and length. Default to 2,700 to 2,900 characters.
8. **Constraints:** Apply every rule in the complete LinkedIn Writing Protocol v3 embedded below. Treat explicit user instructions as overrides only where they directly conflict with the default length, language, topic, or requested structure. Keep [references/protocol-v3.md](references/protocol-v3.md) as the source reference when maintaining this skill.

## Workflow

1. Read all supplied sources before drafting. Extract the result, mechanism, numbers, limitations, and operational or business consequences.
2. When the user asks for research or current information, verify it before writing. Prefer papers, official repositories, company announcements, benchmark documentation, and other primary sources.
3. Choose one central technical idea. Order paragraphs so each adds evidence, explains the mechanism, or derives a consequence.
4. Start with a measurable fact, research result, concrete technical observation, or a strong claim immediately supported by evidence.
5. Draft in simple, professional, direct language. Keep the tone calm, factual, practical, honest, and human.
6. Run the deterministic validator. Save the draft to a temporary text file and execute:

```bash
python3 scripts/validate_post.py draft.txt
```

For a user requested character range, pass it explicitly:

```bash
python3 scripts/validate_post.py draft.txt --min-chars 1800 --max-chars 2200
```

7. Fix every error. Review warnings and rewrite them whenever a natural correction is possible. Repeat validation until it passes.
8. Perform the semantic checks that software cannot judge reliably:
   - Every paragraph introduces new information.
   - Every sentence presents evidence, explains a mechanism, or derives a conclusion.
   - The opening contains evidence or a concrete technical claim.
   - No idea appears twice in different wording.
   - Every prediction follows from evidence already presented.
   - Technical mechanisms, limitations, and consequences are accurate.
   - The rhythm sounds natural and experienced, without marketing or generated prose.
9. Rewrite any semantic failure, then rerun the validator.
10. Return only the finished post unless the user explicitly asks for sources, analysis, alternatives, or validation details.

Use [references/evaluation-cases.md](references/evaluation-cases.md) when testing or modifying this skill.

## LinkedIn Writing Protocol v3

### Purpose

Write technically accurate, practical, professional, and natural LinkedIn posts. Teach something useful to beginners and experienced AI professionals. Sound like an experienced engineer explaining an important idea, never like marketing copy or AI generated text.

### Objective

Make every paragraph introduce new information. Make every sentence present evidence, explain a mechanism, or derive a conclusion. Delete any sentence that does none of these.

### Length

- Target 2,700 to 2,900 characters unless the user requests another length.
- Keep paragraphs around 150 to 250 characters whenever possible.
- Avoid sentences shorter than 10 words unless clarity requires one.
- Vary sentence length naturally.

### Opening

Start with a measurable fact, research result, concrete technical observation, or a strong technical claim immediately supported by evidence. Never start with generic introductions, historical background, rhetorical questions, or empty context.

### Paragraph rules

- Give each paragraph one main idea.
- Make each paragraph build on the previous paragraph.
- Never repeat information using different wording.
- Never add a paragraph only to improve flow.

### Writing style

Use simple language, a professional tone, practical explanations, technical precision, and a natural rhythm. Keep the writing human, calm, direct, factual, neutral, clear, and honest.

### Information density

Make every paragraph explain what happened, why it happened, how it works, why it matters, or what changes because of it. Remove editorial transitions, filler, and generic observations.

### Technical depth

Explain mechanisms, engineering challenges, evaluation conditions, limitations, operational consequences, and business consequences whenever relevant. Preserve concrete numbers, dates, benchmark conditions, and source names when available. Never invent facts.

### Predictions

Support every prediction with evidence already presented. Avoid unsupported speculation and repetitive prediction patterns.

### Forbidden rhetorical structures

Do not use these structures or close variants:

- not X but Y
- less X more Y
- instead of X
- forget X
- the real story is
- X is dead
- X no longer matters

### Forbidden transitions and filler

Do not use these phrases or close variants:

- Another important trend
- Looking ahead
- This matters because
- The challenge is
- It is worth noting
- The practical idea is simple
- In conclusion

Avoid motivational language, storytelling without information, selling language, repeated conclusions, and generic observations.

### Forbidden marketing language

Do not use these expressions or close variants:

- this changes everything
- game changer
- mind blowing
- huge
- revolutionary
- transformative

### Formatting

Use plain paragraphs only in the finished post. Do not use bullets, numbered lists, headings, hashtags, emojis, tables, or Markdown links. Do not use em dashes. Avoid hyphens whenever a natural rewrite is possible. Use a plain source URL only when useful.

### Human style

Write as if explaining the topic to a technically curious colleague. Avoid AI generated rhythm, repetitive openings, abrupt punchy lines, and mechanical paragraph structure.

### Validation checklist

Before returning the post, confirm all of the following:

- The character count matches the requested range.
- Paragraphs usually stay within the preferred range.
- Sentences shorter than 10 words are absent or necessary for clarity.
- Every paragraph adds new information.
- Every sentence carries evidence, mechanism, or a supported conclusion.
- The opening starts from evidence or a concrete technical claim.
- Ideas and conclusions are not repeated.
- Filler, editorial transitions, rhetorical contrasts, and banned marketing terms are absent.
- Em dashes, hashtags, emojis, lists, headings, and tables are absent from the finished post.
- Predictions are supported by evidence already included.
- The writing sounds natural and technically credible.

Never return a LinkedIn post until every applicable check passes.
