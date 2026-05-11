# Technical Details

## What It Does

The Cloudflare Tunnel Route Manager provides a CLI wrapper around `cloudflared` tunnel configuration. Instead of manually editing YAML config files and running multiple `cloudflared` commands, it combines ingress rule management (adding/removing entries in `~/.cloudflared/config.yml`) and DNS route creation (`cloudflared tunnel route dns`) into single commands. The core value is eliminating the error-prone manual editing of the config YAML — particularly maintaining the required catch-all rule at the end of the ingress list.

As a Claude Code skill, it teaches Claude the exact workflow for exposing local services through Cloudflare Tunnels, so users can say "give my app a public URL" and get a working HTTPS endpoint.

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `tunnel_manager.py` | CLI tool — parses args, reads/writes config YAML, shells out to `cloudflared` |
| `SKILL.md` | Claude Code skill definition — trigger phrases, prerequisites, step-by-step instructions |
| `~/.cloudflared/config.yml` | Cloudflare Tunnel config (the file being managed) |

### Data Flow

```
User command
    |
    v
tunnel_manager.py
    |
    +---> Read/write ~/.cloudflared/config.yml (PyYAML)
    |
    +---> Shell out to `cloudflared tunnel route dns` (optional, for DNS records)
    |
    v
User restarts tunnel: `cloudflared tunnel run <name>`
    |
    v
Cloudflare edge network serves traffic to local ports
```

### Dependencies

- **Python 3.6+** — standard library plus PyYAML
- **PyYAML** — parsing and writing the cloudflared config file
- **cloudflared** (runtime) — Cloudflare's tunnel daemon, needed for actual tunnel operation and DNS route creation
- **Cloudflare account** (runtime) — a domain with DNS managed by Cloudflare

### No Model Calls

This tool makes no LLM API calls. It is a pure CLI utility. When used as a Claude Code skill, it provides instructions that Claude follows — Claude orchestrates the commands, but the skill itself is stateless documentation.

## Limitations

- **Does not create tunnels** — assumes a tunnel already exists (`cloudflared tunnel create` must be run first)
- **No API-based DNS cleanup** — removing a route deletes the ingress config entry but does not automatically remove the Cloudflare DNS record (requires API token or dashboard)
- **Single config file** — manages one config file at a time; doesn't handle multi-tunnel setups with separate configs automatically
- **No validation of service URLs** — doesn't verify that `http://localhost:8000` is actually running
- **No TLS origin config** — for HTTPS backends (e.g., `https://localhost:443`), users must manually add `originRequest` settings
- **Restart not automated** — after config changes, the user must restart the tunnel manually or via systemd

## Why This Matters

For teams building Claude-driven products:

- **Agent factories / dev infra**: Agents that spin up services (APIs, dashboards, webhooks) need a way to expose them. This skill lets Claude give any local service a persistent public URL in one step — useful for demo deployments, webhook receivers, or agent-to-agent communication endpoints.

- **Lead-gen and marketing**: Quickly expose Gradio demos, Streamlit dashboards, or landing page prototypes at branded subdomains without configuring nginx or cloud hosting. Iterate faster on public-facing assets.

- **Voice AI / webhook receivers**: Voice AI systems often need publicly reachable callback URLs. A Cloudflare Tunnel route is more reliable than ngrok (persistent, no session timeouts) and cheaper than dedicated cloud VMs.

- **Security posture**: Cloudflare Tunnels avoid opening inbound ports on your firewall. Traffic flows outbound through the tunnel daemon. This is meaningfully safer than port forwarding or public-facing servers for development and staging.
