"""Demo: Tool-calling agent with a calculator tool."""

from langchain_core.tools import tool
from mock_llm import MockChatModel


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression safely."""
    # Only allow digits and basic math operators
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: invalid characters in expression"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def main():
    print("=== Tool-Calling Agent Demo ===")

    # Simulate the agent loop:
    # 1. User asks a question
    # 2. Agent decides to call calculator tool
    # 3. Tool returns result
    # 4. Agent formulates final answer

    user_question = "What is 42 * 17?"

    # Step 1: Agent recognizes this needs calculation
    tool_call_expression = "42 * 17"

    # Step 2: Execute the tool
    tool_result = calculator.invoke(tool_call_expression)
    print(f"Agent called: calculator(\"{tool_call_expression}\") -> {tool_result}")

    # Step 3: Agent produces final answer using LLM
    llm = MockChatModel()
    from langchain_core.messages import HumanMessage
    response = llm.invoke([HumanMessage(content=f"42 * 17")])
    print(f"Final answer: {response.content}")
    print()


if __name__ == "__main__":
    main()
