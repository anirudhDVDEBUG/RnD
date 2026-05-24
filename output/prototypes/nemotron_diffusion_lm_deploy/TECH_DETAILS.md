# Technical Details — Nemotron-Labs Diffusion Language Models

## What It Does

Nemotron-Labs Diffusion Language Models (DLMs) replace the standard autoregressive (AR) "one token at a time" generation with **masked diffusion**: the model starts with a fully masked sequence and iteratively denoises it, predicting multiple tokens per forward pass. A single checkpoint supports three generation modes — AR, diffusion, and self-speculation — switchable at serving time via SGLang flags.

The self-speculation mode pairs a **bidirectional diffusion draft** (fast, parallel, lower confidence) with a **causal verification pass** (sequential, high accuracy). This draft-then-verify loop generates 32-token blocks, achieving ~4x throughput on B200 GPUs while matching or exceeding the accuracy of comparable AR models.

## Architecture

### Key Components

- **Backbone:** Transformer decoder with both causal and bidirectional attention masks, trained jointly on AR and diffusion objectives.
- **Diffusion head:** Predicts all masked positions in parallel. Uses a noise schedule to gradually reduce masking over refinement steps.
- **Self-speculation pipeline:** Bidirectional forward pass drafts a 32-token block; causal forward pass verifies and corrects. Only accepted tokens advance.
- **Serving:** SGLang runtime handles KV-cache, batching, and mode selection. OpenAI-compatible REST API.

### Data Flow

```
User prompt
    |
    v
SGLang Server (mode flag: ar / diffusion / self-speculation)
    |
    +--> AR mode:          standard left-to-right decode
    +--> Diffusion mode:   [MASK]*32 -> refine x N -> next block
    +--> Self-spec mode:   diffusion draft -> causal verify -> accept/reject
    |
    v
OpenAI-compatible JSON response
```

### Key Files (this demo)

| File | Purpose |
|------|---------|
| `nemotron_dlm_demo.py` | Simulates all three modes, prints benchmark comparison |
| `run.sh` | One-command entry point |
| `requirements.txt` | Dependencies (stdlib only for demo) |

### Dependencies (production)

- **SGLang** — inference server with native DLM support
- **PyTorch + CUDA** — GPU compute
- **OpenAI SDK** — client-side querying
- **Megatron-Bridge** — training/fine-tuning recipes (optional)

## Limitations

- **GPU required for real inference.** The demo simulates timing; actual throughput depends on GPU (B200 benchmarks cited).
- **SGLang-only serving.** No vLLM or TGI support yet — SGLang is the only framework with diffusion mode.
- **Fixed block size of 32.** Not configurable in current SGLang release.
- **No streaming in diffusion mode.** Tokens are generated in 32-token blocks, so streaming is block-granular, not token-granular.
- **Fill-in-the-middle** works in diffusion mode but is not exposed through the OpenAI-compatible API yet.
- **Vision model (VLM)** supports image input but only in AR mode currently.
- **Fine-tuning** requires Megatron-Bridge and multi-GPU setup; no LoRA/QLoRA adapters available yet.

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent factories** | DLMs can serve as fast local inference backends for tool-calling agents where latency matters more than frontier accuracy. A Claude orchestrator dispatches subtasks to a local Nemotron DLM for 4x faster tool-output generation. |
| **Ad creatives / marketing** | Bulk-generating ad copy variants benefits directly from higher throughput. Run 4x more variants per GPU-hour. |
| **Lead-gen pipelines** | Faster inference = lower per-lead cost when generating personalized outreach at scale. |
| **Voice AI** | Block-granular generation (32 tokens at a time) is a natural fit for voice synthesis pipelines that consume text in chunks. Lower time-to-first-chunk. |
| **Hybrid architectures** | Same checkpoint works in AR mode for exact compatibility and diffusion mode for speed — no model duplication needed. |

## References

- Blog: https://huggingface.co/blog/nvidia/nemotron-labs-diffusion
- Models: https://huggingface.co/collections/nvidia/nemotron-labs-diffusion
- Technical report: http://bit.ly/Nemotron-Labs-Diffusion-Report
- Training code: https://github.com/NVIDIA-NeMo/Megatron-Bridge/
