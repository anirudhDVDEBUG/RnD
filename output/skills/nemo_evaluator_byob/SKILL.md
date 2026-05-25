---
name: nemo_evaluator_byob
description: |
  Create custom LLM evaluation benchmarks using NVIDIA NeMo Evaluator's Bring Your Own Benchmark (BYOB) framework. Generates evaluation configs, custom judge prompts, and dataset schemas for assessing LLM quality.
  Triggers: create custom benchmark, evaluate LLM, nemo evaluator, byob evaluation, custom eval config
---

# NeMo Evaluator BYOB (Bring Your Own Benchmark)

Create and run custom LLM evaluation benchmarks using NVIDIA NeMo Evaluator's BYOB framework. This skill helps you define custom evaluation criteria, build evaluation datasets, write judge prompts, and generate the configuration files needed to run evaluations via NeMo Evaluator.

## When to use

- "Create a custom benchmark to evaluate my LLM on domain-specific tasks"
- "Set up a BYOB evaluation config for NeMo Evaluator"
- "Build an evaluation dataset and judge prompt for my use case"
- "I need to evaluate LLM responses with custom scoring criteria"
- "Generate a NeMo Evaluator config with a custom rubric"

## How to use

### Step 1: Define the evaluation task

Ask the user what they want to evaluate. Gather:
- **Task type**: e.g., summarization, Q&A, code generation, classification, reasoning
- **Evaluation criteria**: e.g., accuracy, relevance, coherence, safety, factual correctness
- **Scoring method**: numeric scale (1-5), binary pass/fail, or multi-label
- **Judge model**: which LLM will serve as the judge (default: a strong model like GPT-4 or Claude)

### Step 2: Create the evaluation dataset schema

Build a JSONL dataset file with the required fields:

```jsonl
{"input": "<prompt or question>", "reference": "<optional gold answer>", "context": "<optional context>"}
```

Each record should contain at minimum an `input` field. The `reference` field is used for ground-truth comparison. Additional custom fields can be added as needed.

### Step 3: Write the judge prompt template

Create a judge prompt that instructs the evaluator model on how to score responses:

```yaml
judge_prompt: |
  You are an expert evaluator. Given the following input and response, evaluate the response quality.

  ## Input
  {{input}}

  ## Response
  {{response}}

  ## Reference Answer (if available)
  {{reference}}

  ## Evaluation Criteria
  Rate the response on a scale of 1-5 for each criterion:
  - **Accuracy**: Does the response correctly answer the question?
  - **Completeness**: Does it cover all relevant aspects?
  - **Clarity**: Is the response well-structured and easy to understand?

  Return your evaluation as JSON:
  {"accuracy": <1-5>, "completeness": <1-5>, "clarity": <1-5>, "reasoning": "<explanation>"}
```

### Step 4: Generate the NeMo Evaluator config

Create the evaluation configuration YAML:

```yaml
# eval_config.yaml
type: custom
name: my-custom-benchmark

dataset:
  path: ./eval_dataset.jsonl
  format: jsonl

evaluation:
  method: llm-as-judge
  judge:
    prompt_template: ./judge_prompt.yaml
    model: nim/meta-llama/llama-3.1-70b-instruct
    response_format: json
  metrics:
    - name: accuracy
      type: numeric
      range: [1, 5]
    - name: completeness
      type: numeric
      range: [1, 5]
    - name: clarity
      type: numeric
      range: [1, 5]
  aggregation: mean

target:
  model: <model-to-evaluate>
  endpoint: <nim-endpoint-url>
```

### Step 5: Run the evaluation

Provide instructions to execute:

```bash
# Install NeMo Evaluator if needed
pip install nemo-evaluator

# Run the custom benchmark
nemo-evaluator run --config eval_config.yaml --output results/
```

### Step 6: Analyze results

Parse the output results and present a summary table with per-metric scores, distribution analysis, and flagged low-scoring examples for review.

## Key files to generate

| File | Purpose |
|------|--------|
| `eval_dataset.jsonl` | Evaluation examples with inputs and optional references |
| `judge_prompt.yaml` | Template instructing the judge model how to score |
| `eval_config.yaml` | NeMo Evaluator configuration tying everything together |
| `results/` | Output directory for evaluation results |

## Tips

- Start with 50-100 evaluation examples for quick iteration, scale to 500+ for production benchmarks
- Use diverse examples that cover edge cases and failure modes
- Calibrate judge prompts by running on examples with known scores first
- Include chain-of-thought reasoning in judge prompts for more reliable scoring
- Use multiple evaluation criteria rather than a single overall score

## References

- Source: [NVIDIA/skills - NeMo-Evaluator/byob](https://github.com/NVIDIA/skills/tree/main/skills/NeMo-Evaluator/byob)
- [NVIDIA NeMo Evaluator Documentation](https://docs.nvidia.com/nemo/evaluator/)
- [VoltAgent Awesome Agent Skills](https://github.com/VoltAgent/awesome-agent-skills)
