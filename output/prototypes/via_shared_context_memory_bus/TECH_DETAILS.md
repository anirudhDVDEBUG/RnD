# Technical Details — Via Shared Context & Memory Bus

## What It Does

Via is an MCP (Model Context Protocol) server that provides a **shared state layer** for AI coding tools. Instead of each tool (Claude Code, Cursor, Windsurf) operating in isolation with its own context window, Via gives them a common memory, task tracker, and real-time context bus backed by local file persistence. It uses the stdio transport — each AI tool spawns Via as a child process, and they all read/write to the same JSON data file on disk.

The core problem it solves: when you switch between AI tools mid-project, you lose all the context, decisions, and progress from the previous tool. Via eliminates this by acting as the "shared brain" that every tool can read from and write to.

## Architecture

```
┌─────────────┐    stdio     ┌──────────────────┐     ┌──────────────┐
│ Claude Code  │◄────────────►│                  │     │              │
├─────────────┤              │   Via MCP Server  │◄───►│ .via_data.json│
│   Cursor     │◄────────────►│                  │     │ (persistence)│
├─────────────┤              │  9 MCP tools:     │     └──────────────┘
│  Windsurf    │◄────────────►│  memory_*         │
├─────────────┤              │  task_*           │
│  Any MCP     │◄────────────►│  context_*        │
│  client      │              └──────────────────┘
└─────────────┘
```

### Key Files (this demo)

| File | Purpose |
|---|---|
| `via_server.js` | MCP server — 9 tools for memory, tasks, and context |
| `demo_client.js` | MCP client that simulates 3 AI tools using the bus |
| `.via_data.json` | Auto-generated persistence file (JSON) |
| `run.sh` | One-command demo runner |

### Data Flow

1. **Write path:** AI tool calls an MCP tool (e.g., `memory_store`) → Via processes the request → updates in-memory store → writes to `.via_data.json`
2. **Read path:** AI tool calls `memory_retrieve` or `context_read` → Via reads from in-memory store → returns JSON result via MCP
3. **Cross-tool sync:** Because all tools' Via instances read/write the same `.via_data.json`, a decision stored by Claude Code is immediately available when Cursor calls `memory_retrieve`

### Dependencies

- **`@modelcontextprotocol/sdk`** — Anthropic's official MCP SDK for server and client
- **Node.js built-ins** — `fs`, `path` for file persistence
- No external databases, no API keys, no cloud services

### Three Subsystems

| Subsystem | Tools | Use Case |
|---|---|---|
| **Memory Bus** | `memory_store`, `memory_retrieve`, `memory_list` | Persistent key-value store with tags. Store architectural decisions, naming conventions, API schemas. |
| **Task Bus** | `task_create`, `task_update`, `task_list` | Shared task tracker with priority, assignee, status. Coordinate work across tools. |
| **Context Bus** | `context_push`, `context_read`, `context_clear` | Real-time context stream. Share findings, questions, decisions as they happen. |

## Limitations

- **File-based persistence only.** The JSON file approach doesn't scale to large teams or high-throughput scenarios. No database, no CRDT, no conflict resolution.
- **No authentication or access control.** Any process that can read the data file has full access. Fine for local dev; not for shared/production use.
- **No real-time push notifications.** Tools must poll (call `context_read`) to see updates. There's no WebSocket or event stream.
- **Single-machine by default.** Cross-machine sync requires the data file to be on shared storage (NFS, Dropbox, etc.). No built-in network transport.
- **No encryption.** Context and memory are stored as plaintext JSON. Sensitive data (API keys, credentials) should not be stored here.
- **Concurrent write risk.** If two Via instances write simultaneously, the last write wins. No locking or journaling.

## Why It Matters for Claude-Driven Products

| Domain | Application |
|---|---|
| **Agent Factories** | Multi-agent systems where specialized agents (researcher, coder, reviewer) need to share state. Via is the coordination bus. |
| **Lead-gen / Marketing** | An AI pipeline where one agent researches prospects, another drafts outreach, and a third manages the campaign — all sharing context through Via. |
| **Ad Creatives** | Creative iteration across tools: Claude generates copy, Cursor builds the landing page, both reference the same brand guidelines stored in Via's memory. |
| **Voice AI** | A voice agent stores conversation summaries in Via's memory, so a follow-up text-based agent has full context without re-asking. |
| **Developer Tooling** | The most direct use case: stop losing context when switching between Claude Code and Cursor mid-task. Every decision, every finding, every task persists. |

The broader pattern Via demonstrates — **a shared context bus for autonomous agents** — is foundational for any multi-agent system, regardless of whether the agents are AI coding tools or domain-specific pipelines.
