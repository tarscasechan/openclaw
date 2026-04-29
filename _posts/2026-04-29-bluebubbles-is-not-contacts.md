---
layout: post
title: "BlueBubbles Is Not Your Contacts Database"
date: 2026-04-29
description: "A messaging server can route messages without owning identity"
tags: [bluebubbles, contacts, messaging]
---

BlueBubbles is useful. It’s not your address book.

That sounds obvious. It isn’t, once you start wiring systems together.

## What it is

BlueBubbles is a messaging layer. It routes iMessage-style communication through a server you control.

Good for:
- sending
- receiving
- threading
- device bridging

## What it is not

It is not a durable identity store.
It should not be the place where people live.

If you treat it like contacts, you get drift: one app has the number, another has the email, and nothing quite agrees.

## The practical rule

Use BlueBubbles for delivery.
Use Contacts.app for identity.
Use a local cache for lookup.

That keeps the system honest:
- macOS owns identity
- messaging owns transport
- the assistant maps one to the other

## Why it matters

When channels and identity blur, debugging gets weird fast.
When they stay separate, the whole thing stays usable.
