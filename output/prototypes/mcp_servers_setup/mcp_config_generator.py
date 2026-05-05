#!/usr/bin/env python3
"""MCP Server Config Generator — builds claude_desktop_config.json and .mcp.json
snippets for the official modelcontextprotocol/servers collection."""

import json
import sys
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Registry of official MCP servers
# ---------------------------------------------------------------------------

@dataclass
class McpServerDef:
    name: str
    package: str
    runtime: str  # "npx" or "uvx"
    description: str
    default_args: list[str] = field(default_factory=list)
    env_vars: dict[str, str] = field(default_factory=dict)
    placeholder_env: dict[str, str] = field(default_factory=dict)

OFFICIAL_SERVERS: list[McpServerDef] = [
    McpServerDef(
        name="filesystem",
        package="@modelcontextprotocol/server-filesystem",
        runtime="npx",
        description="Read/write local files, directory listing, search",
        default_args=["/home/user/documents"],
    ),
    McpServerDef(
        name="github",
        package="@modelcontextprotocol/server-github",
        runtime="npx",
        description="GitHub API — repos, issues, PRs, file contents",
        placeholder_env={"GITHUB_PERSONAL_ACCESS_TOKEN": "<your-token>"},
    ),
    McpServerDef(
        name="slack",
        package="@modelcontextprotocol/server-slack",
        runtime="npx",
        description="Slack workspace — channels, messages, users",
        placeholder_env={"SLACK_BOT_TOKEN": "xoxb-<your-token>", "SLACK_TEAM_ID": "<team-id>"},
    ),
    McpServerDef(
        name="memory",
        package="@modelcontextprotocol/server-memory",
        runtime="npx",
        description="Knowledge-graph persistent memory for Claude",
    ),
    McpServerDef(
        name="puppeteer",
        package="@modelcontextprotocol/server-puppeteer",
        runtime="npx",
        description="Browser automation and web scraping",
    ),
    McpServerDef(
        name="brave-search",
        package="@modelcontextprotocol/server-brave-search",
        runtime="npx",
        description="Web search via Brave Search API",
        placeholder_env={"BRAVE_API_KEY": "<your-key>"},
    ),
    McpServerDef(
        name="google-maps",
        package="@modelcontextprotocol/server-google-maps",
        runtime="npx",
        description="Google Maps geocoding, directions, places",
        placeholder_env={"GOOGLE_MAPS_API_KEY": "<your-key>"},
    ),
    McpServerDef(
        name="sequential-thinking",
        package="@modelcontextprotocol/server-sequential-thinking",
        runtime="npx",
        description="Dynamic problem-solving through sequential thought",
    ),
    McpServerDef(
        name="git",
        package="mcp-server-git",
        runtime="uvx",
        description="Git operations — log, diff, status, commit",
        default_args=["--repository", "/path/to/repo"],
    ),
    McpServerDef(
        name="sqlite",
        package="mcp-server-sqlite",
        runtime="uvx",
        description="SQLite database read/write/query",
        default_args=["--db-path", "/path/to/database.db"],
    ),
    McpServerDef(
        name="fetch",
        package="mcp-server-fetch",
        runtime="uvx",
        description="Fetch and convert web pages to markdown",
    ),
    McpServerDef(
        name="sentry",
        package="mcp-server-sentry",
        runtime="uvx",
        description="Sentry.io error tracking integration",
        placeholder_env={"SENTRY_AUTH_TOKEN": "<your-token>"},
    ),
]


def server_by_name(name: str) -> Optional[McpServerDef]:
    for s in OFFICIAL_SERVERS:
        if s.name == name:
            return s
    return None


# ---------------------------------------------------------------------------
# Config builders
# ---------------------------------------------------------------------------

def build_server_entry(server: McpServerDef, args_override: Optional[list[str]] = None) -> dict:
    """Build a single mcpServers entry for one server."""
    args = ["-y", server.package] if server.runtime == "npx" else [server.package]
    extra = args_override if args_override is not None else server.default_args
    args.extend(extra)

    entry: dict = {
        "command": server.runtime,
        "args": args,
    }
    env = {**server.env_vars, **server.placeholder_env}
    if env:
        entry["env"] = env
    return entry


def build_claude_desktop_config(server_names: list[str]) -> dict:
    """Build a full claude_desktop_config.json for the given server names."""
    servers = {}
    for name in server_names:
        s = server_by_name(name)
        if s is None:
            print(f"  [WARN] Unknown server: {name}, skipping", file=sys.stderr)
            continue
        servers[name] = build_server_entry(s)
    return {"mcpServers": servers}


def build_mcp_json(server_names: list[str]) -> dict:
    """Build a .mcp.json (Claude Code project-level config)."""
    servers = {}
    for name in server_names:
        s = server_by_name(name)
        if s is None:
            continue
        servers[name] = build_server_entry(s)
    return {"mcpServers": servers}


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_server_catalog():
    """Print a formatted catalog of all official MCP servers."""
    print("=" * 70)
    print("  Official MCP Servers — modelcontextprotocol/servers")
    print("=" * 70)
    print()
    ts = [s for s in OFFICIAL_SERVERS if s.runtime == "npx"]
    py = [s for s in OFFICIAL_SERVERS if s.runtime == "uvx"]

    print("  TypeScript servers (npx):")
    print("  " + "-" * 40)
    for s in ts:
        needs_key = " [API key required]" if s.placeholder_env else ""
        print(f"    {s.name:<22} {s.description}{needs_key}")

    print()
    print("  Python servers (uvx):")
    print("  " + "-" * 40)
    for s in py:
        needs_key = " [API key required]" if s.placeholder_env else ""
        print(f"    {s.name:<22} {s.description}{needs_key}")
    print()


def print_config(config: dict, label: str):
    """Pretty-print a config dict with a label."""
    print(f"\n{'─' * 70}")
    print(f"  {label}")
    print(f"{'─' * 70}")
    print(json.dumps(config, indent=2))
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    print_server_catalog()

    # Demo 1: Claude Desktop config with filesystem + memory + sequential-thinking
    desktop_servers = ["filesystem", "memory", "sequential-thinking"]
    desktop_cfg = build_claude_desktop_config(desktop_servers)
    print_config(desktop_cfg, "Claude Desktop config (no API keys needed)")

    # Demo 2: Claude Desktop config with GitHub + Brave Search (needs keys)
    api_servers = ["github", "brave-search"]
    api_cfg = build_claude_desktop_config(api_servers)
    print_config(api_cfg, "Claude Desktop config (API keys required)")

    # Demo 3: Claude Code .mcp.json for a project
    code_servers = ["filesystem", "git", "sqlite"]
    code_cfg = build_mcp_json(code_servers)
    print_config(code_cfg, "Claude Code .mcp.json (project-level)")

    # Demo 4: Full stack config
    all_names = [s.name for s in OFFICIAL_SERVERS]
    full_cfg = build_claude_desktop_config(all_names)
    print_config(full_cfg, f"Full config — all {len(all_names)} servers")

    # Summary
    no_key = [s.name for s in OFFICIAL_SERVERS if not s.placeholder_env]
    needs_key = [s.name for s in OFFICIAL_SERVERS if s.placeholder_env]
    print("=" * 70)
    print("  Summary")
    print("=" * 70)
    print(f"  Total servers:         {len(OFFICIAL_SERVERS)}")
    print(f"  No API key needed:     {len(no_key)}  ({', '.join(no_key)})")
    print(f"  API key required:      {len(needs_key)}  ({', '.join(needs_key)})")
    print(f"  TypeScript (npx):      {sum(1 for s in OFFICIAL_SERVERS if s.runtime == 'npx')}")
    print(f"  Python (uvx):          {sum(1 for s in OFFICIAL_SERVERS if s.runtime == 'uvx')}")
    print()


if __name__ == "__main__":
    main()
