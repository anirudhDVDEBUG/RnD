#!/usr/bin/env bash
# CVE Triage — Should I Care? Demo
# Runs end-to-end with mock data, no API keys needed.
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================================"
echo "  CVE Triage — Should I Care?  (Demo)"
echo "============================================================"
echo ""

# --- Scenario 1: Critical CVE that MATCHES a project dependency ---
echo ">>> Scenario 1: xz-utils backdoor (CVE-2024-3094)"
echo "    Checking against sample project dependencies..."
echo ""
python3 cve_triage.py CVE-2024-3094
echo ""
echo "============================================================"
echo ""

# --- Scenario 2: CVE with broad impact (HTTP/2 Rapid Reset) ---
echo ">>> Scenario 2: HTTP/2 Rapid Reset (CVE-2023-44487)"
echo "    A CVE affecting many implementations — grpc found in go.mod..."
echo ""
python3 cve_triage.py CVE-2023-44487
echo ""
echo "============================================================"
echo ""

# --- Scenario 3: CVE that does NOT match (Firefox) ---
echo ">>> Scenario 3: Firefox code injection (CVE-2024-29944)"
echo "    Firefox is not a project dependency — should be NOT APPLICABLE..."
echo ""
python3 cve_triage.py CVE-2024-29944
echo ""
echo "============================================================"
echo ""

# --- Scenario 4: Unknown CVE ---
echo ">>> Scenario 4: Unknown CVE (CVE-9999-99999)"
echo "    Demonstrates graceful handling of unknown CVE IDs..."
echo ""
python3 cve_triage.py CVE-9999-99999
echo ""
echo "============================================================"
echo ""
echo "Done. See HOW_TO_USE.md for integration with Claude Code skills."
