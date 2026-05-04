# How to Use: Doc Audit Skill

## Install (30 seconds)

This is a **Claude Code skill** — a markdown file that teaches Claude Code a new capability.

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/doc-audit

# Copy the skill file
cp SKILL.md ~/.claude/skills/doc-audit/SKILL.md
```

That's it. No packages to install, no server to run. The skill activates inside Claude Code sessions automatically.

## Trigger Phrases

Say any of these to Claude Code in a project:

- `"audit docs"`
- `"check documentation"`
- `"docs out of date"`
- `"trim CLAUDE.md"`
- `"documentation drift"`
- `"stale docs"`
- `"doc debt"`

## First 60 Seconds

1. Open Claude Code in any repo that has markdown docs:
   ```bash
   cd ~/my-project
   claude
   ```

2. Type a trigger phrase:
   ```
   > audit docs
   ```

3. Claude will execute the 7-phase pipeline:
   - **Discovery**: finds all .md files, docstrings, doc-comments
   - **Claim Extraction**: pulls out verifiable statements ("uses Express 4", "run `npm test`")
   - **Cross-Reference**: checks each claim against actual code
   - **Triage**: categorizes as Critical / Stale / Minor / OK
   - **Interactive Resolution**: asks you how to fix each issue
   - **Atomic Commits**: one commit per fix with descriptive messages
   - **CLAUDE.md Trim**: removes redundant/outdated instructions, shows diff for approval

4. Example interaction:
   ```
   Found 3 critical issues:

   [1/3] README.md:18 — claims `src/auth.ts` exports `validateToken(jwt)`
         Actual: `validateToken(token: string, opts?: ValidateOpts)`

         1. Fix the doc to match code
         2. Fix the code to match doc
         3. Remove the claim
         4. Skip

   Your choice? > 1

   ✓ Applied fix → commit: "docs: fix validateToken signature in README"
   ```

## Requirements

- Claude Code (any version with skills support)
- A git repo with at least one markdown doc file

## Tips

- Run after major refactors or dependency upgrades
- Works best with repos that have README + CLAUDE.md + inline docs
- Each fix is an atomic commit — easy to revert individually
- The CLAUDE.md trim phase requires your approval before committing
