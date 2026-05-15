#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR="$SCRIPT_DIR/demo_company_brain"

# Clean previous demo
rm -rf "$DEMO_DIR"

echo "============================================================"
echo "  Company Execution Layer — Demo"
echo "  Concept by Bradley Bonanno"
echo "  Source: youtube.com/watch?v=gMm50Sy_GmQ"
echo "============================================================"
echo ""
echo "This demo scaffolds a company brain, validates it, runs"
echo "skills against live context, and adds a custom skill."
echo ""

python3 "$SCRIPT_DIR/execution_layer.py" demo "$DEMO_DIR"

echo ""
echo "── Sample output file ──────────────────────────────────────"
echo ""
# Show the generated output file
OUTPUT_FILE=$(find "$DEMO_DIR/output" -name "*.md" -type f | head -1)
if [ -n "$OUTPUT_FILE" ]; then
    cat "$OUTPUT_FILE"
else
    echo "(no output files generated)"
fi

echo ""
echo "── Demo directory tree ─────────────────────────────────────"
echo ""
# Simple tree display without requiring 'tree' command
find "$DEMO_DIR" -type f | sort | while read -r f; do
    rel="${f#$DEMO_DIR/}"
    depth=$(echo "$rel" | tr -cd '/' | wc -c)
    indent=$(printf '%*s' "$((depth * 2))" '')
    basename=$(basename "$f")
    echo "  ${indent}${basename}"
done

echo ""
echo "Done. Explore the demo at: $DEMO_DIR/"
