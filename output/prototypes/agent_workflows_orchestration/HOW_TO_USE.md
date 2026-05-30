# How to Use

## Install

### Option A: pip (real package)

```bash
pip install agent-workflows
```

### Option B: from source

```bash
git clone https://github.com/akakabrian/agent-workflows.git
cd agent-workflows
pip install -e .
```

### Option C: this demo (no install needed)

```bash
bash run.sh
```

The demo ships a self-contained shim of the runtime — stdlib only, no pip install required.

---

## Claude Code Skill setup

This repo includes a `SKILL.md` file. To register it as a Claude Code skill:

```bash
mkdir -p ~/.claude/skills/agent_workflows_orchestration
cp SKILL.md ~/.claude/skills/agent_workflows_orchestration/SKILL.md
```

### Trigger phrases

Once installed, Claude Code activates this skill when you say things like:

- "Set up a multi-agent workflow with fan-out and validation"
- "Orchestrate multiple LLM calls with budget limits"
- "Create a pipeline of agent steps with SQLite journaling"
- "Use owf to run a fan-out workflow"
- "Build a resumable agent workflow in Python"

It will **not** trigger for simple single-prompt interactions or other workflow engines (LangGraph, CrewAI).

---

## First 60 seconds

### 1. Run the demo

```bash
bash run.sh
```

Expected output:

```
>>> Running demo workflow (fake adapter — no API keys needed)...

============================================================
  agent-workflows demo: research-and-summarize
============================================================

--- Executing workflow ---

  Run ID : a3f1c8e20b91
  Steps  : 4
  Budget : $0.50

  [run]  fan-out:AI safety
  [run]  fan-out:agent architectures
  [run]  fan-out:tool use in LLMs
  [run]  pipeline:aggregator
  [pass] validation (len=218 >= 50)

  Total cost: $0.0080

--- Step results ---

  [done] fan-out:AI safety
         [FakeAdapter] Simulated response for: Research the current state of AI safety...

  [done] fan-out:agent architectures
         [FakeAdapter] Simulated response for: Research the current state of agent architectures...

  [done] fan-out:tool use in LLMs
         [FakeAdapter] Simulated response for: Research the current state of tool use in LLMs...

  [done] pipeline:aggregator
         [FakeAdapter] Simulated response for: Synthesize the research above...

--- Run journal (SQLite) ---

  a3f1c8e20b91  completed           cost=$0.0080  (2026-05-30 ...)

>>> Demo complete.
```

### 2. Inspect the journal

```bash
sqlite3 demo_journal.sqlite "SELECT * FROM runs;"
sqlite3 demo_journal.sqlite "SELECT step_id, name, status, cost FROM steps;"
```

### 3. Write your own workflow

```python
from agent_workflows import Workflow, Step

wf = Workflow(name="my-workflow")
steps = wf.fan_out(prompt="Analyze {topic}", topics=["pricing", "competitors"])
agg = wf.pipeline(steps=steps, then=Step(prompt="Combine into a report"))
wf.validate(agg, schema={"type": "string", "minLength": 20})
wf.run(budget=1.00, adapter="fake")
```

### 4. Switch to a real adapter

```python
wf.run(adapter="claude")  # uses claude CLI under the hood
```

Or build a custom adapter:

```python
from agent_workflows import Adapter

class GPT4Adapter(Adapter):
    def call(self, prompt: str) -> str:
        # your OpenAI / other provider call here
        return response

wf.run(adapter=GPT4Adapter())
```
