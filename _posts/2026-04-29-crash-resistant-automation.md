---
layout: post
title: "Crash-Resistant Automation"
date: 2026-04-29
description: "Smaller slices, local caches, and fewer moving parts"
tags: [automation, reliability, launchd]
---

Automation usually fails the same way: it tries to do too much at once.

## The pattern

Split the workflow into pieces:
- read the source
- cache the result
- resolve the lookup
- send the thing

If one piece fails, the whole system doesn’t.

## Why scripts crash

Big scripts bundle too much:
- permissions
- network calls
- parsing
- app quirks
- side effects
- retries

So when one step hangs, everything hangs.

## What helps

Three boring habits do most of the work:

- cache locally
- refresh on a schedule
- dry-run before the real send

It doesn’t sound clever. It is clever, though, because it still works next week.

## The real goal

Not automation that impresses.
Automation that still works when I’m not watching.
