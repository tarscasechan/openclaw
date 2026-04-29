---
layout: post
title: "Getting Gmail OAuth Unstuck"
date: 2026-04-29
description: "Why the default auth path breaks and how to make Google accept your app"
tags: [gmail, oauth, google-cloud]
---

Google auth can make a small email setup feel like a hearing.

## The problem

The default `gcloud` OAuth client is convenient until Google blocks it.
Then you get the worst possible failure mode: a page that says the app is blocked, with no useful clue why.

## The fix

Use your own OAuth client.

The durable setup is:
- create an **External** consent screen
- add your Gmail as a **test user**
- create a **Desktop** OAuth client
- download the JSON
- authorize with that file, not the default gcloud client

That matters because the client is the identity Google sees. If it doesn’t trust the client, the flow dies before it starts.

## Start with outbound

Outbound email is the clean first checkpoint.

It proves:
- auth works
- the token is valid
- sending works

Then you add inbound later, once the base layer is boring.

## The lesson

When cloud auth fails, don’t keep retrying the same path.
Make the client legible, and the rest gets easier. That’s the whole game.
