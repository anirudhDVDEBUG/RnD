# How to Use: Browse Anthropic Skills Marketplace

## Install steps

```bash
git clone <this-repo>
cd browse_anthropic_skills_marketplace
# No dependencies beyond Python 3.8+
bash run.sh
```

No `pip install` needed — the browser uses only Python stdlib.

## As a Claude Skill

This repo wraps the **browse-anthropic-skills-marketplace** skill. To install it:

1. Copy the `SKILL.md` from the source into your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/browse-anthropic-skills-marketplace
   cp SKILL.md ~/.claude/skills/browse-anthropic-skills-marketplace/SKILL.md
   ```

2. Restart Claude Code. The skill activates on these trigger phrases:
   - "Browse available Claude skills"
   - "Find a skill for document generation"
   - "Install a skill from the Anthropic marketplace"
   - "What skills are available on skills.sh?"
   - "Show me enterprise skills for Claude"

## Using the Python module directly

```python
from skills_browser import search_skills, get_skill_detail, install_instructions

# Search for document-related skills
results = search_skills("PDF")
for s in results:
    print(s["name"], "—", s["description"])

# Get install instructions
skill = get_skill_detail("document-to-pdf")
print(install_instructions(skill, "claude-code"))
```

## First 60 seconds

```
$ bash run.sh

=== Anthropic Skills Marketplace Browser ===
No external dependencies required — pure Python 3.

============================================================
  Anthropic Skills Marketplace Browser
============================================================
  Source: https://skills.sh/b/anthropics/skills
  Catalog snapshot: 12 skills across 4 categories

============================================================
  1. Skill Categories
============================================================
  1. Creative & Design (3 skills)
  2. Development & Technical (3 skills)
  3. Documents (4 skills)
  4. Enterprise & Communication (2 skills)

============================================================
  3. Search: 'document'
============================================================
  Found 4 matching skills:

   1. [Documents                    ] document-to-docx
      Generate professional DOCX documents with formatting, headers, tables,
   2. [Documents                    ] document-to-pdf
      Create styled PDF reports from markdown or structured data using Report
   ...

============================================================
  6. Install Instructions (Claude Code)
============================================================
  # Install "create-mcp-server" in Claude Code

  Option A — Claude Code CLI:
    claude skill add anthropics/skills/create-mcp-server

  Option B — Manual:
    1. git clone https://github.com/anthropics/skills.git
    2. cp -r skills/skills/create-mcp-server/SKILL.md ~/.claude/skills/create-mcp-server/SKILL.md
    3. Restart Claude Code
```

The full output covers all 12 skills, category filtering, search, detail views, and JSON export.
