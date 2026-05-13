"""Create a sample SQLite database for the Datasette demo."""
import sqlite3
import os
import json
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "demo.db")


def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table 1: AI tools catalog
    c.execute("""
        CREATE TABLE ai_tools (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            stars INTEGER,
            language TEXT,
            description TEXT,
            last_updated TEXT
        )
    """)

    tools = [
        ("Claude Code", "coding-agent", 15200, "TypeScript", "Agentic coding tool from Anthropic", "2026-05-12"),
        ("Datasette", "data-exploration", 9800, "Python", "Explore and publish SQLite databases", "2026-05-12"),
        ("LangChain", "framework", 98000, "Python", "Framework for LLM application development", "2026-05-11"),
        ("Ollama", "local-inference", 112000, "Go", "Run LLMs locally", "2026-05-10"),
        ("Cursor", "coding-agent", 5400, "TypeScript", "AI-first code editor", "2026-05-09"),
        ("CrewAI", "agent-framework", 24000, "Python", "Multi-agent orchestration framework", "2026-05-08"),
        ("AutoGen", "agent-framework", 38000, "Python", "Microsoft multi-agent conversation framework", "2026-05-07"),
        ("Dify", "platform", 52000, "TypeScript", "Open-source LLM app development platform", "2026-05-06"),
        ("Open WebUI", "local-inference", 67000, "Svelte", "Self-hosted WebUI for LLMs", "2026-05-05"),
        ("Haystack", "framework", 18000, "Python", "LLM orchestration framework by deepset", "2026-05-04"),
        ("MCP Servers", "mcp", 21000, "TypeScript", "Model Context Protocol server implementations", "2026-05-12"),
        ("Aider", "coding-agent", 28000, "Python", "AI pair programming in the terminal", "2026-05-11"),
    ]

    c.executemany(
        "INSERT INTO ai_tools (name, category, stars, language, description, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
        tools,
    )

    # Table 2: Daily trend signals
    c.execute("""
        CREATE TABLE trend_signals (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            tool_name TEXT NOT NULL,
            signal_type TEXT NOT NULL,
            value REAL,
            source TEXT
        )
    """)

    signal_types = ["github_stars_delta", "hacker_news_mentions", "reddit_mentions", "twitter_mentions"]
    sources = ["github-api", "hn-algolia", "reddit-api", "twitter-api"]
    base_date = datetime(2026, 5, 1)

    signals = []
    for day_offset in range(12):
        date = (base_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for tool_name, _, stars, _, _, _ in tools:
            for sig_type, source in zip(signal_types, sources):
                value = round(random.uniform(0, stars / 1000), 1)
                signals.append((date, tool_name, sig_type, value, source))

    c.executemany(
        "INSERT INTO trend_signals (date, tool_name, signal_type, value, source) VALUES (?, ?, ?, ?, ?)",
        signals,
    )

    # Table 3: Empty table (demonstrates 1.0a29 fix - headers show on empty tables)
    c.execute("""
        CREATE TABLE upcoming_reviews (
            id INTEGER PRIMARY KEY,
            tool_name TEXT,
            scheduled_date TEXT,
            reviewer TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)

    conn.commit()
    conn.close()
    print(f"Created demo database: {DB_PATH}")
    print(f"  - ai_tools: {len(tools)} rows")
    print(f"  - trend_signals: {len(signals)} rows")
    print(f"  - upcoming_reviews: 0 rows (tests 1.0a29 empty-table fix)")


if __name__ == "__main__":
    create_database()
