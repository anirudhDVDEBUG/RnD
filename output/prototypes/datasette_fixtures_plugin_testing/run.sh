#!/usr/bin/env bash
# End-to-end demo of datasette-fixtures for plugin testing.
# No external API keys required. Uses mock fixtures if Datasette is not installed.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo " datasette-fixtures: Plugin Testing Demo"
echo "============================================"
echo ""

# Run the main demo (creates DB, lists tables, queries data)
python3 demo_fixtures.py
echo ""

# Run the example plugin tests
python3 test_plugin_example.py
echo ""

# Clean up generated databases
rm -f demo_fixtures.db test_fixtures.db

echo "============================================"
echo " Demo complete."
echo ""
echo " To use real Datasette fixtures:"
echo "   pip install --pre datasette datasette-fixtures"
echo ""
echo " To explore interactively:"
echo "   uvx --prerelease=allow --with datasette-fixtures datasette"
echo "   # Then browse http://localhost:8001/fixtures"
echo "============================================"
