#!/usr/bin/env bash
# NeMo Evaluator BYOB — end-to-end demo
# Produces evaluation dataset, config, judge prompt, runs mock eval, prints results.
set -euo pipefail
cd "$(dirname "$0")"

echo "--- NeMo Evaluator BYOB Demo ---"
echo ""

python3 byob_evaluator.py

echo "--- Generated artifacts ---"
echo ""
ls -lh output/eval_dataset.jsonl output/judge_prompt.yaml output/eval_config.yaml output/results/*.json output/results/*.jsonl 2>/dev/null
echo ""
echo "--- Sample eval_config.yaml ---"
head -20 output/eval_config.yaml
echo ""
echo "--- Sample eval_dataset.jsonl (first 3 lines) ---"
head -3 output/eval_dataset.jsonl
