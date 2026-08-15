# TVL AI Skills

Open source Agent Skills for ChatGPT, Codex, Claude Code, and other compatible AI agents.

Each skill combines concise operating instructions with the references, scripts, and tests needed for repeatable results. The repository is structured as a monorepo so new skills can be added without changing the installation model.

## Available skills

| Skill | Purpose |
| --- | --- |
| [`tvl-write-linkedin-post`](skills/tvl-write-linkedin-post/) | Draft, rewrite, and validate technical LinkedIn posts using CROFTAFC and LinkedIn Writing Protocol v3. |
| [`tvl-design-diagram`](skills/tvl-design-diagram/) | Turn rough ideas, systems, workflows, and decision gates into clear Mermaid diagrams with an Ethical AI check. |
| [`tvl-ethical-ai-audit`](skills/tvl-ethical-ai-audit/) | Audit drafts, claims, citations, plans, and agent behavior for EthicalAI failure modes. |
| [`tvl-confirmation-bias-audit`](skills/tvl-confirmation-bias-audit/) | Audit conclusions for one-sided evidence, missing alternatives, and failure to falsify. |
| [`tvl-seo-geo-audit`](skills/tvl-seo-geo-audit/) | Audit pages for technical SEO, structured data, multilingual hygiene, and AI answer visibility. |

## Install

### Agent Skills CLI

The simplest public install path is the Agent Skills CLI:

```bash
npx skills add danlex/tvl-skills
```

Command grammar:

```bash
npx skills add <owner>/<repo> --skill <skill-name> --agent <agent>
```

- `npx`: runs the npm package command without a separate global install.
- `skills`: the Agent Skills CLI.
- `add`: installs skills from a package or GitHub repository.
- `danlex/tvl-skills`: the GitHub repository that contains the skills.
- `--skill`: optional; install one skill instead of every skill in the repo.
- `--agent`: optional; target a specific agent such as `claude-code` or `codex`.
- `--global`: optional; install user-wide instead of project-local.

Install one skill:

```bash
npx skills add danlex/tvl-skills --skill tvl-design-diagram
```

Install the Ethical AI judge:

```bash
npx skills add danlex/tvl-skills --skill tvl-ethical-ai-audit
```

Install the confirmation bias auditor:

```bash
npx skills add danlex/tvl-skills --skill tvl-confirmation-bias-audit
```

Install the SEO/GEO auditor:

```bash
npx skills add danlex/tvl-skills --skill tvl-seo-geo-audit
```

Install all skills globally for Claude Code:

```bash
npx skills add danlex/tvl-skills --agent claude-code --global --skill '*' -y
```

Verify a Claude Code install:

```bash
npx skills ls -g -a claude-code
```

### Codex

Codex loads user skills from `~/.agents/skills` and repository skills from `.agents/skills`.

Install all skills for the current user:

```bash
tmp="$(mktemp -d)" && git clone --depth 1 https://github.com/danlex/tvl-skills.git "$tmp" && mkdir -p ~/.agents/skills && cp -R "$tmp"/skills/* ~/.agents/skills/
```

Install one skill:

```bash
tmp="$(mktemp -d)" && git clone --depth 1 https://github.com/danlex/tvl-skills.git "$tmp" && mkdir -p ~/.agents/skills && cp -R "$tmp"/skills/tvl-design-diagram ~/.agents/skills/tvl-design-diagram
```

### Claude Code

Claude Code loads personal skills from `~/.claude/skills` and project skills from `.claude/skills`.

Install all skills for the current user:

```bash
tmp="$(mktemp -d)" && git clone --depth 1 https://github.com/danlex/tvl-skills.git "$tmp" && mkdir -p ~/.claude/skills && cp -R "$tmp"/skills/* ~/.claude/skills/
```

Install all skills into the current project:

```bash
tmp="$(mktemp -d)" && git clone --depth 1 https://github.com/danlex/tvl-skills.git "$tmp" && mkdir -p .claude/skills && cp -R "$tmp"/skills/* .claude/skills/
```

## Use the skills

Invoke a skill explicitly when you want consistent behavior.

### LinkedIn writing

```text
Use $tvl-write-linkedin-post to turn this paper into a 2,700 to 2,900 character LinkedIn post.
```

The skill extracts evidence through CROFTAFC, drafts the post, runs deterministic checks, performs semantic review, and rewrites any failed rule before returning the result.

The complete LinkedIn Writing Protocol v3 is embedded directly in `SKILL.md` so the main instruction file is self contained. A reference copy remains in `references/protocol-v3.md` for maintenance and review.

### Diagram design

```text
Use $tvl-design-diagram to turn this product flow into a Mermaid diagram.
```

The skill supports three diagram templates:

- `system-map`: components, actors, data stores, integrations, and outputs.
- `workflow`: ordered steps, handoffs, review loops, and final outputs.
- `decision-flow`: validation gates, branch conditions, and `PASS` / `FLAG` / `BLOCK` outcomes.

Before returning a diagram, the skill runs a lightweight Ethical AI check for hallucination, confabulation, sycophancy, confirmation bias, source fabrication, prompt injection, selective evidence, anchoring, and overconfidence.

### Ethical AI detection

```text
Use $tvl-ethical-ai-audit to audit this draft before I publish it.
```

The skill checks drafts, plans, claims, citations, summaries, and agent behavior against the EthicalAI failure modes from `ethicalai.alexandrudan.com`: hallucination, confabulation, source fabrication, narrativity drift, sycophancy, capitulation, confirmation bias, selective evidence, anchoring, automation bias, overconfidence, prompt injection, scope creep, and specification gaming. It returns a terse evidence-first report with `PASS`, `REVISE`, or `BLOCK`.

### Confirmation bias audit

```text
Use $tvl-confirmation-bias-audit to audit this root-cause conclusion for one-sided evidence.
```

The skill focuses on confirmation bias: whether the answer stated and tested the strongest alternative explanation, looked for disconfirming evidence, interpreted ambiguous evidence fairly, and calibrated certainty. It includes chatbot-specific audit modes and evaluation cases for interpersonal advice, health, shopping, code review, political framing, belief reinforcement, and incident triage. It returns a falsification-first audit with `PASS`, `REVISE`, or `BLOCK`.

Anonymized example patterns include: mistaking co-primed reviewer agreement for independent confirmation, treating generic website navigation as proof that a specific archive exists, declaring a best fix before measurement, declaring business payback from stacked assumptions, and generalizing a metric from one small sample while ignoring variance.

### SEO and GEO audit

```text
Use $tvl-seo-geo-audit to audit this page for technical SEO, structured data, multilingual hygiene, and AI answer visibility.
```

The skill audits indexability, canonical and hreflang, sitemap freshness, robots.txt, titles, descriptions, headings, structured data, Open Graph, content quality, entity clarity, source trust, and AI answer visibility. It treats GEO as an extension of good SEO: crawlable, clear, factual, source-backed content that can be understood and cited by search and AI answer systems. It returns `PASS`, `REVISE`, or `BLOCK` with prioritized fixes.

## Repository structure

```text
skills/
  tvl-design-diagram/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
  tvl-ethical-ai-audit/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
  tvl-confirmation-bias-audit/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
  tvl-seo-geo-audit/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
  tvl-write-linkedin-post/
    SKILL.md
    agents/openai.yaml
    assets/icon.svg
    references/
    scripts/
```

## Validate

Run the automated tests:

```bash
python3 skills/tvl-write-linkedin-post/scripts/test_validator.py
python3 skills/tvl-design-diagram/scripts/test_templates.py
python3 skills/tvl-ethical-ai-audit/scripts/test_audit.py
python3 skills/tvl-confirmation-bias-audit/scripts/test_confirmation_bias_audit.py
python3 skills/tvl-seo-geo-audit/scripts/test_seo_geo_audit.py
```

Validate a LinkedIn draft directly:

```bash
python3 skills/tvl-write-linkedin-post/scripts/validate_post.py draft.txt
```

Validate skill structure with the OpenAI skill creator utility when available:

```bash
python3 /path/to/quick_validate.py skills/tvl-write-linkedin-post
python3 /path/to/quick_validate.py skills/tvl-design-diagram
python3 /path/to/quick_validate.py skills/tvl-ethical-ai-audit
python3 /path/to/quick_validate.py skills/tvl-confirmation-bias-audit
python3 /path/to/quick_validate.py skills/tvl-seo-geo-audit
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the required skill structure and validation process.

Codex should follow [AGENTS.md](AGENTS.md) for repository rules. Use [CODEX_HANDOFF.md](CODEX_HANDOFF.md) for the one time GitHub publication workflow.

## License

This repository is available under the [MIT License](LICENSE).
