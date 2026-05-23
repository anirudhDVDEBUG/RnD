# OpenMCP Server Manager

**Manage all your MCP server configurations from one CLI.** Add, validate, update, remove, and export MCP server configs in the format Claude Code expects -- no desktop app required. Zero dependencies, pure Node.js.

## Headline result

```
$ bash run.sh
  MCP Servers (5):
  [stdio] filesystem    cmd: npx -y @modelcontextprotocol/server-filesystem /home/user/documents
  [stdio] github        cmd: npx -y @modelcontextprotocol/server-github
  [stdio] postgres      cmd: npx -y @modelcontextprotocol/server-postgres
  [stdio] brave-search  cmd: npx -y @modelcontextprotocol/server-brave-search
  [sse]   custom-sse    cmd: node ./my-server/index.js

  -> Exports ready-to-paste JSON for ~/.claude.json
```

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install, configure, first 60 seconds.
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, limitations, why it matters.
- **Source**: [hacimertgokhan/openmcp](https://github.com/hacimertgokhan/openmcp)
