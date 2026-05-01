#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Awesome Agent Skills Finder ==="
echo ""

python3 skills_finder.py demo
