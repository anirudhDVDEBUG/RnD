# Technical Details — Claude Pets

## What It Does

Claude Pets bridges Claude Code sessions to the [OpenPets](https://openpets.dev) desktop app via two mechanisms: **lifecycle hooks** that fire on session and tool events, and an **MCP server** that lets Claude directly control the pet. When Claude reads a file, the pet squints in focus; when a test passes, it celebrates; when the session ends, it waves goodbye and sleeps. The hooks send HTTP PUT requests to the OpenPets local API (`localhost:42069`), while the MCP server exposes `set_pet_status` and `get_pet_status` tools over stdio JSON-RPC.

The entire integration is ~200 lines of TypeScript (Bun) with zero npm dependencies. It adds negligible latency to Claude Code — each hook is a single HTTP call that resolves in <10ms on localhost.

## Architecture

```
Claude Code Session
  │
  ├─ on_session_start ──► hooks/on_session_start.ts ──► OpenPets API (PUT /api/pet/status)
  ├─ on_tool_call ──────► hooks/on_tool_call.ts ──────► OpenPets API
  ├─ on_session_end ────► hooks/on_session_end.ts ────► OpenPets API
  │
  └─ MCP stdio ────────► src/mcp-server.ts
                            ├─ set_pet_status(state, message)
                            └─ get_pet_status() → current + history
```

### Key Files (source repo)

| File | Purpose |
|---|---|
| `hooks/on_session_start.ts` | Wakes pet, sets "alert" state |
| `hooks/on_tool_call.ts` | Maps tool name → pet mood (Read→focused, Edit→busy, Bash→happy, etc.) |
| `hooks/on_session_end.ts` | Waves goodbye, sets "sleeping" |
| `src/mcp-server.ts` | Stdio MCP server with 2 tools |
| `setup.ts` | One-command installer: writes hooks + MCP config to Claude settings |

### Data Flow

1. Claude Code fires a hook event (e.g., `on_tool_call` with `{"tool_name":"Read"}`)
2. Hook script maps tool name to a pet state (`Read` → `reading`)
3. Script sends `PUT http://localhost:42069/api/pet/status` with `{state, mood, emoji, message}`
4. OpenPets desktop app renders the updated pet animation

The MCP path is optional and additive — Claude can call `set_pet_status` to send custom messages (e.g., "I found 3 bugs!") beyond the automatic hook-driven states.

### Dependencies

- **Runtime:** Bun (or Node 18+ for this demo)
- **External:** OpenPets desktop app (provides the local HTTP API + pet rendering)
- **npm dependencies:** None (uses built-in `fetch`)

## Limitations

- **OpenPets required:** Without the OpenPets desktop app running, hooks silently fail (no pet to update). The demo repo works in mock mode without it.
- **Local only:** The OpenPets API binds to localhost — no remote pet watching.
- **Limited pet states:** 10 predefined states. Custom animations require modifying OpenPets itself.
- **No Windows support yet:** OpenPets currently supports macOS and Linux.
- **One-way hooks:** Claude Code hooks are fire-and-forget; the pet cannot send data back to Claude through hooks (only through the MCP server's `get_pet_status`).
- **No persistence:** Pet state history is in-memory only, lost when the MCP server restarts.

## Why It Matters

For teams building Claude-driven products, claude-pets demonstrates two important integration patterns:

1. **Claude Code hooks as a side-channel:** The hook system (`on_tool_call`, `on_session_start`, `on_session_end`) can drive any external system — not just pets. The same pattern works for logging to Datadog, updating a Slack channel, triggering CI, or feeding real-time analytics dashboards. If you're building agent factories or marketing automation, hooks are how you get observability into what Claude is doing without modifying prompts.

2. **MCP as bidirectional control:** The MCP server pattern shown here — exposing simple tools over stdio — is the lightweight way to give Claude access to any local service. For voice AI or ad-creative pipelines, the same `set_status`/`get_status` pattern maps directly to updating campaign state or controlling TTS output.

The implementation is minimal enough to fork and adapt in an afternoon.
