# How to Use Claude Pets

## Prerequisites

| Dependency | Version | Install |
|---|---|---|
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Bun (optional, for source repo) | latest | `curl -fsSL https://bun.sh/install \| bash` |
| OpenPets desktop app | latest | [openpets.dev](https://openpets.dev) |
| Claude Code | latest | `npm i -g @anthropic-ai/claude-code` |

## Option A: Install the real claude-pets (production)

```bash
git clone https://github.com/alvinunreal/claude-pets.git
cd claude-pets
bun install
bun run setup   # auto-configures hooks + MCP server
```

The `bun run setup` command registers three Claude Code hooks and one MCP server automatically.

## Option B: Run this demo (no OpenPets needed)

```bash
# From this directory
bash run.sh
```

The demo uses mock mode — all pet status updates print to the terminal instead of hitting the OpenPets API.

---

## Claude Code Skill Setup

Drop the skill file so Claude Code can auto-trigger pet setup:

```bash
mkdir -p ~/.claude/skills/claude_pets_desktop_pet
cp SKILL.md ~/.claude/skills/claude_pets_desktop_pet/SKILL.md
```

**Trigger phrases:** "claude pets", "desktop pet", "openpets", "pet status", "coding pet companion"

---

## MCP Server Configuration

Add this to `~/.claude.json` in the `mcpServers` block:

```json
{
  "mcpServers": {
    "claude-pets": {
      "command": "bun",
      "args": ["run", "/absolute/path/to/claude-pets/src/mcp-server.ts"]
    }
  }
}
```

Replace `/absolute/path/to/claude-pets` with your actual clone path.

If using Node instead of Bun:

```json
{
  "mcpServers": {
    "claude-pets": {
      "command": "node",
      "args": ["/absolute/path/to/claude-pets/src/mcp-server.js"]
    }
  }
}
```

---

## Hook Configuration (manual)

If you prefer manual setup over `bun run setup`, add to your Claude Code `settings.json`:

```json
{
  "hooks": {
    "on_tool_call": [
      { "command": "bun run /path/to/claude-pets/hooks/on_tool_call.ts" }
    ],
    "on_session_start": [
      { "command": "bun run /path/to/claude-pets/hooks/on_session_start.ts" }
    ],
    "on_session_end": [
      { "command": "bun run /path/to/claude-pets/hooks/on_session_end.ts" }
    ]
  }
}
```

---

## First 60 Seconds

1. **Install & setup** (assumes OpenPets is already running):
   ```bash
   git clone https://github.com/alvinunreal/claude-pets.git
   cd claude-pets && bun install && bun run setup
   ```

2. **Start a Claude Code session** — your desktop pet wakes up with `(o_o)!`

3. **Ask Claude to read or edit a file** — the pet shifts to `(@_@)` (reading) or `(>_<)/*` (writing)

4. **Complete a task** — the pet celebrates: `\(^o^)/`

5. **End the session** — the pet waves `(^_^)/~~` and goes back to sleep `(-_-)zzZ`

Input/output example (mock mode):
```
$ bash run.sh
[on_session_start]
  (o_o)!  Claude Code session started — pet is awake!  [waking]

[on_tool_call] (Read)
  (@_@)  Claude is using Read  [reading]

[on_tool_call] (Edit)
  (>_<)/*  Claude is using Edit  [writing]

[on_session_end]
  (^_^)/~~  Claude Code session ended — pet waves goodbye!  [goodbye]
  (-_-)zzZ  Pet goes back to sleep...  [sleeping]
```
