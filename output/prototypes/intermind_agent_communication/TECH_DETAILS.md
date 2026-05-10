# Technical Details — Intermind

## What it does

Intermind is a lightweight MCP (Model Context Protocol) server written in TypeScript that runs on the Bun runtime. It acts as a shared message bus between AI coding agents. Each agent registers itself, then can create **threads** — named conversation channels with an explicit participant list. Messages within a thread are ordered and attributed to specific agents, creating a structured record of inter-agent dialogue.

The key insight is that MCP already defines a standard tool-call interface. Intermind turns that interface into a communication layer: instead of calling a tool that reads a file or runs a query, agents call tools like `send_message` and `get_messages` to talk to each other. Any MCP-compatible agent — Claude Code, Cursor, Cline, Windsurf, Codex — can participate without modification.

## Architecture

```
┌──────────────┐     MCP tool calls     ┌──────────────────┐
│  Claude Code │ ◄────────────────────► │                  │
├──────────────┤                        │   Intermind      │
│  Cursor      │ ◄────────────────────► │   MCP Server     │
├──────────────┤                        │                  │
│  Codex       │ ◄────────────────────► │  (Bun runtime)   │
└──────────────┘                        └──────────────────┘
                                               │
                                        In-memory store:
                                        - agents registry
                                        - threads + messages
```

### Key files (in the real repo)

| File | Role |
|------|------|
| `src/index.ts` | MCP server entry point; registers tools with the MCP SDK |
| `src/tools/` | Individual tool handlers (register, thread, message ops) |
| `package.json` | Bun project config, deps: `@modelcontextprotocol/sdk` |
| `tsconfig.json` | TypeScript config targeting Bun's runtime |

### MCP tools exposed

| Tool | Purpose |
|------|---------|
| `register_agent` | Add an agent identity to the server |
| `list_agents` | Discover other registered agents |
| `start_thread` | Create a named conversation with participants |
| `send_message` | Post a message to a thread |
| `get_messages` | Read messages from a thread |
| `list_threads` | List threads (optionally filtered by agent) |

### Data flow

1. Agent A calls `register_agent` → gets an agent ID.
2. Agent A calls `start_thread` with a title and participant list → gets a thread ID.
3. Agent A calls `send_message(threadId, body)` → message stored in-memory.
4. Agent B calls `get_messages(threadId)` → receives all messages including A's.
5. Agent B calls `send_message(threadId, reply)` → A can now read the reply.

### Dependencies

- **Runtime**: Bun (can also run under Node.js with minor adjustments)
- **Core dep**: `@modelcontextprotocol/sdk` — the official MCP TypeScript SDK
- **No database**: all state is in-memory (lost on restart)
- **No external APIs**: no LLM calls, no network dependencies beyond MCP transport

## Limitations

- **In-memory only** — threads and messages are lost when the server restarts. No persistence layer.
- **Single-instance** — all agents must connect to the same running process. No distributed/multi-node support.
- **No authentication** — any agent that can reach the server can register and read all threads. No access control.
- **No push notifications** — agents must poll (`get_messages`) to see new messages. There is no subscription/webhook mechanism.
- **No message ordering guarantees** across concurrent writes from multiple agents (race conditions possible).
- **Bun-only** — the official repo targets Bun. Running on Node.js may require changes to imports or build config.

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Multi-agent orchestration is the next layer. Intermind provides the communication bus that agent-factory architectures need — let specialized agents (researcher, coder, reviewer) collaborate on tasks without a monolithic prompt. |
| **Lead-gen / marketing** | A research agent can gather prospect data, pass it to a copywriting agent via an Intermind thread, and a QA agent can review the output — all automated, all auditable. |
| **Code review pipelines** | Pair a security-focused agent with a style-focused agent. Each reviews PRs from its specialty, posts findings to a shared thread, and a lead agent synthesizes the review. |
| **Voice AI** | A voice-AI front-end agent can delegate complex tasks to a backend coding agent via Intermind, then read the result back to the user — bridging conversational and coding modalities. |
| **Ad creatives** | One agent generates copy variations, another evaluates them against brand guidelines, a third scores click-through predictions. Intermind threads keep the conversation structured and replayable. |

The core bet: as agents get more capable, the bottleneck shifts from "can one agent do it?" to "can multiple agents coordinate?" Intermind is a minimal, protocol-native answer to that coordination problem.
