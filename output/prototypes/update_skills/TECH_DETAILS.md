# Tech Details: update-skills

## What it does

update-skills is a Claude Code skill that automates keeping your custom skills current. When triggered, Claude scans the `~/.claude/skills/` directory, parses each skill's SKILL.md for source repository metadata (frontmatter `source` field or embedded GitHub URLs), then fetches the latest version from upstream. For git-cloned skills it runs `git pull`; for URL-installed skills it re-downloads SKILL.md via the GitHub raw content API.

The skill also validates that updated SKILL.md files contain valid YAML frontmatter (the `---` delimited header with `name` and `description` fields), rejecting corrupt downloads.

## Architecture

```
~/.claude/skills/
  ├── skill-a/
  │   ├── SKILL.md          ← has frontmatter with source repo
  │   └── .git/             ← git-cloned → uses git pull
  ├── skill-b/
  │   └── SKILL.md          ← has GitHub URL in body → uses curl
  └── skill-c/
      └── SKILL.md          ← no source info → skipped
```

**Key files in this demo:**

| File | Purpose |
|------|---------|
| `update_skills.py` | Core logic: scan, detect sources, fetch, validate |
| `run.sh` | Creates mock skills dir, runs demo end-to-end |
| `SKILL.md` | The actual skill definition Claude Code reads |

**Data flow:**
1. Enumerate subdirectories of `~/.claude/skills/`
2. For each, parse SKILL.md frontmatter for `source` field or scan body for GitHub repo patterns
3. Determine update method: `git pull` (if `.git/` exists) or `curl` raw GitHub URL
4. Fetch latest SKILL.md, validate YAML frontmatter
5. Write updated file, report diff summary

**Dependencies:** Python 3.8+ standard library only (no pip packages). Uses `subprocess` for git, `urllib` for HTTP fetches, `re` for YAML frontmatter parsing.

## Limitations

- Only supports GitHub-hosted source repos (no GitLab, Bitbucket).
- Does not handle authentication — private repos require pre-configured git credentials or SSH keys.
- Does not version-lock skills; always pulls latest `main` branch.
- No rollback mechanism — if an update breaks a skill, you must manually revert.
- Skills installed without any source metadata (no git, no URL) are silently skipped.
- Does not update files beyond SKILL.md (if a skill bundles scripts or configs, those won't sync unless git-cloned).

## Why it matters

For teams building Claude-driven products (agent factories, lead-gen pipelines, marketing automation), skills are becoming a key extensibility layer. As skill ecosystems grow, manually updating dozens of skills is unsustainable. This pattern — a "skill that manages skills" — is an early example of meta-tooling for Claude Code, similar to package managers for traditional development. Anyone building a skill registry or distribution system will want this update-check-and-sync loop as a primitive.
