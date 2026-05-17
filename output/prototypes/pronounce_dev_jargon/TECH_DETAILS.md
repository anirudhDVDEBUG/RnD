# Technical Details

## What It Does

Pronounce is a curated pronunciation database for 540+ developer terms — CLI tools, protocols, frameworks, acronyms, and jargon that engineers regularly mispronounce or debate. Each entry carries a confidence level (high/medium/contested) and a source citation (official docs, creator statements, RFCs, or community consensus). The tool exposes this data through a Bash CLI, an interactive quiz mode, voice output (macOS `say`), an MCP server, and a Claude Code skill file.

## Architecture

```
pronounce/
├── pronounce          # Main Bash CLI entrypoint
├── data/
│   └── terms.json     # Core database: 540+ entries
├── mcp-server.sh      # MCP stdio server (JSON-RPC)
├── SKILL.md           # Claude Code skill definition
└── quiz.sh            # Interactive pronunciation quiz
```

**Data format** (each entry in `terms.json`):
```json
{
  "term": "kubectl",
  "ipa": "/kuːb.kənˈtɹoʊl/",
  "spoken": "koob-control",
  "alt": ["koob-cuddle", "koob-C-T-L"],
  "confidence": "high",
  "source": "Kubernetes official documentation",
  "tags": ["cli", "kubernetes"]
}
```

**Data flow:**
1. User queries a term (CLI arg, MCP request, or Claude skill trigger)
2. Lookup performs case-insensitive exact match, then fuzzy/prefix search
3. Returns pronunciation, confidence level, alternatives, and source
4. Optional: pipes spoken form to macOS `say` for audio output

**Dependencies:** Bash 4+, `jq` for JSON parsing. No external API keys. No network calls at runtime (fully offline after clone). Python demo in this repo uses zero dependencies (stdlib only).

## Limitations

- Audio playback (`say` command) only works on macOS
- No IPA-to-audio rendering on Linux (text output only)
- Database is manually curated — community PRs needed for new terms
- "Contested" entries (GIF, SQL, char) reflect real disagreement; the tool does not force a single answer
- MCP server is a thin Bash wrapper — no streaming, no batching
- No auto-update mechanism; must `git pull` for new entries

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Voice AI** | Correct pronunciation data feeds TTS systems — avoids embarrassing mispronunciations in voice agents |
| **Agent factories** | Skills like this show the pattern: curated data + CLI + SKILL.md = instant Claude capability |
| **Marketing / content** | Video scripts, podcasts, and tutorials that pronounce terms correctly build credibility |
| **Lead-gen chatbots** | A bot that correctly says "engine-X" instead of "nn-jinx" signals technical competence |
| **Developer onboarding** | Quiz mode helps new hires avoid pronunciation pitfalls in meetings |

The broader pattern here is **structured knowledge as a skill**: a static JSON database, a thin CLI, and a SKILL.md trigger file turn any curated dataset into a Claude-native capability with zero API cost.
