# Write Post Evals

Goal: test `skills/write-post` with evals instead of relying on skill wording.

Status: passing
Last run: 2026-04-30T21:14:17Z
Static checks: pass (0 failures)
Model cases: 1/1 passed (1 ran)
Quality judge: 1/1 passed (enabled)
Behavioral completeness: run
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
- behavioral claims require a non-static run with model cases
- qualitative claims require `--quality-judge` on selected high-signal cases
- at least 80% of selected model-run cases pass
- no hard-fail case fails
