# Technical Details — McClaude

## What It Does

McClaude is a two-part system that bridges Claude Code (running locally) with a live Minecraft server. The **Paper/Spigot plugin** (Java) runs inside the Minecraft server, exposing a WebSocket endpoint and WebDAV file server. The **MCP server** (Node.js, installed via `npx mcclaude-mcp`) translates Claude Code's MCP tool calls into WebSocket messages sent to the plugin. All communication is end-to-end encrypted with AES-256-GCM using a shared secret.

This enables a fully live development loop: Claude reads console output, writes Skript files, runs reload commands, and verifies results — all without the developer touching the Minecraft client or server terminal.

## Architecture

```
Claude Code  <-->  MCP Server (Node.js)  <--[AES-256-GCM WebSocket]--> Paper Plugin (Java)
   |                    |                                                     |
   |  MCP protocol      |  WebSocket + JSON                                  |
   |  (stdio)           |  Port 25580                                        |
   |                    |                                                     |
   v                    v                                                     v
 Tool calls       mcclaude-mcp            McClaude.jar in plugins/
                  (npm package)            - Console log buffer
                                           - Command dispatcher
                                           - WebDAV for .sk files
                                           - Eval engine (Groovy/Java)
```

### Key Files (in the upstream repo)

| Path | Purpose |
|------|---------|
| `plugin/src/main/java/.../McClaude.java` | Paper plugin entry point, registers listeners |
| `plugin/src/main/java/.../WebSocketServer.java` | Encrypted WS endpoint, handles all bridge actions |
| `plugin/src/main/java/.../WebDavHandler.java` | Serves Skript files for read/write over HTTP |
| `mcp-server/index.js` | MCP server that Claude Code spawns, translates tool calls to WS messages |
| `mcp-server/encryption.js` | AES-256-GCM encrypt/decrypt using shared secret |

### Data Flow

1. User asks Claude to edit a Skript → Claude calls `write_script` MCP tool
2. MCP server encrypts `{ action: "write_script", payload: { filename, content } }` with AES-256-GCM
3. WebSocket delivers the ciphertext to the Paper plugin on port 25580
4. Plugin decrypts, writes the `.sk` file to `plugins/Skript/scripts/`
5. Plugin returns `{ action: "script_saved" }` (encrypted) back through WebSocket
6. MCP server decrypts and returns structured result to Claude Code

### Dependencies

**Plugin (Java):**
- Paper API 1.21+ (or Spigot)
- Java 17+
- Built-in Java crypto for AES-256-GCM

**MCP Server (Node.js):**
- `ws` — WebSocket client
- Node.js crypto module for AES-256-GCM
- MCP SDK (`@anthropic-ai/mcp` or stdio-based protocol)

## Limitations

- **Minecraft server required:** The plugin only runs on Paper/Spigot servers. Bedrock, Fabric, and vanilla are not supported.
- **Skript-only file editing:** The WebDAV bridge serves `.sk` files from `plugins/Skript/scripts/`. It does not handle Java plugin source code — only Skript files deployed on the server.
- **No streaming console:** Console output is polled (buffered), not streamed in real-time via SSE or WebSocket push.
- **Single-user:** The bridge assumes one Claude Code session at a time. Concurrent connections are not explicitly handled.
- **Eval security:** The `eval` action executes arbitrary code on the server JVM. It is gated by the shared secret but has no sandboxing within the server.
- **Network exposure:** Port 25580 must be reachable from the machine running Claude Code. If the server is remote, SSH tunneling or VPN is recommended over opening the port publicly.

## Why This Matters

For builders of Claude-driven products, McClaude demonstrates a pattern with broad applicability:

- **Agent factories:** The MCP bridge pattern (Claude <-> encrypted WS <-> live system) generalizes beyond Minecraft. Any application with a console, file system, and eval capability could expose the same interface — game servers, CMS platforms, IoT controllers.
- **Live-loop development:** The ability to edit code and see results immediately (without rebuild/deploy) is the same feedback loop that makes AI-assisted development practical. This pattern could apply to web apps (hot reload via MCP), data pipelines (live SQL editing), or marketing automation (edit campaign logic live).
- **E2E encryption as default:** McClaude's encryption approach is a good reference for anyone building MCP servers that handle sensitive data — credentials, API keys, or proprietary business logic flowing through the bridge.
