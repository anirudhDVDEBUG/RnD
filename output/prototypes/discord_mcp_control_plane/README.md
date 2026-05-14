# Discord MCP Control Plane

**A multi-server Discord control plane that exposes messaging, channel management, and server administration as MCP tools, resources, and prompts — letting Claude (or any MCP client) operate Discord servers programmatically.**

## Headline result

```
Tool: send_message(guild_id='1001', channel_id='3001', ...)
{
  "ok": true,
  "message": {
    "id": "m101",
    "author": "claude-bot",
    "content": "Automated update: build #47 passed all checks."
  }
}
```

One MCP call → message delivered across any server the bot has joined. Seven tools, three resources, three prompt templates — all exposed over the standard Model Context Protocol.

## Quick start

```bash
bash run.sh        # full demo with mock data, no API keys needed
```

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — install steps, MCP client config, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, data flow, limitations, and why this matters
