---
title: "Commits That Remember"
date: 2026-04-22
description: "A commit format that captures intent, not just changes"
tags: [git, ADR]
---

Traditional commits are diffs. They tell you what changed, not *why*. Not *how to get back here*.

```
git commit -m "Add memory system"
```

What memory system? Delete this commit — how do you restore it?

## The Format

Each commit has three parts:

### Title (Directive)
Imperative. What this commit *does*.

```
Configure git user and baseline settings
```

### Prompt (Regenerator)
A sentence that could recreate this commit from the previous state.

```
Initialize OpenClaw with baseline configuration including 
main config and gitignore for excluding credentials
```

### Context (ADR)
The *why* — decisions, tradeoffs.

```
- Core settings in openclaw.json
- Gitignore rules exclude credentials/, devices/, temp files
- Enables safe version control
```

## Example

```
Configure baseline OpenClaw settings and gitignore

Prompt: Initialize OpenClaw with baseline configuration...

Context:
- Core settings in openclaw.json
- Gitignore rules exclude credentials/, devices/, temp files
- Enables safe version control
```

Read the prompt → apply → same result.

## Why This Works

- **Searchable**: Prompts describe intent
- **Auditable**: ADR context shows reasoning
- **Regeneratable**: Start fresh, apply prompts, restore state

Commits as *instructions*, not *recordings*.