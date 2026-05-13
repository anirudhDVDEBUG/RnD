# Claude Security Skills

**TL;DR:** 25 production-tested Claude Code skills for defensive security -- from VPS hardening and Docker audits to OWASP LLM Top 10, slopsquatting detection, and prompt injection defense. Install one folder and Claude gains security superpowers across your entire stack.

## Headline Result

```
$ bash run.sh

  SECURITY AUDIT REPORT: mock_project
  Total findings: 28
    CRITICAL: 10
    HIGH: 12
    MEDIUM: 3
    LOW: 1
    INFO: 0

  [Slopsquatting]  HIGH  Possibly hallucinated npm package: ai-prompt-utils
  [Prompt Injection]  CRITICAL  Eval on user input (code injection)  @ app.py:39
  [Hardcoded Secrets]  CRITICAL  Anthropic API key  @ app.py:7
  [Docker Security]  HIGH  No USER instruction - runs as root
  [OWASP LLM Top 10]  HIGH  LLM08: Auto-execution without human approval
  [GitHub Actions]  CRITICAL  Potential script injection via github.event
  ...
```

The demo runs 6 of the 25 skill categories against an intentionally vulnerable mock project. No API keys needed.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Install steps, trigger phrases, first-60-seconds walkthrough
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, what it does/doesn't do, why it matters
