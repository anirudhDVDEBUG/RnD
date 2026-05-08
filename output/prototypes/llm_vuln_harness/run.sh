#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "======================================================================"
echo "  LLM Vulnerability Research Harness — Demo Run"
echo "  Methodology: Steer / Scale / Stack (Mozilla Firefox approach)"
echo "======================================================================"
echo ""
echo "Target directory: sample_targets/"
echo "Scanning C files for vulnerability classes..."
echo ""

# Run the harness in text mode (default)
python3 vuln_harness.py sample_targets text

echo ""
echo "----------------------------------------------------------------------"
echo "  JSON output also available:"
echo "    python3 vuln_harness.py sample_targets json"
echo ""
echo "  Point at your own code:"
echo "    python3 vuln_harness.py /path/to/your/c/project"
echo "----------------------------------------------------------------------"
echo ""
