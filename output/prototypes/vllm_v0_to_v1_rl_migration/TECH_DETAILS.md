# Technical Details

## What This Does

This prototype encodes the findings from ServiceNow AI's blog post on migrating vLLM from V0 (0.8.x) to V1 (0.18.x+) for reinforcement learning workloads. The core problem: vLLM V1 changed several defaults that silently break RL training by introducing train-inference mismatch in logprob computation.

The tool provides a config validator that checks for the 5 critical settings, a metric simulator that shows the quantitative impact of each misconfiguration, and generates the correct YAML config and weight-update code. It separates "backend correctness" (getting inference to match the trainer) from "objective-side corrections" (off-policy/async adjustments) -- the key methodology from the source post.

## Architecture

```
vllm_v1_migration.py    Core module
  VLLMConfig            Dataclass with RL-safe defaults, exports to dict/YAML
  validate_config()     Runs 5 checks against a config dict, returns issues
  simulate_logprob_mismatch()  Models metric impact of config choices
  run_full_validation() Combined check + simulation
  generate_weight_update_snippet()  Correct V1 pause/update/resume pattern

demo.py                 End-to-end demo comparing naive vs correct migration
run.sh                  Entry point
```

**Data flow:** Config dict -> 5 independent checks -> list of `MigrationIssue` objects + simulated `DiagnosticMetrics`. No external calls, no GPU, no vLLM installation required.

**Dependencies:** Python 3.8+ stdlib only (`dataclasses`, `json`, `math`, `random`).

## The 5 Critical V0-to-V1 Differences

| Setting | V1 Default | RL-Safe Value | Why It Matters |
|---------|-----------|---------------|----------------|
| `logprobs-mode` | `raw` | `processed_logprobs` | V1 returns pre-temperature logprobs; RL needs post-processing values for accurate policy ratios |
| `enable-prefix-caching` | `true` | `false` | Cached KV states become stale after weight updates, producing wrong logprobs |
| `async-scheduling` | `true` | `false` | Changes request ordering vs V0, breaks deterministic replay |
| `fp32_lm_head` | not set | `true` | fp16 logit projection introduces precision errors visible in policy ratio and KL |
| Weight update API | N/A | `pause_generation(mode="keep")` | V1 requires explicit pause/resume around weight sync |

## Limitations

- **Simulation only**: Metrics are modeled, not measured from real vLLM. The relative magnitudes match the blog's reported findings but exact values will vary with model/data.
- **Config validation only**: Does not patch vLLM, modify training code, or connect to a running engine.
- **No version detection**: Does not auto-detect your vLLM version or read existing config files from disk.
- **Focused scope**: Only covers the 5 settings from the blog post. Other V1 changes (new attention backends, speculative decoding) are not checked.

## Why This Matters for Claude-Driven Products

For teams building **agent factories** or **AI-powered services** that use RL-finetuned models:

- **Inference engine upgrades are invisible failure modes.** If you upgrade vLLM for performance gains but break logprob parity, your RL training loop degrades silently. Policy ratio divergence means your model stops learning from its own generations effectively.
- **The "correctness before corrections" principle applies broadly.** When building production ML pipelines with Claude or other LLMs, always validate infrastructure parity before tuning hyperparameters or adding compensations. This is the same principle as fixing data quality before tuning model architecture.
- **Config validation as a skill pattern.** This prototype demonstrates encoding domain expertise (RL + inference engine internals) as a reusable Claude skill -- the kind of specialized knowledge that accelerates engineering teams.

## References

- [vLLM V0 to V1: Correctness Before Corrections in RL](https://huggingface.co/blog/ServiceNow-AI/correctness-before-corrections) -- ServiceNow AI
- [ScaleRL (arXiv:2510.13786)](https://arxiv.org/abs/2510.13786) -- fp32 lm_head recommendation
- [MiniMax-M1 (arXiv:2506.13585)](https://arxiv.org/abs/2506.13585) -- precision best practices
