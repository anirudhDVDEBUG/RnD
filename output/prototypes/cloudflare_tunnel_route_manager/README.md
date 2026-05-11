# Cloudflare Tunnel Route Manager

**Manage Cloudflare Tunnel ingress routes from the CLI — add, remove, and list persistent HTTPS subdomains for any local port. No browser, no dashboard.**

## Headline Result

```
$ python3 tunnel_manager.py -c config.yml add api.example.com http://localhost:8000 --tunnel my-tunnel
Added route: api.example.com -> http://localhost:8000
Creating DNS route for 'api' via tunnel 'my-tunnel'...
DNS route created successfully.
```

One command gives your local service a persistent, production-grade HTTPS URL through Cloudflare's network.

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, Claude skill setup, and "first 60 seconds" walkthrough
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, limitations, and why this matters

## Demo

```bash
bash run.sh
```

Runs a full add/list/remove cycle using mock config data. No `cloudflared` or API keys required.

## Source

[nachum10/cloudflare-tunnel-routes](https://github.com/nachum10/cloudflare-tunnel-routes)
