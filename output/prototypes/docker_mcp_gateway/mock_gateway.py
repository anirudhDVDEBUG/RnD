"""
Mock MCP Gateway Server

Simulates the behavior of hwdsl2/docker-mcp-gateway without Docker.
Demonstrates the architecture: Caddy (auth) -> MCPHub (routing) -> MCP servers.
"""

import http.server
import json
import os
import sys
import datetime

BEARER_TOKEN = os.environ.get("MCP_BEARER_TOKEN", "demo-token-12345")
PORT = int(os.environ.get("MCP_GATEWAY_PORT", "3000"))

# Simulated MCP servers and their tools
MCP_SERVERS = {
    "filesystem": {
        "description": "Read/write files in mounted volumes",
        "tools": [
            {"name": "read_file", "description": "Read contents of a file", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
            {"name": "write_file", "description": "Write contents to a file", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
            {"name": "list_directory", "description": "List files in a directory", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
        ],
    },
    "fetch": {
        "description": "Make HTTP requests to external URLs",
        "tools": [
            {"name": "fetch_url", "description": "Fetch content from a URL", "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "method": {"type": "string", "default": "GET"}}, "required": ["url"]}},
        ],
    },
    "github": {
        "description": "Interact with GitHub repos, issues, PRs",
        "tools": [
            {"name": "create_issue", "description": "Create a GitHub issue", "inputSchema": {"type": "object", "properties": {"repo": {"type": "string"}, "title": {"type": "string"}}, "required": ["repo", "title"]}},
            {"name": "list_repos", "description": "List repositories for a user/org", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}}, "required": ["owner"]}},
            {"name": "get_pull_request", "description": "Get pull request details", "inputSchema": {"type": "object", "properties": {"repo": {"type": "string"}, "number": {"type": "integer"}}, "required": ["repo", "number"]}},
        ],
    },
    "brave-search": {
        "description": "Web search via Brave Search API",
        "tools": [
            {"name": "search_web", "description": "Search the web", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "count": {"type": "integer", "default": 10}}, "required": ["query"]}},
        ],
    },
    "git": {
        "description": "Git operations on repositories",
        "tools": [
            {"name": "git_log", "description": "Show git commit log", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}, "max_count": {"type": "integer", "default": 10}}, "required": ["path"]}},
            {"name": "git_diff", "description": "Show git diff", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
        ],
    },
    "postgresql": {
        "description": "Query PostgreSQL databases",
        "tools": [
            {"name": "query", "description": "Execute a SQL query", "inputSchema": {"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}},
        ],
    },
    "memory": {
        "description": "Persistent knowledge graph / memory store",
        "tools": [
            {"name": "store_memory", "description": "Store a fact in the knowledge graph", "inputSchema": {"type": "object", "properties": {"subject": {"type": "string"}, "predicate": {"type": "string"}, "object": {"type": "string"}}, "required": ["subject", "predicate", "object"]}},
            {"name": "recall_memory", "description": "Recall facts about a subject", "inputSchema": {"type": "object", "properties": {"subject": {"type": "string"}}, "required": ["subject"]}},
        ],
    },
}

# In-memory store for the memory server demo
memory_store = {}


def get_all_tools():
    """Aggregate tools from all servers with server attribution."""
    tools = []
    for server_name, server in MCP_SERVERS.items():
        for tool in server["tools"]:
            tools.append({**tool, "server": server_name})
    return tools


def handle_tool_call(tool_name, arguments):
    """Simulate executing a tool call and return mock results."""
    if tool_name == "read_file":
        path = arguments.get("path", "/data/example.txt")
        return {"content": f"[Mock] Contents of {path}:\nHello from the MCP gateway filesystem server!\nThis file is served via the unified /mcp endpoint."}

    if tool_name == "list_directory":
        return {"entries": [{"name": "example.txt", "type": "file", "size": 128}, {"name": "reports", "type": "directory"}, {"name": "config.json", "type": "file", "size": 256}]}

    if tool_name == "search_web":
        query = arguments.get("query", "MCP protocol")
        return {"results": [
            {"title": "Model Context Protocol", "url": "https://modelcontextprotocol.io", "snippet": "The Model Context Protocol (MCP) is an open standard for connecting AI assistants to external tools and data sources."},
            {"title": "MCP Specification", "url": "https://spec.modelcontextprotocol.io", "snippet": "Full specification for the Model Context Protocol, including JSON-RPC transport and tool definitions."},
            {"title": f"Search results for: {query}", "url": "https://example.com", "snippet": "Additional results would appear here from Brave Search API."},
        ]}

    if tool_name == "list_repos":
        owner = arguments.get("owner", "anthropic")
        return {"repositories": [
            {"name": "claude-code", "full_name": f"{owner}/claude-code", "stars": 25000, "language": "TypeScript"},
            {"name": "anthropic-sdk-python", "full_name": f"{owner}/anthropic-sdk-python", "stars": 8000, "language": "Python"},
        ]}

    if tool_name == "store_memory":
        subj = arguments.get("subject", "unknown")
        memory_store.setdefault(subj, []).append({"predicate": arguments.get("predicate"), "object": arguments.get("object")})
        return {"stored": True, "subject": subj, "total_facts": len(memory_store[subj])}

    if tool_name == "recall_memory":
        subj = arguments.get("subject", "unknown")
        facts = memory_store.get(subj, [])
        return {"subject": subj, "facts": facts, "count": len(facts)}

    if tool_name == "git_log":
        return {"commits": [
            {"hash": "abc1234", "message": "feat: add MCP gateway support", "author": "dev", "date": "2026-05-01"},
            {"hash": "def5678", "message": "fix: bearer token validation", "author": "dev", "date": "2026-04-30"},
        ]}

    return {"result": f"[Mock] Tool '{tool_name}' executed successfully", "arguments": arguments}


class MCPGatewayHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler simulating the Caddy + MCPHub gateway."""

    def log_message(self, format, *args):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"  [{timestamp}] {args[0]}")

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _check_auth(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or auth[7:] != BEARER_TOKEN:
            self._send_json({"error": "Unauthorized", "message": "Invalid or missing Bearer token"}, 401)
            return False
        return True

    def do_GET(self):
        if self.path == "/health":
            self._send_json({"status": "ok", "servers": len(MCP_SERVERS), "uptime": "mock"})
            return

        if self.path == "/mcp":
            if not self._check_auth():
                return
            self._send_json({
                "servers": {name: {"description": s["description"], "tool_count": len(s["tools"])} for name, s in MCP_SERVERS.items()},
                "tools": get_all_tools(),
                "total_tools": len(get_all_tools()),
            })
            return

        self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path == "/mcp":
            if not self._check_auth():
                return

            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {}

            method = body.get("method", "")
            if method == "tools/list":
                self._send_json({"jsonrpc": "2.0", "id": body.get("id", 1), "result": {"tools": get_all_tools()}})
            elif method == "tools/call":
                params = body.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                result = handle_tool_call(tool_name, arguments)
                self._send_json({"jsonrpc": "2.0", "id": body.get("id", 1), "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}})
            else:
                self._send_json({"jsonrpc": "2.0", "id": body.get("id", 1), "result": {"tools": get_all_tools()}})
            return

        self._send_json({"error": "Not found"}, 404)


def main():
    server = http.server.HTTPServer(("127.0.0.1", PORT), MCPGatewayHandler)
    print(f"  Mock MCP Gateway running on http://127.0.0.1:{PORT}")
    print(f"  Bearer token: {BEARER_TOKEN}")
    print(f"  Servers loaded: {len(MCP_SERVERS)} ({', '.join(MCP_SERVERS.keys())})")
    print(f"  Total tools: {len(get_all_tools())}")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
