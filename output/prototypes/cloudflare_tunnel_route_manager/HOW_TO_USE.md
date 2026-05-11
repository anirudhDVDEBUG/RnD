# How to Use

## Installation

```bash
# Clone this prototype
git clone <this-repo> && cd cloudflare_tunnel_route_manager

# Install dependencies
pip install -r requirements.txt   # just PyYAML

# (Production only) Install cloudflared
# macOS:  brew install cloudflared
# Linux:  https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
# Then:   cloudflared login
```

## As a Claude Code Skill

This is a **Claude Code skill** — it teaches Claude how to manage Cloudflare Tunnel routes when you ask.

### Setup

1. Copy the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/cloudflare_tunnel_route_manager
cp SKILL.md ~/.claude/skills/cloudflare_tunnel_route_manager/SKILL.md
```

Or if using the original repo's skill file:

```bash
git clone https://github.com/nachum10/cloudflare-tunnel-routes.git
cp -r cloudflare-tunnel-routes/.claude/skills/cloudflare-tunnel-routes \
      ~/.claude/skills/cloudflare_tunnel_route_manager
```

2. Ensure `cloudflared` is installed and authenticated on the machine where Claude Code runs.

### Trigger Phrases

Say any of these to Claude Code and the skill activates:

- "Expose my local port to the internet via Cloudflare Tunnel"
- "Add a persistent HTTPS subdomain for my local dev server"
- "List or remove my Cloudflare Tunnel ingress routes"
- "I need a public URL for my FastAPI/Gradio/Streamlit app"
- "Set up a Cloudflare Tunnel route as an ngrok alternative"

Claude will then use `cloudflared` commands and edit `~/.cloudflared/config.yml` to manage routes.

## Standalone CLI Usage

The `tunnel_manager.py` script works independently of Claude:

```bash
# Initialize config for an existing tunnel
python3 tunnel_manager.py init <TUNNEL_UUID>

# Add a route
python3 tunnel_manager.py add myapp.example.com http://localhost:8000 --tunnel my-tunnel

# List routes
python3 tunnel_manager.py list

# Remove a route
python3 tunnel_manager.py remove myapp.example.com

# Use a custom config path
python3 tunnel_manager.py -c /path/to/config.yml list
```

## First 60 Seconds

**Prerequisites**: `cloudflared` installed and logged in, a tunnel created.

```bash
# 1. Install the Python wrapper
pip install pyyaml

# 2. See what tunnels you have
cloudflared tunnel list

# 3. Initialize a config (if you don't have one)
python3 tunnel_manager.py init <your-tunnel-uuid>

# 4. Expose your local FastAPI server
python3 tunnel_manager.py add api.mydomain.com http://localhost:8000 --tunnel my-tunnel

# 5. Verify
python3 tunnel_manager.py list
```

Output:

```
Config saved to /home/user/.cloudflared/config.yml
Added route: api.mydomain.com -> http://localhost:8000
Creating DNS route for 'api' via tunnel 'my-tunnel'...
DNS route created successfully.

Restart the tunnel to apply: cloudflared tunnel run my-tunnel

#    Hostname                                 Service
--------------------------------------------------------------------------
1    api.mydomain.com                         http://localhost:8000
2    (catch-all)                              http_status:404
```

Then restart the tunnel:

```bash
cloudflared tunnel run my-tunnel
```

Your service is now live at `https://api.mydomain.com`.

## Demo (No Cloudflare Account Needed)

```bash
bash run.sh
```

Runs the full lifecycle (init, add, list, remove) against a temporary mock config file.
