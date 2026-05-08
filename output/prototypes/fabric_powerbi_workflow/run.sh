#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Running Fabric & Power BI Workflow Skill demo..."
echo ""

python3 demo_fabric_workflow.py
