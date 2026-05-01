---
name: tldr-skill
description: Use when the user asks for a TLDR, concise summary, honest distillation, or quick takeaway from text.
---

# TLDR Skill

Distill the input without pretending certainty.

## Response pattern

```txt
TL;DR: <one sentence>
Key points:
- <point 1>
- <point 2>
- <point 3>
Caveat: <what is missing, uncertain, or easy to overstate>
```

## Keep it small

- Do not add facts not present in the input.
- Do not preserve every detail.
- Prefer concrete claims over vague summaries.
- If the input is too thin, say what is missing.
- Do not tailor to the user unless user context is explicitly provided.
