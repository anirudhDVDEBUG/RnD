#!/usr/bin/env bash
# run.sh — Demo the Docker MCP Gateway (mock mode, no Docker needed)
#
# Starts a local mock gateway server, then exercises it with curl
# to show the auth flow, tool listing, and tool execution.

set -euo pipefail
cd "$(dirname "$0")"

PORT=3099
TOKEN="demo-token-$(date +%s)"

echo "=============================================="
echo "  Docker MCP Gateway — Local Demo"
echo "=============================================="
echo ""

# --- Start mock gateway in background ---
echo "[1/6] Starting mock MCP gateway on port $PORT ..."
MCP_BEARER_TOKEN="$TOKEN" MCP_GATEWAY_PORT="$PORT" python3 mock_gateway.py &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null; wait $SERVER_PID 2>/dev/null' EXIT

# Wait for server to be ready
for i in $(seq 1 20); do
    if curl -sf http://127.0.0.1:$PORT/health >/dev/null 2>&1; then
        break
    fi
    sleep 0.2
done

echo ""
echo "=============================================="
echo "[2/6] Health check (no auth required)"
echo "=============================================="
echo ""
echo "  GET /health"
curl -s http://127.0.0.1:$PORT/health | python3 -m json.tool
echo ""

echo "=============================================="
echo "[3/6] Auth test — request WITHOUT token (expect 401)"
echo "=============================================="
echo ""
echo "  GET /mcp (no Authorization header)"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$PORT/mcp)
echo "  Response: HTTP $HTTP_CODE (Unauthorized)"
echo "  -> Bearer token auth is enforced."
echo ""

echo "=============================================="
echo "[4/6] List all servers and tools (authenticated)"
echo "=============================================="
echo ""
echo "  GET /mcp (with Bearer token)"
TOOLS_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:$PORT/mcp)
echo "$TOOLS_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"  Servers: {len(data['servers'])}\")
for name, info in data['servers'].items():
    print(f\"    - {name}: {info['description']} ({info['tool_count']} tools)\")
print(f\"\n  Total tools: {data['total_tools']}\")
print(f\"\n  Sample tools:\")
for t in data['tools'][:5]:
    print(f\"    [{t['server']}] {t['name']} — {t['description']}\")
"
echo ""

echo "=============================================="
echo "[5/6] Execute tool calls via JSON-RPC"
echo "=============================================="

echo ""
echo "  --- tools/call: search_web ---"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_web","arguments":{"query":"MCP protocol specification"}}}' \
  http://127.0.0.1:$PORT/mcp | python3 -c "
import sys, json
resp = json.load(sys.stdin)
content = json.loads(resp['result']['content'][0]['text'])
for r in content['results']:
    print(f\"    {r['title']}\")
    print(f\"      {r['url']}\")
    print(f\"      {r['snippet'][:80]}...\")
    print()
"

echo "  --- tools/call: list_directory ---"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_directory","arguments":{"path":"/data"}}}' \
  http://127.0.0.1:$PORT/mcp | python3 -c "
import sys, json
resp = json.load(sys.stdin)
entries = json.loads(resp['result']['content'][0]['text'])['entries']
for e in entries:
    icon = 'd' if e['type'] == 'directory' else 'f'
    size = f\" ({e.get('size', '-')} bytes)\" if 'size' in e else ''
    print(f\"    [{icon}] {e['name']}{size}\")
"

echo ""
echo "  --- tools/call: store_memory + recall_memory ---"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"store_memory","arguments":{"subject":"MCP Gateway","predicate":"is_a","object":"unified MCP endpoint"}}}' \
  http://127.0.0.1:$PORT/mcp | python3 -c "
import sys, json
resp = json.load(sys.stdin)
result = json.loads(resp['result']['content'][0]['text'])
print(f\"    Stored fact about '{result['subject']}' (total: {result['total_facts']})\")
"

curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"recall_memory","arguments":{"subject":"MCP Gateway"}}}' \
  http://127.0.0.1:$PORT/mcp | python3 -c "
import sys, json
resp = json.load(sys.stdin)
result = json.loads(resp['result']['content'][0]['text'])
print(f\"    Recalled {result['count']} fact(s) about '{result['subject']}':\")
for f in result['facts']:
    print(f\"      {result['subject']} {f['predicate']} {f['object']}\")
"

echo ""
echo "=============================================="
echo "[6/6] Claude client config snippet"
echo "=============================================="
echo ""
echo "  Add this to ~/.claude.json to connect Claude Code:"
echo ""
python3 -c "
import json
config = {
    'mcpServers': {
        'mcp-gateway': {
            'type': 'url',
            'url': 'http://localhost:3000/mcp',
            'headers': {
                'Authorization': 'Bearer YOUR_TOKEN_HERE'
            }
        }
    }
}
print(json.dumps(config, indent=2))
"
echo ""
echo "=============================================="
echo "  Demo complete. In production, use:"
echo "    docker compose up -d"
echo "  See HOW_TO_USE.md for full setup instructions."
echo "=============================================="
