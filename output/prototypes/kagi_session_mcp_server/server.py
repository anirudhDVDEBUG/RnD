#!/usr/bin/env python3
"""
Kagi Session2API MCP Server

An MCP (Model Context Protocol) server that provides Kagi Search and Summarizer
tools using session tokens instead of paid API keys. Connects to Kagi's web
endpoints with your browser session cookie, giving any MCP client (Claude Desktop,
Cursor, Windsurf, Claude Code) free access to Kagi's search and summarization.

When KAGI_SESSION_TOKEN is not set, runs in demo/mock mode with sample data.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from typing import Any

# ---------------------------------------------------------------------------
# MCP protocol helpers (minimal stdio JSON-RPC implementation)
# ---------------------------------------------------------------------------

def read_message() -> dict:
    """Read a JSON-RPC message from stdin (Content-Length framed)."""
    headers = {}
    while True:
        line = sys.stdin.buffer.readline()
        if line == b"\r\n" or line == b"\n":
            break
        if b":" in line:
            key, value = line.decode().strip().split(":", 1)
            headers[key.strip()] = value.strip()
    content_length = int(headers.get("Content-Length", 0))
    if content_length == 0:
        return {}
    body = sys.stdin.buffer.read(content_length)
    return json.loads(body)


def send_message(msg: dict):
    """Write a JSON-RPC message to stdout (Content-Length framed)."""
    body = json.dumps(msg)
    header = f"Content-Length: {len(body)}\r\n\r\n"
    sys.stdout.buffer.write(header.encode())
    sys.stdout.buffer.write(body.encode())
    sys.stdout.buffer.flush()


def make_response(req_id: Any, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def make_error(req_id: Any, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


# ---------------------------------------------------------------------------
# Kagi API helpers
# ---------------------------------------------------------------------------

SESSION_TOKEN = os.environ.get("KAGI_SESSION_TOKEN", "")
DEMO_MODE = not SESSION_TOKEN

KAGI_SEARCH_URL = "https://kagi.com/api/autosuggest"
KAGI_SEARCH_HTML_URL = "https://kagi.com/search"
KAGI_SUMMARIZE_URL = "https://kagi.com/mother/summary_labs"


def kagi_search(query: str, limit: int = 10) -> list[dict]:
    """Perform a Kagi web search using the session token."""
    if DEMO_MODE:
        return _mock_search(query, limit)
    params = urllib.parse.urlencode({"q": query})
    url = f"{KAGI_SEARCH_HTML_URL}?{params}"
    req = urllib.request.Request(url, headers={
        "Cookie": f"kagi_session={SESSION_TOKEN}",
        "User-Agent": "KagiMCP/1.0",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("data", data.get("results", []))
            return results[:limit]
    except Exception as e:
        return [{"title": "Search error", "snippet": str(e), "url": ""}]


def kagi_summarize(url_or_text: str, summary_type: str = "summary") -> str:
    """Summarize a URL or text using Kagi's summarizer."""
    if DEMO_MODE:
        return _mock_summarize(url_or_text, summary_type)
    payload = json.dumps({"url": url_or_text, "summary_type": summary_type}).encode()
    req = urllib.request.Request(KAGI_SUMMARIZE_URL, data=payload, headers={
        "Cookie": f"kagi_session={SESSION_TOKEN}",
        "User-Agent": "KagiMCP/1.0",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get("output", data.get("summary", json.dumps(data, indent=2)))
    except Exception as e:
        return f"Summarization error: {e}"


# ---------------------------------------------------------------------------
# Mock / demo data
# ---------------------------------------------------------------------------

def _mock_search(query: str, limit: int) -> list[dict]:
    results = [
        {
            "title": f"Kagi Search Result 1 for '{query}'",
            "snippet": f"Kagi delivers high-quality, ad-free results for '{query}'. "
                       "Unlike traditional search engines, Kagi prioritizes relevance "
                       "and user privacy with zero tracking.",
            "url": f"https://example.com/result1?q={urllib.parse.quote(query)}",
        },
        {
            "title": f"Wikipedia — {query.title()}",
            "snippet": f"An encyclopedic overview of {query}. This article covers "
                       "history, key concepts, notable developments, and further reading.",
            "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query.replace(' ', '_'))}",
        },
        {
            "title": f"GitHub — Open-source projects related to {query}",
            "snippet": f"Browse repositories, libraries, and tools related to {query}. "
                       "Star counts, recent activity, and contributor stats included.",
            "url": f"https://github.com/search?q={urllib.parse.quote(query)}",
        },
        {
            "title": f"Stack Overflow — {query} Q&A",
            "snippet": f"Top voted questions and answers about {query} from the "
                       "developer community.",
            "url": f"https://stackoverflow.com/search?q={urllib.parse.quote(query)}",
        },
        {
            "title": f"Research papers on {query}",
            "snippet": f"Peer-reviewed publications and preprints exploring the latest "
                       f"advances in {query}.",
            "url": f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}",
        },
    ]
    return results[:limit]


def _mock_summarize(url_or_text: str, summary_type: str) -> str:
    return (
        f"[DEMO MODE — Summary of: {url_or_text[:80]}]\n\n"
        f"This is a demonstration summary (type: {summary_type}). In live mode with a "
        "valid KAGI_SESSION_TOKEN, this would return a real Kagi-powered summary.\n\n"
        "Key points:\n"
        "- Kagi's summarizer uses advanced AI to distill content into concise summaries\n"
        "- Supports URLs (web pages, articles, PDFs) and raw text input\n"
        "- Available summary types: summary, key_moments, takeaway\n"
        "- No API key billing — uses your existing Kagi subscription via session cookie\n"
    )


# ---------------------------------------------------------------------------
# MCP tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "kagi_search",
        "description": "Search the web using Kagi. Returns high-quality, ad-free results. "
                       "Kagi prioritizes relevance over ads and tracking.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max number of results to return (default: 5)",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "kagi_summarize",
        "description": "Summarize a URL or text using Kagi's AI summarizer. "
                       "Supports web pages, articles, and raw text.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url_or_text": {
                    "type": "string",
                    "description": "A URL to summarize, or raw text to condense",
                },
                "summary_type": {
                    "type": "string",
                    "description": "Type of summary: 'summary', 'key_moments', or 'takeaway'",
                    "default": "summary",
                    "enum": ["summary", "key_moments", "takeaway"],
                },
            },
            "required": ["url_or_text"],
        },
    },
]

# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------

def handle_tool_call(name: str, arguments: dict) -> dict:
    if name == "kagi_search":
        query = arguments.get("query", "")
        limit = arguments.get("limit", 5)
        results = kagi_search(query, limit)
        text = f"Kagi search results for: {query}\n"
        text += "=" * 50 + "\n\n"
        for i, r in enumerate(results, 1):
            text += f"{i}. {r.get('title', 'No title')}\n"
            text += f"   {r.get('snippet', '')}\n"
            text += f"   URL: {r.get('url', '')}\n\n"
        return {"content": [{"type": "text", "text": text}]}

    elif name == "kagi_summarize":
        url_or_text = arguments.get("url_or_text", "")
        summary_type = arguments.get("summary_type", "summary")
        result = kagi_summarize(url_or_text, summary_type)
        return {"content": [{"type": "text", "text": result}]}

    else:
        return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}], "isError": True}


# ---------------------------------------------------------------------------
# MCP server main loop (stdio transport)
# ---------------------------------------------------------------------------

SERVER_INFO = {
    "name": "kagi-session-mcp",
    "version": "1.0.0",
}

CAPABILITIES = {
    "tools": {},
}


def run_server():
    """Run the MCP server over stdio."""
    while True:
        try:
            msg = read_message()
        except Exception:
            break
        if not msg:
            break

        method = msg.get("method")
        req_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            send_message(make_response(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": CAPABILITIES,
                "serverInfo": SERVER_INFO,
            }))

        elif method == "notifications/initialized":
            pass  # no response needed

        elif method == "tools/list":
            send_message(make_response(req_id, {"tools": TOOLS}))

        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            result = handle_tool_call(tool_name, arguments)
            send_message(make_response(req_id, result))

        elif method == "shutdown":
            send_message(make_response(req_id, {}))
            break

        elif req_id is not None:
            send_message(make_error(req_id, -32601, f"Method not found: {method}"))


# ---------------------------------------------------------------------------
# CLI demo mode
# ---------------------------------------------------------------------------

def run_demo():
    """Run a quick demo showing the tools in action (no MCP client needed)."""
    mode = "DEMO (mock data)" if DEMO_MODE else "LIVE (session token set)"
    print(f"Kagi Session MCP Server — {mode}")
    print("=" * 60)

    # Demo: search
    print("\n[Tool: kagi_search]")
    print(f"  Query: 'Model Context Protocol'\n")
    results = kagi_search("Model Context Protocol", limit=3)
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['title']}")
        print(f"     {r['snippet'][:100]}...")
        print(f"     {r['url']}")
        print()

    # Demo: summarize
    print("[Tool: kagi_summarize]")
    print("  Input: 'https://modelcontextprotocol.io'\n")
    summary = kagi_summarize("https://modelcontextprotocol.io", "summary")
    for line in summary.strip().split("\n"):
        print(f"  {line}")
    print()

    # Show MCP config snippet
    print("=" * 60)
    print("To use as an MCP server, add this to your MCP client config:\n")
    server_path = os.path.abspath(__file__)
    config = {
        "mcpServers": {
            "kagi-search": {
                "command": "python3",
                "args": [server_path],
                "env": {
                    "KAGI_SESSION_TOKEN": "<your_kagi_session_cookie>"
                }
            }
        }
    }
    print(json.dumps(config, indent=2))
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    elif sys.stdin.isatty():
        run_demo()
    else:
        run_server()
