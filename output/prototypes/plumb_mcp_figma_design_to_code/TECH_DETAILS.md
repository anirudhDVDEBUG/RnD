# Technical Details — Plumb MCP

## What It Does

Plumb MCP is a local MCP (Model Context Protocol) server that gives AI coding agents structured access to Figma design data without hitting Figma's REST API. Instead of making authenticated HTTP requests to `api.figma.com` (which has strict rate limits and requires a paid plan for Dev Mode), plumb-mcp uses a companion Figma plugin that reads the design document locally inside Figma Desktop and streams the data over a local WebSocket to the MCP server. The MCP server then exposes this data as callable tools to any MCP-compatible agent (Claude Code, Cursor, Windsurf).

The key differentiator is the **verification loop**: after the agent generates code from design data, it can call `verify_implementation` to score how well the generated output matches the original design tokens — creating a closed feedback loop that doesn't exist in Figma's official Dev Mode MCP or Framelink.

## Architecture

```
Figma Desktop                    Local Machine
+-----------------+              +------------------+
| Figma Plugin    |  WebSocket   | plumb-mcp server |   MCP/stdio
| (reads document |  -------->   | (Node.js)        |  <--------->  AI Agent
|  layer tree)    |  localhost    | Exposes tools:   |              (Claude Code,
+-----------------+              |  - get_file_*    |               Cursor, etc.)
                                 |  - extract_*     |
                                 |  - verify_*      |
                                 +------------------+
```

### Key Files (in the real repo)

| Path | Purpose |
|---|---|
| `src/index.ts` | MCP server entry point, registers tools via `@modelcontextprotocol/sdk` |
| `src/tools/` | Tool implementations (file structure, tokens, verification) |
| `figma-plugin/code.ts` | Figma plugin — walks the document tree, serializes to JSON |
| `figma-plugin/manifest.json` | Plugin manifest for Figma Desktop import |
| `figma-plugin/ui.html` | Plugin UI panel |

### Data Flow

1. **Plugin → Server**: Figma plugin traverses the document node tree (`figma.root.children`), serializes component properties (fills, strokes, text styles, auto-layout, constraints), and sends the payload over WebSocket to `localhost`.
2. **Server → Agent**: The MCP server holds the latest document snapshot in memory. When the agent calls a tool (e.g., `get_component_details`), the server queries its in-memory model and returns structured JSON.
3. **Verification**: `verify_implementation` accepts generated HTML/CSS/JSX as a string, extracts token values from the design snapshot, and checks which tokens appear in the generated code. Returns a score and per-token pass/fail list.

### Dependencies

- **Runtime**: Node.js 18+
- **Key packages**: `@modelcontextprotocol/sdk` (MCP protocol), `ws` (WebSocket server)
- **Figma plugin**: Uses Figma's Plugin API (no npm dependencies — bundled by Figma)

## Limitations

- **Requires Figma Desktop**: The plugin communicates over localhost WebSocket, so it cannot work with Figma in a browser tab (browser extensions cannot open local sockets).
- **No image export**: Plumb MCP extracts structure and tokens but does not export raster images or SVG paths from Figma. You still need Figma's export API or manual export for icons/illustrations.
- **Single-file at a time**: The plugin serves one open Figma file. Switching files requires re-running the plugin.
- **Verification is token-level, not visual**: The verification loop checks whether design token values (colors, font sizes) appear in generated code. It does not do pixel-level visual comparison (no screenshot diffing).
- **No design system sync**: It reads the current file state; it doesn't sync with Figma's published component library or team styles across files.

## Why This Matters for Claude-Driven Products

| Use Case | How plumb-mcp helps |
|---|---|
| **Agent factories** | Agents that scaffold UI from a Figma mockup can use plumb-mcp as a tool — no API key provisioning, no rate-limit handling logic. Simplifies the tool-calling chain. |
| **Lead-gen / marketing sites** | Marketing teams iterate on Figma mockups daily. With plumb-mcp + Claude Code, a designer changes the Figma file and the agent regenerates the landing page component in seconds — including a verification score. |
| **Ad creatives** | Rapid variant generation: extract tokens from one Figma ad design, generate 10 layout variations in code, verify each against the source tokens automatically. |
| **Design system enforcement** | The verification loop catches token drift — when generated code diverges from the design system, it flags missing/wrong values before the code ships. |
| **Free-tier accessibility** | Unlike Figma's official MCP (requires Dev Mode, a paid feature), plumb-mcp works on Figma Free. Teams evaluating design-to-code workflows can prototype without committing to a paid plan. |
