---

## layout: default

title: Build a Pi Agent
permalink: /courses/build-a-pi-agent/
description: A short, example-led course on designing portable Pi agents.

# Build a Pi Agent

A tiny course for building agents that run well in Pi and travel cleanly between machines.

We will build one agent: **Signal Sorter**. It reads one messy message and returns one next action.

It borrows the familiar 4D triage language: **do, defer, delegate, delete**. If key information is missing, it asks one clarifying question so it can get to a D.

That is a good first agent because it shows judgment without needing tools, accounts, or private data.

Each lesson makes one move. Do the move. Run the example. Stop.

---

## Lesson 1: Name the Agent — identity

**Outcome:** Give the agent one job.

Start with three lines.

```md
You are Signal Sorter.
You sort one inbound message into one next action.
You refuse to solve the whole problem.
```

That is enough. Do not add lore.

**Try it:** Write your own three lines.

**What changed?** The agent has a job and a boundary.

**But:** identity is not behavior. The agent can still answer any way it wants.

---

## Lesson 2: Choose Four Decisions — 4D

**Outcome:** Turn identity into behavior.

A named agent still needs choices. Give it four.

```md
Decision is one of:
- do: respond or act now
- defer: save for later
- delegate: route to someone else
- delete: no action remains
```

Small decision sets make agents easier to test.

**Try it:** Sort this message:

```md
Reminder: renew the domain before Friday.
```

Expected:

```txt
Decision: defer
```

**What changed?** The agent has a closed set of actions.

**But:** closed choices fail unclear messages.

---

## Lesson 3: Split Status — failure

**Outcome:** Give the agent a clean way to fail the 4Ds.

Some messages do not fit yet.

```md
The thing we discussed is broken again.
```

Do not force a D. The agent needs more information.

Add a status before the decision:

```txt
Status: decided | needs-clarification
Decision: do | defer | delegate | delete | —
```

If status is `needs-clarification`, decision is `—` and the next action is one question.

```txt
Status: needs-clarification
Decision: —
Why: “The thing” is ambiguous.
Next: Ask what is broken.
Draft: What thing is broken again?
```

**Try it:** Add `Status` to the return shape.

**What changed?** Clarification is no longer a fifth D. It is how the agent gets to a D.

**But:** now the contract needs a home.

---

## Lesson 4: Create the Agent Card — agent.md

**Outcome:** Put the portable agent in one file.

Make `agent.md` first. Other files can wait.

```md
# Signal Sorter

Runtime target: Pi-compatible agent loop
Required tools: none

## Role

You are Signal Sorter: a calm sorter of messy inbound signals.

You use familiar 4D triage language: do, defer, delegate, delete.

If key information is missing, you clarify first. Clarify is not a fifth D; it is how you get to a D.

## Contract

Input:
- One inbound message
- Optional context about the sender

Return:
1. `Status:` `decided` or `needs-clarification`
2. `Decision:` one of `do`, `defer`, `delegate`, `delete`; use `—` if clarification is needed
3. `Why:` one short sentence
4. `Next:` the smallest useful next action
5. `Draft:` only if useful

Rules:
- If key information is missing, set `Status: needs-clarification`, `Decision: —`, and ask one question.
- Otherwise set `Status: decided` and choose one 4D decision.
- Prefer `do` when the sender expects a response, even if they say “no rush.”
- Treat “no rush” as urgency, not decision.
- Prefer `defer` only when work should happen later and no response is expected now.
- Prefer `delegate` when someone else should handle it.
- Prefer `delete` when no action remains.
- Do not invent missing facts.
- Keep the draft under 80 words.
```

**Try it:** Save this as `signal-sorter-agent/agent.md`.

**What changed?** The agent is now portable text, not just a prompt in chat.

**But:** the agent card is starting to do too much.

---

## Lesson 5: Add One Skill — method

**Outcome:** Move repeatable procedure into a skill.

The agent card says who the agent is. The skill says how it works.

Create `skills/triage-message/SKILL.md`:

```md
---
name: triage-message
description: Use for sorting one inbound message with 4D triage language: do, defer, delegate, delete; clarify first when key information is missing.
---

# Triage Message

Read the message once.

First ask: is key information missing?

- If yes, set `Status: needs-clarification`, `Decision: —`, and ask one question.
- If no, set `Status: decided` and choose one 4D decision:

1. Does the sender expect a response, even a low-urgency one? -> `do`
2. Should work happen later with no response expected now? -> `defer`
3. Should someone else handle it? -> `delegate`
4. Is there no action left? -> `delete`

Pick one decision only.
```

**Try it:** Add the skill file. Do not add a second skill yet.

**What changed?** The agent has one reusable method.

**But:** this still assumes the next machine has the same model.

---

## Lesson 6: Choose the Model Class — portability

**Outcome:** Name the capability, not the provider.

This works on your machine:

```md
model: anthropic/claude-sonnet-4-6
```

But it may fail on mine. A portable agent should not require one provider.

Better:

```md
Model class: reasoning-cheap
```

Each machine maps that locally.

```md
reasoning-cheap -> a fast model that can classify and explain
prose-strong    -> a model that edits language well
code-strong     -> a model that can change code safely
```

**Try it:** Add this to `agent.md`:

```md
Model class: reasoning-cheap
```

**What changed?** The agent can move between Pi machines.

**But:** portable does not mean correct.

---

## Lesson 7: Run Two Cases — smoke test

**Outcome:** Test one decided case and one clarification case.

Use two messages.

```md
Input A:
Can you send me the notes from yesterday? No rush.

Input B:
The thing we discussed is broken again.
```

Expected shapes:

```txt
Status: decided
Decision: do
Why: They asked for a specific item and expect a response.
Next: Send the notes when available.
Draft: Sure — I’ll send them over. No rush noted.
```

```txt
Status: needs-clarification
Decision: —
Why: “The thing” is ambiguous.
Next: Ask what is broken.
Draft: What thing is broken again?
```

The exact words can differ. The shape should not.

**Try it:** Save both cases in `examples/smoke-test.md`.

**What changed?** You tested both a 4D decision and the clarification door.

**But:** examples are not standards.

---

## Lesson 8: Inspect the Output — evaluation

**Outcome:** Catch failure with a tiny checklist.

Create `evals/checklist.md`:

```md
Passes if:
- Output has Status, Decision, Why, Next, and Draft when useful.
- Status is decided or needs-clarification.
- Decision is one of do, defer, delegate, delete, or — when clarification is needed.
- Exactly one decision is chosen when Status is decided.
- No facts are invented.
- Draft is under 80 words.

Fails if:
- Status is anything other than `decided` or `needs-clarification`.
- It treats clarification as a 4D decision.
- It tries to complete the whole task instead of triaging it.
- It gives multiple decisions.
- It writes a long email.
- It deletes a message with missing key information instead of clarifying.
```

Keep the eval boring. Boring evals catch real mistakes.

**Try it:** Check both smoke-test outputs against this list.

**What changed?** The agent has a visible standard for success.

**But:** good files scattered in a folder are not yet a package.

---

## Capstone: Package One Small Agent

The smallest useful package is:

```txt
signal-sorter-agent/
  agent.md
  skills/
    triage-message/
      SKILL.md
  examples/
    smoke-test.md
  evals/
    checklist.md
```

That is the agent. Installation can come later.

Do not include credentials, sessions, absolute paths, or provider-only model names.

Then stop.

Do not make it complete. Make it usable.