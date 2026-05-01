# Awesome Agent Skills Finder

Browse, search, and install community agent skills from the [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) curated collection.

## What it does

- Fetches the awesome-agent-skills catalog (falls back to mock data if offline)
- Parses skill entries with name, URL, description, category, and tags
- Supports browsing, searching by keyword, and installing skills locally
- Installs skills as `SKILL.md` files into `.claude/skills/` (project) or `~/.claude/skills/` (global)

## Install

```bash
# No external dependencies needed (Python 3 stdlib only)
pip install -r requirements.txt
```

## Run

```bash
bash run.sh
```

This runs the full demo workflow: lists categories, searches for skills, and installs one.

## CLI Usage

```bash
python3 skills_finder.py browse              # Browse all skills
python3 skills_finder.py categories           # List skill categories
python3 skills_finder.py search docker        # Search for skills matching "docker"
python3 skills_finder.py install docker-debug # Install a skill by name
python3 skills_finder.py install k8s-helper --global  # Install globally
python3 skills_finder.py demo                 # Run full demo
```

## Expected Output

```
[*] Fetching skill catalog from VoltAgent/awesome-agent-skills...
[+] Live catalog fetched successfully.
[+] Parsed 21 skills from catalog.

--- Step 1: List Categories ---
  - Backend (3 skills)
  - Database (3 skills)
  - DevOps (4 skills)
  ...

--- Step 2: Search for 'docker' ---
  1. docker-debug
     Category: DevOps
     Desc:     Debug Docker containers interactively
     ...

--- Step 3: Install a skill (project-level) ---
[+] Installed skill 'docker-debug' to: .claude/skills/docker-debug.md
```
