# How to Use: ck-skills Agent Toolkit

## Installation

### Option A: Use as a Claude Code Skill (recommended)

This is a skill that helps you browse and install *other* skills from the ck-skills collection.

```bash
# 1. Create the skills directory in your project
mkdir -p .claude/skills/ck-skills-browser

# 2. Copy the SKILL.md into it
cp SKILL.md .claude/skills/ck-skills-browser/SKILL.md
```

Once in place, Claude Code will automatically detect it. No config file changes needed.

**Trigger phrases** that activate this skill:

- "Install skills from bestagentkits"
- "Set up ck-skills"
- "Show me the AgentBrain / GoClaw skill catalog"
- "Browse curated Claude Code skill packs"
- "What skills are available in bestagentkits/ck-skills?"

### Option B: Install the full ck-skills collection directly

```bash
# Clone the upstream repo
git clone https://github.com/bestagentkits/ck-skills.git /tmp/ck-skills

# Copy all 14 skills into your project
mkdir -p .claude/skills
cp -r /tmp/ck-skills/skills/* .claude/skills/
```

### Option C: Run the demo standalone

```bash
git clone https://github.com/bestagentkits/ck-skills.git /tmp/ck-skills
cd /path/to/this/prototype
bash run.sh
```

No API keys or external dependencies required (Python 3.8+ stdlib only).

## First 60 seconds

**Input:** Run the demo.

```bash
bash run.sh
```

**Output:** The script walks through 5 steps:

1. **Browse** — prints all 14 skills with name, author, and tags
2. **Search** — filters for "security"-tagged skills (finds `code-review` and `security-scan`)
3. **Inspect** — shows the full SKILL.md preview for `code-review`
4. **Install** — writes 3 skill SKILL.md files into `demo_output/.claude/skills/`
5. **Verify** — lists the installed files

You will also get `demo_output/skill_catalog.json` — the full catalog as machine-readable JSON.

### Interactive mode

```bash
python3 ck_skills_browser.py --interactive
```

Commands:
- `list` — show all 14 skills
- `list security` — filter by tag
- `search deploy` — full-text search
- `show code-review` — SKILL.md preview
- `install test-writer` — write to `.claude/skills/`
- `quit`

## Where skills go

| Path | Scope |
|------|-------|
| `<project>/.claude/skills/<name>/SKILL.md` | Project-level (committed to repo) |
| `~/.claude/skills/<name>/SKILL.md` | User-level (all projects) |

Skills are plain Markdown files with YAML frontmatter. Claude Code detects them automatically — no restart or config changes needed.
