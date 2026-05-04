---
name: vibe_coding_skills
description: |
  Vibe coding workflow skills for natural-language-driven AI development.
  TRIGGER: user mentions "vibe coding", "vibe skills", "describe and code",
  "natural language coding", "let AI write the code", "vibe-driven development",
  "prompt-first coding", "conversational coding workflow", "code from description"
---

# Vibe Coding Skills

A collection of agent skills for "vibe coding" — the development workflow where you describe what you want in natural language and let AI agents write, iterate, and refine the code. These skills help structure the vibe coding process for reliable, high-quality results.

## When to use

- "I want to vibe code a new feature — just describe it and have AI build it"
- "How do I structure my prompts for vibe coding?"
- "Help me set up a vibe coding workflow for my project"
- "I want to describe what I need and let the agent handle implementation"
- "What are best practices for natural-language-driven development?"

## How to use

### Step 1: Set the Context (Ground the Vibe)

Before describing what you want built, establish context so the agent produces relevant code:

1. **State the tech stack** — Language, framework, key libraries (e.g., "This is a Next.js 14 app with TypeScript and Tailwind")
2. **Point to existing patterns** — Reference existing files the agent should follow (e.g., "Follow the pattern in `src/components/Button.tsx`")
3. **Define constraints** — Performance requirements, accessibility needs, API compatibility

### Step 2: Describe the Intent (Not the Implementation)

Write your request focusing on *what* you want, not *how* to build it:

1. **Lead with the goal** — "I need a search bar that filters products by name and category"
2. **Describe behavior** — "When the user types, results update after 300ms debounce. Empty query shows all items."
3. **Specify edge cases** — "If no results match, show a 'No results found' message with a clear-filters button"
4. **Skip implementation details** — Let the agent choose the approach; intervene only if it picks something wrong

### Step 3: Iterate in Conversation

Vibe coding is iterative. Refine through natural dialogue:

1. **Review the output** — Read through the generated code and test it
2. **Give directional feedback** — "Make the animation smoother" or "This is too complex, simplify it"
3. **Steer, don't rewrite** — Instead of dictating code changes, describe the desired outcome
4. **Checkpoint working states** — Commit when something works before asking for the next change

### Step 4: Validate and Harden

Once the feature works, shift from vibing to verifying:

1. **Ask the agent to add tests** — "Write tests for the search component covering empty query, partial match, and no results"
2. **Check edge cases** — "What happens if the API is slow? Add loading and error states"
3. **Review for quality** — Ask the agent to review its own code for security issues, performance, and accessibility

### Best Practices

| Practice | Why |
|---|---|
| **One feature per conversation** | Keeps context focused; avoids agent confusion |
| **Commit after each working increment** | Creates restore points; makes rollback easy |
| **Show, don't tell** | Paste example data, screenshots, or existing code rather than lengthy descriptions |
| **Name things explicitly** | "Add a `ProductSearchBar` component" is better than "add a search thing" |
| **Let the agent ask questions** | If your description is ambiguous, a good agent will clarify — let it |
| **Avoid micro-managing** | Trust the agent's implementation choices; correct only when wrong |

### Anti-Patterns to Avoid

- **Wall-of-text prompts** — Break complex features into smaller, sequential requests
- **Dictating implementation** — If you're writing pseudocode, you're not vibe coding
- **Skipping review** — Always read generated code before moving on
- **Never committing** — Vibe coding without checkpoints leads to lost work
- **Ignoring tests** — Vibe-coded features need tests just like hand-written ones
