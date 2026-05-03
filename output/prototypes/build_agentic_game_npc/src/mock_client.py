"""Mock Anthropic client that simulates tool-use responses for demo purposes.

This lets `bash run.sh` work without an API key. Each NPC has scripted
behaviours that exercise different tools so the output is interesting.
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolUseBlock:
    type: str = "tool_use"
    id: str = ""
    name: str = ""
    input: dict = field(default_factory=dict)


@dataclass
class TextBlock:
    type: str = "text"
    text: str = ""


@dataclass
class MockResponse:
    content: list = field(default_factory=list)
    stop_reason: str = "end_turn"


# ── Scripted behaviour per NPC ───────────────────────────────────────────

_SCRIPTS: dict[str, list[list[Any]]] = {
    "elara": [
        [
            TextBlock(text="I should check the well for travelers to trade with."),
            ToolUseBlock(id="t1", name="move_npc", input={"x": 6, "y": 6}),
        ],
        [
            TextBlock(text="Ah, a fellow adventurer! Let me offer a deal."),
            ToolUseBlock(id="t2", name="speak", input={"message": "Greetings! I have rare herbs for trade.", "target": "Grim the Guard"}),
        ],
        [
            ToolUseBlock(id="t3", name="trade", input={"target": "Grim the Guard", "offer": "Moonpetal Herb", "request": "Iron Sword"}),
        ],
        [
            TextBlock(text="Let me inspect what's in that chest."),
            ToolUseBlock(id="t4", name="interact_object", input={"object_id": "chest", "action": "inspect"}),
        ],
        [
            ToolUseBlock(id="t5", name="speak", input={"message": "The chest is locked... I'll need a key. Until next time!"}),
        ],
    ],
    "grim": [
        [
            TextBlock(text="Time to begin my patrol route."),
            ToolUseBlock(id="t1", name="move_npc", input={"x": 0, "y": 0}),
        ],
        [
            ToolUseBlock(id="t2", name="move_npc", input={"x": 11, "y": 0}),
            ToolUseBlock(id="t3", name="speak", input={"message": "All clear on the northern perimeter."}),
        ],
        [
            ToolUseBlock(id="t4", name="move_npc", input={"x": 11, "y": 11}),
        ],
        [
            TextBlock(text="I see the merchant near the well. I should check in."),
            ToolUseBlock(id="t5", name="move_npc", input={"x": 6, "y": 6}),
            ToolUseBlock(id="t6", name="speak", input={"message": "Elara, have you seen anything suspicious today?", "target": "Elara the Merchant"}),
        ],
        [
            ToolUseBlock(id="t7", name="interact_object", input={"object_id": "chest", "action": "inspect"}),
            ToolUseBlock(id="t8", name="speak", input={"message": "This chest should stay locked. I'll keep watch."}),
        ],
    ],
}

_counters: dict[str, int] = {}


class MockAnthropicMessages:
    """Drop-in replacement for anthropic.Anthropic().messages."""

    def create(self, *, model: str, max_tokens: int, system: str, tools: list, messages: list, **kw) -> MockResponse:
        # Determine which NPC from the system prompt
        npc_key = "grim" if "grim" in system.lower() else "elara"
        idx = _counters.get(npc_key, 0)
        script = _SCRIPTS[npc_key]
        blocks = script[idx % len(script)]
        _counters[npc_key] = idx + 1
        return MockResponse(content=list(blocks))


class MockAnthropicClient:
    """Mimics anthropic.Anthropic() interface."""

    def __init__(self, **kw):
        self.messages = MockAnthropicMessages()
