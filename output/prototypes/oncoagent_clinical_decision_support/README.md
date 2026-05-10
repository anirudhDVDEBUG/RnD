# OncoAgent: Dual-Tier Multi-Agent Clinical Decision Support

**TL;DR:** A privacy-preserving oncology decision support system that routes cases by complexity to fast or deep-reasoning tiers, retrieves evidence via Corrective RAG with anti-hallucination gates, and validates every output through a deterministic reflexion critic — all running on-premises with zero PHI leakage.

**Headline result:** 4 demo cases processed end-to-end — PHI auto-redacted, dual-tier routing applied, guideline-grounded recommendations generated, and safety-validated — in under 1 second with no API keys or external calls.

---

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, run, and integrate
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations

## Quick Start

```bash
bash run.sh
```

No dependencies. Pure Python 3.8+. No API keys needed.

## Source

Based on the [OncoAgent paper](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper) — a dual-tier multi-agent framework for privacy-preserving oncology clinical decision support using LangGraph orchestration, Corrective RAG, and reflexion-based safety validation.
