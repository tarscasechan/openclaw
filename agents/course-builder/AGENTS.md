# Course Builder OpenClaw Adapter

Use `agent.md` as the canonical Pi-compatible agent card.

When running inside OpenClaw:
- Load the workspace `course-builder` skill when available; it is the local method adapter.
- Preserve the portable return contract from `agent.md`: `Course`, `Artifact`, `Smoke test`, `Eval checklist`, `Cut list / next courses`, and `Verification`.
- Keep courses to 5-8 lessons with one concept per lesson and a `But:` hook at the end of every lesson.
- Use workspace placement rules: public course pages in `_courses/`, course examples in `courses/examples/`, durable skills in `skills/`, and durable agents in `agents/`.
- Do not hide reusable framework components inside course examples.
