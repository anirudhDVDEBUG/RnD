---
name: SR-MoA Adapter
description: |
  Implement Self-Reflective Mixture of Adapters (SR-MoA) for frozen LLMs in PyTorch.
  TRIGGER: user wants test-time adaptation, mixture of LoRA adapters, self-reflective routing, or autonomous neuroplasticity for frozen language models.
---

# SR-MoA Adapter Skill

Build and integrate Self-Reflective Mixture of Adapters (SR-MoA) — a framework that enables autonomous test-time neuroplasticity for frozen LLMs by dynamically routing through and composing multiple LoRA adapters with self-reflective feedback.

## When to use

- "Add test-time adaptation to a frozen LLM using mixture of adapters"
- "Implement self-reflective routing across multiple LoRA adapters"
- "Build an SR-MoA pipeline that dynamically composes adapters at inference"
- "Set up autonomous neuroplasticity for a frozen language model in PyTorch"
- "Create a mixture-of-experts LoRA system with self-reflection"

## How to use

### 1. Install dependencies

```bash
pip install torch transformers peft sr-moa
```

Or install from source:

```bash
git clone https://github.com/narelabs/sr-moa.git
cd sr-moa
pip install -e .
```

### 2. Core architecture

SR-MoA has three key components:

- **Adapter Pool**: A collection of LoRA adapters, each specialized for different capabilities (reasoning, code, creativity, etc.)
- **Self-Reflective Router**: A lightweight module that scores adapter relevance per input and dynamically composes adapter outputs
- **Test-Time Training Loop**: An autonomous feedback loop that updates adapter weights and routing at inference time without modifying the frozen base model

### 3. Basic implementation

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sr_moa import SRMoAConfig, SRMoAModel

# Load frozen base model
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B")

# Configure SR-MoA
config = SRMoAConfig(
    num_adapters=4,           # Number of LoRA adapters in the pool
    lora_rank=16,             # LoRA rank for each adapter
    lora_alpha=32,            # LoRA alpha scaling
    reflection_steps=3,       # Self-reflection iterations at test time
    router_hidden_dim=256,    # Router network hidden dimension
    target_modules=["q_proj", "v_proj"],  # Modules to adapt
)

# Wrap model with SR-MoA
model = SRMoAModel(base_model, config)
```

### 4. Test-time adaptation

```python
# The model autonomously adapts at inference
inputs = tokenizer("Explain quantum entanglement", return_tensors="pt")

# Forward pass triggers self-reflective routing and optional test-time updates
with model.test_time_adapt():
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        reflection_enabled=True,  # Enable self-reflective feedback loop
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### 5. Training adapters

```python
from sr_moa import SRMoATrainer

trainer = SRMoATrainer(
    model=model,
    train_dataset=dataset,
    tokenizer=tokenizer,
    training_args={
        "num_epochs": 3,
        "learning_rate": 1e-4,
        "router_lr": 5e-4,       # Separate LR for router
        "adapter_specialization": True,  # Encourage adapter diversity
    },
)

trainer.train()
model.save_adapters("./sr_moa_adapters")
```

### 6. Key design patterns

- **Freeze the base model** — only adapter parameters and the router are trainable
- **Use diverse training data per adapter** to encourage specialization
- **Set reflection_steps based on latency budget** — more steps improve quality but increase inference time
- **Monitor router entropy** — low entropy means the router is specializing; very low may indicate collapse to a single adapter
- **Adapter merging**: after training, highly correlated adapters can be merged to reduce overhead

### 7. Configuration reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_adapters` | 4 | Number of LoRA adapters in pool |
| `lora_rank` | 16 | Rank of each LoRA adapter |
| `lora_alpha` | 32 | LoRA scaling factor |
| `reflection_steps` | 3 | Self-reflection iterations |
| `router_hidden_dim` | 256 | Router MLP hidden size |
| `target_modules` | `["q_proj", "v_proj"]` | Transformer modules to adapt |
| `router_type` | `"self_reflective"` | Router architecture (`self_reflective`, `top_k`, `soft`) |
| `top_k` | 2 | Adapters selected per token (for top_k router) |

## References

- **Source repository**: [narelabs/sr-moa](https://github.com/narelabs/sr-moa) — Self-Reflective Mixture of Adapters (SR-MoA): Autonomous Test-Time Neuroplasticity for Frozen LLMs in PyTorch
- **Key concepts**: LoRA adapters, mixture-of-experts routing, test-time training, self-reflective feedback
- **Built with**: PyTorch, Hugging Face Transformers, PEFT
