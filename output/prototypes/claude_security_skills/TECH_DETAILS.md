# Technical Details

## What It Does

Claude Security Skills is a curated set of 25 SKILL.md files for Claude Code. Each skill is a structured prompt that teaches Claude a specific security audit methodology -- pattern matching, checklist evaluation, and remediation guidance. When a user says a trigger phrase (e.g., "harden my server"), Claude loads the matching skill and systematically applies it to the user's codebase, configs, or infrastructure.

The demo in this repo (`security_scanner.py`) implements 6 of these skills as standalone Python regex-based scanners to show what kind of findings each skill surfaces -- without requiring Claude or any API keys.

## Architecture

```
claude_security_skills/
  security_scanner.py      # Demo: 6 skills as Python regex scanners
  mock_project/            # Intentionally vulnerable test target
    app.py                 # Hardcoded secrets, prompt injection, OWASP issues
    package.json           # Hallucinated npm packages (slopsquatting)
    requirements.txt       # Hallucinated PyPI packages
    Dockerfile             # Root user, :latest tag, secrets in ENV
    .github/workflows/     # Unpinned actions, script injection, write-all
  run.sh                   # Entry point: runs scanner against mock_project
```

### Data Flow (demo)

1. `run.sh` invokes `security_scanner.py mock_project/`
2. Scanner walks the mock project files
3. Each skill module applies regex patterns and heuristics
4. Findings are collected into an `AuditReport` with severity/category/remediation
5. Report prints to stdout, sorted by category

### Data Flow (real Claude Code usage)

1. User says trigger phrase in Claude Code
2. Claude loads the matching SKILL.md from `~/.claude/skills/`
3. Claude reads the user's actual project files
4. Claude applies the skill's checklist/methodology using its reasoning
5. Claude returns structured findings with fixes

### Key Differences: Demo vs. Real

| Aspect | Demo (this repo) | Real (Claude + SKILL.md) |
|---|---|---|
| Detection | Regex pattern matching | LLM reasoning + pattern matching |
| False positives | Higher (regex is blunt) | Lower (Claude understands context) |
| Coverage | 6 skills, fixed patterns | 25 skills, adaptive analysis |
| Registry verification | Hardcoded known-package list | Can actually query npm/PyPI |
| Remediation | Static text | Context-aware, project-specific |

## Dependencies

- Python 3.7+ (stdlib only -- no pip packages required)
- For real usage: Claude Code with skills support

## Limitations

- **Demo is regex-only.** The standalone scanner cannot reason about code semantics. It will miss context-dependent issues and produce false positives on benign patterns.
- **Known-package lists are subsets.** The slopsquatting check uses ~35 known npm and ~35 known PyPI packages. Real usage with Claude can verify against actual registries.
- **No live infrastructure scanning.** Skills like VPS Hardening and Cloudflare Security require Claude to SSH into servers or call APIs -- the demo cannot do this.
- **No network calls.** The demo runs fully offline with mock data.
- **Skills are prompts, not code.** The 25 SKILL.md files are natural-language instructions. Their effectiveness depends on Claude's reasoning capabilities.

## Why This Matters

For teams building Claude-driven products (agent factories, lead-gen, marketing automation, voice AI):

- **AI agent guardrails** -- The OWASP LLM Top 10 and prompt injection skills directly address security risks in any product that lets users interact with LLMs. If you're building agents that take actions, LLM08 (Excessive Agency) and LLM07 (Insecure Plugin Design) checks are critical.
- **Slopsquatting/supply chain** -- AI-generated code frequently hallucinates package names. The slopsquatting skill catches these before `npm install` or `pip install` pulls in a malicious typosquat.
- **Vibe coding safety net** -- Teams moving fast with AI-generated code need automated checks for hardcoded secrets, missing input validation, and insecure patterns. These skills run as part of the dev loop, not as a separate CI step.
- **Compliance** -- GDPR/DACH skills help EU-focused products stay compliant without hiring a DPO for every project.
- **Infrastructure hardening** -- Docker, VPS, and Cloudflare skills cover the deployment layer that AI products run on.
