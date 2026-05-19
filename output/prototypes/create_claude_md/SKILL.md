---
name: create_claude_md
description: |
  Generate a lean, high-signal CLAUDE.md configuration file for any repository by scanning the codebase structure and conducting a focused user interview.
  Triggers: create claude.md, generate claude config, scaffold CLAUDE.md, bootstrap project config, setup claude instructions
---

# Create CLAUDE.md

Generate a comprehensive yet concise `CLAUDE.md` file for any project by scanning the repository and interviewing the user about their preferences and workflows.

## When to use

- "Create a CLAUDE.md for this project"
- "Generate Claude configuration for this repo"
- "Scaffold a CLAUDE.md from scratch"
- "Bootstrap project instructions for Claude"
- "Set up a CLAUDE.md based on this codebase"

## How to use

### Step 1: Scan the Repository

Analyze the project structure to understand the codebase:

1. **Identify the tech stack** — Read `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Gemfile`, `requirements.txt`, or equivalent manifest files to determine languages, frameworks, and dependencies.
2. **Map project structure** — Use `find`/`ls` to understand the directory layout (src, tests, docs, config, CI files).
3. **Detect build & test commands** — Look for `Makefile`, `justfile`, CI configs (`.github/workflows/`, `.gitlab-ci.yml`), and scripts in `package.json` or equivalent.
4. **Review existing configuration** — Check for `.editorconfig`, linter configs (`.eslintrc`, `ruff.toml`, `.prettierrc`), `tsconfig.json`, and formatting standards.
5. **Read existing docs** — Scan `README.md`, `CONTRIBUTING.md`, and `docs/` for conventions, architecture notes, and contribution guidelines.

### Step 2: Conduct a Focused User Interview

Ask the user **3-5 targeted questions** to capture preferences not discoverable from code alone:

1. **Coding style preferences** — e.g., "Do you prefer functional or OOP patterns? Any naming conventions beyond what linters enforce?"
2. **Testing expectations** — e.g., "Should every PR include tests? What coverage level do you target? Which test runner do you prefer?"
3. **Commit & PR workflow** — e.g., "Conventional commits? Squash merges? Any branch naming conventions?"
4. **Areas of caution** — e.g., "Are there files, directories, or patterns Claude should avoid modifying? Any legacy code that needs special handling?"
5. **Custom instructions** — e.g., "Any other rules or preferences you want Claude to always follow in this project?"

Skip questions whose answers are already clear from the repo scan.

### Step 3: Generate the CLAUDE.md

Write a `CLAUDE.md` file at the project root with the following sections:

```markdown
# CLAUDE.md

## Project Overview
<!-- One-paragraph summary: what the project does, main language/framework -->

## Tech Stack
<!-- Bullet list of languages, frameworks, key dependencies -->

## Project Structure
<!-- Brief directory layout with purpose of each top-level folder -->

## Development Commands
<!-- Common commands: build, test, lint, format, run dev server -->

## Code Style & Conventions
<!-- Naming, formatting, import ordering, patterns to follow -->

## Testing
<!-- Test framework, how to run tests, coverage expectations -->

## Git & Workflow
<!-- Commit message format, branch strategy, PR conventions -->

## Important Notes
<!-- Files to avoid, gotchas, legacy areas, performance considerations -->

## Custom Rules
<!-- User-specified instructions and preferences -->
```

**Guidelines for the output:**
- Keep it **lean and high-signal** — no filler, no obvious statements
- Use **imperative mood** for instructions ("Use snake_case", not "We use snake_case")
- Only include sections that have meaningful content
- Prefer concrete examples over abstract rules
- Target **50-150 lines** — enough to be useful, short enough to be read every time

### Step 4: Review & Refine

Present the generated `CLAUDE.md` to the user and ask:
- "Does this accurately capture your project's conventions?"
- "Anything to add, remove, or change?"

Iterate until the user is satisfied, then write the final file.

## References

- Source: [sruthik27/creating-claude-md](https://github.com/sruthik27/creating-claude-md)
