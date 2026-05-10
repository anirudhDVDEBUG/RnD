#!/usr/bin/env python3
"""
demo.py — End-to-end demonstration of OpenSquilla token-efficient agent.

Run: python demo.py
No API keys needed — uses mock LLM backend.
"""

from opensquilla_agent import Agent, MCPConfig, Skill, PromptCompressor, estimate_tokens

BANNER = """
========================================================
  OpenSquilla — Token-Efficient AI Agent Demo
========================================================
"""

DIVIDER = "-" * 56


def demo_compression():
    """Show prompt compression and token savings."""
    print("\n1) PROMPT COMPRESSION")
    print(DIVIDER)

    examples = [
        (
            "I would like you to please summarize the following document "
            "about quarterly earnings for the fiscal year 2025. Could you "
            "kindly extract the key metrics and present them as bullet points? "
            "It would be great if you also highlighted any year-over-year changes.",
            64,
        ),
        (
            "Can you please help me write a Python function that takes a list "
            "of integers and returns only the even numbers? I want you to make "
            "it efficient and well-documented. Could you also add type hints?",
            48,
        ),
        (
            "Analyze customer feedback data",
            256,
        ),
    ]

    for prompt, budget in examples:
        compressed = PromptCompressor.compress(prompt, budget)
        stats = PromptCompressor.stats(prompt, compressed)
        print(f"  Original  ({stats['original_tokens']:>4} tok): {prompt[:70]}...")
        print(f"  Compressed({stats['compressed_tokens']:>4} tok): {compressed[:70]}...")
        print(f"  Savings: {stats['savings_pct']}%  |  Intelligence density: {stats['intelligence_density']}")
        print()


def demo_skills():
    """Show skill registration and dispatch."""
    print("\n2) SKILL-BASED ARCHITECTURE")
    print(DIVIDER)

    @Skill(name="summarize", description="Summarize text efficiently")
    def summarize(text: str) -> str:
        words = text.split()
        return f"[Skill:summarize] Summary ({len(words)} words input): {' '.join(words[:10])}..."

    @Skill(name="translate", description="Translate text to target language")
    def translate(text: str) -> str:
        return f"[Skill:translate] Translation requested for: {text[:50]}..."

    agent = Agent(
        name="skilled_agent",
        token_budget=256,
        skills=[summarize, translate],
    )

    prompts = [
        "Please summarize the quarterly report on cloud infrastructure spending",
        "Translate this sentence into French: Hello, how are you?",
        "What is the weather forecast for tomorrow?",
    ]

    for prompt in prompts:
        result = agent.run(prompt)
        stats = agent.get_last_stats()
        print(f"  Prompt: {prompt}")
        print(f"  Result: {result}")
        print(f"  Tokens: {stats['original_tokens']} -> {stats['compressed_tokens']} ({stats['savings_pct']}% saved)")
        print()


def demo_memory():
    """Show agent memory persistence."""
    print("\n3) AGENT MEMORY")
    print(DIVIDER)

    import tempfile, os
    mem_dir = tempfile.mkdtemp(prefix="opensquilla_mem_")

    agent = Agent(
        name="memory_agent",
        token_budget=512,
        memory_enabled=True,
        memory_path=mem_dir,
    )

    # Store facts
    agent.memory.remember("user_name", "Alice")
    agent.memory.remember("project", "TrendForge")
    agent.memory.remember("preference", "concise responses")
    print(f"  Stored {len(agent.memory.list_keys())} memory entries: {agent.memory.list_keys()}")

    # Run with memory context
    result = agent.run("What project am I working on?")
    print(f"  Query: What project am I working on?")
    print(f"  Response: {result}")
    print(f"  Memory file: {mem_dir}/memory.json")

    # Clean up
    import shutil
    shutil.rmtree(mem_dir, ignore_errors=True)
    print()


def demo_mcp_config():
    """Show MCP server configuration generation."""
    print("\n4) MCP SERVER CONFIGURATION")
    print(DIVIDER)

    servers = [
        MCPConfig(
            name="filesystem",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"],
        ),
        MCPConfig(
            name="github",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"},
        ),
    ]

    agent = Agent(name="mcp_agent", mcp_servers=servers)

    print("  Generated ~/.claude.json mcpServers config:")
    mcp_block = {}
    for srv in agent.mcp_servers:
        mcp_block.update(srv.to_claude_json())

    import json
    print(json.dumps({"mcpServers": mcp_block}, indent=4))
    print()


def demo_budget_comparison():
    """Compare token efficiency across different budgets."""
    print("\n5) TOKEN BUDGET COMPARISON")
    print(DIVIDER)

    long_prompt = (
        "I would like you to please analyze the following customer feedback data "
        "from our Q1 2025 survey. Could you kindly identify the top 5 themes, "
        "calculate sentiment scores for each theme, and provide actionable "
        "recommendations? It would be great if you also compared results with "
        "the Q4 2024 survey data. Please present everything in a structured format "
        "with bullet points and include confidence intervals where applicable."
    )

    budgets = [32, 64, 128, 256]
    print(f"  Original prompt: {estimate_tokens(long_prompt)} tokens")
    print()
    print(f"  {'Budget':>8}  {'Compressed':>12}  {'Savings':>8}  {'Density':>8}")
    print(f"  {'------':>8}  {'----------':>12}  {'-------':>8}  {'-------':>8}")

    for budget in budgets:
        compressed = PromptCompressor.compress(long_prompt, budget)
        stats = PromptCompressor.stats(long_prompt, compressed)
        print(
            f"  {budget:>8}  {stats['compressed_tokens']:>12}  "
            f"{stats['savings_pct']:>7}%  {stats['intelligence_density']:>8}"
        )
    print()


def main():
    print(BANNER)
    demo_compression()
    demo_skills()
    demo_memory()
    demo_mcp_config()
    demo_budget_comparison()

    print("========================================================")
    print("  All demos completed successfully.")
    print("  See HOW_TO_USE.md for integration instructions.")
    print("========================================================\n")


if __name__ == "__main__":
    main()
