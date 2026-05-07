# How to Use

## Install

```bash
# No external dependencies needed -- pure Python stdlib
git clone <this-repo>
cd vllm_v0_to_v1_rl_migration
python3 demo.py
```

Or just:

```bash
bash run.sh
```

## As a Claude Code Skill

This is a **Claude Skill**. To install:

1. Copy the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/vllm_v0_to_v1_rl_migration
cp SKILL.md ~/.claude/skills/vllm_v0_to_v1_rl_migration/SKILL.md
```

2. **Trigger phrases** that activate this skill:

   - "Migrate vLLM from V0 to V1 for RL training"
   - "Fix logprob mismatch between vLLM inference and trainer"
   - "Policy ratio is diverging after vLLM upgrade"
   - "Configure vLLM V1 for reinforcement learning rollouts"
   - "KL divergence or clip rate spiking after vLLM version change"
   - Any mention of "vLLM V1 RL" or "logprob mismatch"

3. Claude will then guide you through the 5-step migration checklist (logprobs mode, prefix caching, async scheduling, fp32 lm_head, diagnostic validation).

## Using the Validator Programmatically

```python
from vllm_v1_migration import VLLMConfig, validate_config, run_full_validation

# Check your existing config
my_config = {
    "vllm_config": {
        "use_v1": True,
        "vllm_kwargs": {
            "logprobs-mode": "raw",
            "enable-prefix-caching": True,
            "async-scheduling": True,
        }
    },
    "model_config": {"fp32_lm_head": False}
}

result = run_full_validation(my_config)
for issue in result["issues"]:
    print(f"[{issue.severity}] {issue.component}: {issue.message}")

# Generate correct config
correct = VLLMConfig()  # defaults are RL-safe
print(correct.to_yaml_str())
```

## First 60 Seconds

**Input:** Run `bash run.sh`

**Output:** Two scenarios side-by-side:

1. **Naive V1 migration** -- shows 4 issues detected (critical: raw logprobs, prefix caching; warning: async scheduling, fp16 lm_head), with simulated metrics showing clip rate at 0.20, policy ratio diverged to 1.12.

2. **Correct V1 migration** -- shows 0 issues, clip rate at 0.02, policy ratio at 1.00. Plus the generated YAML config and the correct weight update code pattern.

The comparison table at the end makes it immediately clear which settings matter and why.
