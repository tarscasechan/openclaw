# Write Post Contracts

These contracts apply the `SOUL.md` principles to writing work. They are not a separate principle layer.

## Proof Contract

Before claiming task state, check the smallest evidence that settles it.

- `done`, `fixed`, `implemented`, or `updated` needs an artifact plus verification.
- `running`, `waiting`, or `in flight` needs a live process, task id, cron job, or durable state entry.
- `tested`, `verified`, or `checked` needs command output, log output, source inspection, or another verification artifact.
- `blocked` needs the specific missing input, permission, state, error, or decision.

If evidence is missing, downgrade the claim: say what has not been verified.

## State Contract

Use `tasks/write-post.md` only as live state for active writing work.

Keep it short:
- goal
- reader or owner
- current stage
- current slice
- done list
- blocker
- next action
- last verified state

Do not use the task file as doctrine, taste memory, changelog, or replacement for skill instructions.

## Resume Contract

Resume from durable state, not chat memory.

- Read the current stage and next slice before continuing.
- Continue the smallest useful slice.
- Retry only the failed slice after a timeout or interruption.
- Restart from concept only when the concept, reader pain, or structure is wrong.
- Never describe stale or dead work as still running.

## Blocker Contract

Ask only when missing information blocks useful work or the assumption would be risky.

For recoverable ambiguity, state the assumption and move one slice. For blocking ambiguity, ask one focused question and stop there.
