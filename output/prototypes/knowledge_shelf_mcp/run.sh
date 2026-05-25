#!/usr/bin/env bash
# run.sh — End-to-end demo of the knowledge-shelf MCP server
# Installs deps, populates sample knowledge items, then runs the demo client.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Knowledge Shelf MCP — End-to-End Demo"
echo "============================================"
echo ""

# ── 1. Install dependencies ──
echo "[1/3] Installing dependencies ..."
npm install --no-audit --no-fund 2>&1 | tail -3
echo ""

# ── 2. Populate sample knowledge items ──
echo "[2/3] Populating sample knowledge shelf ..."
node setup_sample_shelf.mjs
echo ""

# ── 3. Run demo client ──
echo "[3/3] Running demo client ..."
node demo_client.mjs
echo ""

echo "Done. See HOW_TO_USE.md to integrate with Claude Code."
