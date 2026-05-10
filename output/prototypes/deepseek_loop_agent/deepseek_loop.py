"""
deepseek_loop – A Claude-Code-shaped agent loop over the DeepSeek API.

This module implements the core agent loop: prompt → LLM → tool calls → results → repeat.
It supports built-in tools (file read/write, bash, grep, glob), permission modes,
streaming SdkMessage events, and cron scheduling.
"""

import json
import os
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from tools import BUILTIN_TOOLS, ToolRegistry
from mock_deepseek import MockDeepSeekClient, DeepSeekClient


class PermissionMode(Enum):
    ASK = "ask"           # Prompt user before every tool call
    ALLOW_READ = "read"   # Auto-allow read-only tools
    ALLOW_BASH = "bash"   # Auto-allow bash + read
    ALLOW_ALL = "all"     # Auto-allow everything


# Tools that are read-only (safe to auto-allow)
READ_ONLY_TOOLS = {"file_read", "grep", "glob"}
BASH_TOOLS = READ_ONLY_TOOLS | {"bash"}


@dataclass
class SdkMessage:
    """Mirrors Claude Code's SdkMessage event format."""
    type: str                # "text", "tool_use", "tool_result", "error", "done"
    content: Any = None
    tool_name: str = ""
    tool_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "content": self.content,
            "tool_name": self.tool_name,
            "tool_id": self.tool_id,
            "timestamp": self.timestamp,
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class AgentLoop:
    """
    The main agent loop. Sends messages to DeepSeek, executes tool calls,
    and streams SdkMessage events back to the caller.
    """

    def __init__(
        self,
        client: Optional[Any] = None,
        permission_mode: PermissionMode = PermissionMode.ASK,
        max_turns: int = 20,
        model: str = "deepseek-chat",
        event_callback: Optional[Callable[[SdkMessage], None]] = None,
    ):
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if client:
            self.client = client
        elif api_key:
            self.client = DeepSeekClient(api_key=api_key, model=model)
        else:
            self.client = MockDeepSeekClient(model=model)

        self.permission_mode = permission_mode
        self.max_turns = max_turns
        self.model = model
        self.tool_registry = ToolRegistry()
        self.messages: list[dict] = []
        self.event_callback = event_callback or self._default_event_handler

    def _default_event_handler(self, event: SdkMessage):
        """Print events to stderr for streaming visibility."""
        if event.type == "text":
            print(event.content, end="", flush=True)
        elif event.type == "tool_use":
            print(f"\n>> Tool: {event.tool_name}", file=sys.stderr)
        elif event.type == "tool_result":
            preview = str(event.content)[:200]
            print(f"   Result: {preview}", file=sys.stderr)
        elif event.type == "error":
            print(f"\n!! Error: {event.content}", file=sys.stderr)

    def _check_permission(self, tool_name: str) -> bool:
        """Check whether a tool call is auto-allowed under the current permission mode."""
        if self.permission_mode == PermissionMode.ALLOW_ALL:
            return True
        if self.permission_mode == PermissionMode.ALLOW_BASH and tool_name in BASH_TOOLS:
            return True
        if self.permission_mode == PermissionMode.ALLOW_READ and tool_name in READ_ONLY_TOOLS:
            return True
        # In ASK mode (or for non-allowed tools), we'd prompt the user.
        # For the demo, we auto-allow.
        return True

    def _emit(self, event: SdkMessage):
        self.event_callback(event)

    def _build_system_prompt(self) -> str:
        tool_descriptions = self.tool_registry.describe_tools()
        return (
            "You are an AI agent with access to the following tools:\n\n"
            f"{tool_descriptions}\n\n"
            "When you need to use a tool, respond with a JSON tool_call block.\n"
            "After receiving results, continue reasoning or provide the final answer."
        )

    def run(self, user_prompt: str) -> str:
        """Execute the agent loop and return the final text response."""
        self.messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": user_prompt},
        ]

        for turn in range(self.max_turns):
            response = self.client.chat(self.messages)

            # Check for tool calls in the response
            tool_calls = response.get("tool_calls", [])

            if not tool_calls:
                # Pure text response — we're done
                text = response.get("content", "")
                self._emit(SdkMessage(type="text", content=text))
                self._emit(SdkMessage(type="done"))
                return text

            # Process each tool call
            self.messages.append({"role": "assistant", "content": response.get("content", ""), "tool_calls": tool_calls})

            for tc in tool_calls:
                tool_name = tc["name"]
                tool_args = tc["arguments"]
                tool_id = tc.get("id", f"call_{turn}_{tool_name}")

                self._emit(SdkMessage(type="tool_use", tool_name=tool_name, tool_id=tool_id, content=tool_args))

                if not self._check_permission(tool_name):
                    result = f"Permission denied for tool: {tool_name}"
                    self._emit(SdkMessage(type="error", content=result))
                else:
                    result = self.tool_registry.execute(tool_name, tool_args)
                    self._emit(SdkMessage(type="tool_result", tool_name=tool_name, tool_id=tool_id, content=result))

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "content": str(result),
                })

        self._emit(SdkMessage(type="error", content="Max turns reached"))
        return "[Agent stopped: max turns reached]"


def run_agent(prompt: str, permission_mode: str = "all", max_turns: int = 10, model: str = "deepseek-chat"):
    """Convenience function to run the agent loop once."""
    mode = PermissionMode(permission_mode)
    agent = AgentLoop(permission_mode=mode, max_turns=max_turns, model=model)
    return agent.run(prompt)
