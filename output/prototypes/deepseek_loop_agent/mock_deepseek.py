"""
Mock DeepSeek client for offline demos and a real client for live use.

The mock simulates a multi-turn agent session: the LLM "decides" to use tools
and then produces a final answer — without requiring an API key.
"""

import json
import os
from typing import Any, Optional


class MockDeepSeekClient:
    """
    Simulates DeepSeek API responses for a scripted demo.
    Shows the agent loop pattern: text → tool_call → tool_result → text.
    """

    def __init__(self, model: str = "deepseek-chat"):
        self.model = model
        self.turn = 0
        self._scenario = self._build_scenario()

    def _build_scenario(self) -> list[dict]:
        """Pre-scripted scenario: analyze a Python file, then summarize."""
        return [
            # Turn 0: Agent decides to read a file
            {
                "content": "Let me start by reading the project files to understand the codebase.",
                "tool_calls": [
                    {
                        "id": "call_001",
                        "name": "glob",
                        "arguments": {"pattern": "*.py", "path": "."},
                    }
                ],
            },
            # Turn 1: Agent greps for key patterns
            {
                "content": "Found the Python files. Let me check the main module structure.",
                "tool_calls": [
                    {
                        "id": "call_002",
                        "name": "file_read",
                        "arguments": {"path": "tools.py", "limit": 15},
                    }
                ],
            },
            # Turn 2: Agent runs a command
            {
                "content": "Let me check the Python version and verify the environment.",
                "tool_calls": [
                    {
                        "id": "call_003",
                        "name": "bash",
                        "arguments": {"command": "python3 --version && echo 'Environment OK'"},
                    }
                ],
            },
            # Turn 3: Final answer (no tool calls)
            {
                "content": (
                    "\n--- Agent Analysis Complete ---\n"
                    "\n"
                    "## Codebase Summary\n"
                    "\n"
                    "This project implements a **Claude-Code-shaped agent loop** over the DeepSeek API.\n"
                    "\n"
                    "**Key components:**\n"
                    "- `deepseek_loop.py` — Core agent loop with SdkMessage streaming\n"
                    "- `tools.py` — Built-in tools (file_read, file_write, bash, grep, glob)\n"
                    "- `mock_deepseek.py` — Mock client for offline demos\n"
                    "- `cron_scheduler.py` — Cron-based recurring task scheduler\n"
                    "\n"
                    "**Architecture:** The loop follows the pattern:\n"
                    "  prompt → DeepSeek chat → tool calls → execute tools → feed results back → repeat\n"
                    "\n"
                    "**Permission modes:** ASK (prompt user), ALLOW_READ, ALLOW_BASH, ALLOW_ALL\n"
                    "\n"
                    "This mirrors the Claude Code agent pattern but swaps in DeepSeek as the LLM backend, "
                    "making it useful for cost-sensitive deployments or DeepSeek-specific model capabilities.\n"
                ),
                "tool_calls": [],
            },
        ]

    def chat(self, messages: list[dict]) -> dict:
        """Return the next scripted response."""
        if self.turn < len(self._scenario):
            response = self._scenario[self.turn]
            self.turn += 1
            return response
        # Fallback: return a done message
        return {"content": "(Agent loop complete)", "tool_calls": []}


class DeepSeekClient:
    """
    Real DeepSeek API client. Requires DEEPSEEK_API_KEY.
    Uses the OpenAI-compatible chat/completions endpoint.
    """

    API_URL = "https://api.deepseek.com/v1/chat/completions"

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model

    def chat(self, messages: list[dict]) -> dict:
        """Call the DeepSeek API and return parsed response."""
        import urllib.request

        # Build tool definitions for the API
        tools_schema = [
            {
                "type": "function",
                "function": {
                    "name": "file_read",
                    "description": "Read a file's contents",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "limit": {"type": "integer", "default": 200},
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "file_write",
                    "description": "Write content to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["path", "content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "bash",
                    "description": "Execute a bash command",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string"},
                            "timeout": {"type": "integer", "default": 30},
                        },
                        "required": ["command"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "grep",
                    "description": "Search for a text pattern in files",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string"},
                            "path": {"type": "string", "default": "."},
                        },
                        "required": ["pattern"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "glob",
                    "description": "Find files matching a glob pattern",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string"},
                            "path": {"type": "string", "default": "."},
                        },
                        "required": ["pattern"],
                    },
                },
            },
        ]

        # Clean messages for API (remove internal fields)
        clean_messages = []
        for msg in messages:
            clean = {"role": msg["role"], "content": msg.get("content", "")}
            if "tool_calls" in msg:
                clean["tool_calls"] = [
                    {
                        "id": tc.get("id", ""),
                        "type": "function",
                        "function": {"name": tc["name"], "arguments": json.dumps(tc["arguments"])},
                    }
                    for tc in msg["tool_calls"]
                ]
            if "tool_call_id" in msg:
                clean["tool_call_id"] = msg["tool_call_id"]
            clean_messages.append(clean)

        payload = json.dumps({
            "model": self.model,
            "messages": clean_messages,
            "tools": tools_schema,
            "stream": False,
        }).encode()

        req = urllib.request.Request(
            self.API_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())

        choice = data["choices"][0]
        message = choice["message"]

        result = {"content": message.get("content", ""), "tool_calls": []}
        if message.get("tool_calls"):
            for tc in message["tool_calls"]:
                result["tool_calls"].append({
                    "id": tc["id"],
                    "name": tc["function"]["name"],
                    "arguments": json.loads(tc["function"]["arguments"]),
                })

        return result
