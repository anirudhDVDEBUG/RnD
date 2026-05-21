"""Mock MCP (Model Context Protocol) client.

Demonstrates how Zephyr discovers and invokes tools exposed by MCP servers.
Uses built-in mock servers so no external MCP server is needed.
"""


# -- Mock MCP tool definitions -------------------------------------------
MOCK_TOOLS = {
    "filesystem": {
        "description": "Read/write local files",
        "operations": ["read_file", "write_file", "list_directory"],
    },
    "web_search": {
        "description": "Search the web (mock)",
        "operations": ["search"],
    },
    "database": {
        "description": "Query a local SQLite database",
        "operations": ["query", "execute"],
    },
}


class MCPClient:
    """Simulated MCP client that discovers and invokes tools."""

    def __init__(self):
        self.connected_servers: dict[str, dict] = {}

    def connect(self, server_name: str) -> dict:
        if server_name in MOCK_TOOLS:
            self.connected_servers[server_name] = MOCK_TOOLS[server_name]
            return {
                "status": "connected",
                "server": server_name,
                "tools": MOCK_TOOLS[server_name]["operations"],
            }
        return {"status": "error", "message": f"Unknown server: {server_name}"}

    def list_tools(self) -> list[dict]:
        result = []
        for name, info in self.connected_servers.items():
            result.append({"server": name, **info})
        return result

    def invoke(self, server_name: str, operation: str, params: dict | None = None) -> dict:
        if server_name not in self.connected_servers:
            return {"error": f"Not connected to {server_name}"}
        srv = self.connected_servers[server_name]
        if operation not in srv["operations"]:
            return {"error": f"{operation} not available on {server_name}"}

        # Mock execution
        return {
            "server": server_name,
            "operation": operation,
            "params": params or {},
            "result": f"[mock] {operation} executed successfully",
        }
