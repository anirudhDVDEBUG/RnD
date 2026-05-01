---
name: awesome_claude_skills_discover
description: |
  Discover, browse, and install community Claude Skills from the awesome-claude-skills curated list.
  TRIGGER: user wants to find a Claude skill, browse available skills, install a community skill, search for workflow automation skills, or explore the awesome-claude-skills repository.
---

# Awesome Claude Skills Discovery

Browse, search, and install community-contributed Claude Skills from the [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) curated list — a collection of 57k+ starred skills, resources, and tools for customizing Claude AI workflows.

## When to use

- "Find me a Claude skill for [topic]"
- "What community skills are available for workflow automation?"
- "Browse awesome claude skills"
- "Install a skill from awesome-claude-skills"
- "Show me popular Claude skills for [category]"

## How to use

### 1. Fetch the latest skill catalog

Clone or fetch the curated list from the upstream repository:

```bash
# Fetch the latest README / catalog
curl -sL https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/main/README.md -o /tmp/awesome-claude-skills-catalog.md
```

Or if you have `gh` CLI:

```bash
gh api repos/ComposioHQ/awesome-claude-skills/readme -q '.content' | base64 -d > /tmp/awesome-claude-skills-catalog.md
```

### 2. Search for skills by keyword

Search the downloaded catalog for relevant skills:

```bash
grep -i -A 3 "<keyword>" /tmp/awesome-claude-skills-catalog.md
```

Replace `<keyword>` with the topic you're looking for (e.g., `docker`, `git`, `testing`, `deploy`, `mcp`, `saas`).

### 3. Install a skill

Once you find a skill you want, install it into your project:

```bash
# Create the skills directory if it doesn't exist
mkdir -p .claude/skills

# Download the SKILL.md from the skill's repository
curl -sL "<raw-skill-url>/SKILL.md" -o ".claude/skills/<skill-name>.md"
```

Alternatively, clone the skill repo and copy the SKILL.md:

```bash
git clone --depth 1 <skill-repo-url> /tmp/<skill-name>
cp /tmp/<skill-name>/SKILL.md .claude/skills/<skill-name>.md
```

### 4. Verify installation

Confirm the skill is available:

```bash
ls -la .claude/skills/
cat .claude/skills/<skill-name>.md
```

### Skill categories available

The awesome list covers skills across these areas:

- **AI Agents** — Agent-based workflow skills
- **Automation** — CI/CD, deployment, and workflow automation
- **MCP Servers** — Model Context Protocol integrations
- **SaaS Integrations** — Third-party service connectors (Slack, GitHub, etc.)
- **Code Quality** — Linting, testing, review skills
- **DevOps** — Infrastructure, Docker, Kubernetes skills
- **Workflow Automation** — Custom Claude Code workflow enhancers

### Tips

- Star counts and velocity indicators in the catalog help identify popular/trending skills
- Check each skill's repo for prerequisites (MCP servers, API keys, etc.)
- Skills are SKILL.md files placed in `.claude/skills/` within your project or `~/.claude/skills/` globally
- You can combine multiple skills — they stack and complement each other

## References

- **Source Repository**: [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- **Anthropic Skills Convention**: [github.com/anthropics/skills](https://github.com/anthropics/skills)
- **Topics**: claude-skills, workflow-automation, agent-skills, awesome-list, mcp-server
- **Stars**: 57,288+ (trending at +54/day)
