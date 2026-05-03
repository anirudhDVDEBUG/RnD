# Agentic Game NPC Demo

**AI-powered NPCs that autonomously decide, speak, trade, and patrol using Claude tool-use.**

Build game experiences where every NPC is backed by an AI agent that observes the world, reasons about goals, and takes structured actions via tool-use (MCP-style). Each NPC has a personality, goals, and scoped tool permissions — a guard patrols and reports, a merchant trades and explores.

## Headline Result

```
TICK 3
  01234567891011
 0 G...........
 6 ......#.....    # = Town Well
 5 ....E.......    E = Elara the Merchant
 9 ..........#.    G = Grim the Guard

  [Elara the Merchant] trade({"target":"Grim","offer":"Moonpetal Herb","request":"Iron Sword"}) -> trade proposed
  [Grim the Guard] move_npc({"x":11,"y":0}) -> moved to (11, 0)
  [Grim the Guard] speak({"message":"All clear on the northern perimeter."}) -> broadcast
```

NPCs autonomously choose actions each tick — no scripting required when using the live Claude API.

## Quick Start

```bash
bash run.sh          # runs with mock AI (no API key needed)
# or
ANTHROPIC_API_KEY=sk-... bash run.sh   # live Claude-powered NPCs
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — install, configure, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, data flow, limitations
