# Photo-agents: Vision-Grounded Autonomous Agents

**TL;DR**: Self-evolving agents that use screenshot-based "photographic memory" and auto-extract reusable skills from repeated action patterns. Three-tier memory (working/episodic/semantic) lets agents learn across sessions without retraining.

## Headline Result

```
$ bash run.sh
  Skills learned:  ['navigate_to_url', 'click_button_fill_auto']
  Vision captures: 10
  Episodic memory: 4 episodes stored
  Auto-extracted:  ['click_button_fill_auto']  ← agent wrote this itself
```

An agent that **observes its own successes and codifies them as callable skills** — no human intervention required.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **Source**: https://github.com/jmerelnyc/Photo-agents
