# Agent-Corp Benchmark Demo

Benchmark AI agents on realistic software engineering tasks — bug fixes, features, refactoring, code reviews — inside a simulated company environment. This demo runs 3 mock agents through 7 SWE tasks and produces a side-by-side comparison table.

## Headline Result

```
+---------------+-----------+-------+---------+-------+--------+------------+
| Agent         | Completed | Rate  | Quality | Steps | Tokens | Tool Use   |
+---------------+-----------+-------+---------+-------+--------+------------+
| claude-agent  | 5/7       | 71.4% | 0.81    | 8.4   | 3271   | 0.74       |
| gpt-agent     | 4/7       | 57.1% | 0.77    | 9.1   | 3540   | 0.71       |
| gemini-agent  | 5/7       | 71.4% | 0.83    | 7.9   | 2986   | 0.69       |
+---------------+-----------+-------+---------+-------+--------+------------+
```

## Quick Start

```bash
bash run.sh
```

No API keys required — uses simulated agent runs to demonstrate the benchmark framework.

See [HOW_TO_USE.md](HOW_TO_USE.md) for setup details and [TECH_DETAILS.md](TECH_DETAILS.md) for architecture.
