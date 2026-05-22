# TrustGraph Resource Rater

**Silently scores every external resource Claude Code touches — WebFetch, WebSearch, MCP servers, curl — building a cumulative trust ledger so you know which sources to rely on and which to question.**

## Headline Result

```
Domain                              Avg   Min  Max   #  Tools
--------------------------------------------------------------------------------
sketchy-download.io                  1.3    1    2   3  Bash
random-seo-blog.xyz                  2.4    1    4   7  WebFetch, WebSearch
medium.com                           4.8    3    7   5  WebFetch, WebSearch
developer.mozilla.org                9.6    9   10   4  WebFetch, WebSearch
docs.python.org                      9.2    8   10   6  WebFetch, WebSearch
```

Zero-friction reputation tracking — hooks fire invisibly after every tool call.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the skill, configure hooks, start scoring in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and why this matters

## Try the Demo

```bash
bash run.sh
```

Generates a mock ledger and prints the full trust report. No API keys needed.

## Source

[GusEllerm/trustgraph-skill](https://github.com/GusEllerm/trustgraph-skill)
