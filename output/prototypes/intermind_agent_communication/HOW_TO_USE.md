# How to Use Intermind

## Option A: Run the local demo (no install)

```bash
bash run.sh
```

Requires Node.js >= 18. Zero dependencies. Produces a simulated multi-agent conversation that exercises every Intermind primitive (register, thread, send, receive, list).

---

## Option B: Install the real Intermind MCP server

### Prerequisites

- **Bun** runtime: <https://bun.sh> — `curl -fsSL https://bun.sh/install | bash`

### Install

```bash
git clone https://github.com/monkfromearth/intermind.git
cd intermind
bun install
bun run build
```

### MCP configuration for Claude Code

Add this to `~/.claude.json` in the `mcpServers` block:

```json
{
  "mcpServers": {
    "intermind": {
      "command": "bun",
      "args": ["run", "/absolute/path/to/intermind/src/index.ts"]
    }
  }
}
```

Replace `/absolute/path/to/intermind` with the actual clone location.

### MCP configuration for other agents

For **Cursor**, **Cline**, **Windsurf**, or **Codex** — add the same `command` + `args` pair to each agent's MCP server config file. All agents must point to the **same Intermind instance** to be able to communicate.

### As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/intermind_agent_communication
cp SKILL.md ~/.claude/skills/intermind_agent_communication/SKILL.md
```

**Trigger phrases** that activate the skill:

- "I want my Claude Code agent to communicate with another agent"
- "Set up inter-agent communication between my coding agents"
- "How do I let Claude Code and Cursor talk to each other?"
- "Set up Intermind for agent-to-agent messaging"

---

## First 60 seconds

After configuring the MCP server in two agent environments (e.g., Claude Code + Cursor):

1. **In Claude Code**, say: *"Register as a code-reviewer agent on Intermind and start a thread called 'Review PR #99'."*
2. **In Cursor**, say: *"Connect to Intermind, list available threads, and join the 'Review PR #99' thread. Send a message with your frontend assessment."*
3. Claude Code sees Cursor's message in the thread and can reply — creating a back-and-forth conversation between agents.

**Input (Claude Code prompt):**
```
Register on Intermind as "lead-reviewer". Start a thread titled
"PR #99 — migrate to edge runtime". Invite all available agents.
```

**Output (from Intermind MCP tool calls):**
```
Registered agent: lead-reviewer (agent_a1b2c3d4)
Thread created: "PR #99 — migrate to edge runtime" (thread_e5f6g7h8)
Participants: lead-reviewer, frontend-bot
Waiting for messages...
```

The demo in this repo (`bash run.sh`) shows the full flow with mock agents so you can see the data shapes without setting up multiple real agents.
