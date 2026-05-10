---
name: deepseek_loop_agent
description: |
  Set up and run a Claude-Code-shaped agent loop powered by the DeepSeek API.
  TRIGGER when: user wants to use DeepSeek as an alternative LLM backend, run an agent loop with DeepSeek models, set up a cron-scheduled agent with DeepSeek, or build a CLI agent using DeepSeek tool-use.
  DO NOT TRIGGER when: user is working with Claude API, OpenAI API, or other non-DeepSeek LLM providers.
---

# DeepSeek Loop Agent

A Rust-based CLI that provides a Claude-Code-shaped agent loop over the DeepSeek API, with built-in tools, permission modes, cron scheduling, and streaming SdkMessage events.

## When to use

- "Set up a DeepSeek agent loop with tool use"
- "Run a cron-scheduled agent using DeepSeek models"
- "I want a Claude-Code-like CLI but with DeepSeek as the backend"
- "Configure deepseek-loop with permission modes and built-in tools"
- "Stream agent events from a DeepSeek-powered loop"

## How to use

### 1. Install deepseek-loop

```bash
# Clone and build from source (requires Rust toolchain)
git clone https://github.com/v9ai/deepseek-loop.git
cd deepseek-loop
cargo build --release

# Or install directly via cargo
cargo install --git https://github.com/v9ai/deepseek-loop
```

### 2. Configure your environment

```bash
# Set your DeepSeek API key
export DEEPSEEK_API_KEY="your-api-key-here"
```

### 3. Run the agent loop

```bash
# Basic interactive session
deepseek-loop

# Run with a specific prompt
deepseek-loop "Analyze this codebase and suggest improvements"

# Use cron scheduling (similar to /loop semantics)
deepseek-loop --cron "*/5 * * * *" "Check deployment status"
```

### 4. Key features

- **Built-in tools**: File read/write, bash execution, grep, glob — mirroring Claude Code's tool set
- **Permission modes**: Control which tools the agent can use without prompting
- **Cron scheduler**: Schedule recurring agent tasks with /loop-style semantics
- **Streaming events**: SdkMessage-compatible event stream for integration with other systems
- **Rust CLI**: Fast, single-binary deployment

### 5. Permission modes

Configure tool permissions to control agent autonomy:
- `--allow-all`: Agent can use all tools without prompting
- `--allow-read`: Allow file reads without prompting
- `--allow-bash`: Allow bash commands without prompting

## References

- Source: https://github.com/v9ai/deepseek-loop
- Language: Rust
- Topics: agent, claude-code, cli, cron-scheduler, deepseek, llm, rust, tool-use
