# Anna's Archive Skill Generator

**One MCP tool call: search a book, download it, extract its methodology via Gemini, and output an audited Claude Code SKILL.md.**

## Headline Result

```
Input:  "Getting Things Done by David Allen"
Output: A complete SKILL.md with GTD methodology extracted, structured,
        and ready to drop into ~/.claude/skills/
```

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, configure, and run in 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations

## Demo

```bash
bash run.sh
```

Runs a mock pipeline demonstrating the full search → download → extract → generate → audit flow with sample output.

## Source

[VKirill/mcp-annas-archive-create-skill](https://github.com/VKirill/mcp-annas-archive-create-skill)
