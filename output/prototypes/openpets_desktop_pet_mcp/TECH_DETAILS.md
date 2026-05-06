# Technical Details — OpenPets

## What it does

OpenPets is an Electron desktop application that renders a pixel-art pet sprite as an always-on-top transparent window. It bundles an MCP (Model Context Protocol) server that communicates over stdio JSON-RPC, allowing AI coding agents like Claude Code to update the pet's visual state in real time. When Claude Code is thinking, coding, hitting errors, or celebrating a success, the pet's animation changes to match — giving developers a glanceable, ambient indicator of agent activity without switching windows.

The MCP server exposes four tools: `set_pet_status` (change the pet's state and optional message), `get_pet_status` (query current state), `list_pets` (enumerate available characters), and `set_pet_character` (swap the active sprite). The desktop app listens for state changes and swaps between pre-rendered pixel-art animation frames.

## Architecture

```
Claude Code (or any MCP client)
    |
    |  stdio JSON-RPC (MCP protocol)
    v
+-------------------------+
|  src/mcp-server.ts      |  <- MCP server process
|  - Tool handlers         |
|  - State management      |
+----------+--------------+
           |  IPC / shared state
           v
+-------------------------+
|  Electron Main Process  |
|  - BrowserWindow (pet)  |
|  - Transparent, on-top  |
|  - Loads pet renderer   |
+----------+--------------+
           |
           v
+-------------------------+
|  Pet Renderer (HTML/CSS)|
|  - Sprite sheet loading |
|  - Frame animation loop |
|  - Status text overlay  |
+-------------------------+
```

**Key files** (in the real repo):
- `src/mcp-server.ts` — MCP stdio server, tool definitions, state machine
- `src/main.ts` — Electron main process, window management
- `src/renderer/` — Pet animation, sprite rendering
- `pets/` — Pixel-art sprite sheets (32x32 PNG frames)
- `package.json` — Bun + Electron dependencies

**Dependencies**: Bun (runtime), Electron (desktop window), TypeScript. No external API keys or cloud services required.

## Data flow

1. Claude Code spawns the MCP server as a child process (`bun run src/mcp-server.ts`)
2. Agent sends `tools/call` JSON-RPC messages (e.g., `set_pet_status({status: "coding"})`)
3. MCP server updates internal state and notifies the Electron main process
4. Electron main process sends IPC message to the renderer
5. Renderer swaps sprite animation to match the new state
6. Pet visually changes on the user's desktop within ~50ms

## Limitations

- **Desktop only** — requires a display server (X11/Wayland/macOS/Windows). Won't work in headless or SSH sessions.
- **Bun required** — not compatible with plain Node.js out of the box (uses Bun-specific APIs).
- **Manual path config** — the MCP config requires an absolute path to the cloned repo.
- **Agent must call tools** — the pet only updates when the agent explicitly calls `set_pet_status`. There's no automatic detection of agent activity; the agent (or a wrapper) must be MCP-aware and choose to call the tool.
- **Single pet instance** — only one pet displayed at a time.
- **No persistent state** — pet state resets when the MCP server restarts.

## Why this matters for Claude-driven products

- **Agent UX layer**: As AI agents become background workers (code gen, lead-gen pipelines, ad creative generation), users need ambient status indicators. OpenPets demonstrates a pattern — MCP-based status broadcasting — that applies beyond pets to dashboards, Slack bots, or monitoring widgets.
- **MCP ecosystem signal**: Every new MCP server expands what Claude Code can do without custom integrations. OpenPets proves MCP works for real-time UI updates, not just data retrieval.
- **Developer experience differentiation**: For teams building agent factories or voice-AI pipelines, adding a visual status layer increases trust and reduces "is it still working?" anxiety during long-running agent tasks.
- **Low-friction adoption**: No API keys, no cloud accounts, no billing. Clone, install, configure, working pet in under 2 minutes.
