---
name: ck-skills Agent Toolkit
description: |
  Browse, install, and use curated Claude Code skills from the bestagentkits/ck-skills collection (14 production-ready skills by GoClaw / AgentBrain).
  Trigger: user mentions "ck-skills", "bestagentkits", "AgentBrain skills", "GoClaw skills", "agent toolkit skills", "browse skill marketplace", or wants to install curated Claude Code skill packs.
---

# ck-skills Agent Toolkit

Browse, install, and manage curated Claude Code skills from the **bestagentkits/ck-skills** collection — 14 production-ready skills maintained by GoClaw / AgentBrain.

## When to use

- "Install skills from bestagentkits" or "set up ck-skills"
- "Show me the AgentBrain / GoClaw skill catalog"
- "Add the ck-skills agent toolkit to my project"
- "Browse curated Claude Code skill packs"
- "What skills are available in bestagentkits/ck-skills?"

## How to use

### 1. Clone the skill repository

```bash
git clone https://github.com/bestagentkits/ck-skills.git /tmp/ck-skills
```

### 2. Browse available skills

List all 14 available skills in the collection:

```bash
ls /tmp/ck-skills/skills/ 2>/dev/null || ls /tmp/ck-skills/
```

Each skill directory contains a `SKILL.md` file following Anthropic's skill conventions.

### 3. Install a skill into your project

Copy the desired skill into your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -r /tmp/ck-skills/skills/<skill-name> .claude/skills/
```

Or install all skills at once:

```bash
mkdir -p .claude/skills
cp -r /tmp/ck-skills/skills/* .claude/skills/
```

### 4. Verify installation

Confirm the skills are in place:

```bash
ls .claude/skills/
```

Skills are automatically available to Claude Code once placed in `.claude/skills/`.

### 5. Keep skills updated

Pull the latest versions:

```bash
cd /tmp/ck-skills && git pull
cp -r /tmp/ck-skills/skills/* /path/to/your/project/.claude/skills/
```

## Notes

- The collection is curated and maintained by GoClaw / AgentBrain
- Skills are designed to be composable — install only the ones you need
- Each skill follows Anthropic's official skill format with YAML frontmatter
- The repository uses Python and targets AI agent workflows

## References

- Source repository: https://github.com/bestagentkits/ck-skills
- Topics: agent-tools, agentbrain, ai-agents, claude-code, claude-skills, goclaw, plugin-marketplace
- Anthropic skill conventions: https://github.com/anthropics/skills
