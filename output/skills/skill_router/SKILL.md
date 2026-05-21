---
name: Skill Router
description: |
  A meta-skill that routes user requests to the best-matching installed Claude Code skill.
  Operates in suggest mode (recommends a skill) or silent auto-routing mode.
  TRIGGER: When the user asks which skill to use, wants to find the right skill for a task,
  says "route this", "which skill handles", or has multiple skills installed and needs help choosing.
---

# Skill Router

A meta-skill for Claude Code that intelligently routes requests to the right installed skill — either by suggesting the best match or silently auto-routing.

## When to use

- "Which skill should I use for this task?"
- "Route this request to the right skill"
- "I have multiple skills installed — which one handles X?"
- "Find the best skill for generating a landing page"
- "Auto-route this to the appropriate skill"

## How to use

### Step 1: Inventory installed skills

Scan the current project for all installed skills:

1. Check `.claude/skills/` directory for all `SKILL.md` files
2. Check `.claude/CLAUDE.md` or any referenced skill files
3. Parse each skill's frontmatter (`name`, `description`, trigger conditions)
4. Build a routing table of skill name → description → trigger patterns

### Step 2: Analyze the user's request

1. Identify the core intent of the user's request (e.g., "build a landing page", "write tests", "deploy to production")
2. Extract key domain signals: technologies mentioned, task type, output format expected
3. Match against each installed skill's trigger patterns and description

### Step 3: Route to the best skill

**Suggest mode (default):**
- Present the top 1–3 matching skills ranked by relevance
- For each match, explain why it fits the request
- Let the user confirm before invoking the chosen skill
- Example output:
  ```
  Based on your request, I recommend:
  1. **landing-page-builder** — Matches your request to create a marketing page (95% match)
  2. **html-generator** — Can produce static HTML output (60% match)
  
  Would you like me to use skill #1?
  ```

**Silent auto-routing mode:**
- If the user says "auto-route" or "just do it", skip the suggestion step
- Automatically invoke the highest-confidence match
- Only fall back to suggest mode if confidence is below 70% or multiple skills tie

### Step 4: Hand off execution

1. Once a skill is selected, invoke it by following its SKILL.md instructions
2. Pass through the user's original request context
3. If no matching skill is found, inform the user and suggest they install a relevant skill or proceed manually

## Routing rules

- **Exact trigger match** (skill trigger phrase matches user input): highest priority
- **Domain match** (skill description keywords overlap with request): medium priority
- **Fallback**: If no skill scores above 50% confidence, tell the user no strong match was found and offer to proceed without a skill
- Never fabricate skills that aren't installed — only route to skills that actually exist in the project

## References

- Source: [pcx-wave/skill-router](https://github.com/pcx-wave/skill-router) (GitHub)
