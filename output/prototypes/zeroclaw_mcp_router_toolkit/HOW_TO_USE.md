# How to Use ZeroClaw MCP Router

## Install (real project)

```bash
git clone https://github.com/IKingBarou/Zeroclaw-Plugin-Hub.git
cd Zeroclaw-Plugin-Hub
# Follow the repo README for latest install — project is actively evolving
```

## Install (this demo)

```bash
pip install -r requirements.txt   # just stdlib, no external deps
bash run.sh
```

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/zeroclaw_mcp_router_toolkit
cp SKILL.md ~/.claude/skills/zeroclaw_mcp_router_toolkit/SKILL.md
```

**Trigger phrases:**
- "Set up ZeroClaw for multi-MCP routing"
- "Route Claude Code requests across multiple MCP servers"
- "Configure ZeroClaw plugin hub"
- "How do I use ZeroClaw CLI to manage MCP plugins?"

## As an MCP Server (Claude Code integration)

Add to `~/.claude.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "zeroclaw": {
      "command": "npx",
      "args": ["zeroclaw-plugin-hub"],
      "env": {}
    }
  }
}
```

Or if running from a local clone:

```json
{
  "mcpServers": {
    "zeroclaw": {
      "command": "node",
      "args": ["/path/to/Zeroclaw-Plugin-Hub/index.js"],
      "env": {}
    }
  }
}
```

## First 60 Seconds

```bash
$ bash run.sh

=== ZeroClaw MCP Router Demo ===

[Router] Registering backends...
  + filesystem  (tools: read_file, write_file, list_dir)
  + database    (tools: query, insert, schema)
  + websearch   (tools: search, fetch_url, summarize)

[Router] Dispatching tool call: read_file {path: "./demo.txt"}
  -> routed to: filesystem
  <- result: "Hello from the filesystem backend!"

[Router] Dispatching tool call: search {query: "MCP protocol spec"}
  -> routed to: websearch
  <- result: {"title": "Model Context Protocol", "url": "https://..."}

[Router] Dispatching tool call: query {sql: "SELECT count(*) FROM users"}
  -> routed to: database
  <- result: {"count": 42}

[Summary] 3 tool calls dispatched across 3 backends, 0 errors.
```

## CLI Commands (real ZeroClaw)

| Command | Description |
|---------|-------------|
| `zeroclaw list` | Show registered MCP backends |
| `zeroclaw add <name> <endpoint>` | Register a new MCP server |
| `zeroclaw remove <name>` | Unregister an MCP server |
| `zeroclaw test <name>` | Verify connectivity |
| `zeroclaw route <tool> <args>` | Manually dispatch a tool call |
