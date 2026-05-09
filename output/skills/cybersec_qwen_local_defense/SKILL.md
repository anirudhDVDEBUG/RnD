---
name: cybersec_qwen_local_defense
description: |
  Deploy and use CyberSecQwen-4B, a specialized 4B-parameter defensive cybersecurity model for CWE classification, CVE-to-CWE mapping, and security analyst Q&A. Runs locally on consumer hardware (12 GB VRAM).
  Triggers: local cybersecurity model, CWE classification, CVE triage, defensive security LLM, CyberSecQwen
---

# CyberSecQwen-4B: Local Defensive Cybersecurity Model

Deploy and query a specialized 4B-parameter model fine-tuned for defensive cybersecurity tasks — CWE classification, CVE-to-CWE mapping, and defensive analyst Q&A — entirely locally without sending sensitive data off-premises.

## When to use

- "Classify this vulnerability description to a CWE category locally"
- "Set up a local model for CVE triage and CWE mapping"
- "I need a defensive cybersecurity LLM that runs on consumer hardware"
- "Help me deploy CyberSecQwen-4B for air-gapped security analysis"
- "Map CVE descriptions to CWE IDs without using cloud APIs"

## How to use

### Step 1 — Install dependencies

```bash
pip install torch transformers accelerate
# Optional for high-throughput serving:
pip install vllm
```

### Step 2 — Load the model for inference

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "lablab-ai-amd-developer-hackathon/CyberSecQwen-4B"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
```

**Minimum hardware:** 12 GB VRAM (consumer GPU). Can be quantized to Q4_K_M (~2.5 GB) for edge deployment.

### Step 3 — Query for CWE classification

```python
messages = [
    {
        "role": "system",
        "content": "You are a defensive cybersecurity assistant. Answer with the canonical CWE-ID first, then 1-3 sentences of justification."
    },
    {
        "role": "user",
        "content": "Path traversal in a Java web app where user-controlled input concatenates into a File() path. What's the CWE?"
    },
]

prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
out = model.generate(
    **tok(prompt, return_tensors="pt").to(model.device),
    max_new_tokens=256,
    temperature=0.3
)
print(tok.decode(out[0], skip_special_tokens=True))
```

### Step 4 — (Optional) High-throughput serving with vLLM

For SOC-scale workloads processing thousands of alerts per day:

```bash
# With ROCm (AMD GPUs):
docker run --rm -it \
  --device=/dev/kfd --device=/dev/dri \
  vllm/vllm-openai-rocm:latest \
  python -m vllm.entrypoints.openai.api_server \
  --model lablab-ai-amd-developer-hackathon/CyberSecQwen-4B

# With CUDA (NVIDIA GPUs):
python -m vllm.entrypoints.openai.api_server \
  --model lablab-ai-amd-developer-hackathon/CyberSecQwen-4B
```

Then query via the OpenAI-compatible API at `http://localhost:8000/v1/chat/completions`.

### Supported tasks

| Task | Description |
|------|-------------|
| **CWE Classification** | Map vulnerability descriptions to MITRE CWE categories |
| **CVE-to-CWE Mapping** | Structured threat intelligence extraction |
| **Defensive Analyst Q&A** | Answer cybersecurity concept questions |
| **Triage Assistance** | Support human analysts in CVE prioritization |

### Performance

- **CTI-MCQ (2,500 items):** 0.587 — outperforms Foundation-Sec-8B by +8.7 pp
- **CTI-RCM (1,000 CVE→CWE):** 0.666 — retains 97.3% of 8B accuracy at half the parameters
- Base model: Qwen3-4B-Instruct-2507, fine-tuned with LoRA (r=64, alpha=64)
- License: Apache 2.0 (free for commercial and research use)

### Important usage notes

- **Intended for defensive use only** — CWE classification, CTI Q&A, and triage support
- **Not for exploit generation**, weaponized PoC creation, or automated security decisions without human review
- **Data stays local** — no off-premises transmission of credentials, malware samples, or vulnerability drafts
- Companion 2B model available: `Gemma4Defense-2B` (same recipe, Gemma-4-E2B-it base)

## References

- [CyberSecQwen-4B Blog Post](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/cybersecqwen-4b)
- [Model on Hugging Face](https://huggingface.co/lablab-ai-amd-developer-hackathon/CyberSecQwen-4B)
- [Live Demo](https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/cybersecqwen-chat)
- [GitHub Repository](https://github.com/GPT-64590/CyberSecQwen-4B)
