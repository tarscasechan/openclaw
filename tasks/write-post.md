# write-post

## Goal
Turn topic ideas into publishable posts with strong structure, useful demos, and lean prose.

## Reader
Builders first. General readers second.

## Live workflow
1. Ideate topic
2. Research pain points
3. Package topic with want / need / get
4. Draft from brief
5. Add graphs/code when they teach
6. Humanity edit
7. Zinsser edit
8. Optional image pass

## Current state
- Parent skill: `skills/write-post/`
- Packaged skill: `skills/dist/write-post.skill`
- Posts in play: the six April 29 drafts
- Current issue: review must happen in smaller slices; large async runs are too brittle

## Default follow-up rule
- Do one small slice at a time.
- If a slice times out, restart only that slice.
- Do not claim work is running unless a live process exists.
- Report only: done, blocked, failed.

## Active constraints
- Use want / need / get early.
- Restart from concept if the pain point is weak.
- Add demos only when they clarify the core conceit.
- Keep prose brief and human.

## Next actions
- Re-run post review in small chunks.
- If a post is conceptually weak, restart it from concept instead of polishing.
- Keep the best post set, then commit/push.

- Current status: parent skill rewritten to reflect the composed flow; child skills are being created.
- Modular composition implemented: ideate-topic, research-pain-points, package-topic, draft-post-from-brief, add-graphs-and-figures, humanity-edit, generate-image-for-post, with write-post as orchestrator.
