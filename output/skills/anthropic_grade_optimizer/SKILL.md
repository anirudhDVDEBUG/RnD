---
name: anthropic_grade_optimizer
description: |
  Audits Claude-directing artifacts (CLAUDE.md, SKILL.md, subagent prompts, hooks, MCP configs, API configs) against 189 cited Anthropic rules across 11 dimensions. Every finding must cite a specific rule or stay silent. Voice drift trumps score.
  Trigger: user asks to audit, lint, grade, optimize, or review their CLAUDE.md, SKILL.md, prompt files, subagent configs, hook definitions, MCP server configs, or API configuration for Anthropic best-practice compliance.
---

# Anthropic Grade Optimizer

Audit and optimize Claude-directing artifacts against 189 cited Anthropic rules across 11 quality dimensions.

## When to use

- "Audit my CLAUDE.md for Anthropic best practices"
- "Grade this SKILL.md against Anthropic prompt rules"
- "Lint my subagent prompts for compliance"
- "Optimize my MCP server config for Claude"
- "Review my hook definitions and API config against Anthropic guidelines"

## How to use

### Step 1: Identify the artifact(s) to audit

Locate the Claude-directing artifact(s) in the project. Supported artifact types:
- **CLAUDE.md** — project-level Claude instructions
- **SKILL.md** — skill definitions
- **Subagent prompts** — system/user prompts passed to subagents
- **Hook definitions** — pre/post hooks in settings.json
- **MCP configs** — Model Context Protocol server configurations
- **API configs** — Anthropic API configuration (model, temperature, system prompts)
- **Prompt files** — any file containing prompts that direct Claude behavior

### Step 2: Audit across 11 dimensions

Evaluate the artifact against each dimension. For every finding, **cite the specific Anthropic rule** or remain silent — no uncited opinions.

The 11 audit dimensions are:

1. **Clarity** — Are instructions unambiguous and precisely stated?
2. **Specificity** — Do directives use concrete examples rather than vague guidance?
3. **Structure** — Is the artifact well-organized with clear sections and hierarchy?
4. **Completeness** — Are all necessary instructions present for the intended behavior?
5. **Consistency** — Do instructions avoid contradicting each other?
6. **Voice alignment** — Does the artifact maintain a consistent, appropriate voice? (Voice drift trumps score.)
7. **Safety** — Are safety and refusal boundaries properly defined?
8. **Tool use** — Are tool-use instructions clear, correct, and well-scoped?
9. **Context management** — Does the artifact manage context window efficiently?
10. **Error handling** — Are failure modes and fallback behaviors addressed?
11. **Anthropic conventions** — Does the artifact follow official Anthropic skill/config conventions?

### Step 3: Generate the audit report

Produce a structured report with:

```markdown
## Audit Report: <artifact_name>

### Summary
- **Overall grade**: A-F
- **Dimensions passing**: X/11
- **Critical findings**: N
- **Voice drift detected**: Yes/No

### Findings by Dimension

#### 1. Clarity
- [PASS/WARN/FAIL] <finding> — **Rule**: <cited Anthropic rule>

...(repeat for each dimension with findings)

### Recommended Fixes
1. <Priority-ordered fix with before/after examples>
```

### Step 4: Apply fixes

For each recommended fix:
1. Show the specific line(s) to change with before/after
2. Cite the Anthropic rule that motivates the change
3. Apply edits to the artifact file upon user approval

**Key principle**: Voice drift (inconsistent tone, persona bleed, style shifts) is the most critical signal — it trumps raw numeric score. An artifact scoring well on other dimensions but exhibiting voice drift should be flagged as needing immediate attention.

## References

- Source: [l0z4n0-a1/skill-anthropic-grade-optimizer](https://github.com/l0z4n0-a1/skill-anthropic-grade-optimizer)
- Tags: prompt-optimization, claude-skill, linter, anthropic-rules, prompt-engineering
