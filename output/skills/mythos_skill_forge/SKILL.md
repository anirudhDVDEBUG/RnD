---
name: mythos_skill_forge
description: |
  Scaffold, build, and validate autonomous Claude Code skills and agent plugins.
  Triggers: "create a new skill", "scaffold a claude skill", "build an agent plugin",
  "generate SKILL.md", "forge a skill", "skill forge", "mythos skill"
---

# Mythos Skill Forge

Scaffold and build production-ready Claude Code skills and agent plugins following Anthropic's skill conventions.

## When to use

- "Create a new Claude Code skill from scratch"
- "Scaffold a skill with SKILL.md, CLAUDE.md, and hooks"
- "Build an agent plugin for my workflow"
- "Generate a SKILL.md file for this project"
- "Forge a reusable skill for code review / deployment / testing"

## How to use

### Step 1: Define the skill purpose

Gather the following from the user:
- **Skill name**: A short snake_case identifier (max 60 chars)
- **Description**: What the skill does and when it should trigger
- **Trigger phrases**: 3-5 natural language phrases that activate the skill
- **Core workflow**: The steps the skill performs

### Step 2: Generate the skill structure

Create the following files in a dedicated skill directory:

```
skills/<skill_name>/
  SKILL.md          # Skill definition with YAML frontmatter
  CLAUDE.md         # Optional: agent instructions and context
  hooks/            # Optional: pre/post execution hooks
  templates/        # Optional: output templates
```

### Step 3: Write the SKILL.md

Follow Anthropic's skill conventions:

```markdown
---
name: <skill_name>
description: |
  <One-line description of what the skill does.>
  Triggers: <comma-separated trigger phrases>
---

# <Skill Title>

<Brief description of the skill's purpose.>

## When to use
- <Trigger phrase 1>
- <Trigger phrase 2>
- <Trigger phrase 3>

## How to use
<Concrete numbered steps for the agent to follow>

## References
<Links to relevant docs or source repos>
```

### Step 4: Validate the skill

Check the generated skill against these criteria:
- YAML frontmatter includes `name` and `description` with triggers
- "When to use" section has 3-5 trigger phrases
- "How to use" section has concrete, actionable steps
- The skill is self-contained and runnable
- No placeholder text remains
- Snake_case name is under 60 characters

### Step 5: Integration

To install the skill:
1. Copy the skill directory to `~/.claude/skills/` for global availability
2. Or place it in your project's `.claude/skills/` directory for project-scoped use
3. Claude Code will automatically discover and load the skill

## Skill design best practices

- **Single responsibility**: Each skill should do one thing well
- **Clear triggers**: Use specific, unambiguous trigger phrases
- **Concrete steps**: Instructions should be precise enough for autonomous execution
- **Self-contained**: Include all context needed; avoid external dependencies where possible
- **Subagent-friendly**: Design skills that can be composed with other skills or delegated to subagents
- **Hook-aware**: Use Claude Code hooks for pre/post processing when needed (e.g., validation, formatting)

## References

- Source: https://github.com/rayhayqal/Mythos-Claude-Skill-Forge
- Anthropic skill conventions: https://github.com/anthropics/skills
