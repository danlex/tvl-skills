# Codex Handover: Publish `danlex/tvl-skills`

## Goal

Publish this prepared monorepo as the public GitHub repository `danlex/tvl-skills`. Its first package is `tvl-write-linkedin-post`, built around CROFTAFC and LinkedIn Writing Protocol v3.

## Source

Use the existing repository at:

```text
/workspace/scratch/532f1917f2ad/skills
```

Preserve the current structure. Do not rebuild the repository unless validation identifies a concrete defect.

## Required contents

- `skills/tvl-write-linkedin-post/SKILL.md`, including CROFTAFC and the complete embedded protocol
- `skills/tvl-write-linkedin-post/references/protocol-v3.md`
- `skills/tvl-write-linkedin-post/references/evaluation-cases.md`
- `skills/tvl-write-linkedin-post/scripts/validate_post.py`
- `skills/tvl-write-linkedin-post/scripts/test_validator.py`
- `skills/tvl-write-linkedin-post/agents/openai.yaml`
- `skills/tvl-write-linkedin-post/assets/icon.svg`
- `README.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `AGENTS.md`
- `.github/workflows/validate.yml`

## CROFTAFC requirement

Confirm that the operational instructions cover all eight fields:

1. Context
2. Role
3. Objective
4. Facts
5. Tasks
6. Audience
7. Format
8. Constraints

## Validate before publication

Run from the repository root:

```bash
git status --short --branch
python3 skills/tvl-write-linkedin-post/scripts/test_validator.py
python3 /root/.codex/skills/oai/skill-creator/scripts/quick_validate.py \
  skills/tvl-write-linkedin-post
```

All checks must pass. Review the diff and preserve unrelated changes.

```bash
git diff --check
git diff --stat
git diff
```

## Commit the prepared changes

Stage only the intended files, then create one focused commit:

```bash
git add AGENTS.md CODEX_HANDOFF.md README.md CONTRIBUTING.md \
  .github/workflows/validate.yml skills/tvl-write-linkedin-post
git status --short
git commit -m "Publish CROFTAFC LinkedIn writing skill"
```

If there is nothing to commit, continue with the existing commit. Never amend an unrelated commit.

## Create or connect the GitHub repository

First confirm authentication and check whether the destination exists:

```bash
gh auth status
gh repo view danlex/tvl-skills --json nameWithOwner,visibility,url,defaultBranchRef
```

If `danlex/tvl-skills` does not exist, create it from this local repository:

```bash
gh repo create danlex/tvl-skills --public --source=. --remote=origin --push
```

If it already exists and is the intended repository, configure the remote only when needed:

```bash
git remote -v
git remote add origin https://github.com/danlex/tvl-skills.git
git push -u origin main
```

If `origin` exists with a different URL, stop and report the mismatch. Do not replace it silently. Never force push.

## Verify publication

Confirm the branch, public visibility, files, and workflow:

```bash
git status --short --branch
git ls-remote --heads origin main
gh repo view danlex/tvl-skills --json nameWithOwner,visibility,url,defaultBranchRef
gh run list --repo danlex/tvl-skills --limit 5
```

If a validation run is in progress, wait for that run and confirm its conclusion:

```bash
run_id="$(gh run list --repo danlex/tvl-skills --workflow validate.yml \
  --limit 1 --json databaseId --jq '.[0].databaseId')"
test -n "$run_id"
gh run watch "$run_id" --repo danlex/tvl-skills --exit-status
```

Return the final URL `https://github.com/danlex/tvl-skills`, the published commit, validation results, and GitHub Actions status. Report any authentication, permission, remote mismatch, or workflow failure without bypassing safeguards.
