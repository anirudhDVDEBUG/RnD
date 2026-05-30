---
name: agent_workflows_orchestration
description: |
  Use this skill when the user wants to orchestrate multi-step agent workflows with fan-out, pipelines, validation, budgets, or resumable runs using the `owf` CLI and Python runtime.
  TRIGGER when: user mentions agent workflows, fan-out patterns, pipeline orchestration, durable workflow journals, owf CLI, or wants to coordinate multiple LLM calls from one script.
  DO NOT TRIGGER when: user is building simple single-prompt interactions or using a different workflow engine like LangGraph/CrewAI.
---

# Agent Workflows Orchestration

Provider-agnostic, zero-dependency Python runtime for dynamic agent workflows. Fan out, pipeline, validate, budget, and resume many model calls from one Python script with durable SQLite run journals.

## When to use

- "Set up a multi-agent workflow with fan-out and validation"
- "Orchestrate multiple LLM calls with budget limits and resume support"
- "Create a pipeline of agent steps with SQLite journaling"
- "Use owf to run a workflow that fans out to multiple models"
- "Build a resumable agent workflow in Python"

## How to use

### 1. Install

```bash
pip install agent-workflows
```

Or clone and install from source:

```bash
git clone https://github.com/akakabrian/agent-workflows.git
cd agent-workflows
pip install -e .
```

### 2. Define a workflow script

Create a Python file (e.g. `my_workflow.py`) using the `owf` runtime:

```python
from agent_workflows import Workflow, Step

wf = Workflow(name="research-and-summarize")

# Fan-out: run multiple research steps in parallel
research_steps = wf.fan_out(
    prompt="Research {topic}",
    topics=["AI safety", "agent architectures", "tool use"],
    adapter="claude"  # or "codex", "fake" for testing
)

# Pipeline: feed results into a summarizer
summary = wf.pipeline(
    steps=research_steps,
    then=Step(prompt="Summarize these findings into a report")
)

# Validate output
wf.validate(summary, schema={"type": "string", "minLength": 100})

wf.run(budget=0.50)  # USD budget cap
```

### 3. Run with the CLI

```bash
# Run workflow
owf run my_workflow.py

# Resume a failed/interrupted run
owf resume my_workflow.py --run-id <id>

# List past runs (SQLite journal)
owf runs my_workflow.py

# Use offline fake adapter for testing
owf run my_workflow.py --adapter fake
```

### 4. Key concepts

- **Fan-out**: Execute multiple prompts in parallel, collect all results
- **Pipeline**: Chain steps sequentially, passing output forward
- **Validation**: Assert output matches a schema or condition before continuing
- **Budget**: Set a USD spending cap; workflow pauses if exceeded
- **Resume**: Durable SQLite journal allows resuming from last successful step
- **Adapters**: `claude` (CLI-backed), `codex`, `fake` (offline testing)

### 5. Adapter configuration

Adapters are provider-agnostic backends:

```python
# Claude adapter (uses claude CLI)
wf.run(adapter="claude")

# Fake adapter for tests (zero cost, deterministic)
wf.run(adapter="fake")

# Custom adapter
from agent_workflows import Adapter

class MyAdapter(Adapter):
    def call(self, prompt: str) -> str:
        # Your logic here
        return response

wf.run(adapter=MyAdapter())
```

## References

- Repository: https://github.com/akakabrian/agent-workflows
- Topics: agent-workflows, ai-agents, cli, llm, orchestration, python, sqlite, workflow-engine
