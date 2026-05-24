# Nemotron-Labs Diffusion LM Deploy

**TL;DR:** NVIDIA's Nemotron-Labs Diffusion Language Models generate multiple tokens in parallel via iterative masked diffusion, achieving up to **4x real-world throughput** (865 tok/s on B200) versus autoregressive baselines — with equal or better accuracy. This repo demos all three generation modes and provides copy-paste deployment commands.

## Headline Result

> Self-Speculation mode on a single B200 GPU: **865 tokens/second** — 4x faster than autoregressive, while scoring +1.2% higher than Qwen3 8B on average benchmarks.

## Quick Start

```bash
bash run.sh
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, deploy with SGLang, query the API, skill setup
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — How masked diffusion + self-speculation works, architecture, limitations

## Source

- [Blog post](https://huggingface.co/blog/nvidia/nemotron-labs-diffusion)
- [Model collection](https://huggingface.co/collections/nvidia/nemotron-labs-diffusion)
