# Smoke Test

## Case A: decided

Input:

> Can you send me the notes from yesterday? No rush.

Expected shape:

```txt
Status: decided
Decision: do
Why: They asked for a specific item and expect a response.
Next: Send the notes when available.
Draft: Sure — I’ll send them over. No rush noted.
```

## Case B: needs clarification

Input:

> The thing we discussed is broken again.

Expected shape:

```txt
Status: needs-clarification
Decision: —
Why: “The thing” is ambiguous.
Next: Ask what is broken.
Draft: What thing is broken again?
```
