"""Concrete agent implementations using mock LLM calls."""

from __future__ import annotations

import random
import time
from typing import Any

from agents.base import Agent


class ResearchAgent(Agent):
    name = "research"
    description = "Searches and summarises information on a topic"
    task_types = ["research", "search"]

    def execute(self, task: dict[str, Any]) -> Any:
        topic = task.get("payload", "general AI")
        time.sleep(0.3)  # simulate latency
        findings = [
            f"Found 12 recent papers on '{topic}'",
            f"Top insight: {topic} adoption grew 40% YoY",
            f"Key risk: data quality remains the bottleneck for {topic}",
        ]
        return {"topic": topic, "findings": findings}


class CodeAgent(Agent):
    name = "coder"
    description = "Generates or reviews code snippets"
    task_types = ["code", "review"]

    def execute(self, task: dict[str, Any]) -> Any:
        payload = task.get("payload", "hello world")
        time.sleep(0.2)
        templates = {
            "sort": "def sort_list(xs):\n    return sorted(xs)",
            "hello": 'print("Hello, PRTS!")',
            "fib": "def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a",
        }
        # pick closest template or generate stub
        code = templates.get(payload, f"# stub for: {payload}\npass")
        return {"language": "python", "code": code}


class SummaryAgent(Agent):
    name = "summarizer"
    description = "Condenses long text into a brief summary"
    task_types = ["summarize", "digest"]

    def execute(self, task: dict[str, Any]) -> Any:
        text = task.get("payload", "")
        time.sleep(0.15)
        word_count = len(text.split()) if text else 0
        summary = (
            text[:120] + "..." if len(text) > 120 else text
        ) or "(empty input)"
        return {
            "original_words": word_count,
            "summary": f"[Summary] {summary}",
            "compression": f"{max(1, word_count)}→{len(summary.split())} words",
        }
