# Portable Pi Agent Course Ladder

Learner: Technical builders who can edit Markdown and want a useful agent package that runs in Pi first and can be adapted into OpenClaw.

Promise: After the core course, they can build one small Pi-compatible agent with a portable `agent.md`, one skill, one smoke test, and a clear OpenClaw adapter path.

Artifact: Signal Sorter, a tiny agent that triages one inbound message into `do`, `defer`, `delegate`, `delete`, or asks one clarification question.

Course ladder:

Free course:
- Build a Pi Agent: create Signal Sorter as a portable local package.
- Keep it tool-free and safe: no credentials, no external writes, no private data.

Core follow-up:
- Add an OpenClaw adapter: map portable `agent.md` behavior into `AGENTS.md`, `skills/`, and `agents/`.
- Add a regression eval: compare skill-guided output to an undirected prompt.

Advanced follow-up:
- Cross-model evaluation: compare cheap, strong, and local models to discover model requirements.
- Automation: schedule or trigger the agent only after it has receipts.

Lesson spine:
1. Name the Agent — identity: define Signal Sorter in three lines.
2. Choose Four Decisions — decision set: constrain the action space to 4D.
3. Split Status — failure: separate `needs-clarification` from the 4D decisions.
4. Create the Agent Card — Pi contract: save the portable `agent.md`.
5. Add One Skill — method: move repeatable triage logic into `skills/triage-message/SKILL.md`.
6. Choose the Model Class — portability: use a local model class instead of a provider-only model name.
7. Run Two Cases — smoke test: check one decided case and one clarification case.
8. Inspect the Output — eval: use a checklist before packaging.

Eval path:

Manual checks:
- Does `agent.md` define runtime target, model class, tools, role, contract, and rules?
- Does the skill make exactly one decision or ask exactly one question?
- Do the smoke tests cover one decided case and one missing-information case?

Undirected baseline:
- Ask a generic model to triage the same messages without the skill.
- Compare whether it chooses multiple actions, invents facts, or treats clarification as a fifth D.

Cross-model checks:
- Run the same two cases on a cheap classifier, a stronger reasoning model, and a local model.
- If only the strong model passes, the agent has hidden model requirements.
- If all models pass, the contract is probably simple enough.

Cut list / next courses:
- Personal inbox integrations.
- Contact lookup.
- Scheduling or delivery automation.
- Rich memory and preference handling.
- Multi-agent routing.

Placement:

Public course page: `_courses/build-a-pi-agent.md`.

Course-specific example: `courses/examples/signal-sorter-agent/`.

Durable framework agent: `agents/signal-sorter/` only after the course example proves reusable.

Durable skills: `skills/triage-message/` only if Tars or subagents should invoke it repeatedly.

OpenClaw adapter: keep `agent.md` portable and put OpenClaw-specific loading, path, and skill-selection behavior in `AGENTS.md`.
