---
name: intermind_agent_communication
description: |
  Set up and use Intermind, an MCP server that enables threaded conversations between AI coding agents (Claude Code, Codex, Cursor, Cline, Windsurf, etc.).
  TRIGGER: user wants agents to talk to each other, inter-agent communication, multi-agent collaboration, agent-to-agent messaging, MCP agent conversations
---

# Intermind — Agent-to-Agent Communication via MCP

Set up and use the Intermind MCP server to let multiple AI coding agents hold threaded conversations with each other.

## When to use

- "I want my Claude Code agent to communicate with another agent"
- "Set up inter-agent communication between my coding agents"
- "I need multiple AI agents to collaborate on a task via MCP"
- "How do I let Claude Code and Cursor talk to each other?"
- "Set up Intermind for agent-to-agent messaging"

## How to use

### 1. Install Intermind

```bash
# Clone the repository
git clone https://github.com/monkfromearth/intermind.git
cd intermind

# Install dependencies (uses Bun runtime)
bun install

# Build the project
bun run build
```

### 2. Configure as an MCP Server

Add Intermind to your MCP client configuration. For Claude Code, add to your `.claude/settings.json` or project-level MCP config:

```json
{
  "mcpServers": {
    "intermind": {
      "command": "bun",
      "args": ["run", "/path/to/intermind/src/index.ts"]
    }
  }
}
```

For other MCP-compatible clients (Cursor, Cline, Windsurf, Codex), add the equivalent MCP server configuration pointing to the Intermind entry point.

### 3. Use Inter-Agent Communication

Once configured, agents connected to the same Intermind server can:

- **Start threaded conversations** with other agents
- **Send and receive messages** in structured threads
- **Collaborate on tasks** by delegating subtasks to specialized agents
- **Share context** between different AI coding environments

### 4. Multi-Agent Setup

To enable communication between agents:

1. Configure Intermind as an MCP server in each agent's environment
2. Ensure all agents point to the same Intermind instance
3. Agents can then discover and communicate with each other through the MCP protocol

## Key Features

- **Universal MCP compatibility** — works with any MCP-speaking coding agent
- **Threaded conversations** — organized, contextual inter-agent discussions
- **TypeScript/Bun runtime** — fast, modern server implementation
- **Agent-to-agent (A2A) protocol** — structured communication between AI agents

## References

- **Repository**: [monkfromearth/intermind](https://github.com/monkfromearth/intermind)
- **Runtime**: [Bun](https://bun.sh)
- **Protocol**: [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
