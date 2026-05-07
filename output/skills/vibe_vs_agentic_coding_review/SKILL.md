---
name: vibe_vs_agentic_coding_review
description: |
  Review AI-generated code changes using agentic engineering best practices from Simon Willison's framework.
  Distinguishes between vibe coding (fast, uncritical) and agentic engineering (disciplined, reviewed).
  TRIGGER: When reviewing AI-generated code, evaluating PR quality from AI agents, or deciding whether
  AI-written code meets production standards. Also triggers when discussing vibe coding vs responsible
  AI-assisted development workflows.
---

# Vibe Coding vs Agentic Engineering Review

Apply Simon Willison's agentic engineering framework to review AI-generated code and ensure it meets production-quality standards rather than remaining at "vibe coding" level.

## When to use

- "Review this AI-generated code for production readiness"
- "Is this vibe coded or properly engineered?"
- "Audit the code quality of these agent-written changes"
- "Help me move from vibe coding to agentic engineering on this project"
- "Check if this AI-assisted PR follows responsible coding practices"

## Background

Simon Willison defines two modes of AI-assisted programming:

**Vibe coding**: You don't look at the code closely. You might not even know how to program. You ask for a thing, get a thing, and if it works, great. If not, you tell the AI it doesn't work and cross your fingers. No concern for code quality or constraints. Great for prototypes and throwaway tools.

**Agentic engineering**: Disciplined use of AI coding agents where you maintain responsibility for code quality, review every change, write or require tests, and treat the AI as a junior developer whose output must be verified. The human remains the accountable engineer.

Willison's key insight: these two modes are converging. As AI tools improve, even experienced developers find themselves slipping from agentic engineering into vibe coding — accepting changes without thorough review. This is the danger zone.

## How to use

When reviewing AI-generated code (your own or from a PR), apply this checklist:

### 1. Classify the context

Determine if this code is:
- **Throwaway / prototype**: Vibe coding is acceptable. Ship it if it works.
- **Production / maintained**: Agentic engineering standards apply. Proceed with full review.

### 2. Review every diff line-by-line

Do NOT rubber-stamp AI output. Read the actual diff as you would a junior developer's PR:
- Does each change make sense for the stated goal?
- Are there unnecessary additions, over-engineering, or hallucinated APIs?
- Is the code consistent with existing patterns in the codebase?

### 3. Verify test coverage

- Are there tests for the new behavior?
- Do existing tests still pass?
- Consider test-driven flow: write the test first, then let the AI implement to pass it.
- If no tests exist, flag this as a gap before merging.

### 4. Check for AI anti-patterns

Common issues in AI-generated code:
- **Cargo-culted error handling**: Unnecessary try/catch blocks or validation for impossible states
- **Over-abstraction**: Helpers and utilities for one-time operations
- **Hallucinated imports**: Libraries or APIs that don't exist or have wrong signatures
- **Scope creep**: Changes beyond what was requested (extra refactoring, added comments, renamed variables)
- **Security gaps**: Missing input validation at boundaries, potential injection vectors

### 5. Validate context management

- Was the AI given sufficient context about the codebase to make good decisions?
- Are the changes scoped appropriately, or did the AI lose track of the goal?
- If the diff is very large, consider whether it should be broken into smaller, reviewable chunks.

### 6. Make the call

Rate the changes:
- **Ship it**: Code meets agentic engineering standards
- **Needs revision**: Specific issues identified, send back to the AI with precise feedback
- **Start over**: Fundamental approach is wrong; re-prompt with better context and constraints

## Key principles

1. **You are the engineer, the AI is the tool.** You own the code that ships.
2. **Reading code is as important as writing it.** If you can't explain what a change does, don't merge it.
3. **Tests are your safety net.** They catch what review misses and what AI hallucinates.
4. **Smaller diffs are better diffs.** Break large AI tasks into reviewable increments.
5. **Beware the convergence.** The better AI gets, the more tempting it is to stop reviewing. Resist this.

## References

- [Vibe coding and agentic engineering are getting closer than I'd like](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/#atom-everything) - Simon Willison (May 2026)
- [Not all AI-assisted programming is vibe coding](https://simonwillison.net/2025/Mar/19/vibe-coding/) - Simon Willison (Mar 2025)
- [Agentic Engineering Patterns guide](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/) - Simon Willison
- [High Leverage Podcast Ep. #9: The AI Coding Paradigm Shift](https://www.heavybit.com/library/podcasts/high-leverage/ep-9-the-ai-coding-paradigm-shift-with-simon-willison) - Heavybit