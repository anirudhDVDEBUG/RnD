# Skill Router

**A meta-skill for Claude Code that routes requests to the right installed skill — suggest mode or silent auto-routing.**

If you have 5+ Claude Code skills installed and forget which one handles what, Skill Router scans your `.claude/skills/` directory, scores every skill against your request, and either recommends the best match or auto-invokes it.

### Headline result

```
Query: "Generate Facebook ad copy for summer sale"  [auto-route]
  >>> Auto-routed to **ad-creative-gen** (confidence 85%)
```

### Quick links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install in 60 seconds, trigger phrases, first demo
- [TECH_DETAILS.md](TECH_DETAILS.md) — Scoring algorithm, architecture, limitations
- [SKILL.md](SKILL.md) — The raw skill definition to drop into your project

### Try it now

```bash
bash run.sh
```
