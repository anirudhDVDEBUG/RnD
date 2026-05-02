#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "LangChain Agent Platform — Demo Suite"
echo "======================================="
echo ""

# Check dependencies
python3 -c "import langchain_core" 2>/dev/null || {
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
}

python3 demo_chain.py
python3 demo_agent.py
python3 demo_rag.py
python3 demo_structured.py

echo "======================================="
echo "All demos completed successfully."
echo "See HOW_TO_USE.md for next steps."
