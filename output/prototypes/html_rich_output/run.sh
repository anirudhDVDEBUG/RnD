#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== html_rich_output skill demo ==="
echo ""

python3 generate_html_report.py

echo ""
echo "Done. The generated HTML file is ready to open in any browser."
