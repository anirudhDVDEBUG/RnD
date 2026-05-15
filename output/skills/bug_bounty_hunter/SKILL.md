---
name: Bug Bounty Hunter
description: |
  Autonomous bug bounty hunting framework using multi-agent orchestration.
  TRIGGER: user says "hunt", "bug bounty", "pentest target", "find vulnerabilities", "security scan", "recon target", "OWASP scan"
---

# Bug Bounty Hunter

Autonomous bug bounty hunting framework powered by Claude Code. Orchestrates 20 specialized AI agents with state-machine workflow to perform reconnaissance, vulnerability discovery, exploitation validation, and reporting against authorized targets.

## When to use

- "Hunt target.com for vulnerabilities"
- "Run a bug bounty scan against my authorized target"
- "Pentest this web application and find security issues"
- "Perform recon and vulnerability assessment on this domain"
- "Scan for OWASP Top 10 vulnerabilities on my app"

## How to use

### Prerequisites

1. **Clone the framework:**
   ```bash
   git clone https://github.com/h4ckologic/bughunter-ai.git
   cd bughunter-ai
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure credentials:**
   - Set up your Anthropic API key
   - Configure Burp Suite MCP integration if using active scanning
   - Set up the credential vault for target authentication

### Running a Hunt

1. **Confirm authorization:** Before scanning any target, verify you have explicit written authorization (bug bounty program, pentest engagement, or own infrastructure).

2. **Initialize the hunt:**
   ```bash
   hunt target.com
   ```

3. **Agent pipeline stages:**
   - **Recon agents** — subdomain enumeration, port scanning, technology fingerprinting
   - **Discovery agents** — endpoint mapping, parameter discovery, authentication flow analysis
   - **Vulnerability agents** — injection testing (SQLi, XSS, SSRF, IDOR), misconfig detection, OWASP Top 10 checks
   - **Validation agents** — exploit proof-of-concept generation, false positive elimination
   - **Reporting agents** — structured vulnerability reports with severity ratings, remediation guidance
   - **LLM Security agents** — prompt injection, training data extraction, model manipulation checks

4. **Review results:** The framework produces structured reports with findings, evidence, severity scores, and remediation recommendations.

### Key Architecture

- **State-machine orchestration** — agents transition through defined phases (recon → discovery → exploitation → reporting)
- **20 specialized agents** — each agent handles a specific security testing domain
- **Burp Suite MCP integration** — connects to Burp Suite for active scanning capabilities
- **Credential vault** — secure storage for target authentication credentials
- **LLM security track** — dedicated agents for AI/LLM-specific vulnerability classes

### Important Notes

- **Authorization required:** Only use against targets where you have explicit permission (bug bounty programs, authorized pentests, or your own infrastructure)
- **Scope compliance:** Respect program scope, rate limits, and rules of engagement
- **Responsible disclosure:** Follow coordinated disclosure practices for any findings

## References

- **Repository:** https://github.com/h4ckologic/bughunter-ai
- **Language:** TypeScript
- **Key integrations:** Burp Suite MCP, Playwright, Claude Code
- **Security frameworks:** OWASP Top 10, LLM Security