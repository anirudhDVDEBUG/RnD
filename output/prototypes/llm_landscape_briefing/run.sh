#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== LLM Landscape Briefing Demo ==="
echo ""

# Run all four focus areas
for focus in general coding cost_sensitive multi_provider; do
    python3 llm_briefing.py "$focus"
    echo ""
done

# Also show JSON output for the coding focus
echo "=== JSON output (coding focus) ==="
python3 llm_briefing.py coding json
