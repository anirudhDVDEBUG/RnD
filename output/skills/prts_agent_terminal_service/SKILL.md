---
name: prts_agent_terminal_service
description: |
  Build a PRTS-style (PRTS Rebuild Terminal Service) AI agent orchestration system in Python.
  TRIGGER when: user wants to build a terminal-based agent service, orchestrate multiple AI agents from a terminal interface, create a command-line agent dispatcher, or build a rebuild/restart-capable agent runtime.
  DO NOT TRIGGER when: user is building a simple chatbot, single-agent CLI tool, or web-based agent UI.
---

# PRTS Agent Terminal Service

Build a terminal-based AI agent orchestration service inspired by [PRTS (PRTS Rebuild Terminal Service)](https://github.com/zayokami/PRTS).

## When to use

- "I want to build a terminal service that orchestrates multiple AI agents"
- "Create a command-line agent dispatcher with restart/rebuild capabilities"
- "Build a Python agent runtime that manages agent lifecycles from the terminal"
- "I need an agent orchestration layer that runs as a terminal service"
- "Set up a multi-agent system with terminal-based control and monitoring"

## How to use

### 1. Project Structure

Set up the Python project with the following layout:

```
prts/
├── main.py              # Entry point / terminal service loop
├── agents/
│   ├── __init__.py
│   ├── base.py          # Base agent class with lifecycle hooks
│   └── worker.py        # Concrete agent implementations
├── orchestrator/
│   ├── __init__.py
│   ├── dispatcher.py    # Routes tasks to appropriate agents
│   └── scheduler.py     # Manages agent execution order
├── terminal/
│   ├── __init__.py
│   ├── interface.py     # Terminal UI / command parser
│   └── commands.py      # Registered terminal commands
├── config/
│   └── settings.yaml    # Agent and service configuration
└── requirements.txt
```

### 2. Core Components

**Base Agent** (`agents/base.py`):
- Define an abstract `Agent` class with `start()`, `stop()`, `rebuild()`, and `execute(task)` methods
- Include health-check and status reporting
- Support graceful shutdown and restart (the "Rebuild" in PRTS)

**Orchestrator** (`orchestrator/dispatcher.py`):
- Maintain a registry of available agents
- Dispatch incoming tasks to the correct agent based on task type
- Handle agent failures with retry/rebuild logic

**Terminal Interface** (`terminal/interface.py`):
- Provide an interactive command loop (REPL-style)
- Commands: `list` (show agents), `status`, `dispatch <task>`, `rebuild <agent>`, `stop`, `logs`
- Use Python's `cmd` module or `prompt_toolkit` for rich terminal UX

### 3. Implementation Steps

1. **Install dependencies**: `pip install pyyaml prompt_toolkit` (add LLM SDK as needed)
2. **Define the base agent interface** with lifecycle management (start/stop/rebuild)
3. **Implement the dispatcher** that maps task types to agent instances
4. **Build the terminal REPL** that accepts commands and routes them to the orchestrator
5. **Add rebuild capability**: agents can be hot-reloaded or restarted without terminating the service
6. **Add configuration** via YAML for agent definitions, retry policies, and service settings

### 4. Key Design Patterns

- **Agent Lifecycle**: Each agent has states: `idle → running → completed/failed → rebuilding`
- **Hot Rebuild**: Agents can be restarted mid-session without losing orchestrator state
- **Terminal-First**: All interaction happens via the terminal—no web server required
- **Extensible**: New agents are registered by subclassing `Agent` and adding to config

### 5. Example Usage

```python
# main.py
from terminal.interface import TerminalService
from orchestrator.dispatcher import Dispatcher
from agents.worker import ResearchAgent, CodeAgent

def main():
    dispatcher = Dispatcher()
    dispatcher.register(ResearchAgent())
    dispatcher.register(CodeAgent())
    
    service = TerminalService(dispatcher)
    service.run()  # Starts the interactive terminal loop

if __name__ == "__main__":
    main()
```

## References

- Source repository: https://github.com/zayokami/PRTS
- Topics: ai-agents, agent orchestration, terminal service
- Language: Python
