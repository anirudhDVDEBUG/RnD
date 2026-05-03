# How to Use

## Install

```bash
git clone <this-repo> && cd build_agentic_game_npc
pip install -r requirements.txt
```

Only `pyyaml` is needed for the mock demo. `anthropic` is needed for live mode.

## Run

```bash
bash run.sh
```

This runs 5 ticks of a game simulation with two NPCs (Elara the Merchant, Grim the Guard) making autonomous decisions. Without an `ANTHROPIC_API_KEY`, it uses a mock client with scripted behaviours that exercise every tool type.

For live AI-powered NPCs:

```bash
ANTHROPIC_API_KEY=sk-ant-... bash run.sh
```

## As a Claude Skill

Drop the skill definition into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/build_agentic_game_npc
cp SKILL.md ~/.claude/skills/build_agentic_game_npc/SKILL.md
```

**Trigger phrases:**
- "Build a game with AI-powered NPCs that can use tools"
- "Create autonomous NPC behaviors with agentic AI"
- "Set up an MCP server for game character tool-use"
- "Design a game engine where NPCs make decisions with AI agents"
- "Integrate Claude tool-use into game NPC logic"

When triggered, Claude will scaffold a project structure with engine, agents, tools, and NPC profiles following the patterns in this demo.

## First 60 Seconds

1. Run `bash run.sh`
2. Watch the ASCII map update each tick as NPCs move
3. Read the action log — each NPC thinks, then calls tools (move, speak, trade, interact)
4. Open `config/npc_profiles.yaml` — change a personality or add a new NPC
5. Run again to see different behaviour

**Example output (tick 1):**

```
TICK 1
  0123456789AB
 0 G...........
 2 ........*...
 3 ..*#........
 5 ....E.......
 6 ......#.....
 9 ..........#.

  [Elara the Merchant thinks] I should check the well for travelers to trade with.
  [Elara the Merchant] move_npc({"x": 6, "y": 6}) -> Elara the Merchant moved from (4, 5) to (6, 6)

  [Grim the Guard thinks] Time to begin my patrol route.
  [Grim the Guard] move_npc({"x": 0, "y": 0}) -> Grim the Guard moved from (0, 0) to (0, 0)
```

## Customisation

### Add a new NPC

Edit `config/npc_profiles.yaml`:

```yaml
  - id: luna
    name: "Luna the Healer"
    personality: "A gentle healer who tends to the wounded and gathers herbs."
    goals:
      - "Find and collect healing herbs"
      - "Heal injured characters"
    allowed_tools:
      - move_npc
      - speak
      - interact_object
    start_x: 8
    start_y: 2
```

### Add a new tool

1. Add the tool schema to `TOOL_DEFINITIONS` in `src/tools.py`
2. Add the execution logic to `execute_tool()` in the same file
3. Add the tool name to the NPC's `allowed_tools` in the YAML config
