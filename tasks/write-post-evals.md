# Write Post Evals

Goal: test `skills/write-post` with evals instead of relying on skill wording.

Status: passing
Last run: 2026-04-30T05:07:59Z
Static checks: pass (0 failures)
Model cases: 21/21 passed (21 ran)
Hard failures: 0
Next slice: keep suite as regression guard for skill/model changes
Blocker: none

Artifacts:
- `evals/write-post-eval-plan.md`
- `evals/write-post-cases.json`
- `scripts/write-post-eval.py`

Evidence:
- `logs/write-post/latest.json`
- `logs/write-post/history.jsonl`

Acceptance:
- static checks pass
- deterministic checks pass
- at least 80% of selected model-run cases pass
- no hard-fail case fails
