#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "============================================================"
echo " OpenClaw Orchestra — Multi-Agent Orchestration Demo"
echo "============================================================"
echo ""

# Clean previous workspaces
rm -rf workspaces/

# Run orchestrator in mock mode (no API key needed)
python3 orchestrator.py \
  --config orchestra.yaml \
  --task "Implement user authentication flow with login, registration, and session management"

echo ""
echo "--- Workspace artifacts ---"
echo ""
find workspaces/ -type f | sort | while read -r f; do
  echo ">> $f"
  head -5 "$f"
  echo "..."
  echo ""
done

echo "Done. See workspaces/ for full agent outputs."
