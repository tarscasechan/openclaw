# Evals For Portable Agents

Learner: Builders who have made one portable skill or Pi agent and now need evidence that it works across prompts and models.

Promise: They can create a tiny eval suite, compare agent-guided output against an undirected baseline, and decide whether the agent needs a stronger model.

Artifact: `evals/agent-smoke-cases.json` plus a small runner report that scores one happy path, one ambiguity case, and one overreach case.

Course ladder:

Core course:
- Build a first portable skill or Pi agent.

This course:
- Add deterministic eval cases.
- Compare directed agent behavior to an undirected prompt.
- Capture a short report with pass/fail receipts.

Advanced course:
- Cross-model evaluation for model requirements.
- CI or scheduled eval runs after the local suite is stable.

Lesson spine:
1. Pick the Behaviors — contract: choose the two or three promises that must not break.
2. Save the Cases — fixtures: write one happy path, one failure case, and one overreach case.
3. Define Pass/Fail — rubric: turn expectations into checkable labels.
4. Run the Agent — directed output: score the skill-guided or agent-guided response.
5. Run the Undirected Baseline — comparison: ask the same model without the agent instructions.
6. Compare Models — requirements: run cheap, strong, and local models when available.
7. Write the Report — receipts: save latest JSON, latest Markdown, and history.

Eval path:

Manual eval:
- Read each output against the rubric.
- Mark hard failures separately from style misses.

Undirected baseline:
- Same input, no skill or agent card.
- Expected failure: more drift, more invented facts, or less consistent shape.

Cross-model checks:
- Run the same suite on a cheap model, a strong model, and a local model.
- If cheap and local fail the same case, tighten the contract before assuming the model is too weak.
- If only a strong model passes after contract tightening, document the model requirements.

Cut list / next courses:
- Automatic grading with a model judge.
- Regression dashboards.
- Cron or CI scheduling.
- Per-user taste and memory evals.
- OpenClaw account or gateway provisioning.

Placement:

Public course page: `_courses/agent-evals.md` when promoted.

Course-specific examples: `courses/examples/agent-evals/`.

Durable runner: `scripts/agent-pack-eval.py` only if it supports reusable packs beyond the course.

Durable cases: `evals/agent-course-cases.json` for shared agent-pack checks.

Durable agents: `agents/` for Pi-compatible agent cards plus OpenClaw adapters.

Verification:

This design keeps the first eval course focused on local evidence. It includes undirected and cross-model comparisons as explicit steps without requiring OpenClaw credits for the first pass.
