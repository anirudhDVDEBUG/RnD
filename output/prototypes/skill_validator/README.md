# Skill Validator

Audit any Claude Code SKILL.md file against a 100-point rubric covering structure, content quality, best practices, and trigger reliability. Zero dependencies, instant feedback, actionable fixes.

**Headline result:** A well-formed skill scores 95+/100; a typical first draft scores 30-50 and gets a prioritized fix list to reach publishable quality in minutes.

| Guide | What's inside |
|-------|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, run, integrate as a Claude skill |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, scoring rubric, limitations |

```
bash run.sh          # audit 3 sample skills, see scores + fixes
python3 skill_validator.py path/to/SKILL.md   # audit your own
python3 skill_validator.py --json SKILL.md     # machine-readable output
```

Source: [Anvil-Code/skill-validator](https://github.com/Anvil-Code/skill-validator)
