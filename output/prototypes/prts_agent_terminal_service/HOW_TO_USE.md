# How to Use — PRTS Agent Terminal Service

## Install

```bash
git clone <this-repo>
cd prts_agent_terminal_service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # just pyyaml
```

Or simply run the all-in-one script:

```bash
bash run.sh
```

No external API keys are required — agents use mock data by default.

## As a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/prts_agent_terminal_service
cp SKILL.md ~/.claude/skills/prts_agent_terminal_service/SKILL.md
```

**Trigger phrases** that activate this skill:

- "Build a terminal service that orchestrates multiple AI agents"
- "Create a command-line agent dispatcher with restart/rebuild capabilities"
- "Set up a multi-agent system with terminal-based control"

Claude will scaffold the full project structure from the skill.

## First 60 seconds

1. Run `bash run.sh` — you'll see the PRTS banner and a batch demo dispatching tasks to three agents.

2. For interactive mode, run `python3 main.py`:

```
PRTS> list
  research       idle         execs=0  uptime=0.01s
  coder          idle         execs=0  uptime=0.01s
  summarizer     idle         execs=0  uptime=0.01s

PRTS> dispatch research quantum computing
{
  "agent": "research",
  "result": {
    "topic": "quantum computing",
    "findings": [
      "Found 12 recent papers on 'quantum computing'",
      "Top insight: quantum computing adoption grew 40% YoY",
      "Key risk: data quality remains the bottleneck for quantum computing"
    ]
  }
}

PRTS> dispatch code fib
{
  "agent": "coder",
  "result": {
    "language": "python",
    "code": "def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a"
  }
}

PRTS> rebuild research
  Agent 'research' rebuilt -> idle

PRTS> exit
  Shutting down PRTS...
```

## Available commands

| Command | Description |
|---------|-------------|
| `list` | Show all agents and their state |
| `status <name>` | Detailed JSON status for one agent |
| `dispatch <type> [payload]` | Route a task to the matching agent |
| `rebuild <name>` | Hot-restart an agent (reset state, keep registry) |
| `help_tasks` | Show which task types each agent handles |
| `exit` / `quit` | Shut down the service |

## Adding your own agent

1. Subclass `Agent` in `agents/worker.py` (or a new file):

```python
from agents.base import Agent

class MyAgent(Agent):
    name = "my_agent"
    description = "Does something useful"
    task_types = ["my_task"]

    def execute(self, task):
        return {"result": f"processed: {task['payload']}"}
```

2. Register it in `main.py`:

```python
from agents.worker import MyAgent
dispatcher.register(MyAgent())
```

3. Dispatch: `PRTS> dispatch my_task some input`
