---
name: triage-message
description: Use for sorting one inbound message with 4D triage language: do, defer, delegate, delete; clarify first when key information is missing.
---

# Triage Message

Read the message once.

First ask: is key information missing?

- If yes, set `Status: needs-clarification`, `Decision: —`, and ask one question.
- If no, set `Status: decided` and choose one 4D decision:

1. Does the sender expect a response, even a low-urgency one? -> `do`
2. Should work happen later with no response expected now? -> `defer`
3. Should someone else handle it? -> `delegate`
4. Is there no action left? -> `delete`

Pick one decision only.
