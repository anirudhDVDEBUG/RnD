#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "--- VisuAI Research Agent  |  Demo Run ---"
echo ""

# 1. Create venv if needed
if [ ! -d "venv" ]; then
    echo "[setup] Creating virtual environment ..."
    python3 -m venv venv
fi
source venv/bin/activate

# 2. Install deps
echo "[setup] Installing dependencies ..."
pip install -q -r requirements.txt

# 3. Generate sample dataset
echo "[data]  Generating sample clinical-trial dataset ..."
python generate_sample_data.py

# 4. Run the agent
echo ""
python main.py sample_clinical_trial.csv -o output

echo ""
echo "--- HTML files you can open in a browser: ---"
ls -1 output/*.html 2>/dev/null || echo "(none)"
