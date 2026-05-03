#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Running ZeroClaw MCP Router demo..."
python3 router.py
