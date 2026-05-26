#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo ""
echo "Auto Project Builder — Next.js + shadcn/ui + SQLite"
echo "===================================================="
echo ""
echo "This demo simulates the autonomous pipeline from"
echo "hongmacho/auto-project-builder: idea → scaffold → UI → DB → features → verify"
echo ""

# Run the builder (pure Node, no external deps needed)
node src/builder.mjs

echo "---"
echo ""
echo "Demo complete. The generated project is in ./generated_project/"
echo ""
echo "In the REAL auto-project-builder, Claude Code acts as the agent"
echo "that writes all the code autonomously. This demo shows the exact"
echo "stages and output structure the tool produces."
echo ""
echo "To preview the generated UI (static HTML, no npm install needed):"
echo "  node src/preview-server.mjs"
echo ""
