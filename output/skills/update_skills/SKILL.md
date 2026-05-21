---
name: update-skills
description: |
  Keep all your custom Claude Code skills up-to-date by syncing them from their source repositories.
  Triggers: update skills, sync skills, refresh skills, pull latest skills, skill updater
---

# Update Skills

Automatically update and sync your installed Claude Code custom skills from their original source repositories. This skill scans your installed skills, checks their source repos for updates, and pulls the latest versions.

## When to use

- "Update my skills" — sync all installed custom skills to their latest versions
- "Check for skill updates" — see which skills have newer versions available
- "Refresh my Claude Code skills" — pull the latest changes for all skills
- "Sync skills from GitHub" — update skills that were installed from GitHub repos
- "Keep my skills up to date" — run the skill updater to fetch latest versions

## How to use

1. **Check for updates**: Scan all installed custom skills in `~/.claude/skills/` and identify which ones have upstream changes available.

2. **Update all skills**: For each skill that has a source repository defined, pull the latest version of the SKILL.md and any associated files.

3. **Update a specific skill**: Target a single skill by name to update only that one.

### Steps

1. List all installed skills:
   ```bash
   ls ~/.claude/skills/
   ```

2. For each skill directory that contains a `.git` directory or a source URL reference, check for updates:
   ```bash
   cd ~/.claude/skills/<skill-name> && git pull origin main
   ```

3. For skills installed via URL or registry, re-fetch the latest SKILL.md from the source repository:
   ```bash
   curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/SKILL.md -o ~/.claude/skills/<skill-name>/SKILL.md
   ```

4. Verify updated skills are valid by checking that SKILL.md contains proper YAML frontmatter.

5. Report which skills were updated and which are already at their latest version.

### Configuration

- Skills are stored in `~/.claude/skills/` by default
- Each skill tracks its source repository for update checks
- Use `--dry-run` to preview updates without applying them

## References

- Source: [pcx-wave/update-skills](https://github.com/pcx-wave/update-skills) (⭐ 14)
- Topics: claude, claude-code, claude-skill, productivity, updater
- Language: Python
