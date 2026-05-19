---
name: open_agent_leaderboard_eval
description: |
  Evaluate and benchmark AI agent systems using the Open Agent Leaderboard and Exgentic framework.
  Triggers: agent benchmark, agent leaderboard, evaluate agent system, exgentic, agent evaluation across benchmarks
---

# Open Agent Leaderboard Evaluation

Benchmark full AI agent systems (model + architecture + tools + planning) across diverse realistic tasks using the Open Agent Leaderboard and the Exgentic evaluation framework.

## When to use

- "Benchmark my agent across multiple evaluation suites"
- "Compare agent architectures on SWE-Bench, AppWorld, and tau2-Bench"
- "Submit my agent's results to the Open Agent Leaderboard"
- "Evaluate agent cost vs quality tradeoffs across benchmarks"
- "Set up Exgentic to run standardized agent evaluations"

## How to use

### 1. Install the Exgentic framework

```bash
git clone https://github.com/Exgentic/exgentic.git
cd exgentic
pip install -e .
```

### 2. Wrap your agent in the Exgentic protocol

Exgentic uses a unified protocol with three components shared across all benchmarks:

- **Task** — what the agent must do
- **Context** — what the agent should know
- **Actions** — what tools/operations are allowed

This means your agent speaks one language across all six benchmarks instead of adapting to each one separately.

### 3. Run evaluations

The leaderboard covers six benchmarks testing different capabilities:

| Benchmark | Tests |
|---|---|
| **SWE-Bench Verified** | Fixing real bugs in code repositories |
| **BrowseComp+** | Researching complex questions across the web |
| **AppWorld** | Completing personal tasks across hundreds of apps |
| **tau2-Bench Airline** | Customer service with airline company policies |
| **tau2-Bench Retail** | Customer service with retail company policies |
| **tau2-Bench Telecom** | Technical support with telecom company policies |

Run your agent through the Exgentic framework to produce standardized results, trajectories, and cost reports.

### 4. Review metrics

For each agent system configuration, track:

- **Success rate** — average accuracy across benchmarks
- **Cost per task** — average dollars spent per task
- **Per-benchmark breakdowns** — identify strengths and weaknesses
- **Failure cost analysis** — failed runs typically cost 20–54% more than successful ones

### 5. Submit results to the leaderboard

1. Version your agent and document all components (model, architecture, tools)
2. Make components configurable for reproducibility
3. Open a pull request on the results dataset at `huggingface.co/datasets/open-agent-leaderboard/results`

### Key findings to inform your design

- **Model choice is the primary performance driver**, but agent architecture still matters significantly
- **Tool shortlisting** improved performance across all configurations tested
- **General-purpose agents can match specialized ones** — a single agent can handle multiple task types
- **Cost varies dramatically** — same model with different agent architectures can show 2x+ cost differences
- **Open-weight models** (DeepSeek V3.2, Kimi K2.5) are competitive on specific benchmarks but trail frontier models by 18–29 points on average

## References

- [Open Agent Leaderboard Blog Post](https://huggingface.co/blog/ibm-research/open-agent-leaderboard)
- [Interactive Leaderboard](https://huggingface.co/spaces/open-agent-leaderboard/leaderboard)
- [Exgentic Framework (GitHub)](https://github.com/Exgentic/exgentic)
- [Research Paper (arXiv)](https://arxiv.org/abs/2602.22953) — ICLR 2026 Workshop
- [Results Dataset (HuggingFace)](https://huggingface.co/datasets/open-agent-leaderboard/results)
