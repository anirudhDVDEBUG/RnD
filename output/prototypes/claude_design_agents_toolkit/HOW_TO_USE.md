# How to Use — Claude Design Agents Toolkit

## Install

```bash
git clone https://github.com/Alfredo7777777/claude-design-agents-toolkit.git
cd claude-design-agents-toolkit
```

No dependencies beyond Python 3.8+ standard library.

## Set up as a Claude Code Skill

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/claude_design_agents_toolkit
   ```

2. Copy the SKILL.md into it:
   ```bash
   cp SKILL.md ~/.claude/skills/claude_design_agents_toolkit/SKILL.md
   ```

3. **Trigger phrases** that activate this skill:
   - "Generate a UI layout for this page"
   - "Create a color palette and design tokens"
   - "Convert this design spec into code"
   - "Scaffold a component library"
   - "Design a dashboard layout"

## Integrate design-lint hooks (optional)

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "python3 -c \"from design_hooks import lint_report; import sys; print(lint_report(open(sys.argv[1]).read(), sys.argv[1]))\" \"$TOOL_FILE_PATH\""
      }
    ]
  }
}
```

This runs the design linter every time Claude writes an HTML file.

## First 60 seconds

```bash
# 1. Run the full demo (no API keys needed)
bash run.sh

# 2. Open the generated dashboard in your browser
open output/dashboard.html    # macOS
xdg-open output/dashboard.html  # Linux

# 3. Use agents in your own Python code
python3 -c "
from design_agents import DesignToCodeAgent

agent = DesignToCodeAgent('MyStartup', theme='sunset')
page = agent.generate_page('landing')
open('my-landing.html', 'w').write(page['html'])
print('Wrote my-landing.html')
"
```

**Input:** A layout type (`dashboard`, `landing`, `form`) + optional app name and theme (`ocean`, `forest`, `sunset`, `slate`).

**Output:**
- Complete HTML page with Tailwind CSS (loads via CDN, opens directly in browser)
- CSS custom properties file for design tokens
- Tailwind `theme.extend` config JSON
- Component specs as structured JSON

## Agent API reference

| Agent | Method | Returns |
|---|---|---|
| `LayoutAgent(app_name)` | `.generate("dashboard")` | HTML string |
| `ColorAgent()` | `.generate_tokens("ocean")` | `DesignTokens` object |
| `ComponentAgent()` | `.get_spec("button")` | `ComponentSpec` object |
| `DesignToCodeAgent(name, theme)` | `.generate_page("landing")` | `{html, css_variables, tailwind_config}` |
