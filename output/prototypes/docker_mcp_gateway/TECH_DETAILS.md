# Technical Details: Docker MCP Gateway

## What It Does

Docker MCP Gateway packages multiple MCP (Model Context Protocol) servers into a single Docker container, fronted by Caddy as a reverse proxy with Bearer token authentication. Instead of running 7 separate MCP server processes and configuring each one individually in your client, you get one HTTP endpoint (`/mcp`) that multiplexes requests to the correct backend server. MCPHub handles server aggregation and routing; Caddy handles TLS, auth, and reverse proxying.

The image ships pre-configured with filesystem, fetch, GitHub, Brave Search, Git, PostgreSQL, and memory servers. Configuration is entirely through environment variables — no JSON/YAML config files to manage. Servers that lack required credentials (e.g., GitHub without `GITHUB_TOKEN`) are gracefully disabled.

## Architecture

```
Client (Claude/Cursor/etc.)
    │
    │  HTTP + Bearer token
    ▼
┌──────────┐
│  Caddy   │  ← TLS termination, auth validation, reverse proxy
└────┬─────┘
     │
     ▼
┌──────────┐
│  MCPHub  │  ← MCP server aggregator / router
└────┬─────┘
     │
     ├── filesystem-server  (reads/writes mounted volumes)
     ├── fetch-server       (HTTP requests to external URLs)
     ├── github-server      (GitHub API via token)
     ├── brave-search       (Brave Search API)
     ├── git-server         (git operations on repos)
     ├── postgres-server    (SQL queries)
     └── memory-server      (persistent knowledge graph)
```

### Key Components

| Component | Role |
|-----------|------|
| **Caddy** (Caddyfile) | Reverse proxy on port 3000, validates `Authorization: Bearer <token>` header, rejects unauthorized requests with 401 |
| **MCPHub** (Node.js) | Discovers and aggregates child MCP servers, exposes unified tool/resource listing, routes tool calls to the correct server |
| **MCP servers** (stdio) | Each server runs as a child process communicating via stdio with MCPHub; they implement the MCP spec for their domain |

### Data Flow

1. Client sends HTTP POST to `http://host:3000/mcp` with Bearer token
2. Caddy validates token against `MCP_BEARER_TOKEN` env var
3. Caddy proxies request to MCPHub (internal port)
4. MCPHub parses the MCP JSON-RPC request, identifies the target server
5. MCPHub forwards to the appropriate child server via stdio
6. Response flows back: server → MCPHub → Caddy → client

### Dependencies

- **Runtime**: Node.js (MCPHub), Caddy (reverse proxy), individual MCP server binaries
- **Build**: Multi-stage Dockerfile, multi-arch buildx (amd64 + arm64)
- **Config**: Environment variables only (`.env` file or Docker env)

## Limitations

- **No SSE/streaming**: The gateway uses HTTP request-response, not Server-Sent Events. Long-running tool calls block until complete.
- **Single-tenant auth**: One Bearer token for all clients. No per-user or per-role access control.
- **No custom server plugins**: You cannot add your own MCP servers without rebuilding the Docker image.
- **Filesystem scope**: The filesystem server can only access paths mounted as Docker volumes.
- **No built-in TLS**: Caddy handles TLS but requires a domain name for automatic HTTPS. For localhost use, traffic is unencrypted (HTTP).
- **Memory server persistence**: The memory/knowledge-graph server stores data inside the container by default. Without a volume mount, data is lost on container restart.

## Why It Matters for Claude-Driven Products

**Agent factories**: A single gateway endpoint dramatically simplifies agent configuration. Instead of wiring up 7 MCP servers per agent instance, point every agent at one URL. Spin up gateway per tenant or share one across a fleet.

**Lead-gen / marketing automation**: Agents that need to search the web (Brave), interact with GitHub (issue triage, PR monitoring), read/write files (report generation), and query databases (PostgreSQL) can do all of this through one authenticated endpoint — no per-tool credential distribution.

**Voice AI / ad creatives**: Any Claude-powered pipeline that chains multiple tool calls benefits from reduced latency variance (one HTTP hop vs. multiple process spawns) and centralized auth.

**Self-hosted control**: For regulated industries or privacy-sensitive workflows, running the gateway on your own infrastructure means MCP tool calls never leave your network. The Bearer token auth, while simple, provides a clear access boundary.
