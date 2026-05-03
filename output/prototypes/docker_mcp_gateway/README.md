# Docker MCP Gateway

**One container, one endpoint, all your MCP servers — authenticated and ready.**

Deploy a self-hosted MCP gateway that bundles MCPHub + Caddy into a single Docker container, exposing filesystem, fetch, GitHub, Brave Search, Git, PostgreSQL, and memory MCP servers behind a single HTTP endpoint with Bearer token auth. Multi-arch (amd64/arm64), configured entirely via env vars.

## Headline Result

```
$ curl -s -H "Authorization: Bearer $TOKEN" http://localhost:3000/mcp | jq .tools[:3]
[
  { "name": "read_file",    "server": "filesystem" },
  { "name": "search_web",   "server": "brave-search" },
  { "name": "create_issue", "server": "github" }
]
```

One endpoint. Seven MCP servers. Zero YAML wrangling.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, connect in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **[run.sh](run.sh)** — Local demo (simulates the gateway without Docker)

## Source

- Repository: https://github.com/hwdsl2/docker-mcp-gateway
- Docker Hub: `hwdsl2/mcp-gateway`
