# WCAG 2.2 Accessibility Checks

Use WCAG 2.2 as the accessibility reference. Lighthouse and axe can provide evidence, but they do not prove full WCAG conformance by themselves.

Verified as of: 2026-08-16

## Principles

| Principle | Audit focus | Evidence |
| --- | --- | --- |
| Perceivable | Text alternatives, captions/transcripts, adaptable layout, contrast, resize/reflow. | HTML, media assets, rendered page, Lighthouse, axe, manual visual review. |
| Operable | Keyboard access, focus order, visible focus, no traps, enough time, headings and labels. | Browser/manual keyboard pass, rendered DOM, automated accessibility report. |
| Understandable | Page language, predictable navigation, clear labels, error messages where forms exist. | HTML `lang`, form labels, visible copy, interaction review. |
| Robust | Semantic HTML, valid ARIA, assistive-technology-compatible patterns. | DOM inspection, accessibility tree, axe/Lighthouse diagnostics. |

## Report Rules

- Label accessibility automation as `MEASURED` lab evidence.
- Label full WCAG conformance as `UNVERIFIABLE` unless a complete manual accessibility audit was performed.
- Do not use a high Lighthouse accessibility score as proof of compliance.
- Treat core-content accessibility blockers as `PUBLICATION_BLOCKER` or `INDEXING_BLOCKER` only when they materially prevent access, understanding, or task completion.
