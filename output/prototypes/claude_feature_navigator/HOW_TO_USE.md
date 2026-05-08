# How to Use -- Claude Feature Navigator

## What this is

A **Claude Code skill** that turns Claude into a skill discovery assistant. It searches curated skill catalogs, recommends skills by workflow, and generates install instructions -- all from within a Claude conversation.

## Installation (30 seconds)

### Step 1 -- Create the skills directory

```bash
mkdir -p ~/.claude/skills/claude_feature_navigator
```

### Step 2 -- Copy the skill file

```bash
# From this repo:
cp SKILL.md ~/.claude/skills/claude_feature_navigator/SKILL.md

# Or from GitHub:
git clone https://github.com/ComposioHQ/awesome-claude-skills /tmp/awesome-claude-skills
cp /tmp/awesome-claude-skills/skills/claude_feature_navigator/SKILL.md \
   ~/.claude/skills/claude_feature_navigator/SKILL.md
```

### Step 3 -- Verify

```bash
head -5 ~/.claude/skills/claude_feature_navigator/SKILL.md
```

You should see YAML front-matter with `name: claude_feature_navigator`.

No `pip install`, no `npm install`, no API keys.

## Trigger phrases

Say any of these to Claude and the skill activates:

| Phrase | What happens |
|--------|-------------|
| "Find me Claude skills for testing" | Keyword search across the catalog |
| "What are the best Claude Code skills?" | Top skills by community stars |
| "Browse the awesome Claude skills list" | Full catalog overview by category |
| "Recommend skills for code review" | Workflow-based recommendations |
| "How do I install a Claude skill from GitHub?" | Step-by-step install guide |
| "What MCP servers are available?" | Filters to MCP-type entries |

## First 60 seconds

**Input:**
> "Find me Claude skills for testing"

**Output (Claude responds with):**
```
I found 1 skill matching "testing":

  test-gen       Testing    870 stars   skill
  Generate unit and integration tests for Python and TypeScript codebases.

To install:
  git clone https://github.com/composiohq/awesome-claude-skills/test-gen /tmp/test-gen
  mkdir -p ~/.claude/skills/test-gen
  cp /tmp/test-gen/SKILL.md ~/.claude/skills/test-gen/SKILL.md

Want me to search for more, or browse by category?
```

**Follow-up:**
> "Recommend skills for deployment"

**Output:**
```
For a deployment workflow, I recommend:

  + docker-compose-gen   Scaffold docker-compose.yml from project structure
  + ci-fix               Diagnose and fix failing CI pipelines
  + dep-update           Check for outdated dependencies and create upgrade PRs

Want install instructions for any of these?
```

## Running the CLI demo

```bash
bash run.sh
```

Runs a Python script that demonstrates all navigator features: top skills, category browsing, keyword search, workflow recommendations, detail views, and JSON export. No network or API keys required.

## Interactive mode

```bash
python3 navigator.py --interactive
```

Commands: `search <query>`, `category <name>`, `top [n]`, `detail <name>`, `recommend <workflow>`, `categories`, `quit`.

## Uninstall

```bash
rm -rf ~/.claude/skills/claude_feature_navigator
```
