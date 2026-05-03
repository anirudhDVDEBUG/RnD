#!/usr/bin/env python3
"""Agentic Game NPC Demo — autonomous NPCs making decisions via tool-use."""

from __future__ import annotations
import yaml
import sys

from src.engine import build_demo_world, Entity
from src.agents import NPCProfile, run_npc_turn, _get_client

TICKS = 5
SEPARATOR = "-" * 60


def load_npcs(path: str = "config/npc_profiles.yaml") -> list[NPCProfile]:
    with open(path) as f:
        data = yaml.safe_load(f)
    return [
        NPCProfile(
            id=n["id"],
            name=n["name"],
            personality=n["personality"],
            goals=n["goals"],
            allowed_tools=n["allowed_tools"],
            x=n.get("start_x", 0),
            y=n.get("start_y", 0),
        )
        for n in data["npcs"]
    ]


def render_mini_map(world, npcs: list[NPCProfile]) -> str:
    """Render a tiny ASCII map showing NPC positions."""
    grid = [["." for _ in range(world.width)] for _ in range(world.height)]
    for eid, e in world.entities.items():
        if e.kind == "object":
            grid[e.y][e.x] = "#"
        elif e.kind == "item":
            grid[e.y][e.x] = "*"
    for npc in npcs:
        grid[npc.y][npc.x] = npc.name[0]  # First letter
    lines = ["  " + "".join(f"{i%10}" for i in range(world.width))]
    for y, row in enumerate(grid):
        lines.append(f"{y:2d} {''.join(row)}")
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("  AGENTIC GAME NPC DEMO")
    print("  NPCs make autonomous decisions using AI tool-use")
    print("=" * 60)

    # Check mode
    import os
    mode = "LIVE (Claude API)" if os.environ.get("ANTHROPIC_API_KEY") else "MOCK (no API key)"
    print(f"\n  Mode: {mode}\n")

    world = build_demo_world()
    npcs = load_npcs()

    # Register NPCs as world entities
    for npc in npcs:
        world.add_entity(Entity(npc.id, npc.name, npc.x, npc.y, "npc"))

    client = _get_client()

    print("World objects:")
    for eid, e in world.entities.items():
        if e.kind != "npc":
            print(f"  {e.name} ({e.kind}) at ({e.x}, {e.y})")
    print()
    print("NPCs:")
    for npc in npcs:
        print(f"  {npc.name} at ({npc.x}, {npc.y}) — tools: {npc.allowed_tools}")
    print()

    for tick in range(1, TICKS + 1):
        print(SEPARATOR)
        print(f"TICK {tick}")
        print(SEPARATOR)
        print(render_mini_map(world, npcs))
        print()

        for npc in npcs:
            logs = run_npc_turn(client, npc, world)
            for line in logs:
                print(line)
            print()

        world.tick()

    print(SEPARATOR)
    print("SIMULATION COMPLETE")
    print(SEPARATOR)
    print(f"\nFinal positions:")
    for npc in npcs:
        print(f"  {npc.name}: ({npc.x}, {npc.y})")
    print(f"\nFull event log ({len(world.log)} events):")
    for entry in world.log:
        print(f"  - {entry}")


if __name__ == "__main__":
    main()
