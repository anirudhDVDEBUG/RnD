# Domain Check Availability

Check domain name availability across 7 registrars and 52 TLDs in one shot, powered by the free [digmyname.com](https://digmyname.com) API. Works as a Claude Code skill (trigger: "check domain availability") or standalone CLI tool — no API key required.

## Headline Result

```
Domain                    Status       Best Price     Registrar
----------------------------------------------------------------------
cloudforge.com            TAKEN        $8.88          Namecheap
cloudforge.io             AVAILABLE    $25.99         Porkbun
cloudforge.dev            AVAILABLE    $10.11         Cloudflare
cloudforge.ai             TAKEN        $58.98         Namecheap
cloudforge.xyz            AVAILABLE    $1.00          Porkbun

Summary: 3/5 domains available
Best deal: cloudforge.xyz at $1.00 via Porkbun
```

## Quick Start

```bash
bash run.sh
```

See [HOW_TO_USE.md](HOW_TO_USE.md) for installation and Claude skill setup.
See [TECH_DETAILS.md](TECH_DETAILS.md) for architecture and limitations.
