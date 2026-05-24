---
name: nemotron_diffusion_lm_deploy
description: |
  Deploy and use NVIDIA Nemotron-Labs Diffusion Language Models for fast parallel text generation.
  Triggers: nemotron diffusion, diffusion language model, parallel token generation, masked diffusion LM, nemotron labs fast inference
---

# Nemotron-Labs Diffusion Language Model Deployment

Deploy and configure NVIDIA Nemotron-Labs Diffusion Language Models (DLMs) that generate multiple tokens in parallel via iterative refinement — up to 6× faster than autoregressive baselines.

## When to use

- "Set up Nemotron diffusion model for fast text generation"
- "Deploy a diffusion language model with SGLang"
- "Use parallel token generation instead of autoregressive decoding"
- "Configure self-speculation mode for Nemotron 8B"
- "Compare diffusion vs autoregressive inference speed"

## How to use

### 1. Choose a model

Nemotron-Labs Diffusion models are available in 3B, 8B, and 14B sizes (base + instruct) on HuggingFace under the `nvidia` org:

```
nvidia/Nemotron-Labs-Diffusion-3B-Base
nvidia/Nemotron-Labs-Diffusion-3B-Instruct
nvidia/Nemotron-Labs-Diffusion-8B-Base
nvidia/Nemotron-Labs-Diffusion-8B-Instruct
nvidia/Nemotron-Labs-Diffusion-14B-Base
nvidia/Nemotron-Labs-Diffusion-14B-Instruct
nvidia/Nemotron-Labs-Diffusion-8B-VLM  # Vision-language variant
```

Find all models at: https://huggingface.co/collections/nvidia/nemotron-labs-diffusion

### 2. Select an inference mode

Each checkpoint supports three generation modes:

| Mode | Description | Speed | Use case |
|------|-------------|-------|----------|
| **Autoregressive** | Standard left-to-right, one token at a time | 1× baseline | Drop-in compatibility |
| **Diffusion** | 32-token block iterative denoising | ~2.6× faster | GPU-efficient parallel generation |
| **Self-Speculation (Linear)** | Bidirectional diffusion draft + causal verification | ~6× faster | Maximum throughput |

### 3. Deploy with SGLang

SGLang is the recommended serving framework:

```bash
# Install SGLang with diffusion support
pip install sglang[all]

# Launch server — Autoregressive mode (baseline)
python -m sglang.launch_server \
  --model nvidia/Nemotron-Labs-Diffusion-8B-Instruct \
  --ar-mode true

# Launch server — Diffusion mode (parallel generation)
python -m sglang.launch_server \
  --model nvidia/Nemotron-Labs-Diffusion-8B-Instruct \
  --ar-mode false

# Launch server — Self-Speculation mode (fastest)
python -m sglang.launch_server \
  --model nvidia/Nemotron-Labs-Diffusion-8B-Instruct \
  --ar-mode false \
  --speculation-mode linear
```

### 4. Query the model

Once the server is running, query via the OpenAI-compatible API:

```python
import openai

client = openai.Client(base_url="http://localhost:30000/v1", api_key="none")

response = client.chat.completions.create(
    model="nvidia/Nemotron-Labs-Diffusion-8B-Instruct",
    messages=[{"role": "user", "content": "Explain diffusion language models."}],
    max_tokens=512
)
print(response.choices[0].message.content)
```

### 5. Performance expectations

- **Diffusion mode**: ~2.6× tokens-per-forward-pass vs autoregressive
- **Linear self-speculation**: ~6× tokens-per-forward-pass vs autoregressive
- **Real-world throughput on B200 GPU**: ~865 tok/s (4× AR baseline)
- Accuracy on par or slightly better than comparable AR models (e.g., +1.2% avg vs Qwen3 8B)

### Key advantages over autoregressive models

- **Parallel token generation** — better GPU compute utilization
- **Token revision** — can refine previously generated tokens
- **Flexible compute budget** — reduce refinement steps to trade accuracy for speed
- **Fill-in-the-middle** — native support for infilling tasks
- **Drop-in compatible** — same checkpoint works in AR mode for existing workflows

### Training / fine-tuning

Training recipes are available via NVIDIA Megatron Bridge:

```bash
git clone https://github.com/NVIDIA-NeMo/Megatron-Bridge.git
cd Megatron-Bridge/examples/diffusion/recipes/nemotron_labs_diffusion
```

## References

- Blog post: https://huggingface.co/blog/nvidia/nemotron-labs-diffusion
- Models: https://huggingface.co/collections/nvidia/nemotron-labs-diffusion
- Technical report: http://bit.ly/Nemotron-Labs-Diffusion-Report
- Training code: https://github.com/NVIDIA-NeMo/Megatron-Bridge/
