# Technical Details — Mythos Skill Forge

## What it does

Mythos Skill Forge is a Python CLI that scaffolds Claude Code skill directories following Anthropic's conventions. Given a skill name, description, trigger phrases, and workflow steps, it generates a complete directory with SKILL.md (YAML frontmatter + structured sections), CLAUDE.md (agent behavior instructions), optional hook scripts (pre/post execution), and output templates. It also includes a built-in auditor that scores generated skills against 5 convention checks.

The tool ships with 3 preset templates (code review, deploy checklist, API doc generator) and supports fully custom skill definitions via CLI flags. No external dependencies — it runs on Python 3.10+ stdlib only.

## Architecture

### Key files

| File | Purpose |
|------|---------|
| `skill_forge.py` | Single-file CLI — all logic in ~350 lines |
| `run.sh` | End-to-end demo script |

### Data flow

```
CLI args / preset name
  -> SkillSpec dataclass (validated)
    -> Generator functions (SKILL.md, CLAUDE.md, hooks, templates)
      -> Write to disk (skills/<name>/)
        -> Auditor reads back and scores against 5 checks
```

### Core components

- **SkillSpec** — dataclass holding skill metadata; `.validate()` checks name format, trigger count, description length
- **forge_skill()** — orchestrates generation, creates directory tree, writes files
- **audit_skill()** — reads a SKILL.md back and scores it on 5 criteria: frontmatter structure, trigger definitions, when-to-use section, how-to-use section, no placeholder text
- **PRESETS** — 3 built-in skill templates for common use cases
- **Generators** — `generate_skill_md()`, `generate_claude_md()`, `generate_hook()`, `generate_template()` each produce one file's content from a SkillSpec

### Dependencies

None. Python 3.10+ standard library only (argparse, dataclasses, pathlib, textwrap, re, json).

### No model calls

This tool does not call any LLM APIs. It is a deterministic template generator. The generated SKILL.md files are designed to be consumed by Claude Code's skill loader.

## Limitations

- **Template-based, not AI-generated:** The "How to use" steps are whatever you provide — the tool does not expand or improve them. The quality of the generated skill depends on the quality of your inputs.
- **No YAML parser:** Frontmatter is generated via string templating, not a YAML library. Edge cases with special characters in descriptions could produce invalid YAML.
- **Audit is basic:** The auditor checks structure, not semantics. A skill that passes 5/5 might still have unclear or unhelpful instructions.
- **No skill registry:** Skills are generated as local directories. There is no publish, search, or version management.
- **Single-file design:** Intentionally simple, but not extensible for plugin architectures.

## Why it might matter

- **Agent factories:** If you are building systems that programmatically create Claude Code agents, this tool provides the scaffolding layer — generate skills on the fly for new agent roles.
- **Lead-gen / marketing workflows:** Custom skills for "score these leads" or "generate ad copy" can be forged and installed in seconds, enabling rapid prototyping of Claude-driven business workflows.
- **Skill quality gates:** The built-in auditor can serve as a CI check — ensure all skills in a repo meet Anthropic's conventions before merging.
- **Onboarding:** New team members can use presets to understand skill structure before writing their own.
