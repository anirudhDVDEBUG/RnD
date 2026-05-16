"""
MCP Server wrapper for the DevTools CLI.

This file demonstrates the core value of click-to-mcp:
one function call turns an entire Click CLI group into an MCP server.
"""

from demo_cli import cli

try:
    from click_to_mcp import click_to_mcp
except ImportError:
    import sys
    print("ERROR: click-to-mcp is not installed.", file=sys.stderr)
    print("Run:  pip install click-to-mcp", file=sys.stderr)
    sys.exit(1)

# One line: wrap the entire CLI as an MCP server
mcp_server = click_to_mcp(cli)

if __name__ == "__main__":
    mcp_server.run()
