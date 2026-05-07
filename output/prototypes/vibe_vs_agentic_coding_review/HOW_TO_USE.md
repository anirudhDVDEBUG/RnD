# How to Use

## This is a Claude Code Skill

It runs inside Claude Code as a skill — a reusable prompt template that Claude activates automatically when it matches trigger phrases.

## Install the skill

Copy the `SKILL.md` file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/vibe_vs_agentic_coding_review
cp SKILL.md ~/.claude/skills/vibe_vs_agentic_coding_review/SKILL.md
```

That's it. Claude Code will pick it up on the next conversation.

## Trigger phrases

Say any of these to Claude Code and the skill activates:

- "Review this AI-generated code for production readiness"
- "Is this vibe coded or properly engineered?"
- "Audit the code quality of these agent-written changes"
- "Help me move from vibe coding to agentic engineering on this project"
- "Check if this AI-assisted PR follows responsible coding practices"

## First 60 seconds

**Input** — Ask Claude Code to review a diff or recent changes:

```
Review the last commit for vibe coding anti-patterns
```

**Output** — Claude applies the 6-step checklist from the skill:

1. **Classifies context** — Is this throwaway or production?
2. **Reviews diff line-by-line** — Reads every change like a senior engineer
3. **Checks test coverage** — Flags missing tests
4. **Detects AI anti-patterns** — Nested try/except, over-abstraction, hallucinated imports, scope creep
5. **Validates scope** — Did the AI stay on task or wander?
6. **Makes the call** — Ship it / Needs revision / Start over

Example output from Claude:

> This looks like **vibe coding** that slipped into production code. Key issues:
> - Nested try/except around `request.get_json()` is unnecessary — Flask handles malformed JSON
> - MD5 used for password hashing — critical security issue, use bcrypt
> - Debug info leaked in 500 response: `'debug': str(e)`
> - No tests included
>
> **Verdict: Start over.** Re-prompt with: "Add a login endpoint using bcrypt for password hashing, return only safe fields, and include pytest tests."

## Standalone demo (no Claude Code needed)

The Python tool in this repo demonstrates the same detection logic:

```bash
# No dependencies required — stdlib only, Python 3.10+
bash run.sh
```

This runs 4 sample diffs through all 7 detectors and prints scored reviews.

## Using the Python module directly

```python
from review_diff import review_diff, format_review

diff_text = open("my_change.patch").read()
result = review_diff("My PR", diff_text, context="production")
print(format_review(result))
print(f"Score: {result.score}/100 — {result.classification}")
```
