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
