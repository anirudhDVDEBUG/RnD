# Technical Details

## What It Does

taw-computer is a TypeScript MCP (Model Context Protocol) server that exposes 30+ tools giving AI agents full control over a sandboxed Ubuntu desktop environment. When an MCP client (Claude Code, Cursor, etc.) connects, it can browse the web via Playwright, control the desktop via xdotool/xclip, execute shell commands, and manage files — all inside a Docker container that isolates the agent's actions from the host system.

The server translates high-level MCP tool calls (e.g. `browser_navigate`, `desktop_mouse_click`) into Playwright API calls and Linux system commands running inside the container, then returns structured JSON results back to the AI.

## Architecture

```
┌─────────────────┐         MCP (stdio/SSE)         ┌──────────────────────┐
│  Claude Code /  │◄──────────────────────────────►  │  taw-computer server │
│  Cursor / etc.  │                                  │  (TypeScript/Node)   │
└─────────────────┘                                  └──────────┬───────────┘
                                                                │
                                                     ┌──────────▼───────────┐
                                                     │   Docker Container   │
                                                     │  ┌───────────────┐   │
                                                     │  │ Ubuntu 22.04  │   │
                                                     │  │ + Xvfb + VNC  │   │
                                                     │  │ + Playwright  │   │
                                                     │  │ + xdotool     │   │
                                                     │  └───────────────┘   │
                                                     └──────────────────────┘
```

### Key Files (in the source repo)

| Path | Purpose |
|------|---------|
| `src/index.ts` | MCP server entry point, tool registration |
| `src/tools/browser/` | Playwright-based browser automation tools |
| `src/tools/desktop/` | xdotool/xclip desktop control tools |
| `src/tools/file/` | File read/write/list operations |
| `src/tools/shell/` | Shell command execution |
| `src/tools/window/` | Window management (wmctrl) |
| `docker-compose.yml` | Container orchestration (Ubuntu + VNC + deps) |
| `Dockerfile` | Ubuntu image with Xvfb, Playwright, xdotool |

### Data Flow

1. AI client sends MCP `tools/call` request (JSON-RPC over stdio or SSE)
2. Server routes to the appropriate tool handler
3. Handler executes action inside the Docker container (Playwright for browser, shell for desktop/file)
4. Result (text, base64 image, JSON) returned via MCP response
5. AI client processes result and decides next action

### Dependencies

- **Runtime**: Node.js 18+, Docker
- **Browser engine**: Playwright (Chromium, bundled in container)
- **Desktop**: Xvfb (virtual framebuffer), xdotool, xclip, wmctrl
- **VNC**: noVNC for web-based desktop viewing (port 6080)
- **Protocol**: `@modelcontextprotocol/sdk` for MCP compliance

## Limitations

- **Requires Docker**: No "light" mode — the sandbox must run for any tool to work
- **Single session**: One browser instance, one desktop per container
- **No GPU**: Container runs CPU-only; no WebGL or GPU-accelerated rendering
- **Latency**: Each tool call round-trips through Docker; expect 100-500ms per action
- **No persistent state**: Container resets on restart unless volumes are configured
- **Screenshot bandwidth**: Full-page screenshots are large base64 blobs (~200-400KB each)
- **Linux only in sandbox**: The container is Ubuntu; cannot test Windows/macOS UIs

## Why It Matters for Claude-Driven Products

| Use case | How taw-computer helps |
|----------|----------------------|
| **Lead generation** | Agent browses target sites, fills forms, extracts contact info — all in a sandbox that won't leak credentials |
| **Ad creative testing** | Agent opens ad preview URLs, screenshots them across viewport sizes, compares layouts |
| **Marketing automation** | Agent logs into dashboards, extracts metrics, generates reports without API integrations |
| **Agent factories** | Provides the "hands and eyes" layer — any orchestrator can give sub-agents computer access via MCP |
| **Voice AI + GUI** | Voice agent can trigger visual actions: "show me the dashboard" → agent screenshots and describes it |

The key differentiator vs. Anthropic's built-in computer-use: taw-computer is open-source, self-hosted, works with any MCP client, and the tool set is extensible (add your own tools by dropping files in `src/tools/`).
