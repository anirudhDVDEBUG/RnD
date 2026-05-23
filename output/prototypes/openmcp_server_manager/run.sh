#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== OpenMCP Server Manager Demo ==="
echo ""

# No npm install needed - zero external dependencies
node src/demo.js

echo ""
echo "--- CLI usage examples (also working): ---"
echo ""

CONFIG="demo-cli-servers.json"
rm -f "$CONFIG"

# Add two servers via CLI
node src/cli.js add myapi node ./server.js --config "$CONFIG"
node src/cli.js add search npx -y @modelcontextprotocol/server-brave-search --config "$CONFIG" --env BRAVE_KEY=demo123

# List them
node src/cli.js list --config "$CONFIG"

# Export for Claude
node src/cli.js export --config "$CONFIG"

# Clean up demo artifacts
rm -f "$CONFIG"
echo "Done. See HOW_TO_USE.md for integration instructions."
