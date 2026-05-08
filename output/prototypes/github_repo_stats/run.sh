#!/usr/bin/env bash
# run.sh — Demo GitHub Repo Stats (uses mock data, no API key needed)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== GitHub Repo Stats — Demo ==="
echo ""
echo "Running with mock data (no GitHub token required)..."
echo ""

python3 "$SCRIPT_DIR/github_repo_stats.py" --mock

echo "---"
echo "To query a live repo:  python3 github_repo_stats.py simonw/datasette"
echo "Set GITHUB_TOKEN env var for higher rate limits (5,000 req/hr)."
