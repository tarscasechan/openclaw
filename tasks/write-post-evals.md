# Write Post Evals

Goal: test `skills/write-post` with evals instead of relying on skill wording.

Status: passing
Last run: 2026-04-30T17:58:50Z
Static checks: pass (0 failures)
Model cases: combined evidence covers 25/25
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
- Full model sweep at 2026-04-30T17:40:40Z ran 25/25 and passed 24/25; the only failure was judge extraction on `zinsser_edit_tightens_without_flattening`.
- Targeted rerun after judge fix passed `zinsser_edit_tightens_without_flattening` 1/1.

Acceptance:
- static checks pass
- deterministic checks pass
- at least 80% of selected model-run cases pass
- no hard-fail case fails
