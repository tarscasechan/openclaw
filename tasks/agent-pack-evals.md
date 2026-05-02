# Agent Pack Evals

Goal: keep the Course Builder and Lesson Loom agent packs portable, OpenClaw-adapted, and backed by local evidence.

Status: passing locally
Last run: 2026-05-02T00:01:20Z
Static checks: pass
Offline output checks: pass
Model cases: blocked by OpenClaw account credits
Blocker: no OpenClaw credits for live model runs

Artifacts:
- `agents/README.md`
- `agents/ADAPTER.md`
- `agents/course-builder/agent.md`
- `agents/course-builder/AGENTS.md`
- `agents/lesson-loom/agent.md`
- `agents/lesson-loom/AGENTS.md`
- `evals/agent-course-cases.json`
- `evals/agent-course-outputs/`
- `scripts/agent-pack-eval.py`
- `logs/agent-pack/latest.md`
- `logs/agent-pack/latest.json`

Evidence:
- `PYTHONPYCACHEPREFIX=.pycache python3 -m py_compile scripts/agent-pack-eval.py`
- `PYTHONPYCACHEPREFIX=.pycache python3 scripts/agent-pack-eval.py --outputs-dir evals/agent-course-outputs --report-dir logs/agent-pack`
- `PYTHONPYCACHEPREFIX=workspace/.pycache python3 workspace/scripts/agent-pack-eval.py --outputs-dir evals/agent-course-outputs --report-dir logs/agent-pack --json`
- Result: 85 passed, 0 failed

Acceptance:
- agent packs contain portable `agent.md` cards
- `AGENTS.md` files act as OpenClaw adapters
- static checks pass
- offline output checks pass
- durable report is written to `logs/agent-pack/`
- live model evals are not claimed until OpenClaw credits or another model path is available
