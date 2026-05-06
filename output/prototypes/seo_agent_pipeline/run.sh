#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Install dependencies
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Clean previous output
rm -rf pipeline_output/

# Run the pipeline with a sample topic
echo ""
echo "Running SEO Agent Pipeline demo..."
echo ""
python3 pipeline.py "ai-powered code review tools"

# Show the generated article
echo "─────────────────────────────────────────────────────"
echo "  Generated Article Preview (first 30 lines):"
echo "─────────────────────────────────────────────────────"
head -30 pipeline_output/ai-powered-code-review-tools/index.md
echo ""
echo "..."
echo ""
echo "─────────────────────────────────────────────────────"
echo "  Pipeline Manifest:"
echo "─────────────────────────────────────────────────────"
cat pipeline_output/ai-powered-code-review-tools/pipeline_manifest.json
echo ""
