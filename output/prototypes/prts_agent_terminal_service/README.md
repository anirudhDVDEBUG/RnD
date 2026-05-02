# PRTS Agent Terminal Service

**A terminal-first multi-agent orchestration system in Python.**
Register agents, dispatch tasks, hot-rebuild failed agents — all from a REPL, zero web servers needed.

```
PRTS> dispatch research multi-agent orchestration
{
  "agent": "research",
  "result": {
    "topic": "multi-agent orchestration",
    "findings": ["Found 12 recent papers on 'multi-agent orchestration'", ...]
  }
}
```

## Quick start

```bash
bash run.sh          # runs a full demo, no API keys needed
python3 main.py      # interactive REPL
```

See [HOW_TO_USE.md](HOW_TO_USE.md) for install steps and [TECH_DETAILS.md](TECH_DETAILS.md) for architecture.

## What's inside

| File | Purpose |
|------|---------|
| `agents/base.py` | Abstract `Agent` with start/stop/rebuild lifecycle |
| `agents/worker.py` | Three concrete agents: Research, Code, Summary |
| `orchestrator/dispatcher.py` | Registry + task routing + retry-on-failure |
| `terminal/interface.py` | `cmd.Cmd` REPL with list/dispatch/rebuild/status |
| `main.py` | Wires everything together; `--demo` for batch mode |

Inspired by [zayokami/PRTS](https://github.com/zayokami/PRTS).
