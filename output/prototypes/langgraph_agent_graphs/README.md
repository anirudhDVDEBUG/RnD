# LangGraph Agent Graphs

**Build resilient, stateful language agents as graphs** — with tool calling, conditional routing, checkpointing, and human-in-the-loop, all in pure Python.

LangGraph (+62 stars/day) turns agent logic into a directed graph where nodes are functions and edges define control flow. This repo demonstrates the core patterns with zero API keys required.

## Headline Result

```
User: What is LangGraph?
  [agent] Tool call -> search_web({"query": "langgraph"})
  [tools] search_web returned: LangGraph is a library for building stateful, multi-actor applications...
  [agent] Assistant: Based on my research: LangGraph is a library for building stateful,
          multi-actor applications with LLMs. It extends LangChain with cyclic graph support
          and built-in persistence.
```

5 patterns demonstrated in one script: single tool call, multi-tool parallel execution, calculator, direct response, and checkpointed memory.

## Quick Start

```bash
bash run.sh
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, skill setup, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
