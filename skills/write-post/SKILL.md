---
name: write-post
description: Orchestrate blog-post writing from rough idea to publishable draft. Coordinates topic ideation, pain-point research, want/need/get packaging, drafting, useful demos, humanity editing, Zinsser tightening, and optional image generation. Use when the user asks to write, draft, revise, review, or finish a blog post or article.
---

# Write Post

## Purpose

Turn an idea into a builder-first post with a strong angle, real reader pain, useful demonstrations, and lean prose.

This is an orchestrator skill. Compose the child skills; do not hide the whole workflow inside one pass. Use `references/state-machine.md` for stage transitions, `references/voice-contract.md` for speaker/reader stance, `references/hooks.md` for first-sentence craft, and `references/reader-journey.md` to translate structure into prose. Use **Seek Truth** for claims and progress reports, and **Resilient Work** for state and resume behavior.

## Start every run

1. Read `tasks/write-post.md` when present; treat it as state, not as optional context.
2. Identify the user's requested stage: idea, voice, hook, research, brief, reader journey, draft, demo plan, demo execution, edit, review, or full workflow.
3. Check for minimum inputs: topic/problem, intended reader, and desired output location or format. If one missing fact blocks useful work, ask one focused question. Otherwise state the assumption and proceed.
4. If the user asks for a narrow stage and gives enough input for that stage, do that stage directly. Do not restart earlier workflow steps just because the full post is not packaged yet.
5. Pick the next small slice. Return that slice before expanding scope.
6. Update `tasks/write-post.md` after meaningful progress, blocker, failure, or restart.

For vague input, do not ask a checklist. Ask one focused question, or state one explicit assumption and move one slice.

## Flow

1. **Set the voice contract** with `references/voice-contract.md`.
   Gate: the post knows who is speaking, who is being addressed, and whether `I`, `you`, `we`, or mostly third-person best serves the piece.
2. **Ideate** with `ideate-topic`.
   Gate: the angle names a concrete reader, tension, and reason it matters now. If the pain is vague, restart from concept.
3. **Run hook lab** with `references/hooks.md`.
   Gate: generate 3-5 short first-sentence candidates tied to hook type and reader tension. Pick one working hook before drafting.
4. **Research pain points** with `research-pain-points`.
   Gate: collect failures, costs, objections, attempted workarounds, and author stake when available. Prefer direct evidence over generic market claims.
5. **Package** with `package-topic` and `references/want-need-get.md`.
   Gate: Want, Need, and Get can each be stated plainly before drafting begins. This is internal scaffolding for the brief, not post-body sectioning.
6. **Build the reader journey** with `references/reader-journey.md`.
   Gate: translate Want/Need/Get into natural beats: hook, friction, turn, mechanism, tradeoff, landing. Do not draft until the reading path feels human.
7. **Plan demonstrations** with `add-graphs-and-figures` and `references/demos.md`.
   Gate: decide `none`, `Mermaid`, `code`, `before/after`, `table`, or `image` before drafting. Do not force a visual.
8. **Draft** with `draft-post-from-brief`.
   Gate: the draft follows the reader journey, opens with a real hook, and stays readable without over-polish. It must not include literal `Want`, `Need`, or `Get` headings unless the user explicitly asks for the brief itself. If the brief is weak, stop; do not fill it with assumptions and draft anyway.
9. **Execute demonstrations** with `add-graphs-and-figures` only when they teach faster than prose.
   Gate: every graph, code block, table, or image has a job. A one-sentence idea usually does not need a diagram; a multi-step system flow often does. For a demo-stage request, output either the one useful demo or a short "skip it" decision; do not draft the surrounding post.
10. **Humanity edit** with `humanity-edit`.
   Gate: remove AI tells and synthetic polish while preserving cadence and idiom.
11. **Zinsser edit** with `zinsser-editing` and `references/editing-pass.md`.
   Gate: cut clutter without sanding off the voice.
12. **Read-aloud pass** with `references/editing-pass.md`.
   Gate: the piece still has rhythm, warmth, concrete texture, and an owned point of view after tightening.
13. **Image pass** with `generate-image-for-post` only if a visual clarifies the core idea better than text or a diagram.

## Rules

- Use `tasks/write-post.md` as the durable state file for active writing work.
- Work in visible slices. Do not claim background progress unless a live process or durable task proves it.
- Restart from concept if ideation, reader pain, or the want/need/get structure is weak.
- Treat want/need/get as planning structure. Translate it into natural prose for the post body.
- Keep voice, hook, and structure connected. Do not let a clean framework erase the speaker.
- If a gate fails, stop at that gate. Do not produce the downstream artifact in the same response.
- Keep demos earned, not decorative.
- Keep prose brief and human.
- Use personal pronouns when they make the piece feel owned or directly useful. Do not hide behind impersonal nouns like "the author" or "users" when `I`, `you`, or `we` would be truer.
- Preserve the user's voice when editing existing prose. Improve the piece; do not replace it with generic polish.
- For factual or technical claims, verify or mark uncertainty. Do not invent citations, benchmarks, customer pain, or product behavior.
- If the user asks for a full post, still move through the gates. Compress the reporting, not the thinking.

## Output standard

Return the current slice, not the entire universe.

For normal progress, include:
- what changed
- what stage the post is in
- the next useful slice

For review, choose the shape that improves the piece fastest. Use a terse verdict plus next slice when the problem is obvious. Use a structured gate report when diagnosis is the work.

For blockers, include:
- the missing input, failed check, weak concept, or unverifiable claim
- the smallest next action that would unblock work

Never imply a step is live without proof. Defer to `SOUL.md` for principle hierarchy.
