# CyberSecQwen-4B: Local Defensive Cybersecurity Model

**TL;DR:** A 4B-parameter model fine-tuned for defensive cybersecurity — CWE classification, CVE-to-CWE mapping, and analyst Q&A — that runs locally on a consumer GPU (12 GB VRAM). Outperforms Foundation-Sec-8B on CTI benchmarks at half the parameter count.

## Headline Result

> **CTI-MCQ accuracy: 0.587** — beats the 8B Foundation-Sec model by +8.7 percentage points while using only 4B parameters. Runs entirely offline, keeping vulnerability data on-premises.

## Quick Start

```bash
bash run.sh
```

No GPU or model download needed for the mock demo. Set `USE_REAL_MODEL=1` for actual inference.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, skill setup, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, benchmarks, limitations

## Source

- [Blog Post](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/cybersecqwen-4b)
- [Model on HuggingFace](https://huggingface.co/lablab-ai-amd-developer-hackathon/CyberSecQwen-4B)
- [GitHub](https://github.com/GPT-64590/CyberSecQwen-4B)
