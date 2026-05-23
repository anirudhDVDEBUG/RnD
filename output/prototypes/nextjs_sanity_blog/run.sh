#!/usr/bin/env bash
# run.sh — Scaffolds the blog project structure, then serves a mock preview.
# No API keys or external services required.
set -e

cd "$(dirname "$0")"

echo "============================================"
echo "  Next.js + Sanity Blog Skill — Demo"
echo "============================================"

# Step 1: Generate the scaffold
echo ""
echo "[1/2] Generating Next.js + Sanity blog scaffold..."
node scaffold.js

# Step 2: Show what was generated
echo ""
echo "[2/2] Starting mock blog server (5 seconds)..."
echo "      This previews the blog with sample data."
echo ""

# Run server for 5 seconds so output is visible, then stop
timeout 5 node server.js || true

echo ""
echo "============================================"
echo "  Demo complete!"
echo ""
echo "  Scaffold output:  ./generated-blog/"
echo "  To run server:    node server.js"
echo "  Docs:             HOW_TO_USE.md"
echo "============================================"
