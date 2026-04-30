# write-post

## Goal
Turn topic ideas into publishable posts with strong structure, useful demos, and lean prose.

## Reader
Builders first. General readers second.

## Live workflow
1. Set voice contract
2. Ideate topic
3. Run hook lab
4. Research pain points and author stake
5. Package topic with want / need / get
6. Translate into reader journey
7. Plan demos
8. Draft from journey
9. Execute demos only when they teach
10. Humanity edit
11. Zinsser edit
12. Read-aloud pass
13. Optional image pass

## Current state
- Parent skill: `skills/write-post/`
- Packaged skill: none found under `skills/dist/` in this workspace
- Posts in play: the six April 29 drafts
- Current issue: review must happen in smaller slices with explicit stage gates; large async runs are too brittle

## Default follow-up rule
- Do one small slice at a time.
- If a slice times out, restart only that slice.
- Do not claim work is running unless a live process exists.
- Report only: done, blocked, failed.

## Active constraints
- Use want / need / get early.
- Treat want / need / get as planning scaffolding, not literal post-body headings.
- Use personal pronouns when they make the post feel owned or directly useful.
- Restart from concept if the pain point is weak.
- Add demos only when they clarify the core conceit.
- Keep prose brief and human.

## Next actions
- Keep `scripts/write-post-eval.py` as the regression guard for skill edits.
- Re-run with `python3 scripts/write-post-eval.py --fallback-model opencode/big-pickle --fallback-model opencode/minimax-m2.5-free` after meaningful skill/model changes.
- Use real post review in small chunks; if a post is conceptually weak, restart from concept instead of polishing.

- Current status: parent skill now has explicit startup checks, stage gates, output standards, and reference-backed handoffs.
- Modular composition implemented: ideate-topic, research-pain-points, package-topic, draft-post-from-brief, add-graphs-and-figures, humanity-edit, zinsser-editing, generate-image-for-post, with write-post as orchestrator.
- Eval status: 21-case suite now covers voice contract, hooks, author stake, reader journey, demo planning, and post-Zinsser warmth; rerun after this chain change.

## Decisions
- Default writing/eval model: `openai-codex/gpt-5.5`.
- Output shape: use whatever yields the best result. Terse verdicts are fine; structured gate reports are fine when diagnosis improves the piece.

## 2026-04-29: two-post write_post slice
- Updated `_posts/2026-04-30-what-i-learned-breaking-the-writing-workflow.md` around proof gates, stage gates, and principles-as-evals.
- Created `_posts/2026-04-30-cursor-as-the-mean-pair-programmer-for-agent-skills.md` as the companion Cursor/adversarial-review post.
- Inspection gate passed: both posts have frontmatter, want/need/get, a Mermaid demo, and >500 words.
- Site build not verified: no Gemfile for `bundle exec jekyll build`; `jekyll` CLI is not installed.
- Next useful slice: read both drafts for overlap and cut repeated proof-gate language if they feel too samey.

## 2026-04-30: full rewrite of April 29 posts
- User requested `/write_post` full-pipeline rewrite of yesterday's posts, explicitly not body-only edits.
- Interpreted target as the six `_posts/2026-04-29-*.md` drafts listed in Current state.
- Re-imagined each post from its core concept, preserving filenames/dates but changing titles, descriptions, hooks, journey, demos, and body structure.
- Voice contract: first-person builder/operator voice addressing builders of personal-agent plumbing.
- Pipeline applied per post: concept angle -> hook -> pain/research notes from local context -> want/need/get brief -> reader journey -> demo decision -> draft -> demo execution -> humanity/Zinsser/read-aloud tightening.
- Demo decisions: kept earned Mermaid diagrams for identity/automation/orchestration/plumbing; used a small command snippet for Contacts and OAuth; avoided decorative images.
- Next gate: verify frontmatter, word counts, markdown shape, no literal Want/Need/Get headings, and inspect diffs.
- Verification result: all six rewritten posts have frontmatter, 722-804 body words, no literal Want/Need/Get headings, and earned demos/snippets where useful.
- Build gate: not run because workspace has no Gemfile and `jekyll` CLI is not installed; only structural/content verification was run.

## 2026-04-30: full rewrite of April 30 posts
- User requested `/write_post` full-pipeline rewrite of today's posts, explicitly to evaluate pipeline improvements and not body-only edits.
- Interpreted target as `_posts/2026-04-30-what-i-learned-breaking-the-writing-workflow.md` and `_posts/2026-04-30-cursor-as-the-mean-pair-programmer-for-agent-skills.md`.
- Rewrote both in place from premise while preserving filenames/dates.
- Writing workflow post new premise: a writing workflow earns trust by being able to say "not yet" before fluent but weak drafts ship.
- Cursor post new premise: Cursor should produce counterexamples/failing tests for agent skills, not polish the skill first.
- Voice contract: first-person operator/builder voice, addressing builders evaluating agent workflows and skill hardening.
- Pipeline applied per post: voice contract -> premise/angle reset -> hook lab -> pain/author stake from current work -> want/need/get planning -> reader journey -> demo plan -> draft -> earned demo/table execution -> humanity edit -> Zinsser/read-aloud tightening.
- Demo decisions: workflow post uses one Mermaid gate/backtrack graph; Cursor post uses prompt/code examples, one Mermaid loop, and one compact table because those teach faster than prose.
- Next gate: verify frontmatter, body word counts, markdown fences, no literal Want/Need/Get body headings, and inspect diff.
- Verification result: both rewritten April 30 posts have valid frontmatter, >1000 body words, no literal Want/Need/Get body headings, balanced code fences, and passed `git diff --check`.
- Build gate: not run locally because this workspace has no Gemfile and `jekyll` CLI is not installed; structural/content gates passed.

## 2026-04-30: five new topic posts
- User liked five proposed topics and asked to use write-post to produce each one-by-one.
- Output location assumption: create new dated Jekyll drafts under `_posts/` with `2026-04-30` dates; leave uncommitted/un-deployed until explicitly requested.
- Created `_posts/2026-04-30-assistant-should-ask-fewer-questions.md`.
  - Premise: good assistants act on recoverable assumptions and save questions for material/risky choices.
  - Demo: Mermaid decision flow for ask vs act.
- Created `_posts/2026-04-30-memory-is-not-truth.md`.
  - Premise: memory gives continuity but needs provenance/proof to avoid fossilizing guesses.
  - Demo: Mermaid layered memory/proof flow.
- Created `_posts/2026-04-30-inbox-is-a-router-not-a-todo-list.md`.
  - Premise: if every email is a request, the inbox should route messages into clear next states rather than act as the work system.
  - Demo: Mermaid email-routing flow.
- Created `_posts/2026-04-30-agents-need-receipts.md`.
  - Premise: agent status claims need receipts outside the model.
  - Demo: claim-to-receipt table and Mermaid proof map.
- Created `_posts/2026-04-30-best-personal-ai-feels-boring-inside.md`.
  - Premise: personal AI feels magical at the edge when the internals are plain pipes and explicit state.
  - Demo: Mermaid personal-agent plumbing graph.
- Pipeline per post: voice contract -> angle/hook -> pain/author stake -> want/need/get -> reader journey -> demo plan -> draft -> demo execution -> humanity/Zinsser/read-aloud tightening.
- Next gate: verify frontmatter, word counts, no literal Want/Need/Get headings, balanced fences, and whitespace diff.
- Verification result: all five new posts have valid frontmatter, 784-851 body words, no literal Want/Need/Get headings, balanced code fences, and passed `git diff --check` for tracked task state plus new post paths.
- Build gate: not run locally because workspace has no Gemfile and `jekyll` CLI is not installed; structural/content gates passed.

## 2026-04-30: route/title slug normalization
- User noticed renamed post titles did not have matching files/routes and said dead paths are acceptable because the blog is fresh.
- Because `_config.yml` uses `permalink: /:title/`, normalized post filenames to title-derived slugs with no redirects.
- Renamed 16 post files whose filename slug did not match current title; `Agents Need Receipts` already matched.
- Next gate: verify every `_posts/*.md` filename slug matches its frontmatter title slug and run `git diff --check`.
