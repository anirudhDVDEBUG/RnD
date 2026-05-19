#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== iNaturalist Wildlife Sighting Logger ==="
echo ""
echo "Running demo with sample data from Simon Willison's LA River walk..."
echo ""

python3 sighting_logger.py

echo ""
echo "--- Done. Check sighting_report.md and sighting_report.json for outputs. ---"
