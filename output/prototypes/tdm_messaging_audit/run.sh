#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== TDM Messaging Audit — Demo ==="
echo ""
echo "Running audit on 3 sample landing pages..."
echo "(developer-centric ➜ mixed ➜ TDM-optimized)"
echo ""

python3 tdm_audit.py

echo ""
echo "=== Custom file audit ==="
echo "You can also audit your own copy:"
echo "  python3 tdm_audit.py my_landing_page.txt 'MyProduct'"
