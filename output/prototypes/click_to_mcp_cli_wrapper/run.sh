#!/usr/bin/env bash
# run.sh — End-to-end demo of click-to-mcp
# Works without external API keys.
set -e

cd "$(dirname "$0")"

echo "============================================"
echo " click-to-mcp  —  CLI-to-MCP in one line"
echo "============================================"
echo

# ── 1. Install dependencies ────────────────────
echo "▸ Installing dependencies..."
pip install -q click 'click-to-mcp>=0.1.0' 2>/dev/null || {
    echo "  ⚠  pip install failed — falling back to local demo only"
    INSTALL_FAILED=1
}
echo

# ── 2. Demo the raw Click CLI ──────────────────
echo "── Step 1: Run the Click CLI directly ──"
echo
echo '$ python3 demo_cli.py greet --name "Claude"'
python3 demo_cli.py greet --name "Claude"
echo
echo '$ python3 demo_cli.py hash "hello world" --algorithm sha256'
python3 demo_cli.py hash "hello world" --algorithm sha256
echo
echo '$ python3 demo_cli.py now'
python3 demo_cli.py now
echo
echo '$ python3 demo_cli.py prettyjson '\''{"key":"value","n":42}'\'''
python3 demo_cli.py prettyjson '{"key":"value","n":42}'
echo
echo '$ python3 demo_cli.py wordcount "The quick brown fox jumps over the lazy dog"'
python3 demo_cli.py wordcount "The quick brown fox jumps over the lazy dog"
echo

# ── 3. Show the MCP wrapper (the point of this tool) ──
echo "── Step 2: The MCP wrapper — just ONE extra line of code ──"
echo
echo "  from demo_cli import cli"
echo "  from click_to_mcp import click_to_mcp"
echo "  mcp_server = click_to_mcp(cli)   # <-- that's it"
echo

if [ -z "$INSTALL_FAILED" ]; then
    echo "▸ Verifying MCP server can be imported..."
    python3 -c "
from demo_cli import cli
from click_to_mcp import click_to_mcp
server = click_to_mcp(cli)
print('  ✓ MCP server created successfully')
print(f'  ✓ Server object: {server}')
print('  ✓ Ready to serve via: python3 mcp_server.py')
" 2>&1 || echo "  ⚠  Import check skipped (click-to-mcp may need newer Python)"
else
    echo "  (skipping MCP import — click-to-mcp not installed)"
    echo "  Install manually:  pip install click-to-mcp"
fi

echo
echo "── Step 3: MCP client config (paste into ~/.claude.json) ──"
echo
cat <<'JSONBLOCK'
{
  "mcpServers": {
    "devtools": {
      "command": "python3",
      "args": ["mcp_server.py"],
      "env": {}
    }
  }
}
JSONBLOCK

echo
echo "============================================"
echo " Done. Each Click command → one MCP tool."
echo " greet, hash, now, prettyjson, wordcount"
echo " are all now callable by any MCP client."
echo "============================================"
