# Technical Details: SR-MoA

## What It Does

SR-MoA (Self-Reflective Mixture of Adapters) adds test-time neuroplasticity to frozen LLMs. Rather than serving a single fine-tuned model or naively switching between adapters, it maintains a pool of LoRA adapters and a learned router that dynamically composes them per input. The "self-reflective" part is a multi-step feedback loop: the router proposes adapter weights, observes the intermediate output, and refines its routing decision — all within a single forward pass, without gradient updates to the base model.

This is distinct from standard MoE (Mixture of Experts) because: (1) the experts are parameter-efficient adapters on a frozen backbone, (2) routing is refined iteratively via self-reflection rather than being a single feedforward decision, and (3) optionally, adapter weights can be updated at test time using a self-supervised signal.

## Architecture

```
Input tokens
    |
    v
[Frozen Base LLM] ─── hidden states ───> [Self-Reflective Router]
    |                                           |
    |                                    adapter weights w_i
    |                                           |
    v                                           v
[LoRA Adapter 1] ──┐                    Weighted composition
[LoRA Adapter 2] ──┼── outputs ──────> sum(w_i * adapter_i(x))
[LoRA Adapter 3] ──┤                           |
[LoRA Adapter 4] ──┘                           |
    |                                           |
    v                                           v
    └──── base_output + composed_delta ────> [Reflection Check]
                                                |
                                         (loop N times)
                                                |
                                                v
                                          Final output
```

### Key Files (in narelabs/sr-moa repo)

- `sr_moa/config.py` — `SRMoAConfig` dataclass with all hyperparameters
- `sr_moa/model.py` — `SRMoAModel` wrapper that injects adapters into a frozen model
- `sr_moa/router.py` — Self-reflective router (MLP + attention over adapter outputs)
- `sr_moa/adapters.py` — LoRA adapter pool management (init, merge, save/load)
- `sr_moa/trainer.py` — Training loop with separate LRs for router vs adapters
- `sr_moa/reflection.py` — The iterative refinement loop logic

### Data Flow

1. Input tokenized and passed through frozen base model to get hidden states
2. Router MLP takes hidden states, produces initial adapter scores (softmax)
3. Each LoRA adapter produces its delta independently
4. Deltas are weighted-summed using router scores
5. **Reflection loop**: composed output is fed back to router for re-scoring
6. After N reflection steps, final composed output is added to base output
7. (Optional) Test-time training: gradient on self-supervised loss updates adapter params

### Dependencies

- PyTorch >= 2.0
- Hugging Face Transformers >= 4.35
- PEFT >= 0.7 (for LoRA primitives)
- NumPy (router computations)

## Limitations

- **Inference latency**: each reflection step adds ~15-30% overhead per step. With 3 steps, expect ~1.5-2x baseline latency.
- **No published benchmarks yet**: the repo is early-stage; claims of improvement are directional, not peer-reviewed.
- **Adapter training required**: you need task-diverse training data to specialize adapters. Without it, the router has nothing meaningful to compose.
- **Memory**: N adapters means N x LoRA parameter sets in GPU memory simultaneously (though each is small at rank 16).
- **Router collapse**: if training data isn't diverse enough, the router may collapse to always selecting one adapter, negating the mixture benefit.

## What It Does NOT Do

- Does not modify the frozen base model weights
- Does not provide pre-trained adapters (you train your own)
- Does not handle multi-modal inputs (text-only)
- Does not replace RAG or tool-use — it's about adapter composition, not knowledge retrieval

## Relevance to Claude-Driven Products

| Use Case | Why SR-MoA Matters |
|----------|-------------------|
| **Agent Factories** | Route different agent personas through specialized adapters without separate model deployments |
| **Ad Creatives / Marketing** | Adapters for tone (formal/casual), format (headline/body/CTA), and domain (finance/health/tech) composed on the fly |
| **Voice AI** | Low-latency adapter switching for dialect/style adaptation without model reloads |
| **Lead-gen** | Personalize response style per lead segment using router scores as interpretable signals |

The key insight: if you're running a frozen LLM behind multiple product surfaces, SR-MoA lets you share one base model while dynamically specializing per-request — reducing infrastructure cost while improving task-specific quality.
