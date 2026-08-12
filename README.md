# Alexandru Dan's AI Skills

Open source skills for ChatGPT, Codex, Claude, and other compatible AI agents.

Each skill combines concise operating instructions with the references, scripts, and tests needed for repeatable results. The repository is structured as a monorepo so new skills can be added without changing the installation model.

## Available skills

| Skill | Purpose |
| --- | --- |
| [`write-linkedin-post`](skills/write-linkedin-post/) | Draft, rewrite, and validate technical LinkedIn posts using CROFTAFC and LinkedIn Writing Protocol v3. |

## Install a skill

### ChatGPT and Codex

Download the selected folder and add it from the Skills page. The folder must preserve `SKILL.md` and its supporting directories.

For a local Codex installation, copy the skill into your personal skills directory:

```bash
git clone https://github.com/danlex/skills.git
mkdir -p ~/.codex/skills
cp -R skills/skills/write-linkedin-post ~/.codex/skills/write-linkedin-post
```

### Claude Code

Copy the selected folder into your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -R skills/skills/write-linkedin-post .claude/skills/write-linkedin-post
```

## Use the first skill

Invoke it explicitly when you want consistent behavior:

```text
Use $write-linkedin-post to turn this paper into a 2,700 to 2,900 character LinkedIn post.
```

The skill extracts evidence through CROFTAFC, drafts the post, runs deterministic checks, performs semantic review, and rewrites any failed rule before returning the result.

The complete LinkedIn Writing Protocol v3 is embedded directly in `SKILL.md` so the main instruction file is self contained. A reference copy remains in `references/protocol-v3.md` for maintenance and review.

## Repository structure

```text
skills/
  write-linkedin-post/
    SKILL.md
    agents/openai.yaml
    assets/icon.svg
    references/
    scripts/
```

## Validate

Run the skill's automated tests:

```bash
cd skills/write-linkedin-post/scripts
python3 -m unittest test_validator.py
```

Validate a draft directly:

```bash
python3 skills/write-linkedin-post/scripts/validate_post.py draft.txt
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the required skill structure and validation process.

Codex should follow [AGENTS.md](AGENTS.md) for repository rules. Use [CODEX_HANDOFF.md](CODEX_HANDOFF.md) for the one time GitHub publication workflow.

## License

This repository is available under the [MIT License](LICENSE).
