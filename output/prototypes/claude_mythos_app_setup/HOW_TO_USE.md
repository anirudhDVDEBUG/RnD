# How to Use

## Install (this prototype)

```bash
# Python 3.10+ required
pip install -r requirements.txt   # only anthropic SDK — optional for mock mode
bash run.sh                       # runs demo end-to-end, no API key needed
```

## Install the original C# app

```bash
git clone https://github.com/AbhishekK130804/Claude-Mythos-AI-Anthropic-App.git
cd Claude-Mythos-AI-Anthropic-App
dotnet build && dotnet run
```

## Claude Skill setup

Drop the skill folder so Claude Code can auto-trigger it:

```bash
mkdir -p ~/.claude/skills/claude_mythos_app_setup
cp SKILL.md ~/.claude/skills/claude_mythos_app_setup/SKILL.md
```

**Trigger phrases** that activate the skill:
- "Help me set up Claude Mythos AI app"
- "Configure my Anthropic API key for the Mythos client"
- "Set up prompt formatting for Claude roleplay in Mythos"
- "How do I install and run Claude Mythos on my platform?"
- "Configure a custom system prompt in the Mythos app"

## First 60 Seconds

```bash
$ bash run.sh
# Shows: all 4 prompt templates, mock conversations, SillyTavern formatting demo

$ python3 main.py --list
# Lists all available templates (creative_writing, roleplay, worldbuilding, general_assistant)

$ python3 main.py --interactive --mock
# Launches interactive chat in mock mode. Type messages, switch templates with /use <name>

$ ANTHROPIC_API_KEY=sk-ant-... python3 main.py --interactive
# Live mode — sends real API calls to Claude
```

### Interactive commands

| Command              | Action                            |
|----------------------|-----------------------------------|
| `/templates`         | List all prompt templates         |
| `/use <name>`        | Switch active template            |
| `/inspect <name>`    | Show template details             |
| `/clear`             | Reset conversation history        |
| `/quit`              | Exit                              |

## Configuration

Config is stored at `~/.mythos/config.json` (auto-created on first save):

```json
{
  "api_key": "sk-ant-...",
  "model": "claude-sonnet-4-20250514",
  "active_template": "creative_writing",
  "custom_templates": {},
  "base_url": "https://api.anthropic.com"
}
```

You can also set `ANTHROPIC_API_KEY` as an env var — it overrides the config file.
