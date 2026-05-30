#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Biodefense Threat Briefing Generator ==="
echo ""

# No external dependencies needed — stdlib only
python3 generate_briefing.py

echo ""
echo "--- JSON output demo ---"
echo ""
python3 generate_briefing.py --format json --scope "Regional (Pacific Northwest)" --audience "State epidemiologists" | python3 -m json.tool | head -30
echo "  ... (truncated)"
