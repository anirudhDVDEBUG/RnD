# How to Use: Docker MCP Gateway

## Prerequisites

- Docker Engine 20.10+ and Docker Compose v2
- (Optional) GitHub token, Brave Search API key, PostgreSQL connection string

## Install & Deploy

### 1. Pull and run with Docker Compose

```bash
mkdir -p mcp-gateway && cd mcp-gateway

# Generate a secure token
export MCP_BEARER_TOKEN=$(openssl rand -hex 32)
echo "Your token: $MCP_BEARER_TOKEN"
```

Create `.env`:

```bash
cat > .env <<EOF
MCP_BEARER_TOKEN=${MCP_BEARER_TOKEN}
# GITHUB_TOKEN=ghp_your_token
# BRAVE_API_KEY=your_key
# POSTGRES_CONNECTION_STRING=postgresql://user:pass@host:5432/db
EOF
```

Create `docker-compose.yml`:

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
      - ./data:/data
```

Start it:

```bash
docker compose up -d
```

### 2. Connect Claude Code (or any MCP client)

Add this to your `~/.claude.json` in the `mcpServers` block:

```json
{
  "mcpServers": {
    "mcp-gateway": {
      "type": "url",
      "url": "http://localhost:3000/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Replace `YOUR_TOKEN_HERE` with the value from your `.env` file.

For **Claude Desktop**, add the same block to `claude_desktop_config.json`.

For **Cursor / VS Code**, add to your MCP settings with the same URL and headers.

### 3. Using as a Claude Skill

Copy the skill file to your skills directory:

```bash
mkdir -p ~/.claude/skills/docker_mcp_gateway
cp SKILL.md ~/.claude/skills/docker_mcp_gateway/SKILL.md
```

**Trigger phrases:**
- "Set up a self-hosted MCP gateway"
- "Run multiple MCP servers behind a single endpoint"
- "Deploy MCPHub with Docker"
- "Expose MCP tools over HTTP with auth"

## First 60 Seconds

```bash
# 1. Start the gateway
docker compose up -d

# 2. Wait for startup (~5 seconds)
sleep 5

# 3. List available tools
curl -s -H "Authorization: Bearer $MCP_BEARER_TOKEN" \
  http://localhost:3000/mcp \
  | python3 -m json.tool

# Expected output: JSON listing all available MCP tools from
# filesystem, fetch, git, memory, and any configured servers

# 4. Use from Claude — just ask:
#    "Read the files in /data"
#    "What's in my GitHub notifications?"
#    "Search the web for MCP protocol"
```

## Verify It Works

```bash
# Health check
curl -s http://localhost:3000/health
# → {"status":"ok"}

# Auth check (should fail without token)
curl -s http://localhost:3000/mcp
# → 401 Unauthorized

# Auth check (should succeed with token)
curl -s -H "Authorization: Bearer $MCP_BEARER_TOKEN" http://localhost:3000/mcp
# → JSON with available tools/servers
```

## Troubleshooting

```bash
# View logs
docker compose logs -f mcp-gateway

# Restart
docker compose restart mcp-gateway

# Check which servers loaded
docker compose exec mcp-gateway cat /app/config.json
```
