# write-post

## Goal
Draft and test a new post using the updated writing workflow.

## Reader / Owner
Builders using AI writing assistants; Chan as owner/reviewer.

## Current Stage
read-aloud / review

## Current Slice
Ran taste/read-aloud pass for `What Makes AI Writing Feel Fake`; attempted site build.

## Done
- Compared candidate topic against existing `_posts` and chose a non-overlapping angle.
- Set voice: first-person operator/editor speaking to builders who use AI writing tools.
- Picked hook: `The problem with AI prose is not that it sounds robotic. It sounds too finished too early.`
- Used before/after as the earned demo format.
- Wrote `_posts/2026-04-30-what-makes-ai-writing-feel-fake.md`.
- Ran a taste/read-aloud pass and tightened several lines; current draft is 959 words.

## Blocker
Full Jekyll build could not run locally because `jekyll` is not installed and there is no `Gemfile` for `bundle exec jekyll build`.

## Next Action
Chan review, or add a local Jekyll/Gemfile build path if we want build verification on every post.

## Last Verified State
2026-04-30: verification command passed for `_posts/2026-04-30-what-makes-ai-writing-feel-fake.md` — file exists, frontmatter/title/description present, before/after demo present, no literal Want/Need/Get headings, no banned `AI landscape` phrase, 959 words. Frontmatter shape check passed. `git diff --check` passed for tracked diff; file is currently untracked. Full local Jekyll build is blocked by missing `jekyll` executable / missing `Gemfile`.
