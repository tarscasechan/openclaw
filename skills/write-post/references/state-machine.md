# Write Post State Machine

Use this for orchestration, resume, and evals. Writing judgment still matters, but state transitions should be explicit.

## States

- `ideate`
- `voice_contract`
- `hook_lab`
- `research_pain`
- `package`
- `reader_journey`
- `demo_plan`
- `draft`
- `demo_execution`
- `humanity_edit`
- `zinsser_edit`
- `read_aloud`
- `image_decision`
- `done`
- `blocked`
- `restart_from_concept`

## Normal path

`voice_contract -> ideate -> hook_lab -> research_pain -> package -> reader_journey -> demo_plan -> draft -> demo_execution -> humanity_edit -> zinsser_edit -> read_aloud -> image_decision -> done`

## Gate failures

- weak reader, angle, or pain -> `restart_from_concept`
- unclear speaker, reader relationship, or pronoun stance -> `voice_contract`
- gimmicky or generic hook -> `hook_lab`
- missing input that blocks useful work -> `blocked`
- weak Want/Need/Get -> `restart_from_concept`
- reader journey reads like outline headings instead of natural beats -> `reader_journey`
- weak brief at draft time -> `blocked` or `restart_from_concept`; do not draft
- decorative demo -> stay in `demo_plan` or `demo_execution` and return `skip`
- edit pass would flatten voice -> stay in current edit state and make a smaller edit
- tightening removed warmth, pronouns, or lived texture -> `read_aloud`

## Resume rule

If `tasks/write-post.md` names a current stage or next slice, resume there. Do not restart from `voice_contract` or `ideate` unless the state says `restart_from_concept`.

## Demo rule

For system flows, prefer one compact Mermaid diagram. Use ASCII only when the target format cannot render Mermaid.

Plan the demo before drafting. Execute it after the draft proves the demo still earns its place.
