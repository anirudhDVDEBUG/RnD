#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "========================================"
echo " Agentic Exfiltration Defense Audit"
echo " Demo: scanning sample vulnerable agent"
echo "========================================"
echo ""

echo "--- [1/3] Scanning VULNERABLE agent config + handler ---"
echo ""
python3 "$DIR/audit.py" "$DIR/samples/vulnerable_agent.json" || true
echo ""

echo "--- [2/3] Scanning VULNERABLE handler code ---"
echo ""
python3 "$DIR/audit.py" "$DIR/samples/vulnerable_handler.py" || true
echo ""

echo "--- [3/3] Scanning HARDENED handler (fewer findings expected) ---"
echo ""
python3 "$DIR/audit.py" "$DIR/samples/hardened_handler.py" || true
echo ""

echo "========================================"
echo " JSON output example:"
echo "========================================"
echo ""
python3 "$DIR/audit.py" "$DIR/samples/vulnerable_agent.json" --json 2>/dev/null | head -30 || true
echo "  ..."
echo ""

echo "Done. Run 'python3 audit.py <your-project-dir>' to scan your own code."
