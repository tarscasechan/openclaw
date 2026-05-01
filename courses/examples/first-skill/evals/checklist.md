# First Skill Eval Checklist

Passes if:

- Folder is named `tldr-skill/`.
- File is named `SKILL.md`.
- Frontmatter starts and ends with `---`.
- `name:` is stable and machine-friendly.
- `description:` begins with `Use when...` or equivalent trigger language.
- Skill has one obvious response pattern.
- Skill includes a caveat/uncertainty slot.
- Skill has one happy-path prompt.
- Skill has one miss prompt.
- Skill does not require tools, secrets, accounts, private paths, or user memory.
- Copying the folder preserves all needed context.

Fails if:

- The description is too vague, like “A summary skill.”
- The skill requires local credentials, user memory, or machine paths.
- There is no visible way to tell it triggered.
- The summary can overstate uncertain input without a caveat.