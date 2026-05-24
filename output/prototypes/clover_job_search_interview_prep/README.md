# Clover Job Search & Interview Prep

**TL;DR:** Claude skill + MCP server that gives Claude live job listings, role-specific interview questions, and resume feedback — all from [four-leaf.ai](https://four-leaf.ai). Ask Claude "find me senior engineer jobs" or "prep me for a Stripe interview" and it calls the Clover MCP tools automatically.

## Headline Result

```
> "Prepare me for a Senior Software Engineer interview at Stripe"

Interview Process:
  > Recruiter screen (30 min)
  > Technical phone screen — coding (60 min)
  > On-site: System design (60 min)
  > On-site: Coding pair (60 min)
  > On-site: Behavioral / values (45 min)

Technical Questions:
  Q: Design a payment processing pipeline that handles idempotency and retries.
  Q: How would you build a rate limiter for an API with distributed servers?

Preparation Tips:
  * Stripe values clarity of thought — explain trade-offs explicitly.
  * Show awareness of financial system constraints (idempotency, auditability).
```

## Quick Start

```bash
bash run.sh
```

No API keys needed — the demo uses mock data to show the full tool flow.

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the MCP server, drop the skill, trigger phrases
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations

## Source

[github.com/fourleafai/clover-public](https://github.com/fourleafai/clover-public)
