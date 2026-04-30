---
name: write-post
description: Orchestrate blog-post work end to end by composing topic ideation, pain-point research, want/need/get packaging, drafting, demo insertion, humanity editing, Zinsser tightening, and optional image generation. Use when building a post from concept to publishable draft.
---

# Write Post

## Purpose

Implement the `SOUL.md` principles through a post-writing workflow. Do not do all the work in one pass. Use **Seek Truth** for claims, progress, and architecture decisions.
This is a workflow skill, not a principle layer.

## Flow

1. `ideate-topic`
2. `research-pain-points`
3. `package-topic`
4. `draft-post-from-brief`
5. `add-graphs-and-figures` when they teach
6. `humanity-edit`
7. `zinsser-editing`
8. `generate-image-for-post` if needed

## Rules

- Use `tasks/write-post.md` as the durable state file.
- Restart from concept if ideation or pain points are weak.
- Keep demos earned, not decorative.
- Keep prose brief and human.
- Use `resilient-work` behavior: small slices, explicit blockers, file-backed resume.

## Output standard

Return the current slice, not the entire universe.
If the work is blocked, say exactly why.
Never imply a step is live without proof.
Defer to `SOUL.md` for principle hierarchy.
