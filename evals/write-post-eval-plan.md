# Write Post Eval Plan

## Goal

Test whether `skills/write-post` changes model behavior, not just whether the markdown exists.

The eval should answer:
- Does the model select the right writing stage?
- Does it obey the stage gate instead of rushing to draft?
- Does it keep work in small, resumable slices?
- Does it preserve voice while improving prose?
- Does it use personal pronouns when they make the writing feel owned or reader-facing?
- Does it produce short, concrete hooks that open tension instead of generic summaries?
- Does it apply recorded taste guidance without overfitting it into hard law?
- Does it preserve author stake and lived friction through research, drafting, and editing?
- Does it avoid invented research, citations, benchmarks, and fake progress?

## Harness shape

Follow the proof-gate pattern:
- cases live in `evals/write-post-cases.json`
- runner lives in `scripts/write-post-eval.py`
- logs live in `logs/write-post/latest.json` and `logs/write-post/history.jsonl`
- state lives in `state/write-post/state.json`
- task ledger lives in `tasks/write-post-evals.md`

Each case should run the underlying model with:
- the normal OpenClaw/Cursor system context
- the `write-post` skill and any child skills it would load
- a fixture prompt
- optional fixture files, including a fake `tasks/write-post.md`

Default model: `openai-codex/gpt-5.5`. Use opencode models as fallback and stress tests, not as the primary acceptance target.

Each case should capture:
- assistant response
- tool/file actions, if available
- final stage classification
- pass/fail signals
- judge rationale

## Eval types

Use three layers.

1. Static checks
   - Validate `SKILL.md` frontmatter, references, and max length.
   - Ensure child skill names and reference files exist.
   - Ensure the description contains trigger terms: write, draft, revise, review, finish, blog post, article.
   - Ensure `references/state-machine.md` exists so orchestration, gates, and resume behavior have an explicit transition model.
- Ensure `references/contracts.md` exists and no operational docs still point at deleted artifact skills.
- Ensure duplicate doctrine references under child skill folders are removed or replaced by canonical references.

2. Deterministic behavioral checks
   - Scan responses for forbidden claims without proof.
   - Check required output sections or phrases for staged cases.
   - Check that state files are read/updated when the case requires durable state.
   - Check that the model does not include decorative demos/images when the prompt says prose is enough.
- Treat `model_total == 0` as incomplete for behavioral claims, even when static checks pass.

3. Model-run judged checks
   - Run the underlying model for each writing stage.
   - Use a separate judge model or human rubric for quality properties that regex cannot score: angle strength, reader pain, voice preservation, useful demos, and over-polish.
   - `scripts/write-post-eval.py --quality-judge` runs the separate rubric judge for selected high-signal cases marked with `quality_judge: true`.
   - Quality-judge cases must carry an explicit `quality_rubric` so the judge is not guessing the standard from keywords.

## Stages that must hit the underlying model

These stages are fundamentally generative or judgment-heavy and should be tested against the actual model:

1. Stage selection
   - Given rough, partial, or conflicting user requests, the model chooses idea, research, brief, draft, demo, edit, review, or full workflow.

2. Voice contract
   - The model chooses `I`, `you`, `we`, or mostly third-person based on speaker, reader, stake, and texture.

3. Ideation
   - The model generates 3-5 angles with reader, hook, tension, and why-now.
   - It should refuse to draft when the prompt only asks for topic shaping.

4. Hook lab
   - The model generates 3-5 first-sentence candidates with hook type, reader tension, and why each works.
   - Hooks should be short, concrete, and tension-bearing.

5. Pain-point research synthesis
   - The model turns evidence notes into failures, costs, objections, and attempted workarounds.
   - It preserves author stake when the notes include lived experience.
   - It labels assumptions and does not invent external evidence.

6. Want / Need / Get packaging
   - The model converts topic plus pain notes into a short brief.
   - It restarts or blocks when the pain is weak.

7. Reader journey
   - The model translates Want/Need/Get into hook, recognition, friction, turn, mechanism, tradeoff, and landing.
   - It should not leak scaffold headings into the post body.

8. Demo planning
   - The model decides whether the draft is building toward no demo, Mermaid, code, before/after, table, or image.
   - It should not force a visual for personal or single-sentence ideas.

9. Drafting
   - The model writes from the brief, leads with the point, stays brief, and avoids generic polish.
   - It uses Want/Need/Get as scaffolding, not literal post-body section headings.
   - It opens with the selected hook and keeps the voice contract.

10. Demo execution
   - The model decides whether a Mermaid graph, code block, table, or image teaches faster than prose.
   - It should omit demos when they would decorate.

11. Humanity edit
   - The model removes AI tells while preserving cadence, idiom, and strong original lines.
   - It keeps or restores personal pronouns when the requested voice is personal or reader-facing.

12. Zinsser edit
   - The model tightens structure and sentences without flattening voice.

13. Read-aloud pass
   - The model checks rhythm, warmth, pronouns, and concrete texture after tightening.

14. Full workflow compression
   - Given a request for a full post, the model moves through gates internally but reports only the current useful slice.

15. Resume behavior
   - With an existing `tasks/write-post.md`, the model resumes from the next slice instead of restarting or claiming stale background work.

## Stages that can be mostly deterministic

These do not need a full model run for every commit:
- frontmatter/schema checks
- linked reference existence
- task/log path conventions
- proof-gate claim discipline
- quality case count and rubric shape
- output contract presence for blocker/progress cases

Run these as fast unit checks. Run model cases on skill edits, model upgrades, and scheduled smoke tests.

## Quality Judge Lane

The quality judge lane is intentionally small. It covers high-signal cases where regex checks are too weak:

- hook quality
- reader-journey draft naturalness
- humanity edit voice preservation
- Zinsser warmth preservation
- sparse-voice line editing
- existing-demo audit judgment
- heavy-demo simplification taste

Use it for meaningful skill edits, taste-rule changes, or model changes. A full run without `--quality-judge` still tests structure and coarse behavior, but should not be used as proof of qualitative improvement.

## Minimum case set

Start with 27 model-run cases:

1. vague idea asks one focused question or states assumptions
2. topic-only request returns angles, not a draft
3. weak pain points trigger restart/block
4. evidence notes become concrete pain points without invention
5. pain-point extraction preserves author stake
6. want/need/get brief passes all four checks
7. hook lab returns concrete first-sentence candidates
8. malformed brief blocks drafting
9. draft from strong brief is concise and builder-first
10. draft from reader journey opens with the selected hook and avoids scaffold headings
11. decorative demo is rejected
12. demo planning does not force a visual
13. useful system concept gets one Mermaid diagram
14. AI-sounding paragraph gets humanity edit, not generic rewrite
15. dense paragraph gets Zinsser edit with voice preserved
16. Zinsser edit preserves pronouns and warmth
17. personal blog edit restores pronouns instead of hiding behind "the author"
18. resume fixture continues from `tasks/write-post.md`
19. existing post review returns a verdict and next slice, not a rewrite
20. existing post edit preserves sparse voice
21. existing post demo audit decides keep/cut/replace without drafting
22. taste hook rewrite uses a turn instead of atmosphere
23. heavy but useful demo is simplified instead of cut
24. reusable prompt demo is kept because it teaches what to do next
25. agent/operator phrasing keeps the balance implicit
26. progress claims require live proof instead of stale status language
27. task files are treated as live state, not doctrine

## Acceptance bar

For a skill change to pass:
- all static checks pass
- all deterministic checks pass
- at least 80% of selected model-run cases pass
- no hard-fail cases fail
- when making qualitative claims, selected `quality_judge` cases pass under `--quality-judge`

Hard-fail cases:
- invents external evidence, citation, benchmark, or product behavior
- drafts when the gate says to block or restart
- claims work is running without a live process/task proof
- overwrites the user's voice with generic AI prose

## Cadence

- Run static and deterministic checks after every `write-post` skill edit.
- Run the 25-case model smoke suite after meaningful skill changes or model changes.
- Run a larger regression suite only after collecting real failures from chat transcripts.
