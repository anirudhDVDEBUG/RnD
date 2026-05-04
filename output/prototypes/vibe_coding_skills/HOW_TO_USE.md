# How to Use: Vibe Coding Skills

## What This Is

A **Claude Code skill** — a markdown file that teaches Claude a structured workflow for "vibe coding" (natural-language-driven development). When triggered, Claude follows a 4-step process instead of jumping straight to code.

## Installation

### As a Claude Code Skill

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/vibe_coding_skills
   ```

2. Copy the skill file:
   ```bash
   cp SKILL.md ~/.claude/skills/vibe_coding_skills/SKILL.md
   ```

3. Restart Claude Code (or start a new session). The skill is now active.

### Trigger Phrases

Say any of these to activate the skill:

- "I want to vibe code a new feature"
- "Help me with vibe coding"
- "Let AI write the code, I'll describe what I need"
- "Set up a vibe coding workflow"
- "Describe and code"
- "Natural language coding"
- "Prompt-first coding"
- "Conversational coding workflow"

### As a Standalone Planning Tool

No installation needed — just run the Python demo:

```bash
# Clone this repo
git clone <this-repo-url>
cd vibe_coding_skills

# Run with built-in examples
python3 vibe_planner.py

# Or pass your own request
python3 vibe_planner.py "Build a chat widget with Vue and WebSocket support"
```

**Dependencies:** Python 3.8+ (standard library only, no pip install needed).

## First 60 Seconds

### With the Claude Skill installed:

```
You:    "I want to vibe code a search feature for my Next.js app"

Claude: Following the vibe coding workflow:

        Step 1 — Ground the Vibe:
        What's your tech stack? I see Next.js — are you using TypeScript?
        App Router or Pages? Any UI library (Tailwind, shadcn)?

        Step 2 — Let's describe the intent:
        What should the search do? What data does it search?
        What happens when there are no results?

        ...instead of immediately dumping 200 lines of code.
```

### With the standalone planner:

```
$ python3 vibe_planner.py "Create a product filter sidebar in React with
  TypeScript and Tailwind. Users can filter by category, price range, and
  rating. Handle the empty results and loading states."

================================================================
  VIBE CODING PLAN
================================================================

Feature: product filter sidebar in React with TypeScript and Tailwind
  Detected stack: React, Tailwind CSS, TypeScript

--- Step 2: Intent Analysis ---
  UI elements:  filter, input, list, select, sidebar, slider
  Behaviors:    change, load, select
  Edge cases:   empty, loading

--- Step 3: Recommended Iteration Steps ---
  1. Ground context: state stack as React, Tailwind CSS, TypeScript
  2. Describe the UI: request filter, input, list, select components
  3. Describe the core behavior: 'product filter sidebar in React...'
  4. Specify interactions: change, load, select
  5. Review first output — steer with directional feedback
  6. Commit the working increment before requesting changes
  7. Handle edge cases: empty, loading
  8. Request tests covering happy path, edge cases, and error states
  9. Ask agent to self-review for security, performance, and a11y

--- Step 4: Validation Checklist ---
  [ ] Feature works for the primary use case (happy path)
  [ ] Code follows existing project patterns and conventions
  [ ] UI components are accessible
  [ ] User interactions behave as described
  [ ] Error states handled gracefully
  [ ] No security vulnerabilities
  [ ] Tests written and passing
  [ ] Code committed at working checkpoint

--- Anti-Pattern Warnings ---
  None detected — your request looks well-structured!
```

## Tips

- **One feature per conversation** — don't try to vibe-code an entire app in one go
- **Commit after each working step** — vibe coding without checkpoints = lost work
- **Let Claude ask questions** — ambiguity is better resolved upfront than in code
- **Steer, don't rewrite** — say "make it simpler" instead of dictating exact code changes
