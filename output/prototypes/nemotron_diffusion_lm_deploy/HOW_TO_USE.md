# How to Use — Nemotron-Labs Diffusion LM Deploy

## Install (Real Deployment)

```bash
# SGLang with diffusion support (requires CUDA GPU)
pip install sglang[all]

# For querying the server
pip install openai
```

Minimum hardware: 1x NVIDIA GPU with 24 GB+ VRAM (3B model) or 80 GB+ (14B model).

## Install (This Demo — No GPU Needed)

```bash
git clone <this-repo>
cd nemotron_diffusion_lm_deploy
pip install -r requirements.txt   # stdlib only
bash run.sh
```

## Claude Skill Setup

Drop the skill file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/nemotron_diffusion_lm_deploy
cp SKILL.md ~/.claude/skills/nemotron_diffusion_lm_deploy/SKILL.md
```

**Trigger phrases** that activate the skill:

- "Set up Nemotron diffusion model for fast text generation"
- "Deploy a diffusion language model with SGLang"
- "Use parallel token generation instead of autoregressive decoding"
- "Configure self-speculation mode for Nemotron 8B"
- "Compare diffusion vs autoregressive inference speed"

## Deploy with SGLang (Production)

Pick a model and a mode:

```bash
# Autoregressive mode (baseline, drop-in compatible)
python -m sglang.launch_server \
    --model nvidia/Nemotron-Labs-Diffusion-8B-Instruct \
    --ar-mode true

# Diffusion mode (~2.6x faster)
python -m sglang.launch_server \
    --model nvidia/Nemotron-Labs-Diffusion-8B-Instruct \
    --ar-mode false

# Self-Speculation mode (~4-6x faster)
python -m sglang.launch_server \
    --model nvidia/Nemotron-Labs-Diffusion-8B-Instruct \
    --ar-mode false \
    --speculation-mode linear
```

The server exposes an **OpenAI-compatible API** on `http://localhost:30000`.

## Query the Model

```python
import openai

client = openai.Client(base_url="http://localhost:30000/v1", api_key="none")

response = client.chat.completions.create(
    model="nvidia/Nemotron-Labs-Diffusion-8B-Instruct",
    messages=[{"role": "user", "content": "Explain diffusion language models."}],
    max_tokens=512,
)
print(response.choices[0].message.content)
```

Or via curl:

```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "nvidia/Nemotron-Labs-Diffusion-8B-Instruct",
       "messages": [{"role": "user", "content": "Hello!"}],
       "max_tokens": 512}'
```

## First 60 Seconds

**Input:**

```bash
bash run.sh
```

**Output** (truncated):

```
  NEMOTRON-LABS DIFFUSION LANGUAGE MODEL — DEPLOYMENT DEMO

  Nemotron-Labs Diffusion Model Catalog
  ──────────────────────────────────────
  nvidia/Nemotron-Labs-Diffusion-3B-Base           3B base
  nvidia/Nemotron-Labs-Diffusion-8B-Instruct       8B instruct
  ...

  SGLang Server Launch Commands
  ─────────────────────────────
  # Autoregressive mode
  python -m sglang.launch_server --model nvidia/... --ar-mode true
  ...

  PROMPT: Explain diffusion language models.
  RESPONSE (68 tokens):
    Diffusion language models generate text by iteratively refining ...

  Mode                           Tok/s  Fwd Passes   Tok/Pass  Speedup
  ──────────────────────────     ─────  ──────────   ────────  ───────
  Autoregressive                   250          68        1.0     1.0x
  Diffusion (block=32)             648          12        5.7     2.6x
  Self-Speculation (Linear)       1156           6       11.3     4.6x

  SUMMARY: Expected Real-World Performance (B200 GPU)
  ───────────────────────────────────────────────────
  Self-Speculation (Linear)     ~865 tok/s       4.0x
```

## Available Models

| Model | Params | Type |
|-------|--------|------|
| `nvidia/Nemotron-Labs-Diffusion-3B-Base` | 3B | Base |
| `nvidia/Nemotron-Labs-Diffusion-3B-Instruct` | 3B | Instruct |
| `nvidia/Nemotron-Labs-Diffusion-8B-Base` | 8B | Base |
| `nvidia/Nemotron-Labs-Diffusion-8B-Instruct` | 8B | Instruct |
| `nvidia/Nemotron-Labs-Diffusion-14B-Base` | 14B | Base |
| `nvidia/Nemotron-Labs-Diffusion-14B-Instruct` | 14B | Instruct |
| `nvidia/Nemotron-Labs-Diffusion-8B-VLM` | 8B | Vision |
