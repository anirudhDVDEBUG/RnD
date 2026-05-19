#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "============================================="
echo " Dell Codex On-Prem Enterprise Deploy Planner"
echo "============================================="
echo ""
echo "No external API keys required - runs with built-in scenarios."
echo ""

# No external deps needed - pure stdlib Python
python3 codex_deploy_planner.py --scenarios

echo ""
echo "To save config files:  python3 codex_deploy_planner.py --save"
echo "Done."
