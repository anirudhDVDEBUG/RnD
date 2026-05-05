---
name: metalbear_skills_registry
description: |
  Browse, search, and install reusable Claude Code skills from the MetalBear community skills registry.
  TRIGGER when: user asks to find skills, install a skill, browse available agent skills, search for a skill from metalbear or the community registry, or wants to contribute a skill.
  DO NOT TRIGGER when: user is writing their own SKILL.md from scratch, or asking about unrelated package registries.
---

# MetalBear Skills Registry

Browse, search, and install community-contributed Claude Code skills from the [metalbear-co/skills](https://github.com/metalbear-co/skills) registry.

## When to use

- "Find a skill for Kubernetes debugging"
- "Install a Claude Code skill from the MetalBear registry"
- "What community skills are available for Docker?"
- "Browse the skills registry for testing utilities"
- "Contribute my skill to the MetalBear skills repo"

## How to use

### Browse available skills

1. Clone or fetch the registry:
   ```bash
   git clone --depth 1 https://github.com/metalbear-co/skills.git /tmp/metalbear-skills
   ```
2. List available skills by exploring the directory structure:
   ```bash
   ls /tmp/metalbear-skills/skills/
   ```
3. Each skill folder contains a `SKILL.md` file with frontmatter (name, description, triggers) and usage instructions.

### Search for a skill

1. Search by keyword across all skill definitions:
   ```bash
   grep -rl "<keyword>" /tmp/metalbear-skills/skills/ --include="*.md"
   ```
2. Read the matching `SKILL.md` files to evaluate fit.

### Install a skill

1. Identify the skill folder you want (e.g., `skills/my-skill/SKILL.md`).
2. Copy the `SKILL.md` into your project's `.claude/skills/` directory:
   ```bash
   mkdir -p .claude/skills
   cp /tmp/metalbear-skills/skills/<skill-name>/SKILL.md .claude/skills/<skill-name>.md
   ```
3. The skill is now available in your Claude Code sessions for this project.

### Contribute a skill

1. Fork the [metalbear-co/skills](https://github.com/metalbear-co/skills) repository.
2. Create a new folder under `skills/` with your skill name.
3. Add a `SKILL.md` following the Anthropic skill conventions (YAML frontmatter with `name`, `description`, trigger/anti-trigger lines, plus `When to use`, `How to use`, and `References` sections).
4. Open a pull request to the upstream repository.

## References

- Source repository: https://github.com/metalbear-co/skills
- Anthropic skill conventions: https://github.com/anthropics/skills
- Listed in: [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
