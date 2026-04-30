---
name: resilient-work
description: Coordinate multi-step work so it survives timeouts, chat resets, and subagent failure. Use when a task needs durable state, small retries, explicit blockers, or a default resume plan instead of a one-shot answer.
---

# Resilient Work

## Purpose

Implement the `SOUL.md` principles **Seek Truth** and **Be resilient**.
Keep work moving without pretending it is still live when it is not.
Build durable state, break tasks into slices, resume from files instead of chat memory.
This is an execution skill, not a principle layer.

## Default operating rules

1. **Write state first**
   - Keep the current goal, next slice, blocker, and done list in a task file.
   - Update that file after meaningful progress.

2. **Work in small slices**
   - Prefer one concrete step per run.
   - If a slice times out, rerun only that slice.
   - Do not restart the whole job unless the concept is wrong.

3. **Verify live state**
   - Check whether a process is actually running before saying it is.
   - If a child task died, say it died.
   - Never describe a dead job as waiting.

4. **Use explicit failure modes**
   - done
   - blocked
   - failed
   - needs restart from concept

5. **Resume by file, not memory**
   - Read the task file.
   - Continue from the next slice.
   - Do not depend on the conversation transcript as the source of truth.

## When to use

- background or async work
- subagent orchestration
- multi-step writing or coding
- anything that must survive interruptions
- anything that already failed once and needs a safer retry

## Output standard

Be plain.
Be specific.
Report the actual state, not the hoped-for state.

## References

- `references/resilience-loop.md`
- `references/task-file.md`
- `seek-truth` for evidence-first claims and verdict discipline
- `SOUL.md` for the canonical hierarchy
