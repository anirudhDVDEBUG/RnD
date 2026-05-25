---
name: knowledge_shelf_mcp
description: |
  Set up and use Knowledge Shelf, a personal knowledge management MCP server for AI coding assistants.
  Triggers: "set up knowledge shelf", "knowledge management MCP", "store code patterns locally",
  "personal knowledge base for AI", "knowledge-shelf MCP server"
---

# Knowledge Shelf MCP Server

A personal knowledge management system for AI coding assistants, built as an MCP server. Store documentation, code patterns, templates, and workflows locally — AI pulls only what it needs, when it needs it.

## When to use

- "Set up a personal knowledge base for my AI coding assistant"
- "I want to store code patterns and templates locally for AI to use"
- "Configure knowledge-shelf MCP server"
- "How do I manage reusable knowledge items for Claude Code?"
- "Store documentation and workflows that AI can pull on demand"

## How to use

### 1. Install Knowledge Shelf

```bash
npm install -g knowledge-shelf
```

Or use npx to run without installing:

```bash
npx knowledge-shelf
```

### 2. Configure as MCP Server

Add Knowledge Shelf to your Claude Code MCP configuration (`.claude/settings.json` or project-level config):

```json
{
  "mcpServers": {
    "knowledge-shelf": {
      "command": "npx",
      "args": ["-y", "knowledge-shelf"],
      "type": "stdio"
    }
  }
}
```

### 3. Organize Your Knowledge

Knowledge Shelf stores items locally on your filesystem. Create and organize:

- **Documentation** — API references, internal docs, architecture notes
- **Code patterns** — Reusable code snippets, design patterns, idioms
- **Templates** — Project scaffolding, boilerplate, starter files
- **Workflows** — Step-by-step procedures, deployment checklists, runbooks

### 4. Use with AI Assistants

Once configured, your AI coding assistant can:

- Search your knowledge shelf for relevant items
- Pull specific documentation or patterns on demand
- Reference stored templates when scaffolding new code
- Follow stored workflows for complex procedures

The AI only pulls what it needs, when it needs it — keeping context windows efficient.

### Key Features

- **Local-first**: All knowledge stored on your machine
- **MCP protocol**: Works with any MCP-compatible AI assistant
- **On-demand retrieval**: AI fetches only relevant knowledge items
- **TypeScript**: Built with TypeScript for type safety

## References

- **Repository**: https://github.com/joutvhu/knowledge-shelf
- **npm**: `knowledge-shelf`
- **Protocol**: [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
