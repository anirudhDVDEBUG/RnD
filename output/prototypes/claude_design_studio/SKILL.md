---
name: claude_design_studio
description: |
  UI/UX design generator and plugin suite for Claude Code. Creates professional user interface designs, wireframes, mockups, and component layouts directly from natural language descriptions.
  Triggers: generate UI design, create wireframe, design mockup, build UI component, UX layout generator
---

# Claude Design Studio

A Claude Code skill for generating professional UI/UX designs, wireframes, mockups, and component layouts from natural language prompts.

## When to use

- "Generate a UI design for a dashboard"
- "Create a wireframe for a mobile login screen"
- "Design a mockup for an e-commerce product page"
- "Build a responsive navigation component layout"
- "Create a UX flow for a user onboarding experience"

## How to use

1. **Describe the design you need**: Provide a natural language description of the UI/UX you want — specify the type (wireframe, mockup, component), target platform (web, mobile, desktop), and any style preferences.

2. **Generate the design output**: The skill produces structured design artifacts including:
   - HTML/CSS mockups with responsive layouts
   - Component hierarchies and design specifications
   - Color palettes, typography scales, and spacing systems
   - Interactive element descriptions and state definitions

3. **Iterate on the design**: Refine the output by requesting changes such as:
   - Adjusting layout, colors, or typography
   - Adding or removing UI components
   - Changing responsive breakpoints
   - Modifying interaction patterns

4. **Export the result**: The generated HTML/CSS files can be directly used in your project or serve as reference specifications for implementation.

### Design Capabilities

- **Wireframes**: Low-fidelity structural layouts for rapid prototyping
- **Mockups**: High-fidelity visual designs with real content and styling
- **Component Libraries**: Reusable UI component definitions (buttons, forms, cards, navbars)
- **Full Page Layouts**: Complete page designs for dashboards, landing pages, settings screens, etc.
- **Design Systems**: Color tokens, typography scales, spacing units, and design tokens
- **Responsive Design**: Multi-breakpoint layouts for mobile, tablet, and desktop

### Example

```
/design Create a modern SaaS dashboard with a sidebar navigation, header with user avatar,
main content area with 4 metric cards and a line chart, using a dark theme with blue accents.
```

The skill generates a complete HTML/CSS file implementing the described design, ready to preview in a browser.

## References

- Source: [larajuniorlara/Claude-Design-Studio](https://github.com/larajuniorlara/Claude-Design-Studio)
- Tags: claude-skill, ui-ux-design, code-plugin, design-tools
