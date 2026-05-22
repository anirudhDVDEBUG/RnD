---
name: datasette_agent_sprites_sandbox
description: |
  Set up and use datasette-agent-sprites to run commands in a Fly Sprites sandbox via the Datasette Agent plugin system.
  TRIGGER: datasette agent sprites, fly sprites sandbox, datasette sandbox plugin, datasette agent sandbox execution, sandboxed datasette commands
---

# Datasette Agent Sprites Sandbox

A skill for integrating **datasette-agent-sprites**, a Datasette Agent plugin that enables running commands inside a [Fly Sprites](https://sprites.dev) sandbox environment. This provides secure, isolated execution of agent commands through Datasette's plugin system.

## When to use

- "Set up datasette-agent-sprites for sandboxed command execution"
- "Run Datasette Agent commands in a Fly Sprites sandbox"
- "Configure a Datasette plugin for isolated sandbox execution"
- "Install datasette-agent-sprites and connect it to Fly Sprites"
- "Add sandbox support to my Datasette Agent workflow"

## How to use

### 1. Install the plugin

```bash
pip install datasette-agent-sprites
```

Or install the alpha release directly:

```bash
pip install datasette-agent-sprites==0.1a0
```

### 2. Prerequisites

- **Datasette** must be installed and configured.
- **Datasette Agent** must be installed (the plugin extends its functionality).
- A **Fly.io** account with access to [Fly Sprites](https://sprites.dev) for sandbox environments.
- A valid Fly.io API token configured in your environment.

### 3. Configure Fly Sprites access

Ensure your Fly.io credentials are available:

```bash
export FLY_API_TOKEN="your-fly-api-token"
```

### 4. Use with Datasette Agent

Once installed, the plugin registers itself with Datasette Agent's plugin system. Commands executed through the agent can be routed to a Fly Sprites sandbox, providing:

- **Isolated execution**: Commands run in ephemeral Fly Sprites VMs, not on your host machine.
- **Security**: Sandboxed environments prevent unintended side effects.
- **Plugin integration**: Works seamlessly with the Datasette Agent plugin architecture.

### 5. Verify installation

```bash
datasette plugins
```

Confirm `datasette-agent-sprites` appears in the plugin list.

## Key concepts

- **Fly Sprites**: Lightweight, ephemeral sandbox VMs provided by Fly.io for secure command execution.
- **Datasette Agent**: An agent framework built on Datasette that supports plugins for extending its capabilities.
- **Plugin system**: datasette-agent-sprites registers as a Datasette Agent plugin, adding sandbox execution as a capability.

## References

- [datasette-agent-sprites 0.1a0 announcement](https://simonwillison.net/2026/May/21/datasette-agent-sprites/#atom-everything)
- [datasette-agent-sprites on GitHub](https://github.com/datasette/datasette-agent-sprites)
- [Fly Sprites](https://sprites.dev)
- [Datasette documentation](https://docs.datasette.io)
