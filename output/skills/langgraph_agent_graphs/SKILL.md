---
name: langgraph_agent_graphs
description: |
  Build resilient language agents as graphs using LangGraph.
  TRIGGER when: user asks to build an agent graph, multi-agent system, stateful LLM workflow,
  LangGraph application, or agent with tool-calling and human-in-the-loop.
  DO NOT TRIGGER when: user is using plain LangChain chains without graph structure,
  or building with a different agent framework (CrewAI, AutoGen, etc.).
---

# LangGraph Agent Graphs

Build resilient, stateful language agents as graphs with [LangGraph](https://github.com/langchain-ai/langgraph).

## When to use

- "Build a multi-agent system with LangGraph"
- "Create a stateful agent graph with tool calling"
- "Add human-in-the-loop approval to my LangGraph agent"
- "Set up a LangGraph workflow with conditional edges"
- "Implement checkpointing and memory in my agent"

## How to use

### 1. Install

```bash
pip install langgraph langchain-openai
# Or with other providers:
pip install langgraph langchain-anthropic
```

### 2. Define State

Use `TypedDict` or Pydantic to define the graph state — the data that flows between nodes.

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

### 3. Build the Graph

Add nodes (functions) and edges (transitions). Use conditional edges for branching logic.

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-20250514")

def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
```

### 4. Add Tools and Conditional Routing

```python
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

model_with_tools = model.bind_tools([search])

def agent(state: State):
    return {"messages": [model_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("agent", agent)
graph_builder.add_node("tools", ToolNode([search]))
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", tools_condition)
graph_builder.add_edge("tools", "agent")
```

### 5. Add Checkpointing (Memory)

Persist state across interactions with a checkpointer.

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Invoke with a thread_id for persistent conversations
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"messages": [{"role": "user", "content": "Hello"}]}, config)
```

### 6. Human-in-the-Loop

Add an `interrupt_before` to pause execution for human approval.

```python
graph = graph_builder.compile(
    checkpointer=memory,
    interrupt_before=["tools"],  # Pause before tool execution
)

# After review, resume with:
result = graph.invoke(None, config)  # Continue from checkpoint
```

### 7. Multi-Agent Patterns

Create subgraphs or use the prebuilt `create_react_agent` for common patterns.

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, tools=[search])
result = agent.invoke({"messages": [{"role": "user", "content": "Search for LangGraph"}]})
```

## Key Concepts

| Concept | Description |
|---|---|
| **StateGraph** | Core graph class; nodes read/write shared state |
| **Nodes** | Python functions that transform state |
| **Edges** | Define transitions; can be conditional |
| **Checkpointer** | Persists state for memory, time-travel, fault tolerance |
| **ToolNode** | Prebuilt node that executes tool calls from LLM output |
| **interrupt_before/after** | Human-in-the-loop breakpoints |
| **Subgraphs** | Nested graphs for multi-agent orchestration |

## References

- **Repository**: https://github.com/langchain-ai/langgraph
- **Documentation**: https://langchain-ai.github.io/langgraph/
- **Tutorials**: https://langchain-ai.github.io/langgraph/tutorials/
- **API Reference**: https://langchain-ai.github.io/langgraph/reference/
- **LangGraph Platform**: https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/
