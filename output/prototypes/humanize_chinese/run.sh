#!/usr/bin/env bash
# run.sh — end-to-end demo of humanize_chinese
# No API keys needed. Pure Python, no pip install required.
set -euo pipefail
cd "$(dirname "$0")"

echo "=========================================="
echo " humanize_chinese — demo"
echo "=========================================="
echo

# --- Sample 1: typical AI-generated paragraph ---
SAMPLE1="人工智能技术在近年来取得了显著的进展。此外，它在各个领域都有着广泛的应用，包括医疗、教育和金融等。需要注意的是，人工智能的发展也带来了一些挑战，因此我们需要谨慎对待。"

echo "[Sample 1] AI-generated tech overview"
echo "--------------------------------------"
python3 humanize_chinese.py "$SAMPLE1"
echo

# --- Sample 2: AI marketing copy ---
SAMPLE2="综上所述，本产品具有重要意义，在很大程度上满足了用户的需求。与此同时，我们的团队对产品进行了详细的分析，给予了高度评价。毋庸置疑，该产品将产生了深远的影响。"

echo "[Sample 2] AI marketing copy"
echo "-----------------------------"
python3 humanize_chinese.py "$SAMPLE2"
echo

# --- Sample 3: AI educational content ---
SAMPLE3="众所周知，在当今社会，编程技能发挥着重要作用。然而，学习编程并不是一件容易的事情。如前所述，我们需要持续不断地练习，才能取得进步。不可否认，坚持是成功的关键。"

echo "[Sample 3] AI educational content"
echo "-----------------------------------"
python3 humanize_chinese.py "$SAMPLE3"
echo

echo "=========================================="
echo " Done! All samples humanized successfully."
echo "=========================================="
