"""MCP (Model Context Protocol) handler for Seidr-Smidja."""

import json
import sys


def run_mcp():
    """Run as an MCP server over stdio (JSON-RPC 2.0)."""
    print("[MCP] Seidr-Smidja MCP server ready", file=sys.stderr)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            _send_error(-32700, "Parse error", None)
            continue

        method = request.get("method", "")
        req_id = request.get("id")
        params = request.get("params", {})

        if method == "initialize":
            _send_result(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "seidr-smidja", "version": "0.3.0"}
            })
        elif method == "tools/list":
            _send_result(req_id, {
                "tools": [
                    {
                        "name": "create_avatar",
                        "description": "Create a VRM avatar with specified style and customizations",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Avatar name"},
                                "style": {"type": "string", "enum": ["anime", "cyberpunk", "fantasy", "casual"]},
                                "hair": {"type": "string", "description": "Hair style"},
                                "eyes": {"type": "string", "description": "Eye style"},
                                "outfit": {"type": "string", "description": "Outfit type"},
                            },
                            "required": ["name"]
                        }
                    },
                    {
                        "name": "list_styles",
                        "description": "List available style presets",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            })
        elif method == "tools/call":
            tool_name = params.get("name", "")
            args = params.get("arguments", {})

            if tool_name == "create_avatar":
                from seidr_smidja import create_avatar
                result = create_avatar(**args)
                _send_result(req_id, {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                })
            elif tool_name == "list_styles":
                from style_presets import PRESETS
                _send_result(req_id, {
                    "content": [{"type": "text", "text": json.dumps(list(PRESETS.keys()))}]
                })
            else:
                _send_error(-32601, f"Unknown tool: {tool_name}", req_id)
        else:
            _send_error(-32601, f"Method not found: {method}", req_id)


def _send_result(req_id, result):
    response = {"jsonrpc": "2.0", "id": req_id, "result": result}
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()


def _send_error(code, message, req_id):
    response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()
