# Technical Details

## What It Does

The Company Execution Layer Builder is a CLI tool that scaffolds and manages a structured separation between a company's **knowledge base** (context) and **executable playbooks** (skills). It creates a directory structure where context documents (brand guides, SOPs, product specs, org charts) live in `context/`, executable skill definitions live in `skills/`, and a root `CLAUDE.md` wires them together as a registry. The tool can scaffold, list, inspect, validate, run, and add skills — all against live context that skills reference but never duplicate.

The core insight (from Bradley Bonanno's video) is that most teams already have a "second brain" of docs, but no **execution layer** — no way for AI to _do_ things with that knowledge. This tool bridges that gap by treating each SOP/playbook as a skill with explicit steps, context references, and output locations.

## Architecture

```
execution_layer.py          # Single-file CLI (all logic here)
├── Templates               # CLAUDE.md, SKILL.md, context file templates
├── scaffold()              # Creates full directory structure
├── list_skills()           # Parses SKILL.md front matter across skills/
├── inspect_skill()         # Deep-reads a skill + checks context refs exist
├── validate()              # Checks structural integrity (missing files, broken refs)
├── run_skill()             # Loads context, executes steps, writes output
├── add_skill()             # Creates new skill + regenerates CLAUDE.md
└── run_demo()              # End-to-end demo combining all operations
```

**Data flow:**
1. `scaffold` writes context files + skill definitions + CLAUDE.md
2. `validate` walks `skills/*/SKILL.md`, extracts `` context/...`` references, checks they resolve
3. `run` reads the skill's steps, loads referenced context files, produces output in `output/<skill>/`
4. `add-skill` creates a new `SKILL.md` from template and regenerates `CLAUDE.md` registry

**Dependencies:** Python 3.8+ standard library only (pathlib, json, argparse, textwrap, datetime). No external packages, no API keys.

**Key files:**
- `execution_layer.py` — All logic in one file (~450 lines)
- `run.sh` — Demo entry point
- Generated `CLAUDE.md` — The root config Claude Code reads
- Generated `skills/*/SKILL.md` — Individual skill definitions

## Limitations

- **No actual AI execution** — `run_skill()` simulates execution by loading context and writing a summary. In production, Claude Code reads the SKILL.md and executes steps itself.
- **Front matter parsing is basic** — uses simple string matching, not a full YAML parser. Works for the standard template but may break on unusual formatting.
- **No skill dependencies** — skills can't declare that they depend on other skills. Each skill runs independently.
- **No versioning** — context and skills aren't versioned; changes take effect immediately. This is by design (live context), but means there's no rollback.
- **Single-user** — no access control, audit log, or multi-user collaboration features. Designed for one team sharing a directory.

## Why It Matters

For anyone building Claude-driven products or workflows:

- **Agent factories** can use this pattern to give each agent a scoped set of skills + context, rather than dumping everything into one prompt.
- **Lead-gen / marketing teams** can encode their content creation, proposal, and reporting playbooks as skills that any team member (or Claude) can run consistently.
- **Consulting / services firms** can package their methodology as a skills marketplace — new hires run the same playbooks as veterans.
- **The "reference, don't hard-code" pattern** is critical for any system where context changes frequently. Skills that reference live docs stay current; skills that embed info drift immediately.

This is essentially the "Claude Code native" approach to building internal tooling — no custom app, no API integration, just structured markdown that Claude can read and execute.
