# Smoke Test

Happy path:

```txt
User: TLDR this deploy note: The release is delayed because staging failed after a config change. Logs are incomplete.
Expected: tldr-skill is selected and includes a Caveat about incomplete logs.
```

Failure case:

```txt
User: Write a launch announcement for this feature.
Expected: tldr-skill is not selected.
```
