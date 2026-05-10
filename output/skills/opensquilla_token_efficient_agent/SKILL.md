---
name: opensquilla_token_efficient_agent
description: |
  Set up and use OpenSquilla, a token-efficient AI agent framework that maximizes intelligence density per token budget.
  TRIGGER when: user mentions "opensquilla", "token-efficient agent", "intelligence density", "opensquilla agent", or wants to build agents that optimize token usage.
  DO NOT TRIGGER when: user is working with unrelated agent frameworks or general Python projects.
---

# OpenSquilla — Token-Efficient AI Agent

OpenSquilla is a Python-based AI agent framework focused on maximizing intelligence density within a given token budget. It supports MCP servers, agent memory, and skill-based architecture.

## When to use

- "Set up an OpenSquilla agent"
- "I want a token-efficient AI agent"
- "Help me configure opensquilla with MCP"
- "Build an agent that optimizes token usage"
- "Use opensquilla for agent memory and skills"

## How to use

### 1. Install OpenSquilla

```bash
pip install opensquilla
```

Or clone and install from source:

```bash
git clone https://github.com/OpenSquilla/opensquilla.git
cd opensquilla
pip install -e .
```

### 2. Basic Agent Setup

Create a Python script to initialize an OpenSquilla agent:

```python
from opensquilla import Agent

agent = Agent(
    name="my_agent",
    token_budget=4096,  # Set your token budget
)

response = agent.run("Your task prompt here")
print(response)
```

### 3. Configure MCP Server Integration

OpenSquilla supports MCP (Model Context Protocol) servers for extended tool use:

```python
from opensquilla import Agent, MCPConfig

agent = Agent(
    name="mcp_agent",
    mcp_servers=[
        MCPConfig(name="filesystem", command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/path"])
    ]
)
```

### 4. Agent Memory

Enable persistent memory for cross-session context:

```python
agent = Agent(
    name="memory_agent",
    memory_enabled=True,
    memory_path="./agent_memory"
)
```

### 5. Skills Architecture

Register custom skills to extend agent capabilities:

```python
from opensquilla import Agent, Skill

@Skill(name="summarize", description="Summarize text efficiently")
def summarize(text: str) -> str:
    # skill implementation
    return summary

agent = Agent(name="skilled_agent", skills=[summarize])
```

### Key Features

- **Token efficiency**: Optimizes prompt construction to maximize output quality within budget constraints
- **MCP integration**: Connect to any MCP-compatible server for tool use
- **Persistent memory**: Agent retains context across sessions
- **Skill system**: Modular, reusable capabilities
- **Python-native**: Built entirely in Python with minimal dependencies

## References

- Repository: https://github.com/OpenSquilla/opensquilla
- Topics: agent, ai, mcp, memory, python, skills
- Language: Python
