---
name: course-builder
description: Build, revise, stress-test, or package short example-led courses. Use when creating a 5-8 lesson course, lesson plan, curriculum slice, course artifact, smoke test, eval checklist, pain chain, or cut/next-course list.
---

# Course Builder

Build short courses where the learner makes one useful thing and discovers each next concept through a real gap.

Default course length: 5-8 lessons.

## Core loop

For every lesson:

1. **Make** one small thing.
2. **Hit** one pain or gap.
3. **Add** one concept that resolves it.
4. **Test** with a tiny example.
5. **Tease** the next lesson with a `But:` line.

Spine:

```txt
make a thing → hit a pain → add one concept → test → tease the next gap
```

## Start

Ask for or infer:

- Topic
- Learner goal
- Starting knowledge
- Desired artifact
- Constraints: length, tone, platform, time, public/private destination

If one missing fact blocks the course, ask one question. Otherwise assume and proceed.

## Pick the nail

Choose a first artifact that is a nail, not just a hammer.

It must be:

- Useful on its own, even if tiny
- Representative of the real work the learner wants to do
- Low-setup and safe: no private data or external writes
- Specific enough to have stakes, taste, or judgment
- Testable with one happy path and one failure/edge case

Reject merely mechanical demos. If the learner finishes thinking “now I need to find an application,” the artifact is too toy-like.

Good first artifacts are boring-useful: a bug report formatter, commit message skill, inbox sorter, polite refusal draft, tiny explainer, config checker, or honest TL;DR.

## Lesson anatomy

Each lesson should contain:

```md
## Lesson N: Verb the Thing — keyword

**Outcome:** Learner can do one thing.

Pain/gap sentence.

Tiny example.

**Try it:** One action.

**What changed?** One sentence.

**But:** The gap that motivates the next lesson.
```

Title rules:

- Verb-led
- Outcome-based
- Includes the key concept word
- Clear before clever

## Progression rules

- One concept per lesson.
- No exhaustive explanation.
- No concept appears before the pain that earns it.
- Introduce a failure case early.
- Prefer concrete return signatures, file shapes, or expected outputs over prose advice.
- Move useful-but-not-needed material to `Cut list / Next courses`.

## Stress-test loop

After drafting:

1. Build the course artifact exactly as taught.
2. Run the smallest smoke test.
3. Add one failure/edge case.
4. Mark each failure:
   - **missing**: course omitted a needed concept
   - **vague**: instruction was not specific enough
   - **extra**: concept was not needed for first success
   - **bad order**: concept appeared before its pain
5. Patch the course.
6. Re-test.

Do not claim the course works until the artifact and smoke test pass.

## Flow review

Check every transition:

```txt
Lesson N ends with: But ____.
Lesson N+1 answers that gap by ____.
```

If the gap is weak, revise one of:

- the prior lesson’s `But:` line
- the next lesson’s opening pain
- the order of lessons
- the example

## Output

For a new course, produce:

- Course outline or draft
- Minimal example artifact
- Smoke test
- Checklist/eval
- Cut list / next courses

For a revision, produce:

- What changed
- Which pain/gap improved
- What was cut or moved later
- Verification performed

For a site course in this workspace, use `_courses/` for public course pages and keep course-specific examples under `courses/examples/`. Do not hide durable framework skills under course examples.
