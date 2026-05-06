# OpenPets Desktop Pet MCP — Demo

**Pixel-art desktop pets that visually react to your AI coding agent's status in real time.**

OpenPets is an Electron + Bun app that puts a small animated pet on your desktop. It exposes an MCP server so Claude Code (or any MCP-aware agent) can call `set_pet_status` to switch the pet between idle, thinking, coding, error, and success states — giving you an at-a-glance visual indicator of what your agent is doing.

## Headline result

Run `bash run.sh` to see a simulated coding session where an AI agent drives a desktop pet through thinking, coding, error, fix, and success, with ASCII-art animations for each state.

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the real OpenPets app and connect Claude Code via MCP
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and why this matters
