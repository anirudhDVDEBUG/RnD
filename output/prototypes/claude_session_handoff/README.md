# Claude Session Handoff

**Switch Claude Code sessions without losing context.** This skill auto-generates a structured `STATUS.md` capturing your branch, progress, blockers, and next steps — so the next agent picks up in seconds instead of re-reading everything.

### Headline Result

```
$ python3 handoff.py --mock --output STATUS.md
[handoff] Wrote STATUS.md (1.2 KB) — next session starts here
```

The receiving agent reads `STATUS.md` and immediately knows: what branch, what's done, what's blocked, and what to do next.

### Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the skill, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **[run.sh](run.sh)** — End-to-end demo (`bash run.sh`)

### Source

[Phat-Po/claude-skill-handoff](https://github.com/Phat-Po/claude-skill-handoff)
