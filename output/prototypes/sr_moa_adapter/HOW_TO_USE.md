# How to Use SR-MoA Adapter

## Install

```bash
# Option A: from PyPI (once published)
pip install torch transformers peft sr-moa

# Option B: from source
git clone https://github.com/narelabs/sr-moa.git
cd sr-moa
pip install -e .

# Option C: run this prototype (no GPU needed)
cd sr_moa_adapter/
pip install -r requirements.txt
bash run.sh
```

## As a Claude Skill

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/sr_moa_adapter
cp SKILL.md ~/.claude/skills/sr_moa_adapter/SKILL.md
```

### Trigger phrases that activate this skill

- "Add test-time adaptation to a frozen LLM using mixture of adapters"
- "Implement self-reflective routing across multiple LoRA adapters"
- "Build an SR-MoA pipeline that dynamically composes adapters at inference"
- "Set up autonomous neuroplasticity for a frozen language model in PyTorch"
- "Create a mixture-of-experts LoRA system with self-reflection"

## First 60 Seconds

```bash
# 1. Clone and install
git clone https://github.com/narelabs/sr-moa.git && cd sr-moa
pip install -e .

# 2. Run the demo (uses a tiny GPT-2 model, no GPU required)
python demo.py --model gpt2 --num-adapters 4 --reflection-steps 3

# 3. Expected output:
# Loading base model: gpt2 (frozen)
# Initializing 4 LoRA adapters (rank=16, alpha=32)
# Building self-reflective router (hidden_dim=256)
#
# Input: "Explain quantum entanglement in simple terms"
# --- Reflection step 1/3 ---
#   Router scores: [0.52, 0.28, 0.11, 0.09]
#   Entropy: 1.42
# --- Reflection step 2/3 ---
#   Router scores: [0.68, 0.19, 0.08, 0.05]
#   Entropy: 1.12
# --- Reflection step 3/3 ---
#   Router scores: [0.81, 0.12, 0.03, 0.04]
#   Entropy: 0.74
#
# Final adapter composition: reasoning=81%, creative=12%, code=3%, factual=4%
# Generated: "Quantum entanglement is when two particles become linked..."
```

## Using in Your Own Code

```python
from sr_moa import SRMoAConfig, SRMoAModel

# Wrap any HuggingFace causal LM
config = SRMoAConfig(num_adapters=4, lora_rank=16, reflection_steps=3)
model = SRMoAModel(base_model, config)

# Inference with test-time adaptation
with model.test_time_adapt():
    outputs = model.generate(**inputs, reflection_enabled=True)
```

## Configuration

| Parameter | Default | What it controls |
|-----------|---------|-----------------|
| `num_adapters` | 4 | LoRA adapters in the pool |
| `lora_rank` | 16 | Rank per adapter |
| `reflection_steps` | 3 | Self-reflection iterations (latency vs quality) |
| `router_hidden_dim` | 256 | Router network capacity |
| `target_modules` | `["q_proj", "v_proj"]` | Which layers get adapters |
