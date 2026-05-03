---
name: docker_mcp_gateway
description: |
  Deploy a self-hosted MCP (Model Context Protocol) gateway using Docker.
  Powered by MCPHub + Caddy with Bearer token auth, exposing multiple MCP servers
  (filesystem, fetch, GitHub, Brave Search, Git, PostgreSQL, memory, etc.) via a
  single HTTP endpoint. Multi-arch (amd64/arm64), simple env-file config.
  TRIGGER: user wants to set up an MCP gateway, self-host MCP servers behind an
  API gateway, run MCPHub in Docker, or expose multiple MCP tools over HTTP with auth.
---

# Docker MCP Gateway

Deploy a self-hosted MCP (Model Context Protocol) gateway with Bearer token authentication using Docker. This bundles MCPHub + Caddy into a single container, giving you a unified HTTP endpoint for multiple MCP servers.

## When to use

- "Set up a self-hosted MCP gateway with Docker"
- "Run multiple MCP servers behind a single authenticated endpoint"
- "Deploy MCPHub with Caddy reverse proxy and Bearer token auth"
- "I need a Docker-based MCP hub for filesystem, GitHub, Brave Search, and more"
- "How do I expose MCP tools over HTTP with token authentication?"

## How to use

### 1. Create the project directory and env file

```bash
mkdir -p mcp-gateway && cd mcp-gateway
```

Create a `.env` file with your configuration:

```bash
# Required: Bearer token for API authentication
MCP_BEARER_TOKEN=your-secure-random-token-here

# Optional: GitHub token for the GitHub MCP server
GITHUB_TOKEN=ghp_your_github_token

# Optional: Brave Search API key
BRAVE_API_KEY=your_brave_api_key

# Optional: PostgreSQL connection string
POSTGRES_CONNECTION_STRING=postgresql://user:pass@host:5432/db
```

### 2. Create docker-compose.yml

```yaml
version: "3.8"
services:
  mcp-gateway:
    image: hwdsl2/mcp-gateway
    container_name: mcp-gateway
    restart: unless-stopped
    ports:
      - "3000:3000"
    env_file:
      - .env
    volumes:
      # Mount directories you want the filesystem MCP server to access
      - ./data:/data
```

### 3. Start the gateway

```bash
docker compose up -d
```

### 4. Connect your MCP client

Configure your MCP client (e.g., Claude Desktop, Cursor, VS Code) to use the gateway's HTTP endpoint with Bearer token authentication:

```json
{
  "mcpServers": {
    "mcp-gateway": {
      "url": "http://localhost:3000/mcp",
      "headers": {
        "Authorization": "Bearer your-secure-random-token-here"
      }
    }
  }
}
```

For remote access, replace `localhost` with your server's IP or domain.

### 5. Verify the gateway is running

```bash
curl -H "Authorization: Bearer your-secure-random-token-here" http://localhost:3000/mcp
```

### Available MCP Servers

The gateway bundles multiple MCP servers accessible through the single endpoint:

| Server | Description |
|--------|-------------|
| **Filesystem** | Read/write files in mounted volumes |
| **Fetch** | Make HTTP requests to external URLs |
| **GitHub** | Interact with GitHub repos, issues, PRs |
| **Brave Search** | Web search via Brave Search API |
| **Git** | Git operations on repositories |
| **PostgreSQL** | Query PostgreSQL databases |
| **Memory** | Persistent knowledge graph / memory store |

### Architecture

- **Caddy** handles TLS termination, reverse proxy, and Bearer token auth
- **MCPHub** aggregates multiple MCP servers into one endpoint
- Multi-arch support: `amd64` and `arm64`
- Simple env-file configuration — no complex YAML or JSON config needed

### Tips

- Generate a strong random token: `openssl rand -hex 32`
- For production, put behind a proper reverse proxy with TLS
- Use Docker volumes to persist memory server data
- Check container logs for troubleshooting: `docker compose logs -f mcp-gateway`

## References

- **Source repository**: https://github.com/hwdsl2/docker-mcp-gateway
- **Docker Hub**: `hwdsl2/mcp-gateway`
- **MCPHub**: The underlying multi-server MCP hub
- **Model Context Protocol**: https://modelcontextprotocol.io
