# Pi And OpenClaw Adapter Boundary

These agent packs are portable prompt contracts, not standalone executables.

`agent.md` is the Pi-compatible contract:
- role
- model class
- required and optional tools
- input/output contract
- rules

A Pi host should load `agent.md` as the `systemPrompt` for `@mariozechner/pi-agent-core`:

```ts
import { readFile } from "node:fs/promises";
import { Agent } from "@mariozechner/pi-agent-core";
import { getModel } from "@mariozechner/pi-ai";

const systemPrompt = await readFile("agents/course-builder/agent.md", "utf8");

const agent = new Agent({
  initialState: {
    systemPrompt,
    model: getModel("anthropic", "claude-sonnet-4-20250514"),
    tools: [],
  },
});

await agent.prompt("Build a short course from this brief: ...");
```

`AGENTS.md` is the OpenClaw adapter:
- local skill-loading guidance
- workspace placement rules
- OpenClaw-specific conventions

Do not put OpenClaw-only paths, account assumptions, credentials, or local model IDs in `agent.md`.

The unresolved executable gap is intentional for now: this workspace does not currently have a committed TypeScript package for launching these agents. Add that only when there is a real runtime target, package manager setup, and model mapping to test.
