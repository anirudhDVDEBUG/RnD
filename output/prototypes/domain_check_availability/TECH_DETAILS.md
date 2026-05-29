# Technical Details

## What It Does

This is a Claude Code skill that checks domain name availability by calling the free [digmyname.com](https://digmyname.com) API. When a user asks Claude "is myproject.io available?", the skill instructs Claude to issue a `curl` request to the API, parse the JSON response, and present a formatted table showing availability status and pricing across up to 7 registrars and 52 TLDs. No API key, no authentication, no dependencies beyond `curl`.

The standalone Python script (`domain_check.py`) wraps the same API with a CLI interface and includes mock data fallback for offline/demo use.

## Architecture

```
User prompt ("check domain X")
  -> Claude matches SKILL.md trigger phrases
  -> Claude runs: curl https://api.digmyname.com/check?domain=X&tlds=...
  -> API returns JSON: [{domain, available, registrars: [{name, price}]}]
  -> Claude formats and presents results as a table
```

**Key files:**
- `SKILL.md` — Claude Code skill definition with trigger phrases and instructions
- `domain_check.py` — Standalone CLI wrapper (stdlib only: `urllib`, `json`, `sys`)
- `run.sh` — Demo script running three example queries

**Dependencies:** None (Python stdlib only). The skill itself uses only `curl`.

**Data flow:** All queries go to `api.digmyname.com` over HTTPS. No data is stored locally. The API is stateless and free.

## Limitations

- **Third-party API dependency**: All availability data comes from digmyname.com. If the API goes down, the skill fails (CLI falls back to mock data).
- **No WHOIS lookup**: Only checks availability and pricing — does not return WHOIS details, expiry dates, or DNS records.
- **No domain registration**: This is read-only. You cannot buy or reserve domains through it.
- **Rate limits unknown**: The API docs don't specify rate limits. Heavy use may be throttled.
- **Accuracy**: Availability data may lag behind real-time registrar state by minutes or hours. Always verify at the registrar before purchasing.
- **52 TLDs only**: Country-code TLDs and newer gTLDs outside the supported 52 are not covered.

## Why It Matters

For teams building Claude-driven products:

- **Lead-gen / marketing**: Instantly check if a brand name has available domains before pitching clients. Combine with brand-name generators for an end-to-end naming workflow.
- **Agent factories**: Domain checking is a natural tool-use step in startup scaffolding agents — pair with company registration, logo generation, and landing page builders.
- **Ad creatives**: Verify vanity URLs are available before designing ad copy that references them.
- **Low friction**: Zero-auth, zero-cost API means you can wire this into any agent pipeline without credential management overhead.
