# How to Use

## As a Claude Code Skill (recommended)

### Install

```bash
mkdir -p ~/.claude/skills/create_claude_md
# Copy SKILL.md into the skill directory:
cp SKILL.md ~/.claude/skills/create_claude_md/SKILL.md
```

### Trigger phrases

Once installed, say any of these to Claude Code:

- "Create a CLAUDE.md for this project"
- "Generate Claude configuration for this repo"
- "Scaffold a CLAUDE.md from scratch"
- "Bootstrap project instructions for Claude"

Claude will scan your repo, ask 3-5 targeted follow-up questions, and write
the file.

---

## As a standalone CLI tool

### Install

```bash
git clone https://github.com/sruthik27/creating-claude-md.git
cd creating-claude-md
# No dependencies beyond Python 3.8+ stdlib
```

### Usage

```bash
# Preview to stdout (no file written)
python3 create_claude_md.py /path/to/repo --dry-run

# Write CLAUDE.md into the repo root
python3 create_claude_md.py /path/to/repo

# Write to a custom path
python3 create_claude_md.py /path/to/repo -o my-claude-config.md
```

### First 60 seconds

```bash
# 1. Clone this prototype
cd create_claude_md

# 2. Run the demo against the bundled sample project
bash run.sh

# Output (printed to terminal):
#   Scanning sample_project/ ...
#     Languages: ['node', 'typescript']
#     Frameworks: ['react', 'vite']
#     Structure: 4 top-level dirs
#     Tests found: True
#     CI: ['.github/workflows']
#
#   # CLAUDE.md
#
#   ## Project Overview
#   acme-dashboard — Real-time analytics dashboard built with React and TypeScript. ...
#
#   ## Tech Stack
#   - **Languages:** node, typescript
#   - **Frameworks:** react, vite
#   ...

# 3. Inspect the generated file
cat sample_project/CLAUDE.md
```

No API keys required. Pure filesystem scan — runs offline.

### CLI flags

| Flag | Description |
|------|-------------|
| `repo_path` | Path to repo root (default: `.`) |
| `-o / --output` | Output file (default: `<repo>/CLAUDE.md`, `-` for stdout) |
| `--dry-run` | Print to stdout, don't write file |
