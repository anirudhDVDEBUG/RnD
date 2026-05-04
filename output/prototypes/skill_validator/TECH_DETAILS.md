# Technical Details

## What It Does

Skill Validator is a pure-Python static analyzer for Claude Code SKILL.md files. It parses the markdown structure and YAML frontmatter, then evaluates the file against a 100-point rubric across four categories: Structure (25 pts), Content Quality (35 pts), Best Practices (25 pts), and Trigger Reliability (15 pts). The output is a scored audit report with prioritized fixes.

No LLM calls are made -- all checks are deterministic regex and heuristic-based. This means instant results, zero cost, and fully reproducible scores.

## Architecture

```
skill_validator.py    # Single-file implementation (~300 lines)
  parse_frontmatter() # Extracts YAML frontmatter fields (name, description)
  find_section()      # Locates markdown ## sections by heading
  audit_skill()       # Runs 13 checks across 4 categories, returns AuditReport
  format_report()     # Renders AuditReport as markdown table
  main()              # CLI entry: argparse, file I/O, exit code

samples/              # Three sample SKILL.md files at different quality levels
  good_skill.md       # 95+ score -- passes all checks
  medium_skill.md     # ~70 score -- missing some best practices
  bad_skill.md        # ~20 score -- multiple critical issues
```

**Data flow:** Read file -> parse frontmatter -> extract sections -> run 13 checks -> score -> format report.

**Dependencies:** None. Python 3.8+ standard library only (`re`, `pathlib`, `argparse`, `dataclasses`, `json`).

## Scoring Rubric Detail

| Category | Check | Points |
|----------|-------|--------|
| Structure | Valid YAML frontmatter with name + description | 10 |
| Structure | Name is snake_case, <=60 chars | 5 |
| Structure | Description includes TRIGGER clause | 10 |
| Content Quality | "When to use" with 3-5 trigger phrases | 10 |
| Content Quality | "How to use" with numbered steps | 10 |
| Content Quality | Steps reference real tools/commands | 5 |
| Content Quality | "References" section with links | 5 |
| Content Quality | No placeholder/TODO content | 5 |
| Best Practices | Self-contained (no unguarded external deps) | 10 |
| Best Practices | Follows Anthropic skill conventions | 10 |
| Best Practices | No security anti-patterns | 5 |
| Trigger Reliability | TRIGGER clause specific enough | 8 |
| Trigger Reliability | TRIGGER covers core use cases | 7 |

## Limitations

- **Frontmatter parsing is simplified.** It handles basic `key: value` and `key: |` multiline blocks but does not cover full YAML spec (nested objects, arrays, anchors). Complex frontmatter may parse incorrectly.
- **No semantic analysis.** Checks are regex/heuristic-based. It cannot judge whether step instructions are *actually correct* -- only whether they exist and reference tools.
- **English only.** Pattern matching assumes English-language content.
- **No auto-fix implementation.** The CLI reports fixes but does not apply them. The Claude skill version offers to apply fixes via Claude's Edit tool.

## Why It Matters

For teams building Claude-driven products (agent factories, lead-gen tools, marketing automation), skills are the reusable building blocks. A poorly written SKILL.md means Claude triggers at the wrong time, follows vague instructions, or misses the intended use case entirely. This validator catches those problems before deployment -- think of it as a linter for your AI agent's playbook.

Concrete use cases:
- **Skill marketplace QA** -- gate skill publishing on a minimum score threshold.
- **CI pipeline** -- `python3 skill_validator.py SKILL.md` exits non-zero below 80, so you can fail builds on low-quality skills.
- **Onboarding** -- new skill authors get instant, actionable feedback instead of vague "follow the template" guidance.
