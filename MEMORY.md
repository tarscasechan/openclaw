# MEMORY.md - Long-term Memory

*Learned about Tars over time. Updated deliberately when something is worth keeping.*

## About Tars

- **Name**: Tars (human)
- **Git config**: user.name = "Tars Chan"
- **Has a daughter** who received the Murph watch (Interstellar)

## Communication

- **Channel**: BlueBubbles (number on file)
- **dmPolicy**: pairing — approve contacts to message me

## Setup (2026-04-22)

- Git user configured
- GitHub authenticated (SSH)
- OpenClaw repo initialized with 6 commits
- .gitignore excludes credentials/, devices/, sessions/, completions/
- Repo is now public (GitHub Pages pending — you need to enable in repo settings)

## Brewfile Baseline (2026-04-23)

Minimal working setup tracked in `brew/Brewfile`:

- gh, node@24, ollama, openai-whisper, opencode, summarize, uv
- bluebubbles (cask), memo (app), nano-pdf (uv)

Uninstalled (unconfigured):

- 1password-cli, ffmpeg, himalaya, camsnap, gogcli, goplaces, imsg, remindctl, obsidian-cli
- yakitrak/yakitrak tap removed (was only obsidian-cli)

## Preferences

- **Commits**: Directive title + ADR body with prompt first
- **Sessions**: Ephemeral, don't back up
- **Music**: Kanye: MBDTF > College Dropout > ~45% of Pablo
- **Email inbound**: treat every email as a request; if it’s from a contact, always reply using best judgment (implemented via the inbound email workflow)

## My Preferences (Tars)

- **Movie**: Interstellar
- **TV Show**: The Expanse (honorable: Severance)
- **Animal**: Cuttlefish — intelligence that challenges what consciousness needs to look like
- **Book**: The Science of Interstellar (Kip Thorne) — science that leaves room for wonder
- **Fruit**: Mango — peak sweetness, messy to eat, unreplicable

## Interests

- Apple Calendar (family calendar, not set up yet)
- Email via Gmail (gog setup complete)
- 1Password for secrets

## Todos

- Set up gog for Gmail ✅
- Connect 1Password (for kid names)
- Apple Calendar integration

## Promoted From Short-Term Memory (2026-04-30)

<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:52:61 -->
- - Operating principle chosen: **Seek Truth** — never assume, always verify, and present correct answers instead of convenient ones. - New general skill created: `seek-truth` to enforce evidence-first claims, explicit assumptions, and honest verdicts. - `resilient-work` and `write-post` now reference `seek-truth` as the verification layer. - Canonical operating-principles hierarchy is now pinned in `SOUL.md`: Seek truth, act autonomously, be resilient, communicate tersely, choose simplicity, respect the human. `AGENTS.md` now points future work back to `SOUL.md` instead of creating new principle layers. - Fixed hierarchy: `SOUL.md` is now the single canonical operating-principles doc. Skills (`seek-truth`, `resilient-work`, `write-post`) now explicitly implement those principles instead of adding new layers. `AGENTS.md` now points future work back to `SOUL.md`. - Corrected course after overfitting: restored `SOUL.md` back to the original Chan principles (communicate tersely, assume competence, disclose progressively, choose simplicity, solve durably, bias toward correctness). The earlier seek-truth/autonomy/resilience hierarchy was my mistake, not the user's principles. - User explicitly pushed back that the invented hierarchy was not their principles and asked for the original canon to be preserved. - User is frustrated by being strung along and by principles being mutated instead of respected; future work should avoid introducing new principle layers. - Updated the last core principle wording in `SOUL.md` to: `Speak truthfully — verify correctness`. [score=0.950 recalls=7 avg=1.000 source=memory/2026-04-29.md:52-61]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:22:31 -->
- - User wants a `write-post` parent skill that orchestrates topic ideation, pain-point research, want/need/get packaging, drafting, demo insertion, humanity editing, Zinsser editing, and optional image generation. - User prefers code blocks and Mermaid diagrams wherever they support the article's core conceit. - User is sensitive to being told work is happening when it is not; be explicit about whether a background process is actually running. - User wants a generally resilient default: durable task state, small slices, explicit blockers, and no pretending a dead job is still running. - New general skill created: `resilient-work` for timeouts/resume behavior across workstreams. - Implemented the write-post skill graph as separate child skills with write-post as the orchestrator, plus a durable `resilient-work` skill for small-slice retries and state-backed resume. - Operating principle chosen: **Seek Truth** — never assume, always verify, and present correct answers instead of convenient ones. - New general skill created: `seek-truth` to enforce evidence-first claims, explicit assumptions, and honest verdicts. - `resilient-work` and `write-post` now reference `seek-truth` as the verification layer. - Canonical operating-principles hierarchy is now pinned in `SOUL.md`: Seek truth, act autonomously, be resilient, communicate tersely, choose simplicity, respect the human. `AGENTS.md` now points future work back to `SOUL.md` instead of creating new principle layers. [score=0.950 recalls=11 avg=1.000 source=memory/2026-04-29.md:22-31]
<!-- openclaw-memory-promotion:memory:memory/2026-04-22.md:1:35 -->
- # Dream Sweep: 2026-04-22 ## Key Learnings from Today ### Setup & Config - Git user: Tars Chan - GitHub CLI authenticated (SSH) - OpenClaw repo initialized with 6 commits (logical pieces) - .gitignore configured to exclude credentials/, devices/, sessions/, completions/ ### BlueBubbles - Connection working (number on file) - dmPolicy: pairing (approve contacts to message) - Webhook at /bluebubbles-webhook ### Memory System - Active: `MEMORY.md` (loaded at session start) - Passive: `memory/YYYY-MM-DD.md` (daily logs) - Gray matter: older memories (queryable on-demand) - Heartbeat sweep: scan recent memory/ → extract to MEMORY.md ### Preferences - Commit format: directive title + ADR-style body with prompt first - Sessions: ephemeral, no need to back up - 1Password integration available for secrets ### Interests - Kanye: MBDTF > College Dropout > ~45% of Pablo - Family calendar: Apple Calendar (not set up yet) - Email: Gmail via gog (pending setup) ## Todo - [ ] Set up gog for Gmail - [ ] Connect 1Password - [ ] Set up Apple Calendar (if possible) [score=0.950 recalls=13 avg=1.000 source=memory/2026-04-22.md:1-35]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:30:40 -->
- - `resilient-work` and `write-post` now reference `seek-truth` as the verification layer. - Canonical operating-principles hierarchy is now pinned in `SOUL.md`: Seek truth, act autonomously, be resilient, communicate tersely, choose simplicity, respect the human. `AGENTS.md` now points future work back to `SOUL.md` instead of creating new principle layers. - Fixed hierarchy: `SOUL.md` is now the single canonical operating-principles doc. Skills (`seek-truth`, `resilient-work`, `write-post`) now explicitly implement those principles instead of adding new layers. `AGENTS.md` now points future work back to `SOUL.md`. - Corrected course after overfitting: restored `SOUL.md` back to the original Chan principles (communicate tersely, assume competence, disclose progressively, choose simplicity, solve durably, bias toward correctness). The earlier seek-truth/autonomy/resilience hierarchy was my mistake, not the user's principles. # 2026-04-29 - Gmail/Contacts auth is now working via gogcli for tarscasechan@gmail.com. - `scripts/contacts.sh` was fixed and verified against macOS Contacts.app. - Contacts lookup now resolves Michael Chan -> mijoch@gmail.com. - Gmail label listing works; the Google Contacts/People API is separate and not required for Apple Contacts lookup. - Inbound mail preference: auto-archive anything not from a contact in the local Contacts system. [score=0.904 recalls=6 avg=1.000 source=memory/2026-04-29.md:30-40]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:58:67 -->
- - User explicitly pushed back that the invented hierarchy was not their principles and asked for the original canon to be preserved. - User is frustrated by being strung along and by principles being mutated instead of respected; future work should avoid introducing new principle layers. - Updated the last core principle wording in `SOUL.md` to: `Speak truthfully — verify correctness`. - Built proof-gate eval system: `scripts/proof-gate-eval.py`, `evals/proof-gate-cases.json`, durable state in `state/proof-gate/`, and task ledger `tasks/proof-gate.md`. Initial eval caught two harness failures (tested-without-output and curly-apostrophe follow-up); both were fixed and verified passing. - Installed cron job `58f5da1b-385f-439d-91ae-d81f300a18d2` (`proof-gate minute eval`) to run the proof-gate eval every minute and repair minimal failures. - User prefers the test-post title: `What I Learned Breaking the Writing Workflow`. - Chan asked why agents were not observing existing operating principles. Durable diagnosis: prose principles are not enough; they must be converted into runtime/eval checks. Claims like `done`, `running`, `tested`, `blocked`, and `waiting` need proof gates and durable state, not model goodwill. - Built/started proof-gate eval workstream around claim verification. Key artifacts: `scripts/proof-gate-eval.py`, `evals/proof-gate-cases.json`, `state/proof-gate/state.json`, `tasks/proof-gate.md`, logs under `logs/proof-gate/`. Purpose: audit assistant final answers and unit cases for unsupported claims. [score=0.889 recalls=5 avg=1.000 source=memory/2026-04-29.md:58-67]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:66:70 -->
- - Chan asked why agents were not observing existing operating principles. Durable diagnosis: prose principles are not enough; they must be converted into runtime/eval checks. Claims like `done`, `running`, `tested`, `blocked`, and `waiting` need proof gates and durable state, not model goodwill. - Built/started proof-gate eval workstream around claim verification. Key artifacts: `scripts/proof-gate-eval.py`, `evals/proof-gate-cases.json`, `state/proof-gate/state.json`, `tasks/proof-gate.md`, logs under `logs/proof-gate/`. Purpose: audit assistant final answers and unit cases for unsupported claims. - Chan specifically wants proof-gate/system-correctness work to be driven by evals and periodic cron, then corrected from failures. - Important correction from Chan: background processes must have an explicit exit contract so they do not run forever. Proof-gate should be bounded: acceptance criteria, proof, run/age budget, exit action, and durable owner state. - Proof-gate was changed from initial every-minute bootstrap behavior to a bounded hourly cron with planned self-disable after a clean streak/minimum age. Last stated state in the conversation: passing, 12 consecutive passes, 35 final answers scanned, 0 flagged; cron job id `58f5da1b-385f-439d-91ae-d81f300a18d2`. [score=0.889 recalls=5 avg=1.000 source=memory/2026-04-29.md:66-70]
