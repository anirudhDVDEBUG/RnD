---
name: browse-anthropic-skills-marketplace
description: |
  Browse, discover, and install Agent Skills from the official Anthropic skills repository (anthropics/skills).
  TRIGGER when: user wants to find Claude skills, browse the skill marketplace, install agent skills, explore available skills, or search for skills on skills.sh.
  DO NOT TRIGGER when: user is creating their own skill from scratch, or asking about unrelated plugins.
---

# Browse Anthropic Skills Marketplace

Help users discover and install Agent Skills from the official Anthropic skills repository.

## When to use

- "Browse available Claude skills"
- "Find a skill for document generation"
- "Install a skill from the Anthropic marketplace"
- "What skills are available on skills.sh?"
- "Show me enterprise skills for Claude"

## How to use

1. **Browse the repository**: Fetch the skill catalog from the `anthropics/skills` GitHub repository to see available categories:
   - **Creative & Design** — art, music, design applications
   - **Development & Technical** — web app testing, MCP server generation
   - **Enterprise & Communication** — business workflows, branding guidelines
   - **Documents** — DOCX, PDF, PPTX, XLSX document manipulation

2. **Search for skills**: Use the GitHub API or browse `skills.sh/b/anthropics/skills` to find skills matching the user's needs. Each skill is a folder containing a `SKILL.md` with YAML frontmatter (`name`, `description`) and markdown instructions.

3. **Review a skill**: Read the skill's `SKILL.md` to understand what it does, its triggers, guidelines, and examples before installing.

4. **Install in Claude Code**:
   ```bash
   /plugin marketplace add anthropics/skills
   /plugin install <skill-name>@anthropic-agent-skills
   ```

5. **Install in Claude.ai**: Upload the skill folder via the Claude interface. See [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

6. **Install via API**: Follow the [Skills API Quickstart](https://docs.claude.com/en/api/skills-guide#creating-a-skill).

## Skill format reference

Each skill is a folder with a `SKILL.md`:

```yaml
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Instructions Claude follows when this skill is active]

## Examples
## Guidelines
```

## References

- Skill marketplace: https://skills.sh/b/anthropics/skills
- GitHub repository: https://github.com/anthropics/skills
- Skill specification: https://github.com/anthropics/skills/tree/main/spec
- Skill template: https://github.com/anthropics/skills/tree/main/template
