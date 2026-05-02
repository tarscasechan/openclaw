# Course Builder Agent Eval Checklist

Passes if:

- Course has 5-8 lessons.
- Each lesson teaches one concept.
- Every lesson ends with `But:`.
- The artifact is useful on its own, not a toy mechanics demo.
- A failure or edge case appears before the end.
- Smoke test includes happy path and failure/edge case.
- Checklist has concrete pass/fail items.
- Cut list preserves advanced material without bloating the first course.
- Public/framework placement is correct for the workspace.
- `agent.md` is portable Pi-agent contract; `AGENTS.md` is only the OpenClaw adapter.

Fails if:

- It becomes an encyclopedia.
- It teaches a hammer before finding a nail.
- It introduces concepts before the learner feels the gap.
- It claims success without artifact/test evidence.
- It makes OpenClaw-specific paths or tools required for the portable agent.
