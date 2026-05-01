---
name: claude_code_workflow
description: |
  Guide for using Claude Code CLI effectively — agentic coding in the terminal.
  TRIGGER when: user asks about Claude Code CLI usage, wants to set up claude-code,
  asks how to use Claude in the terminal, mentions agentic coding workflow,
  or wants help with claude-code commands and configuration.
  DO NOT TRIGGER when: user is asking about Claude API/SDK integration,
  general Claude model questions, or non-CLI usage.
---

# Claude Code Workflow

Claude Code is an agentic coding tool that lives in your terminal. It understands your codebase and helps you code faster through natural language commands.

## When to use

- "How do I use Claude Code in my terminal?"
- "Set up claude-code for my project"
- "What commands does Claude Code support?"
- "How do I configure Claude Code for my repo?"
- "Help me with Claude Code git workflows"

## How to use

### 1. Installation & Setup

```bash
# Install globally via npm
npm install -g @anthropic-ai/claude-code

# Navigate to your project and start
cd your-project
claude
```

Requires an Anthropic API key or active Claude subscription.

### 2. Core Capabilities

- **Code generation & editing**: Ask Claude to write, refactor, or fix code in natural language
- **Codebase understanding**: Ask questions about your codebase — Claude reads and indexes files
- **Git workflows**: Commit, create PRs, resolve merge conflicts, review diffs
- **Run commands**: Execute shell commands, run tests, manage builds
- **Multi-file edits**: Make coordinated changes across multiple files

### 3. Key CLI Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive REPL session |
| `claude "prompt"` | Run a one-shot command |
| `claude -p "prompt"` | Print-only mode (no file changes) |
| `claude /help` | Show available slash commands |
| `claude /init` | Create a CLAUDE.md project file |
| `claude /compact` | Compress conversation context |
| `claude /cost` | Show token usage and cost |
| `claude /commit` | Generate a commit from staged changes |

### 4. Project Configuration

Create a `CLAUDE.md` in your repo root to give Claude persistent context:

```markdown
# CLAUDE.md
- Use TypeScript with strict mode
- Run tests with `npm test`
- Follow existing code style
- Never commit directly to main
```

### 5. Best Practices

- **Start sessions in the project root** so Claude can discover your codebase
- **Use CLAUDE.md** to encode project conventions, build commands, and style preferences
- **Use `/compact`** when context gets large to keep responses focused
- **Review changes** before accepting — Claude shows diffs for approval
- **Leverage git integration** — let Claude handle commits with meaningful messages
- **Chain commands** — pipe output into Claude: `cat error.log | claude "fix this"`

### 6. Permission Modes

Claude Code supports different permission levels:
- **Default**: Asks before file writes and shell commands
- **Auto-accept edits**: Trust file modifications (`--dangerously-skip-permissions` for full auto)
- **Custom allowlists**: Configure specific tools/commands to auto-approve in settings

## References

- Source repository: https://github.com/anthropics/claude-code
- Documentation: https://docs.anthropic.com/en/docs/claude-code
