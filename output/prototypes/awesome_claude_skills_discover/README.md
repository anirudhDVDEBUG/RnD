# Awesome Claude Skills Discovery Tool

Discover, browse, search, and install community Claude Skills from the [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) curated list.

## What it does

1. **Fetches** the latest skill catalog from GitHub (falls back to built-in sample data if offline)
2. **Parses** markdown entries into structured skill records with name, URL, description, category, and star count
3. **Browses** categories with skill counts
4. **Searches** skills by keyword across name, description, and category
5. **Installs** a skill stub into `.claude/skills/` with metadata and instructions

## Install

```bash
# Python 3.6+ required, no external dependencies
pip install -r requirements.txt   # (empty - stdlib only)
```

## Run

```bash
bash run.sh
```

Or use individual commands:

```bash
python3 discover.py demo           # Full demo walkthrough
python3 discover.py browse         # List categories
python3 discover.py list           # List all skills
python3 discover.py search docker  # Search by keyword
python3 discover.py install docker-skill  # Install a skill
```

## Expected output

The demo run will:
- Fetch the skill catalog from GitHub (or use sample data)
- Show parsed skill count
- List all categories with counts
- Search for "docker", "git", "test", and "mcp"
- Install the top-starred skill into `.claude/skills/`
- Verify the installation

```
============================================================
  Awesome Claude Skills Discovery Tool
  Demo Run
============================================================

--- Step 1: Fetch Skill Catalog ---
[*] Fetching catalog from https://raw.githubusercontent.com/... ...
[+] Catalog fetched and cached (12345 bytes)

--- Step 2: Parse Skills ---
[+] Parsed 27 skills from catalog

--- Step 3: Browse Categories ---
  - AI Agents: 3 skills
  - Automation: 3 skills
  - Code Quality: 4 skills
  ...

--- Step 4: Search for 'docker' ---
  [DevOps] [5120 stars]
  docker-skill
  ...

--- Step 5: Install a Skill ---
[+] Installed skill stub: .claude/skills/docker-skill.md

--- Step 6: Verify Installation ---
[+] Skills directory: .claude/skills/
    docker-skill.md (234 bytes)

============================================================
  Demo complete!
============================================================
```
