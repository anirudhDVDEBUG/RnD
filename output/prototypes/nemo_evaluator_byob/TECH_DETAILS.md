# Technical Details — NeMo Evaluator BYOB

## What It Does

This skill/prototype scaffolds the full pipeline for NVIDIA NeMo Evaluator's "Bring Your Own Benchmark" (BYOB) workflow. Given a domain and evaluation criteria, it generates three artifacts: a JSONL evaluation dataset, a YAML judge prompt template, and a YAML evaluation config. Together, these let you run LLM-as-judge evaluations where one model scores another model's outputs on custom rubrics (e.g., accuracy, completeness, domain-specific criteria).

The demo included here runs the entire pipeline locally using mock data and a heuristic-based mock judge, so you can see the complete input → config → scoring → summary flow without any API keys or GPU infrastructure.

## Architecture

```
byob_evaluator.py          # Single-file pipeline (all 5 steps)
├── SAMPLE_DATASET          → 8 tech-knowledge Q&A pairs
├── MOCK_RESPONSES          → Simulated model outputs (varying quality)
├── JUDGE_PROMPT_TEMPLATE   → YAML template with {{input}}/{{response}} slots
├── EVAL_CONFIG_TEMPLATE    → NeMo Evaluator YAML config scaffold
├── mock_judge_score()      → Heuristic scorer (word overlap + length ratio)
└── main()                  → Orchestrates generate → config → evaluate → summarize

output/
├── eval_dataset.jsonl      # Evaluation inputs (JSONL)
├── judge_prompt.yaml       # Judge instructions with template variables
├── eval_config.yaml        # NeMo Evaluator config (dataset + judge + metrics)
└── results/
    ├── eval_results.jsonl   # Per-example scores
    └── summary.json         # Aggregate statistics
```

### Data Flow

1. **Dataset generation** — Writes JSONL with `input`, `reference`, `context` fields.
2. **Judge prompt** — YAML with Jinja-style `{{variable}}` placeholders that NeMo Evaluator fills at runtime.
3. **Config assembly** — Wires dataset path, judge prompt path, judge model, target model, metric definitions, and aggregation method into a single YAML.
4. **Evaluation** — In production, NeMo Evaluator sends each dataset input to the target model, then sends the response + reference to the judge model. The mock version uses heuristic scoring (word overlap for accuracy, length ratio for completeness, sentence count for clarity).
5. **Results** — Per-example JSONL with scores + reasoning, plus aggregate summary JSON.

### Key Dependencies

- **Demo:** Python 3.10+ standard library only (json, statistics, pathlib, random).
- **Production:** `nemo-evaluator` Python package, NVIDIA NIM endpoint for the target model, a judge model endpoint (NIM, OpenAI-compatible, or local).

## Limitations

- **Mock judge is not an LLM.** The demo's scorer uses word-overlap heuristics, not actual LLM reasoning. Scores are illustrative, not meaningful evaluations.
- **No real model calls.** The prototype doesn't call any API. To evaluate a real model, you need a NIM endpoint and the `nemo-evaluator` package.
- **Config is a starting point.** The generated YAML follows NeMo Evaluator conventions but may need adjustment for specific NeMo Evaluator API versions.
- **Dataset is hardcoded.** The 8 examples are built-in. In practice, you'd bring hundreds of domain-specific examples.
- **No async/batch support.** The demo runs synchronously. Production NeMo Evaluator supports batched inference.

## Why This Matters for Claude-Driven Products

**Agent factories / quality gates:** If you're building agents that generate content (ad copy, marketing emails, support responses), BYOB lets you define domain-specific rubrics and continuously score agent output quality. This is the eval layer that sits between "ship it" and "is it actually good."

**Lead-gen and marketing:** Custom benchmarks for evaluating LLM-generated landing pages, email sequences, or ad creatives against brand voice, persuasiveness, and factual accuracy criteria — scored at scale by a judge model.

**Voice AI:** Evaluate transcript-based responses for empathy, helpfulness, and script adherence using custom judge prompts tailored to call-center scenarios.

**Model selection:** When comparing fine-tuned models or prompt variants, BYOB gives you quantitative per-metric scores instead of vibes-based evaluation. Run the same benchmark across model A and model B, compare aggregate scores.
