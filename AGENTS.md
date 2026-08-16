# Repository Instructions for Codex

## Scope

Maintain a public monorepo of reusable AI skills. Preserve the existing `skills/<skill-name>/` structure and keep every skill self contained.

## Required behavior

1. Read the relevant `SKILL.md` before modifying a skill.
2. Preserve YAML frontmatter with only `name` and `description`.
3. Keep deterministic checks in `scripts/`, detailed supporting material in `references/`, interface metadata in `agents/`, and output assets in `assets/`.
4. Update tests whenever deterministic behavior changes.
5. Run validation and tests before committing.
6. Do not remove the protocol, validator, tests, evaluation cases, licence, or GitHub Actions workflow.
7. Do not force push, rewrite published history, or discard unrelated user changes.

## Validation commands

Run from the repository root:

```bash
python3 skills/tvl-write-linkedin-post/scripts/test_validator.py
python3 skills/tvl-write-linkedin-post/scripts/validate_post.py --help
python3 skills/tvl-design-diagram/scripts/test_templates.py
python3 skills/tvl-ethical-ai-audit/scripts/test_audit.py
python3 skills/tvl-confirmation-bias-audit/scripts/test_confirmation_bias_audit.py
python3 skills/tvl-seo-geo-audit/scripts/test_seo_geo_audit.py
python3 skills/tvl-build-free-website/scripts/test_free_website_skill.py
```

When the OpenAI skill validation utility is available, also run:

```bash
python3 /root/.codex/skills/oai/skill-creator/scripts/quick_validate.py \
  skills/tvl-write-linkedin-post
python3 /root/.codex/skills/oai/skill-creator/scripts/quick_validate.py \
  skills/tvl-design-diagram
python3 /root/.codex/skills/oai/skill-creator/scripts/quick_validate.py \
  skills/tvl-ethical-ai-audit
python3 /root/.codex/skills/oai/skill-creator/scripts/quick_validate.py \
  skills/tvl-build-free-website
```

## Publication rules

Use `main` as the default branch. Publish to `https://github.com/danlex/tvl-skills`. Check whether the repository exists before creating it. Never overwrite a different existing repository. Commit only the intended repository files, push without force, then verify public access and the GitHub Actions result.
