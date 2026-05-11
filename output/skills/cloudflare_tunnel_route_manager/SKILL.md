---
name: cloudflare_tunnel_route_manager
description: |
  Manage Cloudflare Tunnel ingress routes from the CLI. Add, remove, and list persistent HTTPS subdomains for any local port — no browser or dashboard needed.
  Triggers: cloudflare tunnel, expose localhost, public URL for local port, ngrok alternative, persistent subdomain
---

# Cloudflare Tunnel Route Manager

Manage Cloudflare Tunnel ingress routes entirely from the command line. Create persistent HTTPS subdomains for any local port without touching the Cloudflare dashboard.

## When to use

- "Expose my local port to the internet via Cloudflare Tunnel"
- "Add a persistent HTTPS subdomain for my local dev server"
- "List or remove my Cloudflare Tunnel ingress routes"
- "I need a public URL for my FastAPI/Gradio/Streamlit app"
- "Set up a Cloudflare Tunnel route as an ngrok alternative"

## Prerequisites

1. **cloudflared** must be installed and authenticated (`cloudflared login`)
2. A Cloudflare Tunnel must already exist (create one with `cloudflared tunnel create <name>` if needed)
3. A domain managed by Cloudflare (DNS zone) for creating subdomains
4. The tunnel config file (typically `~/.cloudflared/config.yml`) must be accessible

## How to use

### 1. Locate or identify the tunnel

```bash
# List existing tunnels
cloudflared tunnel list
```

Note the tunnel name and UUID. The config file is usually at `~/.cloudflared/config.yml`.

### 2. Add a route (expose a local port)

To map a subdomain to a local service, add an ingress entry to the tunnel config and create a DNS route:

```bash
# Create a DNS record pointing the subdomain to the tunnel
cloudflared tunnel route dns <TUNNEL_NAME> <SUBDOMAIN>

# Example: route myapp.example.com → localhost:8000
cloudflared tunnel route dns my-tunnel myapp
```

Then add the ingress rule to `~/.cloudflared/config.yml`:

```yaml
tunnel: <TUNNEL_UUID>
credentials-file: /home/<user>/.cloudflared/<TUNNEL_UUID>.json

ingress:
  - hostname: myapp.example.com
    service: http://localhost:8000
  # Catch-all rule (required, must be last)
  - service: http_status:404
```

### 3. List current routes

Inspect the ingress rules in the config file:

```bash
# View current tunnel config
cat ~/.cloudflared/config.yml

# Or list DNS routes
cloudflared tunnel route ip show <TUNNEL_NAME>
```

### 4. Remove a route

Remove the corresponding ingress entry from `~/.cloudflared/config.yml` and optionally clean up the DNS record:

```bash
# Remove DNS record via Cloudflare API or dashboard
# Then remove the ingress block from config.yml
```

### 5. Restart the tunnel to apply changes

```bash
# If running as a service
sudo systemctl restart cloudflared

# Or run directly
cloudflared tunnel run <TUNNEL_NAME>
```

### Common use cases

| Local service | Port | Example hostname |
|---|---|---|
| FastAPI | 8000 | `api.example.com` |
| Gradio | 7860 | `demo.example.com` |
| Streamlit | 8501 | `dashboard.example.com` |
| Webhooks | 9000 | `hooks.example.com` |
| Dev server | 3000 | `dev.example.com` |

### Tips

- The catch-all `- service: http_status:404` rule **must** be the last ingress entry
- Routes persist across tunnel restarts — no need to reconfigure each time
- Multiple subdomains can point to different local ports through a single tunnel
- Use `cloudflared tunnel run` in the foreground for debugging, or install as a system service for production

## References

- **Source repository**: [nachum10/cloudflare-tunnel-routes](https://github.com/nachum10/cloudflare-tunnel-routes)
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [cloudflared CLI reference](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/configure-tunnels/)
