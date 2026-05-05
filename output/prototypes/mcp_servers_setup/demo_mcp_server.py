#!/usr/bin/env python3
"""Minimal MCP server demo — shows the server-side pattern used by official
modelcontextprotocol/servers implementations.

This is a self-contained example that implements two tools (echo, word_count)
using the same JSON-RPC 2.0 / stdio transport pattern that real MCP servers use.
No external MCP SDK required — it speaks the raw protocol so you can see
exactly what happens on the wire."""

import json
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Tool definitions (what Claude sees when it connects)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "echo",
        "description": "Echoes back the input text. Useful for testing connectivity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to echo back"}
            },
            "required": ["text"],
        },
    },
    {
        "name": "word_count",
        "description": "Counts words, characters, and lines in the given text.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to analyze"}
            },
            "required": ["text"],
        },
    },
]

# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

def handle_echo(arguments: dict) -> list[dict]:
    text = arguments.get("text", "")
    return [{"type": "text", "text": f"Echo: {text}"}]


def handle_word_count(arguments: dict) -> list[dict]:
    text = arguments.get("text", "")
    words = len(text.split())
    chars = len(text)
    lines = text.count("\n") + (1 if text else 0)
    return [{"type": "text", "text": f"Words: {words}, Characters: {chars}, Lines: {lines}"}]


HANDLERS = {
    "echo": handle_echo,
    "word_count": handle_word_count,
}

# ---------------------------------------------------------------------------
# JSON-RPC 2.0 message handling (MCP transport layer)
# ---------------------------------------------------------------------------

SERVER_INFO = {
    "name": "demo-mcp-server",
    "version": "1.0.0",
}

CAPABILITIES = {
    "tools": {},
}


def handle_request(method: str, params: dict, req_id) -> dict:
    """Route an incoming JSON-RPC request to the appropriate handler."""
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": SERVER_INFO,
                "capabilities": CAPABILITIES,
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        handler = HANDLERS.get(tool_name)
        if handler is None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }
        content = handler(arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": content},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


# ---------------------------------------------------------------------------
# Simulated session (no real stdio loop — just demonstrates the protocol)
# ---------------------------------------------------------------------------

def simulate_session():
    """Walk through a realistic MCP session with mock JSON-RPC messages."""
    print("=" * 70)
    print("  Demo MCP Server — protocol walkthrough")
    print("=" * 70)
    print()
    print(f"  Server: {SERVER_INFO['name']} v{SERVER_INFO['version']}")
    print(f"  Tools:  {', '.join(t['name'] for t in TOOLS)}")
    print(f"  Time:   {datetime.now(timezone.utc).isoformat()}")
    print()

    # Simulate the 3-step handshake + tool calls
    steps = [
        ("1. Client sends initialize", {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05",
                       "clientInfo": {"name": "claude-desktop", "version": "1.0"}},
        }),
        ("2. Client lists available tools", {
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {},
        }),
        ("3. Client calls 'echo' tool", {
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "echo", "arguments": {"text": "Hello from Claude!"}},
        }),
        ("4. Client calls 'word_count' tool", {
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "word_count",
                       "arguments": {"text": "Model Context Protocol enables AI assistants\nto connect with external data sources and tools."}},
        }),
    ]

    for label, request in steps:
        print(f"{'─' * 70}")
        print(f"  {label}")
        print(f"{'─' * 70}")
        print(f"  REQUEST:")
        print(f"  {json.dumps(request, indent=2).replace(chr(10), chr(10) + '  ')}")
        print()

        response = handle_request(
            request["method"],
            request.get("params", {}),
            request["id"],
        )
        print(f"  RESPONSE:")
        print(f"  {json.dumps(response, indent=2).replace(chr(10), chr(10) + '  ')}")
        print()

    print("=" * 70)
    print("  Session complete — this is exactly the JSON-RPC exchange that")
    print("  happens over stdio between Claude and any MCP server.")
    print("=" * 70)
    print()


if __name__ == "__main__":
    simulate_session()
