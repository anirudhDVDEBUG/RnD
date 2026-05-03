"""NPC agent: wraps an AI client to run one decision cycle per tick."""

from __future__ import annotations
import os
import json
from dataclasses import dataclass, field
from typing import Any

from src.engine import World, Entity
from src.tools import get_tools_for_npc, execute_tool


@dataclass
class NPCProfile:
    id: str
    name: str
    personality: str
    goals: list[str]
    allowed_tools: list[str]
    x: int = 0
    y: int = 0


def _get_client():
    """Return a real or mock Anthropic client."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        import anthropic
        return anthropic.Anthropic()
    else:
        from src.mock_client import MockAnthropicClient
        return MockAnthropicClient()


def run_npc_turn(client, npc: NPCProfile, world: World) -> list[str]:
    """Run one agentic decision cycle for an NPC. Returns log lines."""
    system_prompt = (
        f"You are {npc.name}, {npc.personality}.\n"
        f"Your goals: {', '.join(npc.goals)}.\n"
        f"You are at position ({npc.x}, {npc.y}) in a {world.width}x{world.height} grid world.\n"
        "Decide your next action(s) based on the current world state. "
        "Use the tools available to you. Be concise."
    )

    tools = get_tools_for_npc(npc.allowed_tools)
    world_state = world.get_state()

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=system_prompt,
        tools=tools,
        messages=[{"role": "user", "content": f"Current world state:\n{json.dumps(world_state, indent=2)}"}],
    )

    logs: list[str] = []
    for block in response.content:
        if block.type == "text" and block.text:
            logs.append(f"  [{npc.name} thinks] {block.text}")
        elif block.type == "tool_use":
            result = execute_tool(world, npc.id, block.name, block.input)
            logs.append(f"  [{npc.name}] {block.name}({json.dumps(block.input)}) -> {result}")
            # Sync NPC position if they moved
            entity = world.entities.get(npc.id)
            if entity:
                npc.x, npc.y = entity.x, entity.y

    return logs
