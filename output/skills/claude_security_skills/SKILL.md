---
name: claude_security_skills
description: |
  25 production-tested defensive security skills for Claude Code covering WordPress, VPS, Cloudflare, Next.js hardening, AI agent guardrails, MCP security, prompt injection defense, OWASP LLM Top 10, LLM coding failure modes (slopsquatting, hallucinated APIs, sycophancy), incident response, and GDPR/DACH compliance.
  Triggers: "security audit", "harden my server", "check for prompt injection", "OWASP LLM review", "incident response", "WordPress security", "VPS hardening", "Cloudflare security", "Next.js security", "MCP server security", "docker security", "webshell detection", "slopsquatting check", "GDPR compliance", "GitHub Actions security"
---

# Claude Security Skills

25 production-tested defensive security skills for Claude Code. Covers infrastructure hardening, AI/LLM-specific threats, web application security, incident response, and compliance.

## When to use

- "Run a security audit on my WordPress site / VPS / Next.js app"
- "Check my code for prompt injection vulnerabilities or OWASP LLM Top 10 issues"
- "Harden my server, Cloudflare config, or Docker setup"
- "Scan for slopsquatting, hallucinated APIs, or sycophancy patterns in AI-generated code"
- "Help me with incident response, webshell detection, or GDPR/DACH compliance"

## Skill Categories

### Infrastructure Hardening
1. **VPS Hardening** — SSH config, firewall rules, fail2ban, unattended upgrades, kernel hardening
2. **Cloudflare Security** — WAF rules, rate limiting, bot management, SSL/TLS settings, page rules
3. **Docker Security** — Image scanning, rootless containers, secrets management, network policies
4. **GitHub Actions Security** — Workflow hardening, secret scanning, dependency review, OIDC auth

### Web Application Security
5. **WordPress Security** — Plugin/theme audit, wp-config hardening, file permissions, XML-RPC lockdown, database prefix changes
6. **Next.js Security** — CSP headers, API route protection, middleware auth, SSRF prevention, environment variable safety
7. **Webshell Detection** — Scan for obfuscated PHP/JSP/ASPX shells, base64-encoded payloads, suspicious file modifications

### AI & LLM Security
8. **Prompt Injection Defense** — Input sanitization, system prompt protection, output filtering, context boundary enforcement
9. **OWASP LLM Top 10 Review** — Systematic check against all 10 categories: prompt injection, data leakage, insecure output handling, training data poisoning, supply chain, excessive agency, etc.
10. **MCP Server Security** — Transport security, tool permission auditing, input validation, sandboxing, auth token handling
11. **AI Agent Guardrails** — Action scope limits, human-in-the-loop checkpoints, resource consumption caps, output validation
12. **Slopsquatting Check** — Detect hallucinated package names in AI-generated dependency lists, verify packages exist in registries
13. **Hallucinated API Detection** — Flag non-existent API endpoints, deprecated methods, or fabricated SDK functions in generated code
14. **Sycophancy Pattern Detection** — Identify where AI-generated code agrees with flawed premises, skips error handling, or implements insecure shortcuts

### Incident Response
15. **Incident Response Playbook** — Triage, containment, eradication, recovery, and post-mortem steps
16. **Log Analysis** — Parse and correlate auth logs, web server logs, and system logs for indicators of compromise
17. **Forensic Artifact Collection** — Memory dumps, disk images, network captures, timeline reconstruction

### Compliance
18. **GDPR Compliance Audit** — Data inventory, consent mechanisms, DSAR handling, data retention policies, breach notification procedures
19. **DACH Region Compliance** — Germany/Austria/Switzerland-specific requirements, Datenschutz, BDSG, DSG considerations

### Vibe Coding Safety
20. **AI Code Review** — Review AI-generated code for security anti-patterns, missing input validation, hardcoded secrets
21. **Dependency Audit** — Check for known CVEs, outdated packages, typosquatting, and supply chain risks

## How to use

### 1. Pick a security domain
Tell Claude which area you want to audit or harden. Be specific about your stack.

```
"Audit my WordPress site for security issues"
"Harden my Ubuntu VPS"
"Review my Next.js app for OWASP LLM Top 10 vulnerabilities"
"Check my MCP server configuration for security gaps"
```

### 2. Claude performs the audit
Claude will systematically check your codebase, configuration files, and infrastructure settings against the relevant security checklist. It will:
- Scan files for known vulnerability patterns
- Review configurations against security best practices
- Check for AI/LLM-specific threats like prompt injection and slopsquatting
- Flag compliance gaps for GDPR/DACH requirements

### 3. Review findings and apply fixes
Claude provides prioritized findings (Critical / High / Medium / Low) with:
- Description of the vulnerability
- Impact assessment
- Concrete remediation steps with code/config changes
- References to relevant security standards (OWASP, CIS, NIST)

### Example: Prompt Injection Audit
```
User: Check my MCP server for prompt injection vulnerabilities

Claude will:
1. Scan all tool definitions for input validation
2. Check system prompts for injection-resistant patterns
3. Review output handlers for data exfiltration vectors
4. Verify context boundaries between user/system/tool messages
5. Flag any tools with excessive permissions or missing sandboxing
```

### Example: Slopsquatting Check
```
User: Check my package.json and requirements.txt for slopsquatting

Claude will:
1. Extract all dependency names from manifest files
2. Verify each package exists in npm/PyPI registries
3. Flag any packages with suspiciously low download counts
4. Check for typosquatting variants of popular packages
5. Verify package publisher authenticity where possible
```

### Example: VPS Hardening
```
User: Harden my Ubuntu VPS

Claude will:
1. Audit SSH configuration (disable root login, key-only auth)
2. Review firewall rules (UFW/iptables)
3. Check fail2ban configuration
4. Verify automatic security updates
5. Audit running services and open ports
6. Review file permissions on sensitive directories
7. Check kernel hardening parameters (sysctl)
```

## References

- **Source Repository**: [GoldenWing-360/claude-security-skills](https://github.com/GoldenWing-360/claude-security-skills)
- **License**: MIT
- **Topics**: AI security, Claude Code skills, defensive security, OWASP LLM Top 10, prompt injection, WordPress/VPS/Cloudflare/Next.js/Docker hardening, incident response, GDPR compliance, slopsquatting detection, webshell detection, GitHub Actions security
