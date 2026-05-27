# How to Use — Pi Plugin for Claude Code

## Installation

### Option A: Use this demo (no API key needed)

```bash
git clone <this-repo>
cd pi_plugin_cc_agent_routing
bash run.sh
```

Requires only Node.js >= 16. Zero npm dependencies.

### Option B: Install the real plugin

```bash
git clone https://github.com/Agents365-ai/pi-plugin-cc.git
cd pi-plugin-cc
npm install
```

Then register it in your Claude Code configuration. The plugin hooks into Claude Code's slash command system so `/pi:*` commands are available in your sessions.

### Environment Variables (production)

| Variable | Default | Description |
|---|---|---|
| `PI_MODEL` | `deepseek-v4` | Model identifier for the Pi agent |
| `PI_ENDPOINT` | `https://api.deepseek.com/v1/chat/completions` | API endpoint |
| `PI_TIMEOUT` | `30000` | Request timeout in ms |

## This Is a Claude Code Plugin

The Pi Plugin is a **Claude Code plugin** — not a skill or MCP server. It extends Claude Code by adding new slash commands that route tasks to the Pi coding agent.

To register it in Claude Code, add the plugin to your Claude Code settings or follow the upstream repo's configuration guide. Once registered, the `/pi:*` commands appear alongside Claude Code's built-in commands.

## Available Commands

| Command | What it does |
|---|---|
| `/pi:review <code>` | Independent code review from DeepSeek V4 — finds bugs, style issues, security problems |
| `/pi:rescue <description>` | Sends a stuck/failing task to Pi for alternative diagnosis and fix |
| `/pi:explain <code>` | Asks Pi to explain what a code snippet does |
| `/pi:refactor <code>` | Gets refactoring suggestions from Pi |

## First 60 Seconds

1. **Run the demo** (no setup needed):
   ```bash
   bash run.sh
   ```

2. **See all 4 commands** in action — the demo routes each through the mock Pi agent and prints formatted results.

3. **Example input/output**:

   **Input:**
   ```
   /pi:review function getUser(id) { ... }
   ```

   **Output:**
   ```
   Review Score: 6.5/10
   Recommendation: Address the SQL injection issue before merging.

   Findings:
     [error]   Line 41: SQL query uses string concatenation — SQL injection risk.
       Fix: Use parameterized queries
     [warning] Line 12: Potential null dereference — user.profile may be undefined.
       Fix: Add optional chaining: user.profile?.avatar
     [info]    Line 27: Magic number 86400 could be a named constant.
       Fix: const SECONDS_PER_DAY = 86400;

   Tokens used: 550
   ```

4. **Try the rescue command**:

   **Input:**
   ```
   /pi:rescue infinite loop in processItems()
   ```

   **Output:**
   ```
   Diagnosis: The function enters an infinite loop when items is empty.
   Suggested fixes:
     1. Add early return: if (items.length === 0) return [];
     2. Change while(true) to while(index < items.length)
   Confidence: high
   ```

## Programmatic Usage

```javascript
const { PiPluginRouter } = require("./pi_plugin");

const router = new PiPluginRouter();

// Route a command
const result = await router.route("/pi:review myCode()");
console.log(result.result.findings);

// List available commands
console.log(router.listCommands());
```
