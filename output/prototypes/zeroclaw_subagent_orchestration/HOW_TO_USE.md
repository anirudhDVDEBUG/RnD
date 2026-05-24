# How to Use — ZeroClaw Subagent Orchestration

## This is a Claude Code Skill

The ZeroClaw pattern is packaged as a **SKILL.md** file that teaches Claude Code how to orchestrate multi-agent workflows.

### Install the Skill

1. Create the skill directory:

```bash
mkdir -p ~/.claude/skills/zeroclaw_subagent_orchestration
```

2. Copy the skill file:

```bash
cp SKILL.md ~/.claude/skills/zeroclaw_subagent_orchestration/SKILL.md
```

Or clone the source repo directly:

```bash
git clone https://github.com/muhammadqasimkalhoro94-blip/claude-zeroclaw-agentics.git
cp claude-zeroclaw-agentics/SKILL.md ~/.claude/skills/zeroclaw_subagent_orchestration/SKILL.md
```

### Trigger Phrases

Once installed, say any of these to Claude Code:

- "orchestrate subagents"
- "zeroclaw routing"
- "multi-agent pipeline"
- "claude code router"
- "subagent orchestration"
- "MCP agent routing"
- "Set up a multi-agent pipeline to handle this complex task"
- "Route this task across specialized Claude agents using ZeroClaw"

### What Happens

Claude Code will:

1. **Decompose** your task into discrete subtasks (research, code, review, etc.)
2. **Route** each subtask to a specialized subagent (`subagent_type=Explore`, `Code`, or custom)
3. **Execute** independent subtasks in parallel using the Agent tool
4. **Merge** all outputs into a unified result with conflict detection

## First 60 Seconds

**Input:**
```
> orchestrate subagents to add Stripe payment integration to my Flask app
```

**What Claude does:**
```
[1] TASK DECOMPOSITION
    Subtask 1:   research -> Research Stripe API docs, existing payment code
    Subtask 2:       code -> Implement Stripe checkout flow
    Subtask 3:     review -> Validate implementation, run tests

[2] DISPATCHING (parallel_then_merge)
    Spawning 3 subagents via Agent tool...

[3] MERGED RESULT
    Status:     success
    Agents:     3
    Conflicts:  None
    Files modified: src/payments.py, src/routes.py, tests/test_payments.py
```

## Running the Standalone Demo

No API keys needed. The demo uses mock agents to show the full pipeline:

```bash
# Python 3.10+ required, no pip install needed
bash run.sh
```

This runs `demo.py`, which demonstrates:
- Parallel dispatch (3 agents running concurrently)
- Sequential dispatch (chained context passing)
- Custom agent registration (security auditor)

## Using the Python Library Directly

```python
from zeroclaw.orchestrator import Orchestrator

orch = Orchestrator(strategy="parallel_then_merge")
result = orch.run("Refactor the auth module for OAuth2 support")

print(result.overall_status)  # "success" or "needs_review"
print(result.summary)
for d in result.details:
    print(f"  {d['agent']}: {d['status']}")
```

### Custom Agents

```python
from zeroclaw.agents import AgentSpec
from zeroclaw.orchestrator import Orchestrator

security = AgentSpec(
    name="security",
    role="Scan for vulnerabilities",
    agent_type="review",
    tools=["Bash", "Grep"],
)
orch = Orchestrator(agents=[security])
result = orch.run("Audit the login endpoint")
```

## Routing Strategies

| Strategy | When to Use |
|---|---|
| `parallel_then_merge` | Independent subtasks (default, fastest) |
| `sequential` | Each step needs output from the previous one |

## MCP Integration (Optional)

If you have MCP servers configured in `~/.claude.json`, each subagent inherits access to those tools. No additional configuration needed — the Claude Code Agent tool passes MCP context automatically.
