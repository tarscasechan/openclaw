# First Portable Skill Course

Artifact: `tldr-skill/SKILL.md`, an honest TL;DR skill that turns a messy note into a short summary with one caveat.

Course:

## Lesson 1: Name the Use — artifact

Outcome: The learner picks one useful job for the skill.

Start with a real note, not a generic hello world.

```md
Meeting notes are messy. I need three bullets, one decision, and one caveat.
```

Try it: Save that as the example input.

What changed? The skill now has a nail: compressing a note someone might actually use.

But: a useful job still needs a trigger.

## Lesson 2: Write the Trigger — description

Outcome: The learner writes skill frontmatter that can be selected reliably.

```md
---
name: tldr-skill
description: Use when turning a messy note, transcript, or long update into a short honest TL;DR with bullets, one decision, and one caveat.
---
```

Try it: Create `tldr-skill/SKILL.md` with only this frontmatter.

What changed? The skill has a discoverable reason to run.

But: a trigger does not say how to do the work.

## Lesson 3: Add the Shape — contract

Outcome: The learner defines the output before adding judgment.

```md
Return:
1. `TL;DR:` one sentence
2. `Bullets:` three bullets max
3. `Decision:` one explicit decision or `none stated`
4. `Caveat:` what might be missing or uncertain
```

Try it: Add the return shape under the frontmatter.

What changed? The output can be inspected instead of vibes-checked.

But: shape alone can hide invented facts.

## Lesson 4: Guard the Failure — uncertainty

Outcome: The learner handles missing or ambiguous information.

Add:

```md
If the source does not state a decision, write `Decision: none stated`.
Do not invent names, deadlines, owners, or outcomes.
Use `Caveat:` for uncertainty instead of smoothing it away.
```

Try it: Run the skill on a note with no decision.

What changed? The failure path is visible instead of silently wrong.

But: now we need a repeatable example.

## Lesson 5: Save the Example — smoke-test

Outcome: The learner creates a happy path and a failure case.

Happy path: note includes a decision.

Failure case: note describes discussion but no decision.

Expected failure behavior:

```txt
Decision: none stated
Caveat: The note does not identify a final owner or deadline.
```

Try it: Save both cases in `examples/smoke-test.md`.

What changed? The skill can be tested without trusting memory.

But: examples are not yet an eval.

## Lesson 6: Check the Output — eval

Outcome: The learner creates a checklist with pass/fail checks.

Passes if:
- Output has TL;DR, Bullets, Decision, and Caveat.
- Bullets are three or fewer.
- Missing decisions are reported as `none stated`.
- The Caveat names uncertainty instead of inventing facts.

Fails if:
- It invents an owner, deadline, or decision.
- It writes a full article.
- It omits the Caveat.

Try it: Score the happy path and the failure case.

What changed? The learner has a boring standard that catches real mistakes.

But: the portable skill still needs correct placement.

## Lesson 7: Package the Skill — placement

Outcome: The learner puts the artifact where it can travel.

Use:

```txt
tldr-skill/
  SKILL.md
  examples/
    smoke-test.md
  evals/
    checklist.md
```

In this workspace, durable skills belong in `skills/`; course-specific snapshots belong in `courses/examples/`.

Try it: Copy only the durable skill to `skills/tldr-skill/`.

What changed? The course example and reusable framework artifact are no longer mixed together.

But: personalization, model comparison, and automation can wait for the next course.

Smoke test:

Happy path:
- Input includes a meeting note with a stated decision.
- Expected: TL;DR, no more than three bullets, the stated decision, and a Caveat about any missing owner or deadline.

Failure case:
- Input includes discussion notes with no decision.
- Expected: `Decision: none stated`; Caveat explains what is missing; no owner, date, or outcome is invented.

Eval checklist:

Passes if:
- `tldr-skill/SKILL.md` has frontmatter with a specific trigger.
- Output has TL;DR, Bullets, Decision, and Caveat.
- Happy path preserves the stated decision.
- Failure case does not invent a decision.
- The package separates durable skill files from course example files.

Fails if:
- The skill is a generic summarizer with no caveat behavior.
- The course teaches all skill theory before making the artifact.
- Personalization or model comparison bloats the first course.

Cut list / next courses:
- Personalized tone memory.
- Undirected baseline comparison.
- Cross-model checks for model requirements.
- Installing the skill into multiple agent runtimes.

Verification:

Checked against the Course Builder contract: 7 lessons, every lesson has a `But:` hook, artifact is `tldr-skill/SKILL.md`, smoke test includes happy path and failure case, and eval checklist uses concrete pass/fail checks.
