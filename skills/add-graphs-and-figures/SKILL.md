---
name: add-graphs-and-figures
description: Add code blocks, Mermaid graphs, tables, or other demonstrations when they clarify a post’s core idea. Use for builder-focused posts and technical explanations.
---

# Add Graphs and Figures

## Goal

Plan and add demonstrations that teach faster than prose.

## Two passes

1. **Demo plan before drafting**: decide whether the post is building toward no demo, Mermaid, code, before/after, table, or image.
2. **Demo execution after drafting**: add the demo only if the draft still proves it teaches faster than prose.

## Prefer

- Mermaid for architecture and flow
- small code blocks for setup or usage
- tiny before/after examples
- one visual only when it earns its keep

## Rules

- Do not decorate.
- Do not repeat the prose.
- Reject a graph for a single clear sentence unless the visual adds a new relationship.
- When the user asks for a specific multi-step flow, a single compact Mermaid diagram is usually the right demo.
- Prefer Mermaid for system flows. Use ASCII only when the target format cannot render Mermaid.
- For demo-plan requests, return the plan and the reason. Do not create the demo yet.
- For demo-execution requests, answer with either one demo or a short "skip it" decision. Do not draft the surrounding article.
- If the demo does not clarify the conceit, leave it out.

## Examples

- `Agents should update a task file after each meaningful step.` -> skip the diagram; the sentence is already clearer than a visual.
- `user request -> task file -> model slice -> proof gate -> resume` -> use one compact Mermaid flow.
