# Technical Details: datasette-agent-sprites

## What It Does

datasette-agent-sprites is a Datasette Agent plugin that intercepts agent commands and executes them inside ephemeral Fly Sprites VMs instead of the host machine. When the Datasette Agent wants to run a shell command (e.g., to explore data, install packages, or transform files), this plugin spins up a lightweight sandbox, runs the command, captures stdout/stderr, and returns the result to the agent -- all without the command ever touching the host OS.

This follows the Datasette plugin convention: it uses `pluggy` hooks to register itself with Datasette Agent at startup, declaring a `sandbox` execution capability that the agent can route commands to.

## Architecture

```
Datasette Agent (orchestrator)
    |
    v
datasette-agent-sprites plugin (registered via pluggy hookspec)
    |
    v
Fly Sprites API (POST /machines -> ephemeral VM)
    |
    v
Sprite VM executes command, streams output
    |
    v
Plugin collects result, returns to Agent
```

### Key Components

- **Plugin entry point** (`__init__.py`): Registers with Datasette Agent via `@hookimpl` decorator
- **Sprites client** (`sprites_client.py`): Thin wrapper around Fly Sprites REST API -- creates machines, sends commands, polls for completion
- **Result handler**: Parses stdout/stderr from sprite execution, handles timeouts

### Dependencies

- `datasette` >= 0.65
- `datasette-agent` (the base agent framework)
- `httpx` (async HTTP client for Fly Sprites API calls)
- `pluggy` (plugin system, inherited from Datasette)

### Data Flow

1. Agent decides to execute a command
2. Plugin's `execute_command` hook is called
3. Plugin POSTs to Fly Sprites API to create an ephemeral machine
4. Command is sent to the machine via exec endpoint
5. Plugin polls/streams output until completion or timeout
6. Machine is destroyed automatically (ephemeral)
7. stdout/stderr returned to agent

## Limitations

- **Alpha quality** (0.1a0): API surface may change
- **Requires Fly.io account**: Sprites is a paid Fly.io service; no free tier confirmed
- **Network-dependent**: Each command incurs VM boot latency (~1-3s cold start)
- **No persistent state**: Each command runs in a fresh VM; no filesystem persistence between invocations
- **Limited to Datasette Agent**: Cannot be used standalone; requires the Datasette Agent plugin system

## Why It Matters for Claude-Driven Products

1. **Agent Factories**: This is a pattern for safe agent execution. Any system that spawns agents to run arbitrary commands needs sandboxing. Fly Sprites + plugin architecture = reusable pattern for agent safety.

2. **Security-first agent design**: For production agent systems (lead-gen bots, marketing automation, ad-creative pipelines), you need guardrails. This plugin demonstrates how to add sandboxed execution as a drop-in capability.

3. **Composable agent plugins**: The Datasette Agent plugin architecture (pluggy-based) is a lightweight model for building agent tool registries -- relevant to anyone building MCP servers or skill systems.

4. **Simon Willison's ecosystem signal**: Datasette is widely adopted in data journalism and developer tooling. Agent + Sprites integration signals that sandboxed agent execution is becoming table-stakes infrastructure.
