# Public-Channel Coding Agent Workflow

**A transparent, Shopify River-style coding agent that works exclusively in public channels -- enabling osmosis learning across your engineering team.**

Inspired by [Simon Willison's analysis](https://simonwillison.net/2026/May/11/learning-on-the-shop-floor/#atom-everything) of Shopify's "River" coding agent and the German *Lehrwerkstatt* (teaching workshop) pattern: every AI-assisted coding session happens in public, searchable channels so the whole org learns by proximity.

## Headline Result

```
Total interactions: 7
Refused (DM/private): 2    <-- agent enforces transparency
Processed in public:  4    <-- all real work is visible
Channels active: ['#alice_agent', '#bob_agent']
```

The agent **refuses DMs and private channels**, forces work into named public channels (`#person_agent`), threads conversations for navigability, and logs everything for search.

## Quick Start

```bash
bash run.sh
```

No API keys needed -- runs end-to-end with simulated team interactions.

## Next Steps

- [HOW_TO_USE.md](HOW_TO_USE.md) -- installation, skill setup, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) -- architecture, data flow, limitations, and why this matters
