# Cosmos Predict 2.5 LoRA/DoRA for Robot Video Generation

**TL;DR:** Fine-tune NVIDIA's Cosmos Predict 2.5 world foundation model with LoRA adapters to generate realistic robot manipulation videos from a single image + text prompt. Only ~2.5% of parameters are trained, yet instruction-following scores jump from ~2.0 to ~4.0 on a 5-point scale.

## Headline Result

> LoRA r=32 fine-tuning on just 92 robot videos enables Cosmos to correctly follow manipulation instructions (e.g., "use the left hand to pick up the cucumber") while preserving the geometric and physical priors of the 2B-parameter base model. Training takes ~2.5 hours on 8x H100 GPUs.

## Quick Start

```bash
bash run.sh   # runs full pipeline demo (no GPU needed)
```

## Documentation

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install steps, dataset prep, training commands, inference code
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, rectified flow loss, evaluation metrics, limitations

## Source

- [HuggingFace Blog: Fine-Tuning NVIDIA Cosmos Predict 2.5](https://huggingface.co/blog/nvidia/cosmos-fine-tuning-for-robot-video-generation)
- [Training code (Diffusers)](https://github.com/terarachang/diffusers/tree/cosmos_predict_2.5_lora_clean/examples/cosmos)
- [Model: nvidia/Cosmos-Predict2.5-2B](https://huggingface.co/nvidia/Cosmos-Predict2.5-2B)
