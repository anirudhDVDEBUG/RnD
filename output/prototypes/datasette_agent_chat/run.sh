#!/usr/bin/env bash
# datasette-agent chat demo — runs fully offline, no API keys needed.
set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "=== datasette-agent Chat Demo ==="
echo ""

# Step 1 — create sample database
python3 create_sample_db.py
echo ""

# Step 2 — run the agent chat simulation
python3 demo_agent_chat.py
