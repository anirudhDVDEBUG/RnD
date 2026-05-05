# How To Use

## Install as a Claude Code Skill

This is a **Claude Code skill**. To install it:

```bash
mkdir -p ~/.claude/skills/metalbear_skills_registry
cp SKILL.md ~/.claude/skills/metalbear_skills_registry/SKILL.md
```

Or for project-scoped installation:

```bash
mkdir -p .claude/skills
cp SKILL.md .claude/skills/metalbear_skills_registry.md
```

### Trigger Phrases

Once installed, the skill activates when you say things like:

- "Find a skill for Kubernetes debugging"
- "Install a Claude Code skill from the MetalBear registry"
- "What community skills are available for Docker?"
- "Browse the skills registry for testing utilities"
- "Contribute my skill to the MetalBear skills repo"

It will NOT trigger for writing your own SKILL.md from scratch or unrelated package registries.

## CLI Tool (this demo)

The included `skills_registry.py` provides a standalone CLI for exploring the registry:

```bash
pip install -r requirements.txt
python skills_registry.py --help
```

### Commands

```bash
# List all available skills
python skills_registry.py list

# Search by keyword
python skills_registry.py search "docker"

# Show details for a specific skill
python skills_registry.py show docker-compose-gen

# Install a skill into your project
python skills_registry.py install docker-compose-gen

# Install a skill globally
python skills_registry.py install docker-compose-gen --global
```

## First 60 Seconds

```bash
# 1. Run the demo
bash run.sh

# 2. See available skills listed with descriptions
# 3. Search narrows results by keyword
# 4. Install copies the SKILL.md into .claude/skills/

# Output:
# === MetalBear Skills Registry Demo ===
#
# Available skills (12):
#   k8s-debug             Debug Kubernetes pods, services, and deployments
#   docker-compose-gen    Generate docker-compose.yml from project structure
#   ...
#
# Searching for "test"...
#   pytest-gen            Generate pytest test suites from source code
#   load-test-k6         Create k6 load test scripts with AI assistance
#
# Installing "pytest-gen"...
#   Installed -> .claude/skills/pytest-gen.md
```

## Using Inside Claude Code (After Skill Install)

Once the skill is active in Claude Code, just ask naturally:

> "Find me a skill for generating API documentation"

Claude will clone the registry, search it, and offer to install matching skills — all within your session.
