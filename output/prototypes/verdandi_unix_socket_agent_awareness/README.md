# Verdandi: Unix Socket Agent Awareness

**Real-time cross-instance AI agent awareness via Unix domain sockets.**
Verdandi is a lightweight "AI nervous system" that lets multiple agent instances share state, detect each other's presence, and self-heal after disconnections — all through a single local socket with zero network overhead.

## Headline result

```
$ bash run.sh
[HUB] Hub listening  path=/tmp/verdandi_demo.sock
[AGENT:planner] Connected to hub
[AGENT:researcher] Connected to hub
[AGENT:writer] Connected to hub
  ...state broadcast, self-healing, heartbeat...
DEMO COMPLETE
```

Three agents register, publish state, receive peer updates in real-time, survive a simulated crash, and reconnect — in under 2 seconds, using only Python stdlib.

## Quick links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — install, run, integrate with Claude Code skills
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, data flow, limitations
- **Source repo**: https://github.com/hrabanazviking/Verdandi
