#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "  Claude Security Skills - Demo Audit"
echo "=============================================="
echo ""
echo "Scanning mock_project/ with 6 security skill categories:"
echo "  1. Slopsquatting (hallucinated packages)"
echo "  2. Prompt Injection patterns"
echo "  3. Hardcoded Secrets"
echo "  4. Docker Security"
echo "  5. OWASP LLM Top 10"
echo "  6. GitHub Actions Security"
echo ""

python3 "$SCRIPT_DIR/security_scanner.py" "$SCRIPT_DIR/mock_project"

echo ""
echo "Done. See README.md for how to install the full 25-skill set into Claude Code."
