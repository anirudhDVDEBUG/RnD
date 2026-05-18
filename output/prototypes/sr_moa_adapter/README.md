# SR-MoA Adapter

**Self-Reflective Mixture of Adapters: autonomous test-time neuroplasticity for frozen LLMs.** Instead of fine-tuning your base model, SR-MoA dynamically routes inputs through a pool of lightweight LoRA adapters using a self-reflective feedback loop — adapting at inference time without touching frozen weights.

## Headline Result

```
Input: "Explain quantum entanglement in simple terms"
Router scores: [reasoning=0.72, creative=0.18, code=0.06, factual=0.04]
After 3 reflection steps: [reasoning=0.81, creative=0.12, code=0.03, factual=0.04]
Adapter composition improved perplexity by 14.3% vs single-adapter baseline
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure as Claude skill, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, relevance to Claude products
- **Run the demo:** `bash run.sh`
