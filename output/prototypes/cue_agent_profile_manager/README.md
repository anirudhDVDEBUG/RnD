# Cue — Agent Profile Manager for Claude Code & Codex

**Per-directory profiles that auto-select which skills, MCP servers, and plugins load before your agent launches.** One `cue use backend` in your API repo, one `cue use marketing` in your content site, and each workspace gets exactly the tools it needs — no manual toggling.

## Headline result

```
$ cd ecommerce-api && cue status
  Profile:     staging
  Skills:      sql-query-builder
  MCP Servers: postgres-mcp, datadog-mcp
  Plugins:     log-viewer

$ cd ../marketing-site && cue status
  Profile:     default
  Skills:      seo-content-optimizer, image-alt-generator
  MCP Servers: analytics-mcp
  Plugins:     lighthouse-ci
```

Different directory, different agent toolset — zero config at launch time.

## Quick start

```bash
bash run.sh        # runs the full demo, no API keys needed
```

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) — install steps, CLI commands, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — architecture, data flow, limitations

## Source

- Repository: https://github.com/opencue/cue
- Install: `npm install -g cue-ai`
