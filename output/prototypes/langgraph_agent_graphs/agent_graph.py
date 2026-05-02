"""
LangGraph Agent Graph Demo

Demonstrates building a stateful, tool-calling agent as a graph using LangGraph.
Includes: state management, conditional routing, tool execution, checkpointing,
and human-in-the-loop patterns — all with mock LLM responses (no API key needed).
"""

from __future__ import annotations

import json
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


# ---------------------------------------------------------------------------
# 1. Define graph state
# ---------------------------------------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ---------------------------------------------------------------------------
# 2. Mock tools (no API key required)
# ---------------------------------------------------------------------------

TOOL_REGISTRY: dict[str, callable] = {}


def register_tool(fn):
    TOOL_REGISTRY[fn.__name__] = fn
    return fn


@register_tool
def search_web(query: str) -> str:
    """Search the web for information."""
    mock_results = {
        "langgraph": "LangGraph is a library for building stateful, multi-actor applications with LLMs. "
                     "It extends LangChain with cyclic graph support and built-in persistence.",
        "weather": "Current weather: 72F / 22C, partly cloudy, humidity 45%.",
        "python": "Python 3.12 is the latest stable release with improved error messages and performance.",
    }
    for key, val in mock_results.items():
        if key in query.lower():
            return val
    return f"Search results for '{query}': No specific results found."


@register_tool
def calculator(expression: str) -> str:
    """Evaluate a math expression safely."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: Only numeric expressions with +, -, *, / are allowed."
    try:
        result = eval(expression, {"__builtins__": {}})  # noqa: S307
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@register_tool
def get_time(timezone: str = "UTC") -> str:
    """Get the current time in a timezone."""
    from datetime import datetime, timezone as tz
    now = datetime.now(tz.utc).strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time ({timezone}): {now}"


# ---------------------------------------------------------------------------
# 3. Mock LLM that produces AIMessage objects with tool_calls
# ---------------------------------------------------------------------------

SCENARIOS = {
    "tool_use": [
        AIMessage(
            content="",
            tool_calls=[{"name": "search_web", "args": {"query": "langgraph"}, "id": "call_1"}],
        ),
        AIMessage(
            content="Based on my research: LangGraph is a library for building stateful, "
                    "multi-actor applications with LLMs. It extends LangChain with cyclic "
                    "graph support and built-in persistence. It's great for building complex "
                    "agent workflows!",
        ),
    ],
    "multi_tool": [
        AIMessage(
            content="",
            tool_calls=[
                {"name": "search_web", "args": {"query": "weather"}, "id": "call_2a"},
                {"name": "get_time", "args": {"timezone": "US/Eastern"}, "id": "call_2b"},
            ],
        ),
        AIMessage(
            content="Here's your briefing:\n- Weather: 72F / 22C, partly cloudy\n"
                    "- Time (US/Eastern): see above\nHave a great day!",
        ),
    ],
    "calculation": [
        AIMessage(
            content="",
            tool_calls=[{"name": "calculator", "args": {"expression": "(12 * 8) + 15 / 3"}, "id": "call_3"}],
        ),
        AIMessage(content="The result of (12 * 8) + 15 / 3 is 101.0."),
    ],
    "direct": [
        AIMessage(
            content="Hello! I'm a LangGraph-powered agent. I can search the web, do math, "
                    "and tell the time. How can I help you?",
        ),
    ],
}

# Module-level mock LLM state — set before each scenario run
_mock_turns: list[AIMessage] = []
_mock_index: int = 0


def _reset_mock(scenario_key: str):
    global _mock_turns, _mock_index
    _mock_turns = list(SCENARIOS[scenario_key])
    _mock_index = 0


def _mock_invoke(messages: list) -> AIMessage:
    global _mock_index
    if _mock_index >= len(_mock_turns):
        return AIMessage(content="Done.")
    turn = _mock_turns[_mock_index]
    _mock_index += 1
    return turn


# ---------------------------------------------------------------------------
# 4. Graph nodes
# ---------------------------------------------------------------------------

def agent_node(state: AgentState) -> dict:
    """The agent node invokes the (mock) LLM and returns the response."""
    response = _mock_invoke(state["messages"])
    return {"messages": [response]}


def tool_node(state: AgentState) -> dict:
    """Execute tool calls from the last AI message."""
    last_msg = state["messages"][-1]
    results = []
    for tc in last_msg.tool_calls:
        fn = TOOL_REGISTRY.get(tc["name"])
        if fn:
            output = fn(**tc["args"])
        else:
            output = f"Unknown tool: {tc['name']}"
        results.append(ToolMessage(content=output, tool_call_id=tc["id"], name=tc["name"]))
    return {"messages": results}


# ---------------------------------------------------------------------------
# 5. Conditional routing
# ---------------------------------------------------------------------------

def should_call_tools(state: AgentState) -> Literal["tools", "end"]:
    """Route to tools if the last message contains tool calls, else end."""
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return "end"


# ---------------------------------------------------------------------------
# 6. Build the graph
# ---------------------------------------------------------------------------

def build_agent_graph(checkpointer=None):
    """Construct and compile the agent graph."""
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", should_call_tools, {"tools": "tools", "end": END})
    builder.add_edge("tools", "agent")
    return builder.compile(checkpointer=checkpointer)


# ---------------------------------------------------------------------------
# 7. Run demos
# ---------------------------------------------------------------------------

def print_separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def run_scenario(name: str, scenario_key: str, user_message: str, graph):
    """Run a single scenario and print the trace."""
    print_separator(name)
    print(f"\nUser: {user_message}\n")

    _reset_mock(scenario_key)
    initial_state = {"messages": [HumanMessage(content=user_message)]}

    for step in graph.stream(initial_state, stream_mode="updates"):
        for node_name, update in step.items():
            for m in update.get("messages", []):
                if isinstance(m, AIMessage):
                    if m.tool_calls:
                        for tc in m.tool_calls:
                            print(f"  [{node_name}] Tool call -> {tc['name']}({json.dumps(tc['args'])})")
                    elif m.content:
                        print(f"  [{node_name}] Assistant: {m.content}")
                elif isinstance(m, ToolMessage):
                    print(f"  [{node_name}] {m.name} returned: {m.content}")
    print()


def main():
    print("=" * 60)
    print("  LangGraph Agent Graph Demo")
    print("  Build resilient language agents as graphs")
    print("=" * 60)

    graph = build_agent_graph()

    # Demo 1: Tool use (search)
    run_scenario(
        "Demo 1: Single Tool Call (Web Search)",
        "tool_use",
        "What is LangGraph?",
        graph,
    )

    # Demo 2: Multi-tool
    run_scenario(
        "Demo 2: Multi-Tool Call (Weather + Time)",
        "multi_tool",
        "What's the weather and current time?",
        graph,
    )

    # Demo 3: Calculator
    run_scenario(
        "Demo 3: Calculator Tool",
        "calculation",
        "What is (12 * 8) + 15 / 3?",
        graph,
    )

    # Demo 4: Direct response (no tools)
    run_scenario(
        "Demo 4: Direct Response (No Tools)",
        "direct",
        "Hello!",
        graph,
    )

    # Demo 5: Checkpointing / Memory
    print_separator("Demo 5: Checkpointing (Persistent Memory)")
    memory = MemorySaver()
    graph_with_memory = build_agent_graph(checkpointer=memory)
    config = {"configurable": {"thread_id": "demo-thread-1"}}

    print("\n  Checkpointer: MemorySaver (in-memory)")
    print("  Thread ID: demo-thread-1")

    _reset_mock("direct")
    result = graph_with_memory.invoke(
        {"messages": [HumanMessage(content="Remember my name is Alice")]},
        config=config,
    )
    print(f"  Turn 1 -> {len(result['messages'])} messages in state")

    _reset_mock("direct")
    result2 = graph_with_memory.invoke(
        {"messages": [HumanMessage(content="What is my name?")]},
        config=config,
    )
    print(f"  Turn 2 -> {len(result2['messages'])} messages in state (includes history)")
    print("  Checkpoint proves memory: state grew from turn 1 to turn 2")

    # Summary
    print_separator("Summary")
    print("""
  This demo showed 5 LangGraph patterns:
    1. Single tool call with conditional routing
    2. Parallel multi-tool execution
    3. Calculator tool with safe evaluation
    4. Direct LLM response (no tool needed)
    5. Checkpointed memory across turns

  All running WITHOUT an API key (mock LLM).
  Swap MockLLM for ChatAnthropic or ChatOpenAI to go live.
""")


if __name__ == "__main__":
    main()
