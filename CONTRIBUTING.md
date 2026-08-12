# Contributing

Contributions should keep every skill focused, self contained, and easy for another AI agent to apply.

## Requirements

1. Place each skill under `skills/<skill-name>/`.
2. Use lowercase letters, digits, and hyphens for the directory and frontmatter name.
3. Include a `SKILL.md` file with only `name` and `description` in its YAML frontmatter.
4. Keep detailed rules in `references/`, repeatable checks in `scripts/`, and output assets in `assets/`. A core protocol may also be embedded in `SKILL.md` when the skill must remain usable as a single file. Keep any reference copy synchronized.
5. Add or update automated tests for every deterministic behavior.
6. Run all tests and validate the skill structure before opening a contribution.

Avoid adding user documentation inside an individual skill folder. Put repository level documentation at the root.
