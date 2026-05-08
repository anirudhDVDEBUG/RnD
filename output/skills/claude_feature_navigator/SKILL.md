---
name: claude_feature_navigator
description: |
  Discover, browse, and recommend Claude Code skills from curated awesome lists and skill marketplaces.
  TRIGGER: user asks about finding Claude skills, discovering new skills, browsing skill collections,
  exploring awesome lists for Claude, or wants recommendations for Claude Code extensions.
---

# Claude Feature Navigator

Helps users discover, evaluate, and install Claude Code skills from curated community collections like the ComposioHQ/awesome-claude-skills awesome list and Composio's skill marketplace.

## When to use

- "Find me Claude skills for [task]"
- "What are the best Claude Code skills available?"
- "Browse the awesome Claude skills list"
- "Recommend skills for code review / deployment / testing"
- "How do I install a Claude skill from GitHub?"

## How to use

1. **Search for skills by category or keyword**: Fetch the latest curated list from the ComposioHQ/awesome-claude-skills repository or the Composio skill marketplace at https://composio.dev/content/top-claude-skills to find skills matching the user's needs.

2. **Evaluate a skill**: For each candidate skill, check its SKILL.md for:
   - Clear trigger descriptions and use-case alignment
   - Required tools and dependencies
   - Community engagement (stars, forks, recent commits)
   - Compatibility with the user's workflow

3. **Install a skill**: Claude Code skills are installed by placing a `SKILL.md` file in the `.claude/skills/` directory of the user's project or in `~/.claude/skills/` for global availability. To install from a repo:
   ```
   # Clone the skill repo and copy the SKILL.md
   git clone <skill-repo-url> /tmp/skill-install
   cp /tmp/skill-install/SKILL.md .claude/skills/<skill-name>.md
   ```

4. **Recommend by category**: Common skill categories include:
   - **Code Quality**: Linting, formatting, code review automation
   - **DevOps**: CI/CD, deployment, infrastructure management
   - **Testing**: Test generation, coverage analysis
   - **Documentation**: Doc generation, API docs, changelog
   - **Productivity**: Git workflows, project scaffolding, refactoring
   - **Integrations**: Third-party API connectors, MCP servers

5. **Verify before installing**: Always review the skill's source code and SKILL.md content before installing. Check that it follows Anthropic's skill conventions at https://github.com/anthropics/skills.

## References

- Composio Top Claude Skills: https://composio.dev/content/top-claude-skills
- Awesome Claude Skills repo: https://github.com/ComposioHQ/awesome-claude-skills
- Anthropic Skills conventions: https://github.com/anthropics/skills
