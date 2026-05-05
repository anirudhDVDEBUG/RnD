# MCP Servers Setup

**TL;DR:** The [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) repo (+54 stars/day) is the canonical collection of 12+ official MCP server implementations that give Claude filesystem, GitHub, Slack, database, and browser-automation capabilities via simple JSON config. This demo generates ready-to-paste config snippets and walks through the exact JSON-RPC protocol that MCP uses under the hood.

## Headline result

```
bash run.sh
```

Outputs a full catalog of all official servers, generates `claude_desktop_config.json` and `.mcp.json` snippets you can copy-paste immediately, and simulates a live MCP session showing the JSON-RPC handshake + tool calls between Claude and a server.

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — exact install steps, config snippets, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, protocol details, limitations, product implications
