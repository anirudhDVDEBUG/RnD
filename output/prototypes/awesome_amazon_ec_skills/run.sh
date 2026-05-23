#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Install dependencies quietly
pip install -q -r requirements.txt 2>/dev/null || pip install -q tabulate 2>/dev/null || true

echo ""
echo "============================================================"
echo "  Awesome Amazon EC Skills — Full Demo"
echo "  Cross-border e-commerce toolkit (跨境电商工具集)"
echo "============================================================"

# Run all four modules
python -m amazon_ec.listing_optimizer --asin B0EXAMPLE01
python -m amazon_ec.keyword_researcher --seed "insulated water bottle"
python -m amazon_ec.ppc_analyzer --campaign demo_campaign
python -m amazon_ec.sourcing_evaluator --product "stainless steel bottle"

echo "============================================================"
echo "  Demo complete. See HOW_TO_USE.md for integration options."
echo "============================================================"
