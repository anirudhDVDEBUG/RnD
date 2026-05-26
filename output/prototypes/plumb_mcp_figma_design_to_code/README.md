# Plumb MCP — Local Figma MCP Server for Design-to-Code

**TL;DR:** Plumb MCP is a local Figma MCP server that extracts design structure, tokens, and component details from your Figma files with zero REST API rate limits, zero metered tool-call quotas, and a built-in verification loop. Works on every Figma plan including Free — drop-in replacement for Figma's Dev Mode MCP and Framelink.

## Headline Result

```
Score: 100%  (13/13 checks passed)
Verdict: PASS — all design tokens present

What happened:
  1. Retrieved Figma file structure (2 components)
  2. Extracted 8 color tokens, 5 typography scales, 6 spacing values
  3. Read HeroSection layout details (auto-layout, children, text styles)
  4. Generated React component + CSS custom properties from design data
  5. Ran verification loop — 100% token coverage
```

Run `bash run.sh` to see this end-to-end (no API keys, no Figma account needed).

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the real plumb-mcp, configure it in Claude Code / Cursor, first 60 seconds walkthrough.
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and why this matters for agent-driven product teams.
