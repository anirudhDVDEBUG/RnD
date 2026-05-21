# How to Use: update-skills

## What it is

A Claude Code **skill** (not an MCP server). It teaches Claude how to scan your installed skills and pull updates from their source GitHub repos.

## Install

```bash
# Clone into your Claude Code skills directory
mkdir -p ~/.claude/skills/update-skills
curl -sL https://raw.githubusercontent.com/pcx-wave/update-skills/main/SKILL.md \
  -o ~/.claude/skills/update-skills/SKILL.md
```

Or via git:

```bash
git clone https://github.com/pcx-wave/update-skills.git ~/.claude/skills/update-skills
```

The skill is active immediately — no restart needed.

## Trigger phrases

Say any of these to Claude Code:

- "Update my skills"
- "Sync skills"
- "Refresh skills"
- "Pull latest skills"
- "Check for skill updates"

Claude will then scan `~/.claude/skills/`, identify repos with upstream changes, and pull the latest SKILL.md files.

## First 60 seconds

**Input (in Claude Code):**
```
> update my skills
```

**Output (Claude responds with something like):**
```
Scanning ~/.claude/skills/ for installed skills...

Found 4 installed skills:
  - update-skills (source: pcx-wave/update-skills)
  - code-review    (source: acme/code-review-skill)
  - test-gen       (source: acme/test-gen)
  - docs-writer    (no source repo detected)

Checking for updates...
  - update-skills: already up to date (latest)
  - code-review:   updated SKILL.md (3 lines changed)
  - test-gen:      updated SKILL.md (new section added)
  - docs-writer:   skipped (no source repo)

3/4 skills checked. 2 updated, 1 skipped.
```

## Standalone demo

To see the update logic in action without Claude Code:

```bash
cd output/prototypes/update_skills
bash run.sh
```

This runs with mock data (a simulated `~/.claude/skills/` directory) so you can evaluate the workflow without touching your real config.

## Notes

- Skills without a `.git` directory or source URL in their SKILL.md are skipped.
- The skill does `git pull` for git-cloned skills, or `curl` re-fetch for URL-installed ones.
- Use `--dry-run` (tell Claude "do a dry run update of my skills") to preview without applying.
