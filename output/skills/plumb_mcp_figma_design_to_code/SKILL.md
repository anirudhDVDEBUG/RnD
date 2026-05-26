---
name: plumb_mcp_figma_design_to_code
description: |
  Set up and use plumb-mcp, a local Figma MCP server for design-to-code workflows.
  TRIGGER: figma mcp, figma design to code, plumb-mcp, figma plugin mcp, figma free tier mcp, design tokens extraction, local figma server, figma without rate limits
---

# Plumb MCP — Local Figma MCP Server

Plumb MCP is a local Figma MCP server that provides design-to-code capabilities with no REST API rate limits, no metered tool-call quotas, and a built-in verification loop. It is a drop-in alternative to Figma's Dev Mode MCP and Framelink, and works on every Figma plan including Free.

## When to use

- "Set up Figma MCP for my project"
- "Convert this Figma design to code without rate limits"
- "I need a free alternative to Figma Dev Mode MCP"
- "Extract design tokens from Figma locally"
- "Configure plumb-mcp for Claude Code / Cursor / Windsurf"

## How to use

### 1. Install plumb-mcp

```bash
# Clone the repository
git clone https://github.com/tathagat22/plumb-mcp.git
cd plumb-mcp

# Install dependencies
npm install

# Build the project
npm run build
```

### 2. Install the Figma Plugin

Plumb MCP uses a companion Figma plugin to read design data locally (bypassing REST API limits):

1. Open Figma Desktop
2. Go to **Plugins → Development → Import plugin from manifest**
3. Select the `manifest.json` from the `figma-plugin/` directory in the cloned repo
4. Run the plugin on your Figma file — it will serve design data to the local MCP server

### 3. Configure MCP in your editor

**Claude Code** — add to your MCP settings (`.mcp.json` or via `claude mcp add`):

```json
{
  "mcpServers": {
    "plumb-mcp": {
      "command": "node",
      "args": ["<path-to-plumb-mcp>/dist/index.js"],
      "env": {}
    }
  }
}
```

**Cursor / Windsurf** — add the same server configuration in your editor's MCP settings panel.

### 4. Use in your workflow

Once configured, the MCP server exposes tools that your AI coding agent can call to:

- **Fetch design structure** — retrieve the full component tree from a Figma file
- **Extract design tokens** — get colors, typography, spacing, and other tokens
- **Verify implementation** — use the built-in verification loop to compare your code output against the original design
- **Read component properties** — access auto-layout, constraints, and variant details

Example prompt to your AI agent:

> "Using the Figma file I have open, generate a React component that matches the design. Extract the design tokens and verify the output."

### Key advantages over alternatives

| Feature | Plumb MCP | Figma Dev Mode MCP | Framelink |
|---|---|---|---|
| Rate limits | None (local) | REST API limits | REST API limits |
| Figma plan required | Free+ | Paid Dev Mode | Paid |
| Tool-call quotas | None | Metered | Metered |
| Verification loop | Built-in | No | No |

## References

- **Repository**: https://github.com/tathagat22/plumb-mcp
- **Language**: TypeScript
- **License**: See repository for details
