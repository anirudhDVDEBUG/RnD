---
name: Pi Plugin for Claude Code
description: |
  Route coding tasks through the Pi coding agent (DeepSeek V4) via Claude Code slash commands.
  TRIGGER: user wants to route code review, rescue, or other coding tasks through Pi agent / DeepSeek V4,
  user mentions pi-plugin-cc or /pi: commands, user wants multi-agent coding with DeepSeek.
---

# Pi Plugin for Claude Code

Claude Code plugin that routes `/pi:review`, `/pi:rescue`, and other slash commands through the Pi coding agent (default model: DeepSeek V4). This is a 1:1 fork of codex-plugin-cc adapted for the Pi coding agent.

## When to use

- "Route this code review through Pi / DeepSeek"
- "Set up Pi plugin for Claude Code agent routing"
- "Use /pi:review to review my code with DeepSeek V4"
- "I want to use Pi coding agent alongside Claude Code"
- "Install pi-plugin-cc for multi-agent coding"

## How to use

### Installation

1. Clone the plugin repository:
   ```bash
   git clone https://github.com/Agents365-ai/pi-plugin-cc.git
   cd pi-plugin-cc
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure the plugin in your Claude Code settings by adding it as a plugin or following the repo's setup instructions.

### Available Slash Commands

- **`/pi:review`** — Route a code review task through the Pi coding agent (DeepSeek V4). Provides an independent second opinion on code quality, bugs, and improvements.
- **`/pi:rescue`** — Send a stuck or failing task to the Pi agent for an alternative approach or fix.
- Additional `/pi:*` commands may be available depending on plugin version.

### Configuration

- **Default model**: DeepSeek V4 (configurable)
- The plugin acts as a routing layer, forwarding designated tasks from Claude Code to the Pi coding agent backend.
- Environment variables or plugin config can be used to customize the target model and agent endpoint.

### How It Works

1. You invoke a `/pi:` slash command within Claude Code.
2. The plugin intercepts the command and routes the request to the Pi coding agent.
3. The Pi agent (powered by DeepSeek V4 by default) processes the task and returns results.
4. Results are displayed back in your Claude Code session.

This enables a multi-agent workflow where Claude handles primary coding tasks while Pi/DeepSeek provides supplementary code reviews, rescues, and alternative perspectives.

## References

- **Repository**: https://github.com/Agents365-ai/pi-plugin-cc
- **Language**: JavaScript
- **Topics**: claude-code, claude-code-plugin, code-review, coding-agent, deepseek, pi-coding-agent
