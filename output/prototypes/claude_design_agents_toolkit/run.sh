#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================================"
echo "  Claude Design Agents Toolkit — Demo"
echo "============================================================"

python3 demo.py

echo "------------------------------------------------------------"
echo "  Design Lint Hook — checking generated output"
echo "------------------------------------------------------------"

python3 -c "
from design_hooks import lint_report
from pathlib import Path

output_dir = Path('output')
for html_file in sorted(output_dir.glob('*.html')):
    print(lint_report(html_file.read_text(), html_file.name))
    print()
"

echo "============================================================"
echo "  Done. Open output/*.html in a browser to preview layouts."
echo "============================================================"
