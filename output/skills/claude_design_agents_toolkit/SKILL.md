---
name: claude_design_agents_toolkit
description: |
  AI-powered design agents toolkit for Claude Code. Provides subagents and hooks for UI/UX design tasks including generating layouts, color palettes, component specs, and design-to-code workflows.
  Triggers: design agent, UI design, design toolkit, claude design, design plugin
---

# Claude Design Agents Toolkit

A suite of AI design agents and hooks for Claude Code that assist with UI/UX design tasks, component generation, layout scaffolding, and design-to-code translation.

## When to use

- "Generate a UI layout for this page"
- "Create a color palette and design tokens for my project"
- "Convert this design spec into code components"
- "Set up design agents and hooks in my Claude Code project"
- "Scaffold a component library with consistent styling"

## How to use

1. **Clone the toolkit** into your project or install as a Claude Code skill:
   ```bash
   git clone https://github.com/Alfredo7777777/claude-design-agents-toolkit.git
   ```

2. **Use design agents** by describing your design needs. The toolkit provides subagents specialized for:
   - **Layout generation** — Describe a page or screen and get structured layout scaffolding (HTML/CSS/Tailwind).
   - **Color & theme** — Generate color palettes, design tokens, and theme configurations.
   - **Component specs** — Turn wireframe descriptions into detailed component specifications.
   - **Design-to-code** — Translate visual design references into working frontend code.

3. **Integrate hooks** for automated design checks:
   - Add the provided hooks to your `.claude/settings.json` to run design linting or consistency checks on generated UI code.

4. **Iterate on designs** by providing feedback. The agents refine layouts, spacing, typography, and color choices based on your instructions.

### Example workflow

```
User: Design a dashboard layout with a sidebar nav, header, and main content area using Tailwind CSS.

The toolkit agent will:
- Generate semantic HTML structure
- Apply responsive Tailwind utility classes
- Propose a color scheme with design tokens
- Output ready-to-use component code
```

## References

- Source: [Alfredo7777777/claude-design-agents-toolkit](https://github.com/Alfredo7777777/claude-design-agents-toolkit)
- Tags: claude-code, design-tools, agent-plugin, claude-skill, ui-design
