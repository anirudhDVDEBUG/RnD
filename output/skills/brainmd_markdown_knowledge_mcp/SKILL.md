---
name: brainmd_markdown_knowledge_mcp
description: |
  Set up and use brain.md — a local-first markdown knowledge base with a first-class MCP server.
  Provides 16 tools + 2 resources for semantic RAG via LanceDB, per-folder permissions, and a single Bun binary.
  TRIGGER: user wants a local markdown knowledge base, MCP-powered note-taking, semantic search over notes,
  second-brain setup, or vector-indexed markdown files for AI agents.
---

# brain.md — Local-First Markdown Knowledge Base with MCP Server

A local-first markdown notes system with a first-class MCP server. It provides 16 tools and 2 resources for Claude Code, Claude Desktop, Cursor, and any MCP-compatible agent. Features per-folder permissions, semantic RAG via LanceDB, and ships as a single Bun binary.

## When to use

- "Set up a local knowledge base that Claude can search and write to"
- "I want semantic search over my markdown notes from Claude Code"
- "Install brain.md as an MCP server for my second brain"
- "Configure a RAG-powered note-taking system with vector search"
- "I need an Obsidian alternative that works natively with AI agents"

## How to use

### 1. Install brain.md

brain.md requires [Bun](https://bun.sh) as its runtime.

```bash
# Install Bun if not already installed
curl -fsSL https://bun.sh/install | bash

# Clone and install brain.md
git clone https://github.com/mi4uu/brain.md.git
cd brain.md
bun install
```

### 2. Configure as MCP Server for Claude Code

Add brain.md to your Claude Code MCP settings (`.claude/settings.json` or project-level):

```json
{
  "mcpServers": {
    "brain-md": {
      "command": "bun",
      "args": ["run", "/path/to/brain.md/src/index.ts"],
      "env": {
        "BRAIN_MD_ROOT": "/path/to/your/notes"
      }
    }
  }
}
```

For Claude Desktop, add the same configuration to your `claude_desktop_config.json`.

### 3. Key Features

- **16 MCP Tools**: Create, read, update, delete, search, and organize markdown notes
- **2 MCP Resources**: Access note indexes and metadata
- **Semantic RAG**: Vector search powered by LanceDB for intelligent note retrieval
- **Per-folder permissions**: Control which folders agents can read/write
- **Local-first**: All data stays on your machine — no cloud dependency
- **Single binary**: Ships as a single Bun binary for easy deployment
- **Obsidian-compatible**: Works with standard markdown files and folder structures

### 4. Usage with Claude Code

Once configured, Claude Code can use brain.md tools to:

```
# Search notes semantically
"Search my notes for anything related to project architecture decisions"

# Create new notes
"Create a new note summarizing today's meeting"

# Read and reference existing notes
"What do my notes say about the API design?"

# Organize knowledge
"Tag all notes mentioning deployment with a 'devops' label"
```

### 5. Configuration Options

Set environment variables to customize behavior:

- `BRAIN_MD_ROOT` — Path to your notes directory (required)
- Configure per-folder permissions to restrict agent access to specific directories
- LanceDB vector index is built automatically on first run for semantic search

## References

- **Repository**: https://github.com/mi4uu/brain.md
- **License**: AGPL
- **Runtime**: [Bun](https://bun.sh)
- **Vector DB**: [LanceDB](https://lancedb.com)
- **Topics**: mcp-server, knowledge-management, markdown-notes, rag, vector-search, local-first, second-brain
