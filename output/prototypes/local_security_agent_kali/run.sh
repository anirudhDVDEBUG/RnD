#!/usr/bin/env bash
# run.sh — Run the local security agent in mock/demo mode.
# No external API keys or LM Studio required.
set -e

cd "$(dirname "$0")"

echo "=== Local Security Agent — Demo ==="
echo ""

# Use mock mode so the demo works without LM Studio
export MOCK_MODE=1

python3 agent.py \
    --target "192.168.1.100" \
    --objective "enumerate open services and check for known vulnerabilities"
