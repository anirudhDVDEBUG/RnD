# Technical Details

## What It Does

This is a minimal game engine where NPCs are autonomous AI agents. Each game tick, every NPC receives the current world state as context, reasons about its goals, and emits tool-use calls (move, speak, trade, interact) that mutate the shared world. The architecture mirrors how you'd build an MCP-powered game server: game actions are exposed as structured tools, and the AI chooses which to invoke based on personality and goals.

The demo includes a mock client for zero-dependency runs and seamlessly switches to the live Anthropic API when a key is provided.

## Architecture

```
main.py                  Entry point, game loop
config/npc_profiles.yaml NPC definitions (personality, goals, tool permissions)
src/
  engine.py              World state, entity management, grid, tick counter
  tools.py               Tool definitions (Claude tool-use schema) + execution
  agents.py              NPC agent: builds prompt, calls client, processes tool-use blocks
  mock_client.py         Scripted mock that returns tool_use blocks without API calls
```

### Data Flow (per tick)

```
World.get_state() -> JSON snapshot
    |
    v
agents.run_npc_turn()
    |-- Build system prompt from NPC profile (personality, goals, position)
    |-- Send world state + tools to Claude (or mock)
    |-- Receive response with TextBlock / ToolUseBlock items
    |-- For each ToolUseBlock: call tools.execute_tool() -> mutate world
    v
World.tick() -> increment counter, next NPC
```

### Key Design Decisions

- **Tools as structured actions**: Every game action is a Claude tool-use definition with JSON schema. This gives the AI constrained, type-safe ways to affect the world — no free-form string parsing.
- **Scoped permissions**: Each NPC only sees tools matching their `allowed_tools` list. A merchant can trade but not patrol; a guard can move but not trade.
- **Stateless per-tick**: Each NPC decision is a single `messages.create` call with the full world state. No conversation history is maintained between ticks (though you could add it).
- **Swap-in real AI**: The mock client returns the same `ToolUseBlock`/`TextBlock` dataclasses, so switching to the real Anthropic SDK requires only setting an env var.

### Dependencies

| Package | Purpose | Required for demo? |
|---------|---------|-------------------|
| `pyyaml` | Parse NPC config | Yes |
| `anthropic` | Claude API client | Only for live mode |

### Model Calls

- One `messages.create` call per NPC per tick
- Uses `claude-sonnet-4-6` with tool-use
- `max_tokens=512` per call (NPCs should be terse)
- With 2 NPCs and 5 ticks = 10 API calls per run in live mode

## Limitations

- **No memory between ticks**: NPCs don't remember previous decisions. Each tick is a fresh prompt with only the current world state. Adding a conversation buffer or summary would improve coherence.
- **No multi-turn tool-use**: The current loop processes one response per NPC per tick. Real agentic behaviour would re-prompt after tool results for multi-step reasoning.
- **No collision/physics**: The grid is cosmetic. NPCs can overlap and there's no pathfinding or line-of-sight.
- **No NPC-to-NPC interaction resolution**: Trades are logged but not actually resolved (no inventory system).
- **Mock is deterministic**: The scripted mock always plays the same sequence, useful for testing but not for showing emergent behaviour.

## Why This Matters for Claude-Driven Products

- **Agent factories**: This is the pattern for any system where multiple AI agents share a world — customer service bots in a CRM, ad-creative agents bidding on placements, marketing agents managing campaign channels.
- **Tool-use as product API**: Exposing your product's actions as Claude tools lets AI agents operate within your system's constraints. The NPC permission model directly maps to role-based access control in SaaS products.
- **MCP server pattern**: The tool definitions here are one step from a full MCP server. Wrap them in `mcp.server.Server` and you have a game that any MCP client can drive.
- **Rapid prototyping**: The mock-client pattern lets you design agent behaviours and tool schemas without burning API credits, then swap in real AI for validation.

## Source

Based on [KennethanCeyer/build-game-with-ai](https://github.com/KennethanCeyer/build-game-with-ai).
