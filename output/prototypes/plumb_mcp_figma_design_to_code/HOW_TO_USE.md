# How to Use Plumb MCP

## Install (real plumb-mcp)

```bash
git clone https://github.com/tathagat22/plumb-mcp.git
cd plumb-mcp
npm install
npm run build
```

Requires Node.js 18+.

## Install the Figma Plugin

Plumb MCP reads design data via a companion Figma plugin (local WebSocket, no REST API):

1. Open **Figma Desktop** (not browser — the plugin uses local networking).
2. Go to **Plugins > Development > Import plugin from manifest**.
3. Select `figma-plugin/manifest.json` from the cloned repo.
4. Open your Figma file, run the plugin. It starts a local server that feeds design data to plumb-mcp.

## Configure as MCP Server in Claude Code

Add to `~/.claude.json` (global) or your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "plumb-mcp": {
      "command": "node",
      "args": ["/absolute/path/to/plumb-mcp/dist/index.js"],
      "env": {}
    }
  }
}
```

Or via CLI:

```bash
claude mcp add plumb-mcp node /absolute/path/to/plumb-mcp/dist/index.js
```

For **Cursor / Windsurf**: add the same `command` + `args` in your editor's MCP settings panel.

## As a Claude Skill

Drop the SKILL.md into your skills directory:

```bash
mkdir -p ~/.claude/skills/plumb_mcp_figma_design_to_code
cp SKILL.md ~/.claude/skills/plumb_mcp_figma_design_to_code/SKILL.md
```

**Trigger phrases:** "figma mcp", "figma design to code", "plumb-mcp", "figma free tier mcp", "design tokens extraction", "local figma server", "figma without rate limits"

## First 60 Seconds

**Input** (tell your AI agent):
```
Using the Figma file I have open, generate a React component
that matches the HeroSection design. Extract the design tokens
and verify the output.
```

**What happens:**

1. Agent calls `get_file_structure` → gets component tree
2. Agent calls `extract_design_tokens` → gets colors, typography, spacing
3. Agent calls `get_component_details("HeroSection")` → gets layout, children, text content
4. Agent generates React + CSS code using the extracted data
5. Agent calls `verify_implementation` → verification loop scores token coverage

**Output** (from the demo with mock data):

```
File: SaaS Dashboard - Landing Page (abc123XYZ)
Components found: 2
  - HeroSection  [FRAME]  1440x680
  - FeatureCard  [COMPONENT]  380x280

Colors:
  --background-primary: #0A0D1C
  --accent-primary: #5E5CFF
  ...

Score: 100%  (13/13 checks passed)
Verdict: PASS — all design tokens present
```

The generated code includes CSS custom properties mapped 1:1 from Figma tokens and a React component whose structure mirrors the Figma layer tree.

## Try the Demo (no Figma needed)

```bash
bash run.sh
```

This runs the full pipeline against mock Figma data — no account, API key, or Figma Desktop required.

## Available MCP Tools

| Tool | Description |
|---|---|
| `get_file_structure` | Returns component tree with names, types, sizes |
| `get_component_details` | Deep dive into a specific component's layout, children, styles |
| `extract_design_tokens` | Colors, typography, spacing, radii as structured JSON |
| `verify_implementation` | Scores generated code against design tokens (verification loop) |
