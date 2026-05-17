# How to Use: Multi-Agent Orchestration

## Install

No external dependencies. Requires Python 3.10+.

```bash
git clone <this-repo>
cd multi_agent_orchestration
bash run.sh
```

## As a Claude Code Skill

This is a **Claude Code Skill**. To install:

```bash
mkdir -p ~/.claude/skills/multi_agent_orchestration
cp SKILL.md ~/.claude/skills/multi_agent_orchestration/SKILL.md
```

### Trigger Phrases

Once installed, Claude Code activates this skill when you say:

- "Set up a multi-agent pipeline to handle this task"
- "Orchestrate multiple agents to work on different parts of this project"
- "Build an agent swarm to process these items in parallel"
- "Create an agent workflow with coordination between steps"
- "Deploy a multi-agent system for this complex task"

Keywords: `multi-agent`, `orchestration`, `agent swarm`, `agent pipeline`, `parallel agents`, `agent coordination`, `agent workflow`

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output:**
```
Running Multi-Agent Orchestration Demo...

============================================================
  PIPELINE: Market Research Pipeline (4 stages)
============================================================

  [1/4] Researcher (researcher)
      Tools: WebSearch, WebFetch
      Status: OK (123.4ms)

  [2/4] Planner (planner)
      Tools: Read, TodoWrite
      Status: OK (89.2ms)

  [3/4] Implementer (implementer)
      Tools: Edit, Write, Bash
      Status: OK (156.7ms)

  [4/4] Reviewer (reviewer)
      Tools: Read, Bash, Grep
      Status: OK (67.1ms)

  Pipeline Summary:
    Stages completed: 4/4
    Total time: 436.4ms
    Quality score: 0.92

============================================================
  FAN-OUT: Multi-Domain Research (5 parallel tasks)
============================================================
  [researcher_competitor_analysis] OK (187.3ms)
  [researcher_pricing_models] OK (142.1ms)
  [researcher_user_feedback] OK (201.4ms)
  [researcher_tech_stack] OK (156.8ms)
  [researcher_market_trends] OK (178.2ms)

  Total wall-clock time: 210.5ms (parallel)
  Sequential equivalent: 865.8ms
  Speedup: 2.83x
```

## Using in Your Own Code

```python
from orchestrator import Agent, AgentRole, Pipeline, FanOut, Coordinator

# Define agents with custom handlers
def my_handler(task_input: dict) -> dict:
    # Your logic here
    return {"result": "done"}

agent = Agent("my_agent", AgentRole.RESEARCHER, ["WebSearch"], my_handler)

# Sequential pipeline
pipeline = Pipeline("My Pipeline")
pipeline.add_stage(agent)
results = pipeline.run({"topic": "AI trends"})

# Parallel fan-out
fanout = FanOut("Parallel Tasks")
fanout.add_task(agent, {"domain": "area1"})
fanout.add_task(agent, {"domain": "area2"})
results = fanout.run()
```

## Mapping to Claude Code

In real Claude Code usage, the skill teaches Claude to use the `Agent` tool for parallelism:

```
# Claude spawns parallel sub-agents:
Agent(prompt="Research competitor pricing", subagent_type="Explore")
Agent(prompt="Research user feedback patterns", subagent_type="Explore")

# Then sequentially processes results:
Agent(prompt="Create implementation plan from research findings")
```

The orchestrator patterns (Pipeline, FanOut, Coordinator) map directly to how Claude Code's Agent tool works in practice.
