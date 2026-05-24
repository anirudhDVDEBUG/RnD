# How to Use Claude Design Studio

## Install

```bash
git clone https://github.com/larajuniorlara/Claude-Design-Studio.git
cd Claude-Design-Studio
# No pip install needed — stdlib only, Python 3.10+
```

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/claude_design_studio
cp SKILL.md ~/.claude/skills/claude_design_studio/SKILL.md
```

### Trigger phrases

Once installed, any of these prompts will activate the skill:

- "Generate a UI design for a dashboard"
- "Create a wireframe for a mobile login screen"
- "Design a mockup for an e-commerce product page"
- "Build a responsive navigation component layout"
- "Create a UX flow for a user onboarding experience"

Claude Code will use the skill instructions to generate HTML/CSS artifacts using the design_studio module or its own design capabilities.

## Standalone CLI usage

```bash
# Dark SaaS dashboard
python3 design_studio.py --layout dashboard --theme dark --accent "#6366f1" --title "My App"

# Light landing page
python3 design_studio.py --layout landing --theme light --accent "#2563eb" \
  --title "Ship Faster" --description "Modern platform for modern teams."

# From a JSON spec file
python3 design_studio.py --json-spec spec.json -o my_design.html
```

### JSON spec format

```json
{
  "title": "Product Catalog",
  "layout": "card-grid",
  "theme": "light",
  "accent": "#059669",
  "description": "Browse our latest arrivals"
}
```

## First 60 Seconds

```
$ bash run.sh

============================================
  Claude Design Studio - Demo Run
============================================

[Claude Design Studio]
  Layout : dashboard
  Theme  : dark
  Accent : #6366f1
  Output : output/dashboard_dark.html  (7,842 bytes)
  Open in a browser to preview the design.

[Claude Design Studio]
  Layout : landing
  Theme  : light
  Accent : #2563eb
  Output : output/landing_light.html  (5,210 bytes)
  Open in a browser to preview the design.

... (2 more designs) ...

--------------------------------------------
  4 designs generated in ./output/
  Open any .html file in a browser to view.
--------------------------------------------
```

Open `output/dashboard_dark.html` in your browser. You'll see a complete SaaS dashboard with sidebar navigation, metric cards, a bar chart, and a data table — all styled, responsive, and ready to iterate on.
