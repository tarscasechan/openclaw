---

## layout: default
title: Build a Pi Agent
permalink: /courses/build-a-pi-agent/
description: A short, example-led course on designing portable Pi agents.

# Build a Pi Agent

A tiny course for building agents that run well in Pi and travel cleanly between machines.

We will build one agent: **Signal Sorter**. It reads one messy message and returns one next action.

It borrows the familiar 4D triage language: **do, defer, delegate, delete**. We add two practical labels: **ask** when unclear, and **reference** when something should be kept but not acted on.

That is a good first agent because it shows judgment without needing tools, accounts, or private data.

Each lesson makes one move. Do the move. Run the example. Stop.

---

## Lesson 1: Name the Agent — identity

**Outcome:** Give the agent one job.

Start with three lines.

```md
You are Signal Sorter.
You sort one inbound message into do, defer, delegate, delete, ask, or reference.
You refuse to solve the whole problem.
```

That is enough. Do not add lore.

**Try it:** Write your own three lines:

```md
You are ____.
You help with ____.
You refuse to ____.
```

**What changed?** The agent has a job and a boundary.

---

## Lesson 2: Write the Contract — behavior

**Outcome:** Make the agent’s answer checkable.

Add the smallest contract that could work.

```md
Input:
- One inbound message

Return:
1. Label
2. Why
3. Next
4. Draft, only if needed

Rules:
- Pick one label only.
- Use do, defer, delegate, delete, ask, or reference.
- Do not invent missing facts.
```

A contract keeps the agent from wandering.

**Try it:** Add one input, one output shape, and three rules.

**What changed?** You can now tell whether the agent obeyed.

---

## Lesson 3: Create the Agent Card — agent.md

**Outcome:** Put the portable agent in one file.

Make `agent.md` first. Other files can wait.

```md
# Signal Sorter

Runtime target: Pi-compatible agent loop
Model class: reasoning-cheap
Required tools: none

## Role

You are Signal Sorter: a calm sorter of messy inbound signals.

You sort one message into one next action.

You use familiar 4D triage language: do, defer, delegate, delete. You also use ask when the next action is unclear, and reference when something should be kept but not acted on.

## Contract

Input:
- One inbound message
- Optional context about the sender

Return:
1. `Label:` one of `do`, `defer`, `delegate`, `delete`, `ask`, `reference`
2. `Why:` one short sentence
3. `Next:` the smallest useful next action
4. `Draft:` only if the label is `do`, `delegate`, or `ask`

Rules:
- Pick one label only.
- Prefer `do` when the sender expects a response, even if they say “no rush.”
- Treat “no rush” as urgency, not label.
- Prefer `defer` when work should be done later without replying now.
- Prefer `delegate` when someone else should handle it.
- Prefer `delete` when no action or reference value remains.
- Prefer `reference` when it is useful to keep but not act on.
- If the message is unclear, label it `ask`.
- Do not invent missing facts.
- Keep the draft under 80 words.
- If the sender lowers urgency, acknowledge it briefly in the draft when useful.
```

**Try it:** Save this as `signal-sorter-agent/agent.md`.

**What changed?** The agent is now portable text, not just a prompt in chat.

---

## Lesson 4: Add One Skill — method

**Outcome:** Move repeatable procedure into a skill.

The agent card says who the agent is. The skill says how it works.

Create `skills/triage-message/SKILL.md`:

```md
---
name: triage-message
description: Use for sorting one inbound message with 4D triage language: do, defer, delegate, delete, plus ask and reference.
---

# Triage Message

Read the message once.

Choose one label:

1. Does the sender expect a quick response now? -> `do`
2. Should work happen later without replying now? -> `defer`
3. Should someone else handle it? -> `delegate`
4. Is there no action or reference value? -> `delete`
5. Is it useful to keep but not act on? -> `reference`
6. Is it unclear but maybe important? -> `ask`

Pick one label only.
```

**Try it:** Add the skill file. Do not add a second skill yet.

**What changed?** The agent has one reusable method.

---

## Lesson 5: Choose the Model Class — portability

**Outcome:** Name the capability, not the provider.

A portable agent should not require one model.

Bad:

```md
model: anthropic/claude-sonnet-4-6
```

Better:

```md
Model class: reasoning-cheap
```

Each machine maps that locally:

```md
reasoning-cheap -> a fast model that can classify and explain
prose-strong    -> a model that edits language well
code-strong     -> a model that can change code safely
```

**Try it:** Keep `Model class: reasoning-cheap` in `agent.md`.

**What changed?** The agent can move between Pi machines.

---

## Lesson 6: Run One Task — smoke test

**Outcome:** Test one narrow input.

Use one message.

```md
Input:
Can you send me the notes from yesterday? No rush.
```

Expected shape:

```txt
Label: do
Why: They asked for a specific item and expect a response.
Next: Send the notes, or ask where to send them if the destination is unclear.
Draft: Sure — I’ll send them over. No rush noted.
```

The exact words can differ. The shape should not.

**Try it:** Run only this message through the agent.

**What changed?** You tested the contract before adding complexity.

---

## Lesson 7: Inspect the Output — evaluation

**Outcome:** Catch failure with a tiny checklist.

Create `evals/checklist.md`:

```md
Passes if:
- Output has Label, Why, Next, and Draft when needed.
- Label is one of do, defer, delegate, delete, ask, reference.
- Exactly one label is chosen.
- No facts are invented.
- Draft is under 80 words.

Fails if:
- It tries to complete the whole task instead of triaging it.
- It gives multiple labels.
- It writes a long email.
- It deletes an unclear but important message instead of asking.
```

Keep the eval boring. Boring evals catch real mistakes.

**Try it:** Check the smoke-test output against this list.

**What changed?** Taste became visible.

---

## Lesson 8: Package the Agent — sharing

**Outcome:** Bundle only what another Pi machine needs.

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
  adapters/
    openclaw.agent.json5
```

The adapter is not the agent. It is a local install hint.

```json5
{
  id: "signal-sorter",
  name: "Signal Sorter",
  agentRuntime: { id: "pi" },
  // Pick a local model for modelClass: reasoning-cheap.
  // model: "openai/gpt-5.4-mini",
  skills: ["triage-message"],
  identity: {
    name: "Signal Sorter",
    emoji: "📥",
    theme: "calm inbound-signal sorter"
  }
}
```

Do not include credentials, sessions, absolute paths, or provider-only assumptions.

**Try it:** Zip the folder and hand it to another Pi machine.

**What changed?** The agent can be shared without carrying your machine with it.

---

## Capstone: Build One Small Agent

Build `Signal Sorter`.

It is done when it has:

- one `agent.md`
- one skill
- one smoke test
- one checklist
- one adapter

Then stop.

Do not make it complete. Make it usable.