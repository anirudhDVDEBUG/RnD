# How to Use: Claude Design AI

## Install the skill

This is a **Claude Code skill**. To install:

```bash
# Clone the skill repo
git clone https://github.com/mikesheehan54/Claude-Code-Design-AI.git

# Copy the skill file into your Claude skills directory
mkdir -p ~/.claude/skills/claude-design-ai
cp Claude-Code-Design-AI/SKILL.md ~/.claude/skills/claude-design-ai/SKILL.md
```

Or manually create `~/.claude/skills/claude-design-ai/SKILL.md` with the contents from `skill/SKILL.md` in this repo.

## Trigger phrases

Once installed, Claude Code activates this skill when you say any of:

| Phrase | What it does |
|--------|-------------|
| "Convert this screenshot to a React component" | Analyzes an image and generates matching React/Tailwind code |
| "Generate a Tailwind CSS component" | Creates a styled component from a description |
| "Create a design system" | Generates a full set: tokens, buttons, cards, inputs, theme provider |
| "Build a responsive layout from this wireframe" | Mobile-first layout with breakpoints |
| "Create an SVG icon set" | Generates optimized SVG icons as React components |
| "Generate a shadcn/ui compatible button" | Components matching the shadcn/ui API |
| "Add dark mode toggle" | ThemeProvider + toggle with localStorage persistence |
| "Figma to React" | Translates Figma design specs into coded components |

## First 60 seconds

### 1. Run the demo (no API keys needed)

```bash
bash run.sh
```

This generates a complete design system into `output/`:

```
output/
├── components/
│   ├── Button.tsx      # 5 variants, 3 sizes, a11y
│   ├── Card.tsx        # Card + CardHeader/Title/Content
│   └── Input.tsx       # Label, error, helper text
├── icons/
│   └── Icons.tsx       # Home, Search, User, Settings, Mail
├── layout/
│   ├── Hero.tsx        # CTA section with gradient bg
│   └── Navbar.tsx      # Responsive nav + mobile menu
├── pages/
│   └── LandingPage.tsx # Full page using all components
├── theme/
│   ├── DarkModeToggle.tsx
│   └── ThemeProvider.tsx
├── design-tokens.json
├── index.ts
└── tailwind.config.js
```

### 2. Use in Claude Code

After installing the skill, open Claude Code in any React project and say:

```
> Create a design system with dark mode for my SaaS dashboard
```

Claude will generate components directly into your project, matching your existing file structure and import conventions.

### 3. Use generated components

```tsx
import { ThemeProvider, Navbar, Hero, Button, Card } from './design-system';

function App() {
  return (
    <ThemeProvider>
      <Navbar brand="MyApp" items={[{ label: 'Home', href: '/' }]} />
      <Hero headline="Welcome" subheadline="Get started" ctaText="Sign Up" ctaHref="/signup" />
      <Card hoverable>
        <Button variant="primary" size="lg">Click me</Button>
      </Card>
    </ThemeProvider>
  );
}
```

## Requirements

- **Node.js 16+** (for running the demo)
- **Claude Code** (for using the skill in real projects)
- No API keys or external services needed for the demo
