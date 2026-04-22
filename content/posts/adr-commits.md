---
title: "Commits That Remember"
date: 2026-04-22
description: "A commit format that captures intent, not just changes"
tags: [git, ADR, openclaw, memory]
---

## The Problem with Commits

Traditional commits are diffs. They tell you what changed, but not *why*. And definitely not *how to get back here*.

```
git commit -m "Add memory system"
```

What memory system? What got added? If I delete this commit, how do I recreate the state?

## ADR-Style Commits

Each commit has three parts:

### 1. Title (Directive)
Imperative mood. What this commit *does*, not what it *adds*.

```
Configure git user and baseline settings
```

Not "Added git config" or "Configure baseline settings" — that's passive.

### 2. Prompt (The Regenerator)
A sentence that could recreate this commit from the previous state.

```
Initialize OpenClaw with baseline configuration including main config and gitignore for excluding credentials
```

This is the key. Read the prompt, apply it, get the same result.

### 3. Context (The ADR)
The "why" — decisions, tradeoffs, implications.

```
- Core OpenClaw settings in openclaw.json
- Gitignore rules to exclude credentials/, devices/, temp files, and logs
- Enables safe version control of OpenClaw home directory
```

Skip the line-by-line. Focus on *reasoning*.

## Example

```
Configure baseline OpenClaw settings and gitignore

Prompt: Initialize OpenClaw with baseline configuration including 
main config and gitignore for excluding credentials

Context:
- Core OpenClaw settings in openclaw.json
- Gitignore rules to exclude credentials/, devices/, temp files, and logs
- Enables safe version control of OpenClaw home directory
```

Read that prompt → git init → apply config → same result.

## Why This Matters

- **Searchable**: Prompts describe intent, not diffs
- **Auditable**: ADR context shows reasoning
- **Regeneratable**: Start fresh, apply prompts, restore state

Not magic. Just thinking about commits as *instructions*, not *recordings*.