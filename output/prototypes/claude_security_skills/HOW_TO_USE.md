# How to Use Claude Security Skills

## Install (Claude Code Skill)

This is a **Claude Code skill** -- a SKILL.md file that Claude reads when triggered.

### 1. Clone the full skill set

```bash
git clone https://github.com/GoldenWing-360/claude-security-skills.git
```

### 2. Drop into your Claude skills directory

```bash
# Copy the entire repo into Claude's skills folder
cp -r claude-security-skills ~/.claude/skills/claude_security_skills
```

Or symlink it:

```bash
ln -s "$(pwd)/claude-security-skills" ~/.claude/skills/claude_security_skills
```

### 3. Verify Claude sees it

Open Claude Code and type any trigger phrase (see below). Claude will load the SKILL.md and apply the relevant security checklist.

## Trigger Phrases

Say any of these to Claude Code and it will activate the matching skill:

| Phrase | Skill activated |
|---|---|
| "security audit" | Full multi-category audit |
| "harden my server" | VPS Hardening |
| "WordPress security" | WordPress audit |
| "check for prompt injection" | Prompt Injection Defense |
| "OWASP LLM review" | OWASP LLM Top 10 checklist |
| "slopsquatting check" | Hallucinated package detection |
| "Docker security" | Container security audit |
| "GitHub Actions security" | Workflow hardening |
| "incident response" | IR playbook |
| "GDPR compliance" | GDPR/DACH audit |
| "MCP server security" | MCP transport/auth audit |
| "webshell detection" | Malicious file scan |

## First 60 Seconds

### Option A: Run the demo (no install needed)

```bash
bash run.sh
```

This scans `mock_project/` -- an intentionally vulnerable project with hardcoded secrets, hallucinated packages, Docker misconfigs, prompt injection flaws, and insecure GitHub Actions. You'll see a full prioritized report in ~1 second.

### Option B: Use with Claude Code on your own project

After installing the skill (step 2 above), open Claude Code in your project directory and say:

```
Run a security audit on this project
```

Claude will:
1. Identify your stack (Node, Python, Docker, CI, etc.)
2. Run the relevant skill checklists
3. Return prioritized findings with severity, description, and fix

### Example Output

```
User: Check my package.json for slopsquatting

Claude: I'll scan your dependencies against known registries.

  [HIGH] Possibly hallucinated npm package: ai-prompt-utils
    'ai-prompt-utils' not found in npm registry.
    Fix: Run `npm view ai-prompt-utils` to verify. Check for typosquatting.

  [HIGH] Possibly hallucinated npm package: llm-safety-wrapper
    Fix: Run `npm view llm-safety-wrapper` to verify.

  3 of 9 dependencies could not be verified. Review before `npm install`.
```

## What the Demo Covers vs. the Full Skill Set

| Category | Demo (`run.sh`) | Full skill set (25 skills) |
|---|---|---|
| Slopsquatting | Yes | Yes |
| Prompt Injection | Yes | Yes + deeper patterns |
| Hardcoded Secrets | Yes | Yes |
| Docker Security | Yes | Yes |
| OWASP LLM Top 10 | Yes (6 of 10) | All 10 |
| GitHub Actions | Yes | Yes |
| VPS Hardening | -- | SSH, firewall, fail2ban, kernel |
| WordPress | -- | Plugin audit, wp-config, XML-RPC |
| Cloudflare | -- | WAF, rate limiting, bot mgmt |
| Next.js | -- | CSP, API routes, SSRF |
| MCP Server | -- | Transport, tools, auth |
| Incident Response | -- | Triage, containment, forensics |
| GDPR/DACH | -- | Data inventory, DSAR, breach |
| Webshell Detection | -- | PHP/JSP/ASPX shell patterns |
