# ZeroClaw Subagent Orchestration

**Decompose complex tasks into specialized subagents, route them in parallel or sequentially, and merge results — all inside Claude Code.** This is the "ZeroClaw" pattern: an orchestrator splits work across research, code, and review agents, each with scoped tools and focused context windows.

## Headline Result

```
Task: "Add user authentication with OAuth2"
  -> 3 subagents dispatched in parallel (research, code, review)
  -> Merged result in ~200ms with conflict detection
  -> Zero external dependencies, zero API keys needed for demo
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, why it matters

## Run the Demo

```bash
bash run.sh
```

Source: [muhammadqasimkalhoro94-blip/claude-zeroclaw-agentics](https://github.com/muhammadqasimkalhoro94-blip/claude-zeroclaw-agentics)
