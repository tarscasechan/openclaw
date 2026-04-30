---
layout: post
title: "Gmail OAuth Fails Before Your Code Gets a Vote"
date: 2026-04-29
description: "When Google blocks the default client, stop retrying and make the OAuth client legible."
tags: [gmail, oauth, google-cloud]
---

The Gmail bug was not in the email code.

That was the annoying part. Sending mail was not failing because the message was malformed, or because the API call was wrong, or because the assistant had the wrong abstraction. The flow died earlier, at consent.

Google looked at the OAuth client and said no.

When auth fails there, more application code does not help. You are not debugging Gmail yet. You are trying to get Google to trust the doorway.

## The failure mode

The default `gcloud auth application-default login` path is convenient until it is not. It can send you through a Google-managed OAuth client that works for some scopes and setups, then fails with a blocked-app style error when you ask for something more sensitive.

That failure is especially irritating because it feels like a local configuration bug. You rerun the command. You adjust scopes. You delete tokens. You try again. The browser still refuses the flow before your code ever receives credentials.

The important reframe is simple:

> The OAuth client is part of the product Google is evaluating.

If the client is not acceptable for the scopes you requested, the rest of the setup does not matter yet.

## The useful fix

Use your own desktop OAuth client.

Not a service account. Not a mystery default. A normal OAuth client that belongs to your Google Cloud project, with a consent screen you can inspect and a test user you control.

The rough shape is:

1. create or choose a Google Cloud project
2. configure the OAuth consent screen
3. choose **External** if this is a personal Gmail/test setup
4. add your Gmail account as a test user
5. create a **Desktop app** OAuth client
6. download the client JSON
7. run ADC login with that client and the scopes you need

The command should look like this, with your own client file path:

```bash
gcloud auth application-default login \
  --client-id-file=/path/to/google-oauth-desktop.json \
  --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/gmail.send
```

The `cloud-platform` scope can be necessary for application-default credentials flows. The Gmail scope is the actual permission you are trying to prove. For broader mailbox work, use only the additional Gmail scopes the workflow truly needs.

## Why this works

This moves the question from “will Google bless the default client for my use case?” to “is my explicit client configured correctly?”

That is a better question because you can answer it.

You can see the consent screen. You can see whether the user is added as a tester. You can see the app type. You can see which project owns the client. You can regenerate the JSON if you chose the wrong type.

It also creates a cleaner future debugging path. If the browser flow succeeds and the token exists, then you can start debugging API calls. If Gmail send fails after that, you are in email territory. Before that, you are in OAuth territory.

Keeping those layers separate saves a lot of pointless motion.

## Start with one outbound proof

Do not build the whole mail assistant the moment auth succeeds.

Send one controlled message first, or list one harmless resource if you are only proving read access. The first checkpoint should answer a narrow question: can this credential do the one thing the next layer needs?

For outbound mail, the proof is small:

- the consent flow completes
- credentials land where the CLI expects them
- the Gmail API accepts the token
- a test send succeeds

Only then should the workflow grow into inbound triage, contact allowlists, reply policy, archiving, or scheduling.

That order matters. Otherwise an OAuth bug, a Gmail query bug, and an agent policy bug all arrive wearing the same costume.

## The tradeoff

Owning the OAuth client adds ceremony.

You now have a Google Cloud project to understand. You have a consent screen to configure. You have a downloaded client file to protect. If the app leaves testing mode or gains more users, you may hit verification requirements. None of that is fun.

But it is still better than treating a blocked consent flow like a code problem.

The ceremony buys legibility. Google knows which client is asking. You know which project owns it. The assistant knows which credential path it is using. The failure, when it happens, has a smaller blast radius.

## The lesson

When Gmail OAuth gets stuck, stop pushing on the send button.

First make the client legible. Then prove one scope. Then build the workflow.

Auth is not the boring prelude to the system. Auth is the first boundary the system has to respect.
