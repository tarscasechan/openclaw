---

## layout: default

title: Build Your First Skill
permalink: /courses/build-your-first-skill/
description: A short, example-led course for creating one useful AgentSkill that triggers reliably.

# Build Your First Skill

A tiny course for making one skill that an agent can notice, use, and test.

We will build one artifact: `tldr-skill/SKILL.md`.

The skill does a small real job: it turns messy text into an honest TL;DR. Short is easy. Short without lying is the point.

Each lesson makes one move. Do the move. Run the example. Stop.

---

## Lesson 1: Make the File — SKILL.md

**Outcome:** Create the smallest valid skill.

A skill starts as one folder with one required file.

```txt
tldr-skill/
  SKILL.md
```

Inside `SKILL.md`:

```md
---
name: tldr-skill
description: Use when the user asks for a TLDR, concise summary, honest distillation, or quick takeaway from text.
---

# TLDR Skill

Distill the input without pretending certainty.
```

**Try it:** Create `tldr-skill/SKILL.md` with that content.

**What changed?** You made the portable unit: a folder plus `SKILL.md`.

**But:** a file can exist and still never trigger.

---

## Lesson 2: Write the Trigger — description

**Outcome:** Make the skill discoverable.

The `description` is the match surface. Vague descriptions fail quietly.

Weak:

```yaml
description: A summary skill.
```

Better:

```yaml
description: Use when the user asks for a TLDR, concise summary, honest distillation, or quick takeaway from text.
```

**Try it:** Rewrite the description so it says `Use when...` and names the user request.

**What changed?** The agent has a reason to choose this skill.

**But:** if it triggers, you still need to know what “good” means.

---

## Lesson 3: Shape the Output — signature

**Outcome:** Give the skill a repeatable answer shape.

A TL;DR should be short, but it should not erase uncertainty.

Add:

```md
## Response pattern

```txt
TL;DR: <one sentence>
Key points:
- <point 1>
- <point 2>
- <point 3>
Caveat: <what is missing, uncertain, or easy to overstate>
```
```

**Try it:** Add the response pattern.

**What changed?** The skill now has a visible success shape.

**But:** a shape can still hallucinate confidence.

---

## Lesson 4: Add Honesty — caveat

**Outcome:** Keep the summary from overstating the input.

The caveat is where the skill earns trust.

Input:

```txt
The deploy failed after the config change. Logs are incomplete.
```

Bad:

```txt
TL;DR: The config change broke the deploy.
```

Better:

```txt
TL;DR: The deploy failed after a config change.
Caveat: The logs are incomplete, so the config change is only a suspect.
```

**Try it:** Add a rule: `Do not add facts not present in the input.`

**What changed?** The skill can be concise without pretending certainty.

**But:** happy paths are not enough; misses matter too.

---

## Lesson 5: Test the Miss — failure case

**Outcome:** Tell when the trigger is too broad.

Test two prompts.

```txt
Happy path:
TLDR this deploy note: The release is delayed because staging failed after a config change. Logs are incomplete.

Miss:
Write a launch announcement for this feature.
```

Expected:

```txt
Happy path -> tldr-skill should trigger.
Miss -> tldr-skill should not trigger.
```

**Try it:** Save both prompts beside the skill as your manual test.

**What changed?** You now test selection and non-selection.

**But:** a skill that tries to do everything becomes noisy.

---

## Lesson 6: Keep It Small — scope

**Outcome:** Keep the skill focused.

Add guardrails:

```md
## Keep it small

- Do not add facts not present in the input.
- Do not preserve every detail.
- Prefer concrete claims over vague summaries.
- If the input is too thin, say what is missing.
- Do not tailor to the user unless user context is explicitly provided.
```

**Try it:** Add the guardrails section.

**What changed?** The skill has boundaries.

**But:** a local demo is useful only if someone else can copy it.

---

## Lesson 7: Package the Skill — portability

**Outcome:** Move the skill without hidden context.

A portable first skill should include everything it needs in one folder.

```txt
tldr-skill/
  SKILL.md
```

No private paths. No machine-specific assumptions. No external accounts.

**Try it:** Copy the folder somewhere else and check that `SKILL.md` still makes sense alone.

**What changed?** Your skill is now a reusable artifact.

**But:** personalized distillation belongs in the next course.

---

## Minimal artifact

```md
---
name: tldr-skill
description: Use when the user asks for a TLDR, concise summary, honest distillation, or quick takeaway from text.
---

# TLDR Skill

Distill the input without pretending certainty.

## Response pattern

```txt
TL;DR: <one sentence>
Key points:
- <point 1>
- <point 2>
- <point 3>
Caveat: <what is missing, uncertain, or easy to overstate>
```

## Keep it small

- Do not add facts not present in the input.
- Do not preserve every detail.
- Prefer concrete claims over vague summaries.
- If the input is too thin, say what is missing.
- Do not tailor to the user unless user context is explicitly provided.

```

---

## Smoke test

Happy path:

```txt
User: TLDR this deploy note: The release is delayed because staging failed after a config change. Logs are incomplete.
Expected: tldr-skill is selected and includes a Caveat about incomplete logs.
```

Failure case:

```txt
User: Write a launch announcement for this feature.
Expected: tldr-skill is not selected.
```

---

## Eval checklist

- Folder is named `tldr-skill/`.
- File is named `SKILL.md`.
- Frontmatter starts and ends with `---`.
- `name:` is stable and machine-friendly.
- `description:` begins with `Use when...` or equivalent trigger language.
- Skill has one obvious response pattern.
- Skill includes a caveat/uncertainty slot.
- Skill has one happy-path prompt.
- Skill has one miss prompt.
- Skill does not require tools, secrets, accounts, private paths, or user memory.
- Copying the folder preserves all needed context.

---

## Cut list

Moved later:

- Personalizing the TL;DR to a specific reader
- Using user memory or profile context
- Reading files or URLs with tools
- Multi-document synthesis
- Conflict detection across sources
- Installing skills into a live runtime
- Automated harness tests

