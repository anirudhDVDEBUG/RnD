# How to Use — NeMo Evaluator BYOB

## What This Is

A **Claude Code skill** that generates custom LLM evaluation benchmarks using NVIDIA's NeMo Evaluator BYOB framework. It creates evaluation datasets, judge prompt templates, and config files — everything needed to score LLM outputs against custom criteria.

## Install (Skill Setup)

### As a Claude Code Skill

1. Copy the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/nemo_evaluator_byob
cp SKILL.md ~/.claude/skills/nemo_evaluator_byob/SKILL.md
```

2. The skill activates on these trigger phrases:
   - "create custom benchmark"
   - "evaluate LLM"
   - "nemo evaluator"
   - "byob evaluation"
   - "custom eval config"

### Standalone Demo (No API Keys Needed)

```bash
git clone <this-repo>
cd nemo_evaluator_byob
bash run.sh
```

**Requirements:** Python 3.10+ (stdlib only — no pip install needed for the demo).

For production use with real NeMo Evaluator:
```bash
pip install nemo-evaluator
```

## First 60 Seconds

**Input:** Run the demo.

```bash
bash run.sh
```

**Output:** The script generates four artifacts and prints a scored results table:

```
[1/5] Generating evaluation dataset...
      → output/eval_dataset.jsonl  (8 examples)
[2/5] Creating judge prompt template...
      → output/judge_prompt.yaml
[3/5] Building evaluation config...
      → output/eval_config.yaml
[4/5] Running evaluation (mock judge)...
      → output/results/eval_results.jsonl
[5/5] Generating results summary...

========================================================================
  NeMo Evaluator BYOB — Evaluation Results
========================================================================
  #    Accuracy   Complete   Clarity    Question (truncated)
  1    4          4          4          Explain the difference between TCP and...
  2    3          4          3          What is a Python decorator and when wo...
  ...
------------------------------------------------------------------------
  Overall score (mean of all metrics): 3.62 / 5.00
========================================================================
```

**Generated files:**

| File | What It Does |
|------|-------------|
| `output/eval_dataset.jsonl` | 8 evaluation examples with inputs + reference answers |
| `output/judge_prompt.yaml` | Judge template with accuracy/completeness/clarity rubric |
| `output/eval_config.yaml` | NeMo Evaluator config wiring dataset → judge → metrics |
| `output/results/eval_results.jsonl` | Per-example scores from the mock judge |
| `output/results/summary.json` | Aggregate metrics as JSON |

## Using With Real NeMo Evaluator

Once you have `nemo-evaluator` installed and a NIM endpoint running:

1. Edit `output/eval_config.yaml` — set `target.model` and `target.endpoint` to your model.
2. Replace mock data in `eval_dataset.jsonl` with your real evaluation examples.
3. Run:

```bash
nemo-evaluator run --config output/eval_config.yaml --output output/results/
```

## Using the Skill in Claude Code

After installing the skill, ask Claude:

> "Create a custom benchmark to evaluate my customer-support LLM on empathy and accuracy"

Claude will:
1. Ask about your evaluation criteria and scoring method
2. Generate a tailored JSONL dataset schema
3. Write a judge prompt with your custom rubric
4. Output a ready-to-use NeMo Evaluator config
