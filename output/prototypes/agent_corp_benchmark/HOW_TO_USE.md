# How to Use Agent-Corp Benchmark

## Install (this demo)

```bash
pip install -r requirements.txt   # just tabulate
bash run.sh                        # runs the full benchmark demo
```

## Install the real agent-corp

```bash
git clone https://github.com/jmerelnyc/agent-corp.git
cd agent-corp
pip install -e .
```

Then configure your agent adapter and API keys per the repo's README.

## Using as a Claude Skill

Drop the skill folder into your Claude skills directory:

```bash
cp -r agent_corp_benchmark ~/.claude/skills/agent_corp_benchmark/
```

The skill file lives at `~/.claude/skills/agent_corp_benchmark/SKILL.md`.

**Trigger phrases** that activate the skill:

- "Set up agent-corp to benchmark my agent"
- "Run agent evaluation tasks in a simulated company"
- "Compare agent performance on software engineering benchmarks"
- "Evaluate an AI coding agent with agent-corp"

## First 60 Seconds

**Input:**

```bash
bash run.sh
```

**Output** (truncated):

```
============================================================
  AGENT-CORP BENCHMARK - Simulated Company Environment
============================================================

  Tasks: 7  |  Agents: 3  |  Categories: 5

--- Detailed Results: claude-agent ---

+----------+-------------+------------+--------+-------+--------+---------+----------+
| Task     | Category    | Difficulty | Status | Steps | Tokens | Quality | Tool Use |
+----------+-------------+------------+--------+-------+--------+---------+----------+
| BUG-101  | bug_fix     | easy       | PASS   | 5     | 1200   | 0.87    | 0.72     |
| BUG-204  | bug_fix     | hard       | FAIL   | 12    | 4800   | 0.00    | 0.61     |
| FEAT-301 | feature     | medium     | PASS   | 8     | 3100   | 0.79    | 0.88     |
| ...      | ...         | ...        | ...    | ...   | ...    | ...     | ...      |
+----------+-------------+------------+--------+-------+--------+---------+----------+

Agent Comparison:
+---------------+-----------+-------+---------+-------+--------+----------+
| Agent         | Completed | Rate  | Quality | Steps | Tokens | Tool Use |
+---------------+-----------+-------+---------+-------+--------+----------+
| claude-agent  | 5/7       | 71.4% | 0.81    | 8.4   | 3271   | 0.74     |
| gpt-agent     | 4/7       | 57.1% | 0.77    | 9.1   | 3540   | 0.71     |
| gemini-agent  | 5/7       | 71.4% | 0.83    | 7.9   | 2986   | 0.69     |
+---------------+-----------+-------+---------+-------+--------+----------+

Results saved to results/benchmark_results.json
```

The JSON file contains per-task results, overall summaries, and per-category breakdowns for every agent — ready for dashboards or CI integration.

## Running the Real Benchmark

With the full `agent-corp` installed:

```bash
# Run all tasks
python -m agent_corp.run --all

# Single category
python -m agent_corp.run --category bug_fix

# Single task
python -m agent_corp.run --task BUG-101

# Evaluate
python -m agent_corp.evaluate --results-dir ./results
```

## Key CLI Options

| Flag | Description |
|------|-------------|
| `--all` | Run all benchmark tasks |
| `--category <name>` | Filter by: bug_fix, feature, refactor, code_review, testing |
| `--task <id>` | Run a single task by ID |
| `--results-dir <path>` | Where to write/read JSON results |
