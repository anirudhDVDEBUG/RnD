# How to Use Skill Validator

## Install (CLI mode)

```bash
git clone https://github.com/Anvil-Code/skill-validator.git
cd skill-validator
# No pip install needed -- stdlib only, Python 3.8+
python3 skill_validator.py --help
```

## Install as a Claude Code Skill

Copy the SKILL.md from the source repo into your skills directory:

```bash
mkdir -p ~/.claude/skills/skill_validator
cp SKILL.md ~/.claude/skills/skill_validator/SKILL.md
```

**Trigger phrases** that activate the skill inside Claude Code:

- "validate skill"
- "audit SKILL.md"
- "check my skill"
- "lint skill"
- "score this skill"
- "skill quality"

Once installed, Claude will automatically invoke the audit rubric when you use any of these phrases.

## First 60 Seconds

```
$ python3 skill_validator.py samples/bad_skill.md

## SKILL.md Audit Report

**File:** samples/bad_skill.md
**Score:** 18/100 (F)

### Critical Issues
- Frontmatter missing `description` field → **Fix:** Add `description: <value>` to the YAML frontmatter block
- Name `MyAwesomeSkill` is not snake_case → **Fix:** Rename to `myawesomeskill`
- Description lacks a TRIGGER clause → **Fix:** Add "TRIGGER: user says ..." to the description field
- Missing "When to use" section → **Fix:** Add a "## When to use" section with 3-5 bullet-point trigger phrases
- Found placeholder markers: TODO → **Fix:** Replace all placeholder content with real information
- No TRIGGER clause found → **Fix:** Add TRIGGER: user says "..." to the description
- No TRIGGER clause to evaluate → **Fix:** Add a TRIGGER clause that covers use cases

### Warnings
- Section exists but lacks numbered steps → **Suggestion:** Use "1. Step one\n2. Step two" format
- Steps don't reference specific tools or commands → **Suggestion:** Add inline code
- Missing "References" section → **Suggestion:** Add a "## References" section with links

### Score Breakdown
| Category            | Score | Max |
|---------------------|-------|-----|
| Structure           | 4     | 25  |
| Content Quality     | 6     | 35  |
| Best Practices      | 8     | 25  |
| Trigger Reliability | 0     | 15  |
| **Total**           | **18**| **100** |
```

Every critical issue includes an exact fix. Apply them, re-run, and watch the score climb.

## JSON Output

```bash
python3 skill_validator.py --json SKILL.md
```

Returns a structured JSON object with `score`, `grade`, and a `checks` array -- useful for CI pipelines or batch validation of a skills directory.

## Batch Validation

```bash
for f in ~/.claude/skills/*/SKILL.md; do
  echo "--- $f ---"
  python3 skill_validator.py "$f"
done
```
