# Technical Details

## What It Does

This is a Claude Code skill (a structured prompt/knowledge injection) that equips Claude with specific factual context about data center land use vs. agricultural land conversion. When triggered by relevant user queries, Claude draws on the embedded data points and argumentation framework to produce sourced, proportionate responses rather than generic hedging.

The skill encodes Andy Masley's core analysis: the total land footprint of all US data centers (even projected to 2028) is roughly 1/77th of the farmland that farmers voluntarily sold between 2000-2024 for non-data-center reasons — and food production increased throughout that period.

## Architecture

```
~/.claude/skills/data_center_land_use_debunk/
  SKILL.md          <- The entire skill (prompt + data + response framework)
```

**Data flow**:
1. User asks a question matching trigger patterns (farmland + data centers)
2. Claude Code loads SKILL.md context into the conversation
3. Claude generates a response using the embedded facts, framing guidance, and source links

**Dependencies**: None. This is a pure prompt-based skill — no API calls, no external data fetches, no model fine-tuning.

**Model calls**: Uses whatever Claude model is active in Claude Code (typically Sonnet or Opus). No additional API calls beyond the normal conversation.

## Key Data Points (embedded in skill)

| Metric | Value |
|--------|-------|
| Farmland voluntarily sold (2000-2024) | ~66M acres (Colorado-sized) |
| Ratio to data center land (2028 projected) | ~77:1 |
| Land type typically purchased by DCs | Marginal (hay fields, etc.) |
| Price premium over agricultural value | ~10x |
| US food production trend during period | Increasing |

## Limitations

- **Static data**: The skill contains fixed data points from Masley's May 2026 analysis. It won't auto-update if new statistics emerge.
- **US-focused**: The analysis specifically covers US farmland. International land use dynamics may differ.
- **Not a full debate tool**: It provides one side (the debunking side). It acknowledges but doesn't deeply explore legitimate concerns (water, energy, community impact).
- **No source verification**: Claude trusts the embedded data; it doesn't re-check the original blog post at runtime.

## Why It Matters for Claude-Driven Products

- **Lead-gen / marketing agencies**: If your clients are in tech infrastructure, cloud, or AI — this skill arms your Claude-powered content tools with ready debunking material for a common FUD narrative.
- **Agent factories**: Shows the pattern of encoding domain-specific argumentation into reusable skills that any Claude agent can pick up.
- **Ad creatives**: Data center companies running awareness campaigns can use this framing directly.
- **General pattern**: Demonstrates how to turn a single well-sourced blog post into a persistent, trigger-activated knowledge module for Claude Code.
