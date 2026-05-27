#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Trending Claude Skills Leaderboard ==="
echo ""

# Install deps if needed (requests is optional for mock mode)
if [ -f requirements.txt ]; then
    pip install -q -r requirements.txt 2>/dev/null || true
fi

echo "--- Table view (mock data, no API key needed) ---"
python3 trending_skills.py --top 12

echo ""
echo "--- JSON view (top 5) ---"
python3 trending_skills.py --json --top 5

echo ""
echo "--- Filter by topic: claude-skills ---"
python3 trending_skills.py --topic claude-skills --top 8

echo ""
echo "Done. Use --live flag with GITHUB_TOKEN for real-time data."
