# datasette-agent-sprites Sandbox Demo

**TL;DR:** `datasette-agent-sprites` is a Datasette Agent plugin that routes commands to ephemeral [Fly Sprites](https://sprites.dev) VMs, giving your agent sandboxed execution without touching your host machine. This is the first alpha (0.1a0) from the Datasette project.

## Headline Result

```
$ datasette plugins | grep sprites
datasette-agent-sprites  0.1a0  -- Sandboxed command execution via Fly Sprites
```

Agent commands execute in isolated, ephemeral VMs and return results safely.

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) -- Install, configure, and run in 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) -- Architecture, data flow, limitations

## Source

- [Simon Willison's announcement](https://simonwillison.net/2026/May/21/datasette-agent-sprites/#atom-everything)
- [GitHub repo](https://github.com/datasette/datasette-agent-sprites)
