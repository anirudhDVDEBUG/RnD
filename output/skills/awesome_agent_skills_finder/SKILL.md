---
name: awesome_agent_skills_finder
description: |
  Browse, search, and install community agent skills from the VoltAgent/awesome-agent-skills curated collection.
  TRIGGER when: user asks to "find a skill", "browse skills", "search for agent skills", "install a skill from awesome-agent-skills", "what skills are available", "add a community skill", or mentions "VoltAgent" or "awesome-agent-skills".
  DO NOT TRIGGER when: user wants to create a new skill from scratch, or is asking about built-in Claude Code skills.
---

# Awesome Agent Skills Finder

Browse, search, and install agent skills from the [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) curated collection — a community-maintained catalog of 1000+ agent skills compatible with Claude Code, Codex, Gemini CLI, Cursor, and more.

## When to use

- "Find me a skill for Docker debugging"
- "What community skills are available for database work?"
- "Install an agent skill for Kubernetes from awesome-agent-skills"
- "Browse popular Claude Code skills"
- "Search awesome-agent-skills for a testing helper"

## How to use

### 1. Browse or search the catalog

Fetch the awesome-agent-skills README to browse categories, or search for a specific skill:

```bash
# Clone or fetch the catalog index
curl -sL https://raw.githubusercontent.com/VoltAgent/awesome-agent-skills/main/README.md | head -500

# Or use gh CLI if authenticated
gh api repos/VoltAgent/awesome-agent-skills/readme --jq '.content' | base64 -d
```

Skills are organized by category (e.g., DevOps, Database, Testing, Frontend, Backend, Security, Documentation, etc.). Each entry links to a SKILL.md or a repository containing one.

### 2. Evaluate a skill

Before installing, review the skill's SKILL.md for:
- **Triggers**: When it activates (make sure it doesn't conflict with existing skills)
- **Dependencies**: Any tools, CLIs, or packages it requires
- **Permissions**: What tool access it needs (Bash, file writes, network, etc.)

```bash
# Preview a skill's SKILL.md from its source repo
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/SKILL.md
```

### 3. Install a skill

Claude Code skills are installed by placing a `SKILL.md` file in the `.claude/skills/` directory of your project or in `~/.claude/skills/` for global availability:

```bash
# Project-level install
mkdir -p .claude/skills
curl -sL <SKILL_MD_RAW_URL> -o .claude/skills/<skill_name>.md

# Global install (available across all projects)
mkdir -p ~/.claude/skills
curl -sL <SKILL_MD_RAW_URL> -o ~/.claude/skills/<skill_name>.md
```

### 4. Verify installation

After installing, confirm the skill is recognized by checking that its trigger phrases activate correctly in a new Claude Code session.

## Tips

- **Star count & community signals**: Prefer skills with more community validation.
- **Compatibility**: Skills in this collection target multiple agents; verify Claude Code compatibility.
- **Conflicts**: Check that new skill triggers don't overlap with your existing skills.
- **Updates**: Re-fetch the catalog periodically — new skills are added frequently (the repo gains ~97 stars/day).

## References

- **Source**: [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- **Anthropic skill conventions**: [anthropics/skills](https://github.com/anthropics/skills)
- **Claude Code docs on skills**: [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code)
