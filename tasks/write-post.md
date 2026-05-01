# write-post

## Goal
Draft a referenced post about the role of skills, tasks, references, and evals in agent workflows.

## Reader / Owner
Builders designing personal-agent or agent-workflow systems; Chan as owner/reviewer.

## Current Stage
review

## Current Slice
Drafted `_posts/2026-05-01-skills-tasks-references-evals.md` with supporting references and ran structural verification.

## Done
- Loaded `write-post` workflow state and references.
- Gathered support from OpenClaw docs (`concepts/system-prompt.md`, `automation/tasks.md`, `automation/standing-orders.md`) and external Anthropic/OpenAI references.
- Packaged the angle: skills are recipes, tasks are receipts, references are libraries, evals are behavioral pressure.
- Wrote `_posts/2026-05-01-skills-tasks-references-evals.md`.
- Included one compact Mermaid flow and seven reference footnotes.
- Ran structural checks for frontmatter, description, Mermaid block, references section, footnote count, banned literal Want/Need/Get headings, word-count range, and trailing whitespace.

## Blocker
Full Jekyll build has not been run in this workspace; previous local state showed no `Gemfile`/`jekyll` build path.

## Next Action
Chan review, then tighten or adjust the angle/references if needed.

## Last Verified State
2026-05-01: `python3` structural check passed for `_posts/2026-05-01-skills-tasks-references-evals.md` — file exists, frontmatter/title/description present, Mermaid present, references heading present, 7+ footnote definitions, no literal `## Want`/`## Need`/`## Get` headings, 1780 words. Trailing-whitespace check passed. `git status --short` shows the post as untracked.
