#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Running Pipecat Voice Pipeline Demo (mock services, no API keys needed)..."
echo ""
python3 mock_pipeline_demo.py
