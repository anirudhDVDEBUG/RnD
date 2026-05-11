---
name: via_shared_context_memory_bus
description: |
  Set up and use Vektor-Memory/Via — the universal integration layer that connects Claude, Cursor, Windsurf, ChatGPT, LangChain, and other AI tools to a shared context, task, and memory bus via MCP.
  TRIGGER: user wants shared context across AI tools, cross-tool memory, universal AI integration layer, MCP shared memory bus, or syncing state between Claude and other AI agents
---

# Via — Shared Context & Memory Bus for AI Tools

Via is an MCP server that acts as a universal integration layer for AI tools. It connects Claude Code, Cursor, Windsurf, ChatGPT, LangChain, and every other AI tool to a shared context, task, and memory bus — so your work follows you across every tool, every session, and every machine.

## When to use

- "I want to share context between Claude Code and Cursor"
- "Set up a shared memory bus across my AI tools"
- "How do I sync tasks and context between different AI agents?"
- "I need a universal integration layer for my AI workflow"
- "Connect Claude and other LLM tools to a shared state"

## How to use

### 1. Install Via

```bash
# Clone the repository
git clone https://github.com/Vektor-Memory/Via.git
cd Via

# Install dependencies
npm install
```

### 2. Configure as an MCP Server

Add Via to your Claude Code MCP configuration (in `.claude/settings.json` or project-level `.mcp.json`):

```json
{
  "mcpServers": {
    "via": {
      "command": "node",
      "args": ["/path/to/Via/index.js"],
      "type": "stdio"
    }
  }
}
```

For other tools (Cursor, Windsurf, etc.), add the same MCP server configuration following each tool's MCP setup instructions.

### 3. Use shared context across tools

Once Via is running as an MCP server for multiple AI tools:

- **Shared Memory**: Store and retrieve context that persists across tools and sessions
- **Task Bus**: Create and track tasks that are visible to all connected AI tools
- **Context Sync**: Work started in one tool (e.g., Claude Code) can be continued seamlessly in another (e.g., Cursor)
- **Cross-machine support**: Your context follows you across machines when backed by shared storage

### 4. Key concepts

- **Context Bus**: A shared channel where all connected AI tools can read and write contextual information
- **Task Management**: Create, update, and complete tasks that any connected tool can access
- **Memory Persistence**: Information stored via Via persists across sessions, so you never lose context
- **Universal Protocol**: Uses MCP (Model Context Protocol) for standardized communication between tools

## References

- **Repository**: https://github.com/Vektor-Memory/Via
- **Language**: JavaScript
- **Protocol**: MCP (Model Context Protocol) via stdio transport
- **License**: See repository for details
