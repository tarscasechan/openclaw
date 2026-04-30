# Write Post Taste Follow-Up

## Status

This is a synthesis from the taste-eval packet generated on 2026-04-30 plus the user's review answers.

Primary evidence:

- `logs/write-post-taste/latest.json`
- `logs/write-post-taste/latest.md`
- `logs/write-post-taste/user-review-2026-04-30.json`
- 17 posts scanned from `_posts`
- 461 candidate excerpts extracted
- 8 high-signal review items selected
- 8 user taste answers recorded

## What the Loop Surfaced

The selected excerpts clustered around three taste questions:

1. **Do diagrams earn trust or expose machinery?**
   - Workflow gate diagram in `a-writing-workflow-is-a-machine-for-saying-not-yet`
   - Decision tree in `the-assistant-should-ask-fewer-questions`
   - Long prompt block in `cursor-should-write-the-counterexample`

2. **Which hooks feel alive versus over-shaped?**
   - Lyrical science opening in `the-cuttlefish-problem`
   - Personal discovery opening in `the-best-identity-layer-is-the-one-you-already-maintain`
   - Aphoristic systems opening in `a-script-is-not-automation-until-it-can-be-interrupted`

3. **Which compact lines should survive editing?**
   - `Magic is allowed at the interface. The inside should look like plumbing.`
   - `Not because Contacts.app is glamorous. Because it is already where the human work happens.`

## What Resonated

- **Demos can earn their place, but weight matters.** The prompt block and the fewer-questions decision tree should stay. The workflow-gates diagram should be simplified, not cut.
- **Older pre-skill posts are not reliable taste canon.** The cuttlefish opening should be rewritten and should not drive current hook rules.
- **Hooks need a stronger turn.** The Contacts.app opening should be rewritten with a `but` turn. The automation opening should become `A happy path is not an automation.`
- **Compact metaphors are useful but not sacred.** The magic/plumbing line has value, but the wall metaphor may carry the idea better.
- **Agent/human balance should stay implicit.** The Contacts.app line is fine, but `where the human work happens` may be too explicit. `shared workspace between agent and operator` is a better direction.

## Taste Rules

These are grounded in one review pass and should be treated as medium-confidence rules:

- **Demo rule:** Keep demos that show judgment mechanics or executable prompts. Simplify diagrams when the diagram is structurally right but too heavy.
- **Hook rule:** Prefer hooks with a turn, especially a `but`-style reversal, over descriptive openings that merely set a scene.
- **Article rule:** Small wording choices matter in aphoristic hooks. `A happy path is not an automation` is sharper than `The happy path is not the automation`.
- **Metaphor rule:** Prefer metaphors that carry an actual system relationship. For personal AI, wall/plumbing/decor may be stronger than plumbing alone.
- **Operator rule:** When writing about agent/human collaboration, avoid overexplaining the human. Prefer language like `shared workspace between agent and operator` when it preserves the balance.
- **Canon rule:** Do not overfit to older posts written before the current skill chain.

## Proposed Skill Changes

1. Add `taste-memory.md` under `skills/write-post/references/` with the taste rules above and the source examples.
2. Reference `taste-memory.md` from `write-post/SKILL.md`, especially in hook lab, demo planning, Zinsser, and read-aloud stages.
3. Add eval cases for:
   - `but`-turn hook rewrites
   - simplifying an over-heavy diagram instead of cutting it
   - keeping prompt blocks that function as useful demos
   - preserving agent/operator balance without overexplaining the human
4. Keep this as a subjective guidance layer, separate from hard proof-gate behavior.

## Candidate Rewrite Directions

- Contacts.app hook:
  - Current: `I tried to make the agent smarter. The answer was already sitting in Contacts.app.`
  - Direction: `I tried to make the agent smarter, but the answer was already sitting in Contacts.app.`
- Automation hook:
  - Current: `The happy path is not the automation.`
  - Direction: `A happy path is not an automation.`
- Magic/plumbing line:
  - Current: `Magic is allowed at the interface. The inside should look like plumbing.`
  - Direction: explore wall metaphor: plumbing in the walls; paint, wallpaper, and decor on the outside.
- Contacts.app human-work line:
  - Current: `Not because Contacts.app is glamorous. Because it is already where the human work happens.`
  - Direction: `Not because Contacts.app is glamorous. Because it is already the shared workspace between agent and operator.`

## Next Implementation Plan

Implement the taste memory and a small eval extension in a separate change. Do not rewrite existing posts automatically unless explicitly requested.
