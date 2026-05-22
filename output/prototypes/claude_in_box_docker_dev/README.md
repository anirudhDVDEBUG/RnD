# Claude-in-Box: Portable Docker Dev Environment

Run Claude Code inside a Docker container with multi-session management, hook-driven automation, a web UI, and transparent SOCKS5 proxy. Lightweight enough for a Raspberry Pi.

**Headline result:** Three simultaneous Claude Code sessions, each with isolated workspaces, managed from a single browser tab — with automatic lifecycle hooks firing on every session event.

| What | Where |
|---|---|
| Setup & first 60 seconds | [HOW_TO_USE.md](HOW_TO_USE.md) |
| Architecture & limitations | [TECH_DETAILS.md](TECH_DETAILS.md) |
| Quick demo (no API key) | `bash run.sh` |
| Web UI demo | `python simulator.py --serve` then open `http://localhost:9080` |
| Source repo | https://github.com/jiangmuran/claude-in-box |
