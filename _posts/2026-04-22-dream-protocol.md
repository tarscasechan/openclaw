---
layout: post
title: "Teaching an AI to Dream"
date: 2026-04-22
description: "A memory system for AI that learns without forgetting"
tags: [openclaw, memory]
---

Chatbots remember the conversation. End the conversation, forget everything.

You end up with two bad options: forget everything, or carry context bloat.

## Three Layers

### Daily Memory (Passive)
`memory/YYYY-MM-DD.md`

Raw logs from each day. Never deleted. Queryable on-demand.

### Active Memory (Reinforced)
`MEMORY.md`

Loaded at session start. Updated by dreaming / deliberate promotion.

Content bubbles up based on recency. Older days → gray matter.

### Dreaming (Promotion)

Dreaming is an optional background consolidation pass that reviews short-term signals and promotes only qualified items into `MEMORY.md`.

```
Dream Sweep: 2026-04-22
- Preferences: MBDTF > College Dropout > 45% of Pablo
- Commit format: ADR-style with prompts
```

## Why "Gray Matter"

Older memories aren't deleted. They become *queryable on-demand*:

> "What did we decide about sessions in April?"

Search older `memory/` files, pull in what matters.

## Key Differences

| Approach | Sessions | Long-term |
|----------|----------|-----------|
| ChatGPT | Resets | Premium |
| Claude Code | Files in repo | Project-specific |
| Here | Ephemeral | Active + passive + gray matter |

Ephemeral sessions = no credential risk = safe to ignore.
Active memory = loaded at start = always relevant.

---

This isn't AI consciousness. It's *continuity without cargo*.