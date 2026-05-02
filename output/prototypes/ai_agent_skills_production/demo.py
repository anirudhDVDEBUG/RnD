#!/usr/bin/env python3
"""Demo: Run all three production skills end-to-end with mock data."""

import sys
import json
sys.path.insert(0, ".")

from skills.registry import registry

# Force import of all skills to trigger registration
import skills.web_scraper  # noqa: F401
import skills.text_summarizer  # noqa: F401
import skills.data_validator  # noqa: F401


def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    print("AI Agent Skills - Production Demo")
    print("=" * 60)

    # Show registered skills
    print("\nRegistered Skills:")
    for skill in registry.list_skills():
        print(f"  - {skill['name']} v{skill['version']}: {skill['description']}")

    # --- Skill 1: Web Scraper ---
    separator("SKILL: web_scraper")

    html_content = """
    <html>
    <head><title>AI Agent Skills - Production Grade</title></head>
    <body>
        <h1>Welcome to AI Agent Skills</h1>
        <h2>Build production-grade agent capabilities</h2>
        <p>This library provides reusable skill modules for Claude, Codex, and Cursor.</p>
        <a href="https://github.com/DevelopersGlobal/ai-agent-skills">Source</a>
        <a href="https://docs.example.com/skills">Documentation</a>
        <h3>Getting Started</h3>
    </body>
    </html>
    """

    print("Input: HTML page with title, headings, and links")
    print("Action: Extract title...")
    result = registry.invoke("web_scraper", {"html": html_content, "selector": "title"})
    print(f"  Result: {result.data}")

    print("\nAction: Extract all links...")
    result = registry.invoke("web_scraper", {"html": html_content, "selector": "links"})
    print(f"  Result: {result.data}")

    print("\nAction: Extract headings...")
    result = registry.invoke("web_scraper", {"html": html_content, "selector": "headings"})
    print(f"  Result: {result.data}")

    # --- Skill 2: Text Summarizer ---
    separator("SKILL: text_summarizer")

    article = (
        "Artificial intelligence agents are transforming how developers build software. "
        "These agents can autonomously write code, debug issues, and deploy applications. "
        "Production-grade agent skills require careful error handling and validation. "
        "The DevelopersGlobal library provides reusable modules that work across multiple platforms. "
        "Each skill is self-contained with clear inputs and outputs for maximum composability. "
        "Teams using agent skills report significant productivity improvements in their workflows. "
        "The modular architecture allows skills to be combined into complex agent pipelines. "
        "Testing and observability are built into every skill from the ground up."
    )

    print(f"Input: {len(article)} chars of text ({len(article.split('.'))-1} sentences)")
    print("Action: Summarize to 2 sentences...\n")
    result = registry.invoke("text_summarizer", {"text": article, "max_sentences": 2})
    print(f"  Summary: {result.data}")
    print(f"  Metadata: {json.dumps(result.metadata, indent=4)}")

    # --- Skill 3: Data Validator ---
    separator("SKILL: data_validator")

    schema = {
        "name": {"type": "str", "required": True, "min_length": 2},
        "age": {"type": "int", "required": True, "max_value": 150},
        "email": {"type": "str", "required": True, "min_length": 5},
        "role": {"type": "str", "required": False},
    }

    # Valid data
    valid_data = {"name": "Alice", "age": 30, "email": "alice@example.com", "role": "engineer"}
    print("Test 1: Valid user data")
    result = registry.invoke("data_validator", {"data": valid_data, "schema": schema})
    print(f"  Valid: {result.data['valid']}")

    # Invalid data
    invalid_data = {"name": "A", "age": 200, "email": "x"}
    print("\nTest 2: Invalid user data (short name, age>150, short email)")
    result = registry.invoke("data_validator", {"data": invalid_data, "schema": schema})
    print(f"  Valid: {result.data['valid']}")
    print(f"  Errors:")
    for err in result.data["errors"]:
        print(f"    - {err}")

    # --- Summary ---
    separator("DEMO COMPLETE")
    print("All 3 skills executed successfully without external API keys.")
    print("Each skill follows the BaseSkill pattern: validate -> execute -> SkillResult")
    print("\nThis framework is ready for integration with Claude, Codex, or Cursor agents.")


if __name__ == "__main__":
    main()
