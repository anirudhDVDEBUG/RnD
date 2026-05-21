#!/usr/bin/env bash
# Sprint Orchestrator — end-to-end demo
# No API keys required. Uses built-in demo projects.
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================================"
echo "  Sprint Orchestrator Demo"
echo "  Multi-agent sprint coordination for Claude Code"
echo "============================================================"
echo ""

# --- 1. Show sprint visualization (dependency graph, gantt, file matrix) ---
echo "[Step 1] Visualize sprint plan for SaaS Landing Page project..."
echo ""
python3 sprint_visualizer.py

# --- 2. Execute the sprint with live progress ---
echo ""
echo "[Step 2] Execute sprint with simulated parallel agents..."
echo ""
python3 sprint_orchestrator.py --project saas_landing_page --report sprint_report.md

echo ""
echo "[Step 3] Sprint report written to sprint_report.md"
echo ""

# --- 3. Run second project to show flexibility ---
echo "============================================================"
echo "  Running second demo project: CLI Analytics Tool"
echo "============================================================"
echo ""
python3 sprint_orchestrator.py --project cli_tool

echo ""
echo "Demo complete. See sprint_report.md for the full markdown report."
