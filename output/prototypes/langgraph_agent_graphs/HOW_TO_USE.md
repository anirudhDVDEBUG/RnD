# How to Use: LangGraph Agent Graphs

## Install

```bash
pip install langgraph langchain-core
# For real LLM calls, add one of:
pip install langchain-anthropic   # Claude
pip install langchain-openai      # OpenAI
```

## Claude Skill Setup

This is a **Claude Skill**. To install:

1. Copy the `SKILL.md` file to `~/.claude/skills/langgraph_agent_graphs/SKILL.md`
2. Restart Claude Code

**Trigger phrases** that activate the skill:

- "Build a multi-agent system with LangGraph"
- "Create a stateful agent graph with tool calling"
- "Add human-in-the-loop approval to my LangGraph agent"
- "Set up a LangGraph workflow with conditional edges"
- "Implement checkpointing and memory in my agent"

The skill provides Claude with ready-made patterns for StateGraph construction, tool binding, conditional edges, checkpointing, and interrupt-based human-in-the-loop flows.

## First 60 Seconds

**Input:**

```bash
bash run.sh
```

**Output** (truncated):

```
=== Running LangGraph Agent Graph Demo ===

============================================================
  Demo 1: Single Tool Call (Web Search)
============================================================

User: What is LangGraph?

  [agent] Tool call -> search_web({"query": "langgraph"})
  [tools] search_web returned: LangGraph is a library for building stateful...
  [agent] Assistant: Based on my research: LangGraph is a library for building...

============================================================
  Demo 5: Checkpointing (Persistent Memory)
============================================================

  Checkpointer: MemorySaver (in-memory)
  Thread ID: demo-thread-1
  Turn 1 -> 2 messages in state
  Turn 2 -> 4 messages in state (includes history)
  Checkpoint proves memory: state grew from turn 1 to turn 2
```

No API keys needed — mock LLM responses demonstrate the full graph execution loop.

## Going Live (Real LLM)

Replace the `MockLLM` in `agent_graph.py` with a real model:

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-20250514")
model_with_tools = model.bind_tools([search_web, calculator, get_time])
```

Then set `ANTHROPIC_API_KEY` in your environment and the graph runs identically — same nodes, same edges, same checkpointing — but with real LLM reasoning.

## File Overview

| File | Purpose |
|------|---------|
| `agent_graph.py` | Full agent graph implementation + 5 demo scenarios |
| `run.sh` | One-command runner (installs deps + runs demo) |
| `requirements.txt` | Python dependencies |
| `SKILL.md` | Claude skill definition (copy to `~/.claude/skills/`) |
