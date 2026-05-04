# Tech Details: Vibe Coding Skills

## What It Actually Does

This is a **Claude Code skill** (a structured markdown prompt) that modifies Claude's behavior during coding sessions. Instead of immediately generating code when a user describes a feature, Claude follows a 4-step methodology: **Ground the Vibe** (establish tech stack and constraints), **Describe Intent** (focus on what, not how), **Iterate in Conversation** (review-steer-commit loop), and **Validate and Harden** (tests, edge cases, security review).

The companion `vibe_planner.py` script demonstrates the methodology as a standalone tool. It performs heuristic keyword analysis on a natural-language feature request to extract structure: tech stack detection, UI element identification, behavior mapping, edge case flagging, and generates a step-by-step iteration plan with a validation checklist.

## Architecture

### Files

| File | Purpose |
|---|---|
| `SKILL.md` | The Claude skill — installed to `~/.claude/skills/vibe_coding_skills/` |
| `vibe_planner.py` | Standalone demo — parses feature requests into structured plans |
| `run.sh` | End-to-end demo runner |

### Data Flow (Skill)

```
User says trigger phrase
  -> Claude loads SKILL.md from ~/.claude/skills/
  -> Claude follows 4-step workflow instead of direct code generation
  -> User gets guided through: context -> intent -> iteration -> validation
```

### Data Flow (Planner Script)

```
Natural language request (string)
  -> Keyword extraction against 4 banks:
     - STACK_HINTS (40+ framework/language keywords -> canonical names)
     - UI_KEYWORDS (40+ component types)
     - BEHAVIOR_KEYWORDS (30+ interaction verbs)
     - EDGE_CASE_SIGNALS (20+ error/boundary terms)
  -> Feature name extraction (regex patterns)
  -> Iteration step generation (rule-based, adapts to detected elements)
  -> Validation checklist generation (conditional on what was detected)
  -> Formatted plan output
```

### Dependencies

- **Skill:** None. It's a markdown file that Claude reads.
- **Planner script:** Python 3.8+ standard library only (`re`, `sys`, `dataclasses`, `textwrap`). Zero pip dependencies.
- **No model calls.** The planner uses keyword matching, not an LLM. The skill itself runs inside Claude's existing context.

## Limitations

- **The skill is a prompt, not enforcement.** Claude generally follows the workflow, but strong user insistence on "just give me the code" may override it.
- **The planner is heuristic, not semantic.** It matches keywords, not meaning. "I need something fast" triggers nothing; "I need fast loading" triggers "load" as a behavior.
- **No project awareness.** The skill tells Claude to ask about the tech stack, but doesn't auto-detect it from `package.json` or `pyproject.toml`.
- **No memory across sessions.** Each new conversation starts the workflow from scratch — there's no persistent "project context" unless the user also uses CLAUDE.md.
- **English only.** Keyword banks and trigger phrases are English.

## What It Does NOT Do

- Does not generate code itself — it structures the process of asking an agent to generate code.
- Does not replace testing, CI/CD, or code review — it adds a pre-coding planning layer.
- Does not integrate with any external service, API, or database.
- Does not require or use any API keys.

## Why It Matters for Claude-Driven Products

**Agent factories / developer tools:** If you're building products where users interact with Claude to generate code (internal tools, low-code platforms, coding assistants), this skill provides a reusable workflow template. Instead of letting users fire-and-forget prompts that produce inconsistent code, you embed a structured methodology.

**Lead-gen / marketing context:** "Vibe coding" is a trending term in the AI development space. Tools and workflows that reference it have organic discovery potential. A structured vibe-coding skill positions a product as opinionated and production-ready vs. "just another AI code generator."

**Quality control at scale:** The biggest risk with AI-generated code is skipping validation. The 4-step methodology bakes in commit checkpoints, test requirements, and security review as non-optional steps — relevant for any team adopting AI coding at scale.

## Source

- [foryourhealth111-pixel/Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills)
- Listed in [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
