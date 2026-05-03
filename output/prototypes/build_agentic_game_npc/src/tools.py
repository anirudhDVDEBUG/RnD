"""Game tools that NPCs can invoke — each maps to a world mutation."""

from __future__ import annotations
from typing import Any

from src.engine import World

# ── Tool definitions (Claude tool-use schema format) ─────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "move_npc",
        "description": "Move this NPC to a new (x, y) position in the game world.",
        "input_schema": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "Target x coordinate"},
                "y": {"type": "integer", "description": "Target y coordinate"},
            },
            "required": ["x", "y"],
        },
    },
    {
        "name": "speak",
        "description": "Say something aloud. Other characters nearby will hear it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "What to say"},
                "target": {"type": "string", "description": "Name of character to address (optional)"},
            },
            "required": ["message"],
        },
    },
    {
        "name": "interact_object",
        "description": "Interact with a nearby game-world object (e.g. open chest, use anvil).",
        "input_schema": {
            "type": "object",
            "properties": {
                "object_id": {"type": "string", "description": "ID of the object to interact with"},
                "action": {"type": "string", "description": "Action to perform: inspect, use, pickup, open"},
            },
            "required": ["object_id", "action"],
        },
    },
    {
        "name": "trade",
        "description": "Propose a trade with another character.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Name of character to trade with"},
                "offer": {"type": "string", "description": "Item being offered"},
                "request": {"type": "string", "description": "Item being requested"},
            },
            "required": ["target", "offer", "request"],
        },
    },
]


def get_tools_for_npc(allowed: list[str]) -> list[dict]:
    """Filter tool definitions to only those an NPC is permitted to use."""
    return [t for t in TOOL_DEFINITIONS if t["name"] in allowed]


# ── Tool execution ───────────────────────────────────────────────────────

def execute_tool(world: World, npc_id: str, tool_name: str, args: dict[str, Any]) -> str:
    """Execute a tool call against the world and return a result string."""
    npc = world.entities.get(npc_id)
    npc_name = npc.name if npc else npc_id

    if tool_name == "move_npc":
        return world.move_entity(npc_id, args["x"], args["y"])

    elif tool_name == "speak":
        target = args.get("target", "everyone")
        msg = f'{npc_name} says to {target}: "{args["message"]}"'
        world.log.append(msg)
        return msg

    elif tool_name == "interact_object":
        obj = world.entities.get(args["object_id"])
        if not obj:
            return f"Object {args['object_id']} not found nearby."
        msg = f"{npc_name} performs '{args['action']}' on {obj.name}"
        world.log.append(msg)
        return msg

    elif tool_name == "trade":
        msg = f"{npc_name} proposes trade to {args['target']}: offers {args['offer']} for {args['request']}"
        world.log.append(msg)
        return msg

    return f"Unknown tool: {tool_name}"
