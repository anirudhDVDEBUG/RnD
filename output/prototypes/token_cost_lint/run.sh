#!/usr/bin/env bash
# Token Cost Lint — end-to-end demo
# Runs a static audit on the included sample_project/ and prints findings.
# No external API keys required.

set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "  Token Cost Lint — Demo Run"
echo "========================================"
echo ""
echo "Auditing sample_project/ for token waste patterns..."
echo "(10 categories x 31 sub-patterns, zero LLM calls)"
echo ""

# Run the audit in report mode
python3 audit.py --target ./sample_project --format report

echo ""
echo "--- JSON output ---"
echo ""

# Also show JSON summary
python3 audit.py --target ./sample_project --format json | python3 -c "
import sys, json
data = json.load(sys.stdin)
s = data['stats']
sm = data['summary']
print(f'Summary (JSON):')
print(f'  Files scanned:  {s[\"files_scanned\"]}')
print(f'  Est. tokens:    {s[\"estimated_tokens\"]:,}')
print(f'  Waste tokens:   {s[\"waste_tokens\"]:,}')
print(f'  Waste %:        {s.get(\"waste_percentage\", 0)}%')
print(f'  Findings:       {sm[\"total_findings\"]}')
print(f'  By severity:    {sm[\"by_severity\"]}')
"

echo ""
echo "Done. Run 'python3 audit.py --target YOUR_PROJECT' to audit your own code."
