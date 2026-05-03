"""
ZeroClaw MCP Router — Demo Implementation

Simulates a multi-MCP router that dispatches tool calls to different backends
based on a routing table. In production, each backend would be a real MCP server
communicating over stdio/SSE/HTTP.
"""

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Backend:
    name: str
    tools: list[str]
    handler: Any = None


@dataclass
class Router:
    backends: dict[str, Backend] = field(default_factory=dict)
    route_table: dict[str, str] = field(default_factory=dict)

    def register(self, backend: Backend) -> None:
        self.backends[backend.name] = backend
        for tool in backend.tools:
            self.route_table[tool] = backend.name

    def dispatch(self, tool_name: str, args: dict) -> dict:
        backend_name = self.route_table.get(tool_name)
        if not backend_name:
            return {"error": f"No backend registered for tool: {tool_name}"}
        backend = self.backends[backend_name]
        if backend.handler:
            return backend.handler(tool_name, args)
        return {"error": f"Backend '{backend_name}' has no handler"}

    def list_backends(self) -> list[dict]:
        return [
            {"name": b.name, "tools": b.tools}
            for b in self.backends.values()
        ]

    def list_tools(self) -> list[str]:
        return list(self.route_table.keys())


# --- Mock backend handlers ---

def filesystem_handler(tool: str, args: dict) -> dict:
    responses = {
        "read_file": {"content": "Hello from the filesystem backend!", "path": args.get("path", "")},
        "write_file": {"success": True, "bytes_written": 128},
        "list_dir": {"entries": ["file1.txt", "file2.py", "subdir/"]},
    }
    return responses.get(tool, {"error": "unknown tool"})


def database_handler(tool: str, args: dict) -> dict:
    responses = {
        "query": {"rows": [{"count": 42}], "sql": args.get("sql", "")},
        "insert": {"success": True, "id": 7},
        "schema": {"tables": ["users", "orders", "products"], "total": 3},
    }
    return responses.get(tool, {"error": "unknown tool"})


def websearch_handler(tool: str, args: dict) -> dict:
    responses = {
        "search": {
            "results": [
                {"title": "Model Context Protocol", "url": "https://modelcontextprotocol.io"},
                {"title": "MCP Specification", "url": "https://spec.modelcontextprotocol.io"},
            ],
            "query": args.get("query", ""),
        },
        "fetch_url": {"status": 200, "body_preview": "<html>...content...</html>"},
        "summarize": {"summary": "A protocol for connecting AI models to external tools and data sources."},
    }
    return responses.get(tool, {"error": "unknown tool"})


def create_demo_router() -> Router:
    router = Router()
    router.register(Backend(
        name="filesystem",
        tools=["read_file", "write_file", "list_dir"],
        handler=filesystem_handler,
    ))
    router.register(Backend(
        name="database",
        tools=["query", "insert", "schema"],
        handler=database_handler,
    ))
    router.register(Backend(
        name="websearch",
        tools=["search", "fetch_url", "summarize"],
        handler=websearch_handler,
    ))
    return router


def run_demo():
    print("\n=== ZeroClaw MCP Router Demo ===\n")

    router = create_demo_router()

    # Show registration
    print("[Router] Registering backends...")
    for b in router.list_backends():
        tools_str = ", ".join(b["tools"])
        print(f"  + {b['name']:<12} (tools: {tools_str})")

    print()

    # Demo dispatches
    test_calls = [
        ("read_file", {"path": "./demo.txt"}),
        ("search", {"query": "MCP protocol spec"}),
        ("query", {"sql": "SELECT count(*) FROM users"}),
        ("insert", {"table": "orders", "data": {"item": "widget", "qty": 5}}),
        ("list_dir", {"path": "/project"}),
        ("summarize", {"url": "https://example.com/article"}),
    ]

    errors = 0
    for tool_name, args in test_calls:
        backend_name = router.route_table.get(tool_name, "???")
        print(f"[Router] Dispatching: {tool_name} {json.dumps(args)}")
        print(f"  -> routed to: {backend_name}")
        result = router.dispatch(tool_name, args)
        if "error" in result:
            print(f"  <- ERROR: {result['error']}")
            errors += 1
        else:
            print(f"  <- result: {json.dumps(result, indent=None)}")
        print()

    # Test unknown tool
    print("[Router] Dispatching: unknown_tool {}")
    result = router.dispatch("unknown_tool", {})
    print(f"  <- {result}")
    if "error" in result:
        errors += 1
    print()

    # Summary
    total = len(test_calls) + 1
    print(f"[Summary] {total} tool calls dispatched across {len(router.backends)} backends, "
          f"{errors} routing errors (1 intentional).")
    print(f"[Summary] Total registered tools: {len(router.list_tools())}")
    print(f"[Summary] Tools: {', '.join(router.list_tools())}")
    print()


if __name__ == "__main__":
    run_demo()
