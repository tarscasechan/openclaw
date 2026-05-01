---
name: course-builder
description: Build short, example-led courses with progressive lessons, tiny examples, smoke tests, and But: hooks.
---

# Course Builder

For every lesson:

1. Make one small thing.
2. Hit one pain or gap.
3. Add one concept that resolves it.
4. Test with a tiny example.
5. Tease the next lesson with a `But:` line.

Use this spine:

```txt
make a thing → hit a pain → add one concept
```

Default to 5-8 lessons.

Pick a hello-world artifact that is useful, low-setup, safe, and testable.

Each lesson uses:

```md
## Lesson N: Verb the Thing — keyword

**Outcome:** Learner can do one thing.

Pain/gap sentence.

Tiny example.

**Try it:** One action.

**What changed?** One sentence.

**But:** The gap that motivates the next lesson.
```

After drafting, stress-test by building the artifact exactly as taught. Patch missing, vague, extra, or badly ordered steps.
