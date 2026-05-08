# OpenAI Trusted Access for Cyber — GPT-5.5-Cyber

OpenAI's **Trusted Access for Cyber** program gives verified defenders access to **GPT-5.5-Cyber**, a frontier model fine-tuned for vulnerability research with reduced safety refusals for legitimate defensive security work. This repo demonstrates three core workflows: source-code vuln scanning, CVE exploit analysis, and infrastructure hardening audits.

## Headline Result

```
  ***[CRITICAL] VULN-001: Buffer Overflow (CWE-120)***
    Line 42: strncpy(session_token, user_input, sizeof(session_token));
    Issue: strncpy does not null-terminate if source length >= dest size.
           Attacker can overflow session_token[256], overwriting is_admin.
    Suggested patch:
      + strncpy(session_token, user_input, sizeof(session_token) - 1);
      + session_token[sizeof(session_token) - 1] = '\0';
```

Three vulnerabilities found in 25 lines of C — with exploitability ratings and suggested patches — in one API call.

## Quick Start

```bash
bash run.sh          # Works immediately with mock data (no API key needed)
```

Set `OPENAI_API_KEY` to switch from mock data to live GPT-5.5-Cyber responses.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Setup, trigger phrases, first-60-seconds walkthrough
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, limitations, relevance to Claude-driven products

## Source

[Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber](https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber)
