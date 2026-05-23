# Technical Details

## What it does

OpenMCP is a TypeScript-based Electron desktop application and CLI for managing MCP (Model Context Protocol) server configurations. It provides a visual GUI and command-line interface to register, configure, start, stop, and monitor MCP servers from a single dashboard. This demo prototype extracts the core config-management logic into a zero-dependency Node.js CLI that reads/writes the same JSON format.

The manager maintains a `mcp-servers.json` file containing all server definitions (command, args, env vars, transport type). It supports CRUD operations, validation, and exports configs directly in the `~/.claude.json` `mcpServers` format that Claude Code consumes.

## Architecture

```
src/
  manager.js   - Core MCPServerManager class (load/save/CRUD/validate/export)
  cli.js       - CLI argument parser and command dispatcher
  demo.js      - End-to-end walkthrough script

mcp-servers.json  - Generated config file (JSON, matches Claude Code schema)
```

**Data flow:**
1. CLI parses command + flags -> calls MCPServerManager methods
2. MCPServerManager reads/writes `mcp-servers.json` on disk
3. `exportForClaude()` transforms configs into Claude Code's expected format
4. User pastes exported JSON into `~/.claude.json`

**Dependencies:** None (Node.js standard library only). The full OpenMCP project uses Electron, React, and TypeScript.

**Key files in upstream OpenMCP:**
- Electron main process for desktop GUI
- React frontend for server management UI
- TypeScript MCP client for server communication
- Configuration storage layer

## Limitations

- **This demo is config management only** -- it does not start/stop actual MCP server processes (the full OpenMCP desktop app does).
- **No GUI** -- the desktop UI requires cloning and building the full OpenMCP repo.
- **No MCP protocol communication** -- this manages configurations, not the MCP wire protocol itself.
- **Single config file** -- no multi-user or team sync; each user manages their own `mcp-servers.json`.
- **No server health checks** -- validation checks config shape only, not whether the server binary exists or responds.

## Why it matters for Claude-driven products

- **Agent factories:** Standardize MCP server setup across teams building Claude-powered agents. One config file, version-controlled, shared across dev environments.
- **Lead-gen / marketing tools:** MCP servers like Brave Search, GitHub, and database connectors are the plumbing behind research agents. Managing them centrally reduces setup friction.
- **Ad creatives / content pipelines:** Agents that pull from multiple data sources (CMS, analytics, image APIs) each need an MCP server. A manager keeps configs organized as the server count grows.
- **Voice AI / multi-modal agents:** Complex agent architectures connect to 5-10+ MCP servers. Without a manager, config drift and misconfiguration become the main failure mode.
- **Rapid prototyping:** `export` command generates paste-ready JSON, cutting setup time from minutes to seconds when wiring new MCP servers into Claude Code.
