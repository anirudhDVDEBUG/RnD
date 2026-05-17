# How to Use

## This is a Claude Code Skill

This is not a standalone tool — it's a **skill file** that teaches Claude Code how to guide CSS architecture decisions.

## Installation

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/css_architecture_guide

# Copy the skill file
cp SKILL.md ~/.claude/skills/css_architecture_guide/SKILL.md
```

That's it. Claude Code will automatically load the skill on next session.

## Trigger Phrases

Say any of these to Claude Code and the skill activates:

- "Help me organize my CSS without Tailwind"
- "How should I structure my stylesheets?"
- "I want to move away from Tailwind"
- "What's the best CSS architecture for this project?"
- "Refactor my utility classes into structured CSS"

## Does NOT trigger for

- Setting up Tailwind (opposite use case)
- CSS-in-JS questions (styled-components, emotion)
- JavaScript framework questions

## First 60 Seconds

**Step 1**: Install the skill (see above)

**Step 2**: Open Claude Code in a project with CSS/HTML files

**Step 3**: Ask:
```
Help me restructure my CSS. I have a lot of Tailwind utilities
and want to move to a cleaner architecture.
```

**Step 4**: Claude will:
1. Audit your existing utility usage
2. Propose a layer structure: `@layer reset, tokens, layout, components, utilities`
3. Extract repeated values into custom properties (design tokens)
4. Convert utility clusters into semantic component classes
5. Suggest layout primitives for common patterns

## Demo (without Claude Code)

Run the included converter to see the architecture in action:

```bash
bash run.sh
```

This runs `css_architect.py` which takes sample HTML with Tailwind classes and outputs structured CSS following the skill's architecture principles.

You can also pass your own HTML:

```bash
python3 css_architect.py your_file.html
```

## What Claude Produces

Given a component like:
```html
<div class="flex flex-col gap-4 p-6 rounded-lg shadow-md bg-white">
  <h2 class="text-2xl font-bold text-gray-900">Title</h2>
  <p class="text-base leading-relaxed text-gray-700">Content</p>
</div>
```

Claude will generate:
```css
@layer tokens {
  :root {
    --space-m: 1rem;
    --space-l: 1.5rem;
    --radius-l: 0.5rem;
    --shadow-md: 0 4px 6px rgb(0 0 0 / 0.07);
    /* ... */
  }
}

@layer components {
  .card {
    display: flex;
    flex-direction: column;
    gap: var(--space-m);
    padding: var(--space-l);
    border-radius: var(--radius-l);
    box-shadow: var(--shadow-md);
    background: var(--color-white);

    & .card-title {
      font-size: var(--text-2xl);
      font-weight: 700;
    }

    & .card-body {
      font-size: var(--text-base);
      line-height: var(--leading-relaxed);
    }
  }
}
```
