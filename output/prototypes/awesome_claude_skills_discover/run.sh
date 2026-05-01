#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Awesome Claude Skills Discovery Tool ==="
echo ""

# No external dependencies needed (stdlib only)
python3 discover.py demo
