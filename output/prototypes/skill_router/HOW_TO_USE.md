# How to Use Skill Router

## This is a Claude Code Skill

Skill Router is **not** a standalone CLI tool or MCP server — it's a **Claude Code skill** that you install into your project. The Python script in this repo is a reference implementation and demo of the routing logic.

## Install (30 seconds)

### Option A: Copy the skill folder

```bash
mkdir -p ~/.claude/skills/skill-router
cp SKILL.md ~/.claude/skills/skill-router/SKILL.md
```

### Option B: Clone from source

```bash
cd ~/.claude/skills
git clone https://github.com/pcx-wave/skill-router.git
```

After either option, Claude Code will automatically pick up the skill on the next session.

## Trigger phrases

Say any of these to Claude Code and Skill Router activates:

- "Which skill should I use for this task?"
- "Route this request to the right skill"
- "Which skill handles X?"
- "Find the best skill for generating a landing page"
- "Auto-route this to the appropriate skill"

## Modes

| Mode | How to activate | Behavior |
|------|----------------|----------|
| **Suggest** (default) | Just ask normally | Shows top 1-3 matches with confidence scores; waits for your confirmation |
| **Auto-route** | Say "auto-route" or "just do it" | Silently invokes the best match if confidence >= 70%; falls back to suggest mode otherwise |

## First 60 seconds

**Input** (you type in Claude Code):

```
Which skill should I use to write tests for my Python API?
```

**Output** (Claude responds):

```
Based on your request, I recommend:
1. test-writer — Generates unit and integration tests for Python
   and TypeScript codebases using pytest and vitest (92% match)
2. seo-audit — Audits a webpage for SEO issues (12% match)

Would you like me to use skill #1?
```

You reply "yes" and Claude invokes the `test-writer` skill with your original context.

## Standalone demo (no Claude Code needed)

To see the routing logic in action without Claude Code:

```bash
# Run the built-in demo with 6 mock skills and 6 test queries
bash run.sh

# Or query directly against mock SKILL.md files on disk
python3 skill_router.py "build a landing page" --skills-dir mock_skills
python3 skill_router.py "deploy to cloudflare" --skills-dir mock_skills --auto
python3 skill_router.py "write tests" --skills-dir mock_skills --json
```

## CLI flags

| Flag | Description |
|------|-------------|
| `--skills-dir PATH` | Directory to scan for SKILL.md files (default: `.claude/skills`) |
| `--auto` | Enable silent auto-routing mode |
| `--json` | Output results as JSON |
| `--demo` | Run the built-in demo with mock skills |
