# Technical Details: CyberSecQwen-4B

## What It Does

CyberSecQwen-4B is a 4-billion parameter language model fine-tuned specifically for defensive cybersecurity tasks. Built on Qwen3-4B-Instruct-2507 using LoRA (rank=64, alpha=64), it specializes in three capabilities: (1) mapping free-text vulnerability descriptions to MITRE CWE categories, (2) structured CVE-to-CWE extraction for threat intelligence pipelines, and (3) answering defensive cybersecurity concept questions.

The model was trained on curated CTI (Cyber Threat Intelligence) datasets and evaluated against two benchmarks — CTI-MCQ (2,500 multiple-choice items) and CTI-RCM (1,000 CVE-to-CWE mapping tasks). It scores 0.587 on CTI-MCQ, outperforming the larger Foundation-Sec-8B by 8.7 percentage points, and 0.666 on CTI-RCM, retaining 97.3% of the 8B model's accuracy at half the parameters.

## Architecture

```
User query (vulnerability description / CVE / question)
        |
        v
+-------------------+
| Qwen3-4B-Instruct |  Base model (4B params, bfloat16)
| + LoRA adapters    |  r=64, alpha=64
+-------------------+
        |
        v
  Chat template applied (system prompt + user message)
        |
        v
  Autoregressive generation (max_new_tokens=256, temp=0.3)
        |
        v
  Structured output: CWE-ID + justification
```

### Key Files

| File | Purpose |
|------|---------|
| `cybersec_demo.py` | Mock demo + real model inference harness |
| `run.sh` | One-command runner |
| `requirements.txt` | Dependencies (stdlib for mock; torch/transformers for real) |

### Dependencies

- **Mock mode:** Python 3.8+ stdlib only
- **Real inference:** `torch`, `transformers`, `accelerate` (12 GB VRAM GPU)
- **High-throughput:** `vllm` for OpenAI-compatible API serving

### Data Flow (Real Model)

1. User provides a vulnerability description or CVE
2. System prompt instructs the model to respond with CWE-ID first, then justification
3. `AutoTokenizer.apply_chat_template()` formats the prompt for Qwen3's chat format
4. Model generates up to 256 tokens at temperature 0.3 (low creativity, high precision)
5. Output is decoded and returned — no data leaves the machine

## Limitations

- **Defensive tasks only** — the model is not designed for exploit generation or offensive research. It will not produce weaponized PoCs.
- **CWE coverage is bounded** — the model maps to established MITRE CWE categories; novel vulnerability classes outside the CWE taxonomy may be misclassified.
- **Not a replacement for human analysts** — intended as triage assistance, not autonomous decision-making. False positives/negatives occur.
- **Context window** — inherits Qwen3-4B's context limits (~32K tokens). Very long CVE descriptions may need truncation.
- **No real-time threat feeds** — the model's knowledge is frozen at training time. It cannot fetch live CVE data.
- **Benchmark scores** — while strong for its size, 0.587 MCQ accuracy means ~41% of multiple-choice CTI questions are answered incorrectly.

## Why This Matters for Claude-Driven Products

### Agent Factories
A locally-runnable CWE classifier can be embedded as a specialized tool in Claude-orchestrated agent pipelines. Claude handles reasoning and orchestration; CyberSecQwen handles domain-specific CWE classification without API calls or data exfiltration risk. This is the "small specialist model as a tool" pattern.

### Security-Sensitive Verticals
For teams building Claude-powered products in regulated industries (finance, healthcare, defense), the ability to classify vulnerabilities without sending data to external APIs is a compliance enabler. Air-gapped deployment on consumer hardware removes a major adoption blocker.

### Lead-Gen / Marketing for Security Products
Security vendors can use CWE classification as a demo hook — "paste your vulnerability description, get instant CWE mapping" — powered by a local model. No API costs, instant response, and the classification quality provides genuine value.

### Cost Efficiency
At 4B parameters with Q4 quantization (~2.5 GB), this model runs on hardware that costs ~$0.50/hr in the cloud or on existing developer laptops. For CVE triage at scale (thousands of alerts/day via vLLM), the per-query cost is negligible compared to API-based LLM calls.

## References

- [CyberSecQwen-4B Blog Post](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/cybersecqwen-4b)
- [Model Card](https://huggingface.co/lablab-ai-amd-developer-hackathon/CyberSecQwen-4B)
- [Live Demo Space](https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/cybersecqwen-chat)
- [GitHub Repository](https://github.com/GPT-64590/CyberSecQwen-4B)
- Companion model: [Gemma4Defense-2B](https://huggingface.co/lablab-ai-amd-developer-hackathon/Gemma4Defense-2B) (same recipe, smaller)
