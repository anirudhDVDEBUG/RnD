# How to Use — Runa Digital Being Agent

## Install

```bash
git clone <this-repo> && cd runa_digital_being_agent
pip install -r requirements.txt   # only pyyaml
```

## Run the Demo

```bash
bash run.sh
```

No API keys needed — the demo uses a built-in mock LLM that simulates autonomous reasoning.

## First 60 Seconds

**Input:** `bash run.sh`

**Output:**
```
============================================================
  RUNA DIGITAL BEING AGENT — Autonomous Agent Demo
============================================================

=== Runa Status ===
[Runa] Purpose: Autonomous digital being that pursues self-directed goals...
Goals: 3 active, 0 completed
  [aspiration] Achieve full operational awareness (0%)
  [objective] Map available capabilities and tools (0%)
  [task] Introduce self and demonstrate autonomy (0%)
Memory bank: 0 entries stored.
Available actions:
  - log_thought: Log an internal thought
  - reflect: Reflect on an observation
  - search_memory: Search past memories
  - set_goal: Set a new goal
Cycles completed: 0

------------------------------------------------------------
  Running 3 autonomous cycles...
------------------------------------------------------------

--- Cycle 1 ---
  Reasoning:  I have an active task: 'Introduce self and demonstrate autonomy'. Let me work on it.
  Action:     log_thought
  Result:     [Thought logged] Working on: Introduce self and demonstrate autonomy
  Reflection: Making progress on my objectives.

--- Cycle 2 ---
  ...

Demo complete. Agent state persisted to logs/
```

## Using as a Claude Skill

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/runa_digital_being_agent
cp SKILL.md ~/.claude/skills/runa_digital_being_agent/SKILL.md
```

**Trigger phrases:**
- "Build me an autonomous agent"
- "Create a digital being with its own identity"
- "Scaffold a sovereign AI agent framework"
- "Set up an autonomous agent with persistent state"

## Connecting a Real LLM

Replace the mock with Anthropic's API:

```python
import anthropic

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

def real_llm(messages):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=messages[0]["content"],
        messages=messages[1:],
    )
    return response.content[0].text

agent = RunaAgent(llm_fn=real_llm)
```

## Extending with Custom Actions

```python
from agent import RunaAgent, ActionRegistry

registry = ActionRegistry()
registry.register("send_email", my_email_fn, "Send an email notification")

agent = RunaAgent(actions=registry)
```
