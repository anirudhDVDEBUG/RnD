# How To Use

## Option A: Claude Code Skill (recommended)

1. Create the skill directory and drop the file:
   ```bash
   mkdir -p ~/.claude/skills/pronounce_dev_jargon
   cp SKILL.md ~/.claude/skills/pronounce_dev_jargon/SKILL.md
   ```

2. **Trigger phrases** — Claude will auto-activate this skill when you ask:
   - "How do you pronounce kubectl?"
   - "What's the correct pronunciation of GIF?"
   - "How do I say nginx out loud?"
   - "Is it sequel or S-Q-L?"

3. The skill instructs Claude to shell out to the `pronounce` CLI (if installed) or fall back to its built-in knowledge of the 540+ entry database.

## Option B: Standalone CLI

```bash
git clone https://github.com/anzy-renlab-ai/pronounce.git ~/.pronounce
chmod +x ~/.pronounce/pronounce

# Look up a term
~/.pronounce/pronounce lookup kubectl

# Search partial matches
~/.pronounce/pronounce search kube

# Hear it spoken (macOS only)
~/.pronounce/pronounce say nginx
```

## Option C: Local Python demo (this repo)

```bash
pip install -r requirements.txt   # no external deps
bash run.sh
```

## First 60 Seconds

```
$ bash run.sh

=== Pronounce Dev Jargon — Demo ===

Looking up: kubectl
  Pronunciation: "koob-control" (alt: "koob-cuddle")
  Confidence: high
  Source: Kubernetes official documentation

Looking up: GIF
  Pronunciation: "jif" (creator's intent) / "gif" (hard G, common)
  Confidence: contested
  Source: Steve Wilhite (creator) vs popular usage

Looking up: JWT
  Pronunciation: "jot"
  Confidence: medium
  Source: RFC 7519 authors

Interactive mode:
  > Enter a term (or 'quit'): nginx
  Pronunciation: "engine-X"
  Confidence: high
  Source: Igor Sysoev (creator)
```

## MCP Server (alternative)

The upstream repo also ships an MCP server. Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "pronounce": {
      "command": "bash",
      "args": ["/home/YOU/.pronounce/mcp-server.sh"],
      "env": {}
    }
  }
}
```

Replace `/home/YOU/` with your actual home directory path.
