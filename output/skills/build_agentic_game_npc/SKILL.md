---
name: build_agentic_game_npc
description: |
  Build agentic game experiences with autonomous NPC behaviors and tool-use capabilities using Python.
  TRIGGER: user wants to create AI-driven NPCs, build agentic game engines, integrate tool-use or MCP servers into game characters, or design autonomous game agent behaviors.
---

# Build Agentic Game with AI NPCs

A skill for scaffolding and building agentic game experiences where NPCs act autonomously using AI agents and tool-use (MCP) capabilities.

## When to use

- "Build a game with AI-powered NPCs that can use tools"
- "Create autonomous NPC behaviors with agentic AI"
- "Set up an MCP server for game character tool-use"
- "Design a game engine where NPCs make decisions with AI agents"
- "Integrate Claude tool-use into game NPC logic"

## How to use

### 1. Project Setup

Create a Python project with the following structure:

```
game-project/
  src/
    engine/          # Core game loop and world state
    agents/          # NPC agent definitions and behaviors
    tools/           # Tool-use definitions (MCP tools NPCs can call)
    server/          # MCP server for exposing game tools
  config/
    npc_profiles.yaml  # NPC personality, goals, and tool permissions
  main.py
  requirements.txt
```

Install dependencies:

```bash
pip install anthropic mcp pydantic
```

### 2. Define Game Tools as MCP Server

Expose game actions (move, speak, interact, craft, trade) as MCP tools so NPCs can invoke them:

```python
from mcp.server import Server
from mcp.types import Tool

server = Server("game-tools")

@server.tool()
async def move_npc(npc_id: str, x: int, y: int) -> str:
    """Move an NPC to a position in the game world."""
    # Update world state
    return f"{npc_id} moved to ({x}, {y})"

@server.tool()
async def speak(npc_id: str, message: str, target: str | None = None) -> str:
    """Have an NPC speak to another character or broadcast."""
    return f"{npc_id} says: {message}"

@server.tool()
async def interact_object(npc_id: str, object_id: str, action: str) -> str:
    """Interact with a game world object."""
    return f"{npc_id} performed {action} on {object_id}"
```

### 3. Create NPC Agent with Autonomous Behavior

Each NPC is backed by an AI agent that observes the game world, reasons about goals, and calls tools:

```python
import anthropic

client = anthropic.Anthropic()

def run_npc_turn(npc_profile: dict, world_state: dict, available_tools: list):
    """Run one decision cycle for an NPC agent."""
    system_prompt = f"""You are {npc_profile['name']}, {npc_profile['personality']}.
    Your goals: {npc_profile['goals']}
    Decide your next action based on the current world state."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        tools=available_tools,
        messages=[{"role": "user", "content": f"World state: {world_state}"}]
    )
    return response
```

### 4. Game Loop Integration

Run NPC agents each tick within your game loop:

```python
async def game_loop(world, npcs):
    while world.running:
        world_state = world.get_state()
        for npc in npcs:
            response = run_npc_turn(npc.profile, world_state, npc.tools)
            for block in response.content:
                if block.type == "tool_use":
                    result = await execute_tool(block.name, block.input)
                    world.apply(result)
        world.tick()
```

### 5. NPC Profile Configuration

Define NPC personalities and tool access in YAML:

```yaml
npcs:
  - name: "Elara the Merchant"
    personality: "A shrewd but fair trader who values rare items."
    goals:
      - "Acquire rare crafting materials through trade"
      - "Build relationships with adventurers"
    allowed_tools: ["speak", "trade", "interact_object"]
  - name: "Grim the Guard"
    personality: "A vigilant guard who patrols the town perimeter."
    goals:
      - "Protect the town from threats"
      - "Report suspicious activity"
    allowed_tools: ["move_npc", "speak", "interact_object"]
```

### Key Design Principles

- **Tool-use as actions**: Every game action an NPC can take is an MCP tool, giving the AI structured ways to affect the world.
- **Scoped permissions**: Each NPC only has access to tools matching their role (guards can patrol, merchants can trade).
- **World-state observation**: NPCs receive current game state as context for decision-making.
- **Agentic loops**: NPCs run multi-step reasoning — observe, plan, act — each game tick.

## References

- Source repository: [KennethanCeyer/build-game-with-ai](https://github.com/KennethanCeyer/build-game-with-ai)
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
