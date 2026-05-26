#!/usr/bin/env bash
# Research Proof — end-to-end demo
# No external API keys required; uses mock data to demonstrate the pipeline.
set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Installing dependencies (stdlib only — nothing to install)"
echo ""

python3 research_proof.py
