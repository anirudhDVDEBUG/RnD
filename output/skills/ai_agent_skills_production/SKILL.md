---
name: ai_agent_skills_production
description: |
  Scaffold and integrate production-grade AI agent skills from the DevelopersGlobal/ai-agent-skills library.
  TRIGGER when: user wants to add agent skills to a project, build production-grade AI agent capabilities,
  integrate Claude/Codex/Cursor skills, or scaffold reusable agent skill modules in Python.
  DO NOT TRIGGER when: user is doing general Python development unrelated to AI agents or skills.
---

# AI Agent Skills for Production-Grade Applications

Integrate and scaffold production-grade AI agent skills using the [DevelopersGlobal/ai-agent-skills](https://github.com/DevelopersGlobal/ai-agent-skills) library. This skill helps you set up, configure, and use reusable agent skill modules compatible with Claude, Codex, and Cursor.

## When to use

- "Add production-grade agent skills to my project"
- "Set up AI agent skills from DevelopersGlobal"
- "Scaffold a reusable Claude/Codex skill module in Python"
- "Integrate agent skills for my AI application"
- "Create a new agent skill following the ai-agent-skills pattern"

## How to use

### 1. Install the skills library

```bash
# Clone or add as a dependency
git clone https://github.com/DevelopersGlobal/ai-agent-skills.git
cd ai-agent-skills
pip install -e .
```

### 2. Explore available skills

Browse the repository for pre-built, production-grade skill modules:

```bash
ls -la skills/
```

Each skill is a self-contained Python module designed for use across multiple AI agent platforms (Claude, Codex, Cursor).

### 3. Integrate a skill into your project

```python
# Example: import and use a skill module
from ai_agent_skills import <skill_module>

# Initialize and configure the skill
skill = <skill_module>.Skill(config={...})
result = skill.run(input_data)
```

### 4. Create a new skill

When scaffolding a new skill, follow these conventions:

- Place skill modules under `skills/` directory
- Each skill should be a self-contained Python module with a clear interface
- Include a `SKILL.md` or `README.md` describing triggers, usage, and examples
- Write tests alongside the skill module
- Ensure compatibility with Claude, Codex, and Cursor agent runtimes

```python
# skills/my_new_skill/__init__.py
class Skill:
    """Production-grade agent skill."""

    def __init__(self, config=None):
        self.config = config or {}

    def run(self, input_data):
        # Implement skill logic
        pass
```

### 5. Validate and test

```bash
python -m pytest tests/
```

## Key conventions

- **Language**: Python
- **Platform compatibility**: Claude, Codex, Cursor
- **Pattern**: Each skill is a self-contained module with clear inputs/outputs
- **Quality**: Production-grade — include error handling, logging, and tests

## References

- **Source repository**: [DevelopersGlobal/ai-agent-skills](https://github.com/DevelopersGlobal/ai-agent-skills)
- **Topics**: ai-agents, claude-skills, codex-plugin, cursor, artificial-intelligence
