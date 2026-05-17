---
name: pronounce_dev_jargon
description: |
  Look up and pronounce developer jargon (kubectl, GIF, JSON, JWT, etc.). 540+ entries with confidence levels.
  TRIGGER when: user asks how to pronounce a tech term, developer jargon, CLI tool name, or acronym.
  TRIGGER when: user asks about pronunciation of kubernetes terms, programming language names, or protocol acronyms.
  DO NOT TRIGGER when: user asks about general English pronunciation or non-tech words.
---

# Pronounce Dev Jargon

Look up correct pronunciations of developer jargon, CLI tools, acronyms, and tech terms using the pronounce database (540+ entries with confidence levels and sources).

## When to use

- "How do you pronounce kubectl?"
- "What's the correct pronunciation of GIF / JSON / JWT?"
- "How do I say nginx out loud?"
- "Pronounce these Kubernetes terms for me"
- "Is it sequel or S-Q-L?"

## How to use

1. **Install the tool** (if not already available):
   ```bash
   # Clone the repository
   git clone https://github.com/anzy-renlab-ai/pronounce.git ~/.pronounce
   # Or use via npx/brew if available
   ```

2. **Look up a pronunciation**:
   ```bash
   ~/.pronounce/pronounce lookup <term>
   ```

3. **Search for partial matches**:
   ```bash
   ~/.pronounce/pronounce search <query>
   ```

4. **Hear it spoken aloud** (macOS with `say` command):
   ```bash
   ~/.pronounce/pronounce say <term>
   ```

5. **Common pronunciations to know**:
   - `kubectl` → "koob-control" or "koob-cuddle"
   - `nginx` → "engine-X"
   - `JWT` → "jot"
   - `SQL` → "sequel" or "S-Q-L" (both accepted)
   - `GIF` → "jif" (creator's intent) or "gif" (hard G, common usage)
   - `char` → "kar" (like car) or "char" (like charcoal)

6. **If the tool is not installed**, provide the pronunciation from known entries or direct the user to the repository for the full database.

## References

- Source: https://github.com/anzy-renlab-ai/pronounce
- 540+ entries with confidence levels and community sources
- Supports: Bash CLI, interactive quiz, voice search, MCP server, Claude Code skill
