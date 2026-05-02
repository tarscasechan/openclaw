# Durable Agents

Each agent directory is a portable Pi-agent package with an OpenClaw adapter.

See `ADAPTER.md` for the boundary between these prompt packages and an executable `@mariozechner/pi-agent-core` host.

Minimum shape:

```txt
agent-name/
  agent.md        # portable Pi-compatible contract
  AGENTS.md       # OpenClaw adapter for this workspace
  SOUL.md         # terse voice/taste layer
  examples/       # prompts or smoke-test inputs
  evals/          # checklist or harness inputs
```

Rules:
- Keep `agent.md` runtime-portable: role, contract, model class, and tool requirements.
- Keep OpenClaw-specific paths, skill-loading behavior, and workspace placement rules in `AGENTS.md`.
- Do not require credentials, private data, or external writes for the first smoke test.
- Add eval cases before claiming an agent is ready.
- Promote reusable methods to `skills/`; keep course-only snapshots in `courses/examples/`.
