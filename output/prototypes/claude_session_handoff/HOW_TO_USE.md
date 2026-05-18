# How to Use — Claude Session Handoff

## Install (Claude Code Skill)

This is a **Claude Code skill**, not an MCP server. Install by placing the skill file:

```bash
# Clone the source
git clone https://github.com/Phat-Po/claude-skill-handoff.git

# Copy the skill into Claude's skills directory
mkdir -p ~/.claude/skills/claude-skill-handoff
cp claude-skill-handoff/SKILL.md ~/.claude/skills/claude-skill-handoff/SKILL.md
```

That's it. No pip install, no npm, no API keys. Claude Code reads the skill file automatically on next session start.

## Trigger Phrases

Say any of these to Claude Code and the skill activates:

| Phrase | What happens |
|---|---|
| "Hand off this session to the next agent" | Full STATUS.md generation + WIP commit |
| "Save my session context for later" | Writes STATUS.md without committing |
| "Generate a handoff document" | Produces the STATUS.md to stdout |
| "I'm ending this session, prepare a handoff" | Full handoff flow |
| "Switch sessions without losing context" | Same as above |

## First 60 Seconds

### 1. Install the skill (10 sec)

```bash
mkdir -p ~/.claude/skills/claude-skill-handoff
# Copy SKILL.md into the directory (see above)
```

### 2. Start Claude Code in any project

```bash
cd ~/my-project
claude
```

### 3. Trigger the handoff

```
You: "Hand off this session to the next agent"
```

Claude will:
1. Read `git status`, `git log`, and `git diff`
2. Summarize completed work, blockers, and next steps
3. Write `STATUS.md` to the project root
4. Optionally commit with a `[WIP]` prefix

### 4. Start a new session

```bash
claude
You: "Read STATUS.md and continue where the last agent left off"
```

The new agent reads the structured handoff and resumes immediately.

## Standalone Demo (no Claude Code required)

This prototype includes a Python script that demonstrates the handoff logic:

```bash
# Mock mode — no git repo needed
python3 handoff.py --mock

# Real mode — reads actual git state
python3 handoff.py --repo /path/to/your/project

# Write to file
python3 handoff.py --mock --output STATUS.md

# JSON output for programmatic use
python3 handoff.py --mock --json
```

Run the full demo:

```bash
bash run.sh
```
