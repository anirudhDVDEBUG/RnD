---
name: vllm_v0_to_v1_rl_migration
description: |
  Migrate vLLM from V0 to V1 for reinforcement learning workloads, ensuring logprob correctness and train-inference parity.
  TRIGGER: vLLM migration, vLLM V1 RL, logprob mismatch, reinforcement learning inference engine, policy ratio divergence
---

# vLLM V0 to V1: Correctness Before Corrections in RL

Guide for migrating vLLM from V0 (0.8.x) to V1 (0.18.x+) in reinforcement learning pipelines, focusing on eliminating train-inference mismatch in logprob computation.

## When to use

- "Migrate vLLM from V0 to V1 for RL training"
- "Fix logprob mismatch between vLLM inference and trainer"
- "Policy ratio is diverging after vLLM upgrade"
- "Configure vLLM V1 for reinforcement learning rollouts"
- "KL divergence or clip rate spiking after vLLM version change"

## How to use

### Step 1: Enable processed logprobs mode

vLLM V1 returns raw logprobs (before temperature/penalties/filtering) by default. For RL you need processed logprobs:

```yaml
vllm_config:
  use_v1: true
  vllm_kwargs:
    logprobs-mode: processed_logprobs
```

### Step 2: Disable prefix caching and async scheduling

V1 defaults differ from V0. Disable features that break RL assumptions:

```yaml
vllm_config:
  use_v1: true
  vllm_kwargs:
    logprobs-mode: processed_logprobs
    enable-prefix-caching: false   # Prevents stale cache after weight updates
    async-scheduling: false         # Matches V0 synchronous behavior
```

- **Prefix caching off**: Prevents cache hits from reusing state computed before weight updates.
- **Async scheduling off**: Ensures deterministic request ordering matching V0.

### Step 3: Handle inflight weight updates correctly

Match V0's weight synchronization semantics:

```python
await engine.pause_generation(mode="keep", clear_cache=False)
await engine_client.collective_rpc_async(
    "receive_weight_update",
    args=(request.model_dump_json(),),
)
await engine.resume_generation()
```

- `mode="keep"`: Preserves inflight generation requests
- `clear_cache=False`: Maintains cached state through weight updates

### Step 4: Use fp32 for lm_head projection

Compute the final logit projection in fp32 to match trainer-side precision. Small logit differences become visible in RL through:
- Policy ratio calculations
- KL divergence metrics
- Clipping behavior

This is recognized as best practice in ScaleRL and MiniMax-M1 papers.

### Step 5: Validate with diagnostic metrics

Before making objective-side changes, confirm backend parity using:
- **Clip rate**: Should match V0 baseline
- **Policy ratio deviation**: Mean should stay around 1.0
- **Effective lag**: Weight sync steps behind
- **KL divergence and entropy**: Should track V0 reference

### Key Methodology

Always separate two problems:
1. **Backend correctness** (inference parity) — fix this FIRST
2. **Objective-side corrections** (off-policy/async adjustments) — only after parity is confirmed

Objective corrections can mask inference bugs if applied prematurely.

## References

- [vLLM V0 to V1: Correctness Before Corrections in RL (HuggingFace Blog)](https://huggingface.co/blog/ServiceNow-AI/correctness-before-corrections)
- [ScaleRL paper (arXiv:2510.13786)](https://arxiv.org/abs/2510.13786)
- [MiniMax-M1 paper (arXiv:2506.13585)](https://arxiv.org/abs/2506.13585)
