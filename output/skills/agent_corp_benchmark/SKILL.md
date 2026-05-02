---
name: agent_corp_benchmark
description: |
  Set up and run agent-corp, an agent benchmark framework that evaluates AI agents on realistic software engineering tasks in a simulated company environment.
  TRIGGER: user wants to benchmark agents, evaluate agent performance on SWE tasks, set up agent-corp, run simulated company tasks, or compare agent capabilities
---

# Agent-Corp Benchmark

Benchmark AI agents on realistic software engineering tasks inside a simulated software company environment using [agent-corp](https://github.com/jmerelnyc/agent-corp).

## When to use

- "Set up agent-corp to benchmark my agent"
- "Run agent evaluation tasks in a simulated company"
- "Compare agent performance on software engineering benchmarks"
- "I want to test how well my agent handles real-world dev tasks"
- "Evaluate an AI coding agent with agent-corp"

## How to use

### 1. Clone and install

```bash
git clone https://github.com/jmerelnyc/agent-corp.git
cd agent-corp
pip install -e .
```

### 2. Configure your agent

Agent-corp expects a Python-based agent interface. Set up your agent adapter following the repo's conventions:

- Define your agent class that implements the expected interface
- Configure API keys and model settings via environment variables or a config file
- Tasks simulate a real software company with bug fixes, feature requests, code reviews, and refactoring work

### 3. Run benchmark tasks

```bash
# Run all benchmark tasks
python -m agent_corp.run --all

# Run a specific task category
python -m agent_corp.run --category bug_fix

# Run a single task by ID
python -m agent_corp.run --task <task_id>
```

### 4. Evaluate results

```bash
# View evaluation summary
python -m agent_corp.evaluate --results-dir ./results
```

The benchmark evaluates agents on:
- **Task completion** — Did the agent solve the assigned task correctly?
- **Code quality** — Are the changes clean, idiomatic, and well-structured?
- **Efficiency** — How many steps/tokens did the agent use?
- **Tool usage** — Did the agent use available tools appropriately?

### 5. Compare agents

Results are saved as structured JSON, making it straightforward to compare multiple agents across task categories.

## Key concepts

| Concept | Description |
|---------|-------------|
| **Simulated company** | Tasks are set in a realistic codebase with PRs, issues, and team context |
| **Task categories** | Bug fixes, feature development, code review, refactoring, testing |
| **Evaluation metrics** | Completion rate, code quality score, efficiency, tool usage patterns |
| **Agent interface** | Python adapter pattern — plug in any agent that can read/write code |

## Tips

- Start with a single task category to validate your agent adapter works before running the full suite
- Review the task definitions in the repo to understand what context is provided to agents
- Use the structured JSON output to build custom dashboards or comparison charts
- The simulated environment is sandboxed — agents operate on isolated copies of the codebase

## References

- **Repository**: [jmerelnyc/agent-corp](https://github.com/jmerelnyc/agent-corp)
- **Language**: Python
- **Topics**: agent-evaluation, ai-agents, benchmark, simulation, software-development, task-automation
