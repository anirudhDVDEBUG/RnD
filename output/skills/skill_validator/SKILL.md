---
name: skill_validator
description: |
  Audit and validate any SKILL.md file for quality, correctness, and best practices.
  TRIGGER: user says "validate skill", "audit SKILL.md", "check my skill", "lint skill", "score this skill", "skill quality", or references validating/auditing a Claude Code skill file.
---

# Skill Validator

Audit any SKILL.md file. Produces a scored report with critical issues, a triggering-quality score, and exact fixes.

## When to use

- "Validate my SKILL.md" or "audit this skill"
- "Check if my skill file follows best practices"
- "Score this SKILL.md for quality"
- "Lint my Claude skill before publishing"
- "What's wrong with this SKILL.md?"

## How to use

1. **Locate the SKILL.md** — Find the SKILL.md file to validate (in the current project or a path the user provides).

2. **Read the file** — Load the full contents of the SKILL.md.

3. **Run the audit checklist** — Evaluate the skill against these criteria:

   ### Structure (max 25 pts)
   - Has valid YAML frontmatter with `name` and `description` fields (10 pts)
   - `name` is snake_case, ≤60 characters (5 pts)
   - `description` includes a TRIGGER clause specifying when the skill activates (10 pts)

   ### Content Quality (max 35 pts)
   - Has a "When to use" section with 3–5 concrete trigger phrases (10 pts)
   - Has a "How to use" section with numbered, actionable steps (10 pts)
   - Steps reference real tools/commands, not vague instructions (5 pts)
   - Has a "References" section linking to source material (5 pts)
   - No placeholder or TODO content remaining (5 pts)

   ### Best Practices (max 25 pts)
   - Self-contained: does not depend on external services without fallback (10 pts)
   - Follows Anthropic skill conventions (https://github.com/anthropics/skills) (10 pts)
   - No security anti-patterns (hardcoded secrets, unsafe shell commands) (5 pts)

   ### Trigger Reliability (max 15 pts)
   - TRIGGER clause in description is specific enough to avoid false positives (8 pts)
   - TRIGGER clause covers the core use cases listed in "When to use" (7 pts)

4. **Produce the report** — Output a markdown report in this format:

   ```
   ## SKILL.md Audit Report

   **File:** <path>
   **Score:** <total>/100 (<grade>)

   ### Critical Issues
   - <issue description> → **Fix:** <exact fix>

   ### Warnings
   - <issue description> → **Suggestion:** <recommendation>

   ### Passed Checks
   - ✅ <check name>

   ### Score Breakdown
   | Category           | Score | Max |
   |--------------------|-------|-----|
   | Structure          | X     | 25  |
   | Content Quality    | X     | 35  |
   | Best Practices     | X     | 25  |
   | Trigger Reliability| X     | 15  |
   | **Total**          | **X** |**100**|
   ```

   Grades: 90–100 = A, 80–89 = B, 70–79 = C, 60–69 = D, <60 = F

5. **Offer to fix** — If the score is below 80, offer to apply the suggested fixes automatically.

## References

- Source: [Anvil-Code/skill-validator](https://github.com/Anvil-Code/skill-validator)
- Anthropic skill conventions: [github.com/anthropics/skills](https://github.com/anthropics/skills)
