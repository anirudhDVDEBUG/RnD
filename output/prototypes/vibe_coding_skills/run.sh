#!/usr/bin/env bash
# run.sh — Demo the vibe coding planner with built-in examples
# No API keys or external services required.
set -euo pipefail

cd "$(dirname "$0")"

echo "=========================================="
echo "  Vibe Coding Skills — Demo"
echo "=========================================="
echo ""

# Run built-in examples
python3 vibe_planner.py

echo ""
echo "--- Custom request demo ---"
echo ""
python3 vibe_planner.py "Create a drag-and-drop kanban board in Next.js with TypeScript. Cards should animate when moved between columns. Handle the empty column state and loading from a GraphQL API."
