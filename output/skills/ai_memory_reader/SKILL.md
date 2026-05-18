---
name: ai_memory_reader
description: |
  Native macOS & iOS app for browsing AI agent memory files.
  Triggers: browse AI memory, view claude memory files, inspect agent memory, memory reader app, view markdown memory
---

# AI Memory Reader

A native macOS & iOS SwiftUI app for browsing and viewing AI agent memory files — supports Claude Code, OpenClaw, Codex, Cursor, and Gemini.

## When to use

- "I want to browse my AI agent's memory files"
- "How can I view Claude Code memory on macOS?"
- "I need a native app to inspect agent memory markdown files"
- "Show me a tool for reading AI memory files across agents"
- "I want to view my Cursor/Codex/Gemini memory files"

## How to use

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nvwalj/ai-memory-reader.git
   cd ai-memory-reader
   ```
2. Open the Xcode project and build for macOS or iOS.
3. Alternatively, check the GitHub releases for a pre-built `.app` binary.

### Supported AI Agents

The app reads memory files from these AI coding agents:

- **Claude Code** — `~/.claude/` directory (CLAUDE.md, memory files)
- **OpenClaw** — agent memory directories
- **Codex** — OpenAI Codex memory files
- **Cursor** — Cursor editor agent memory
- **Gemini** — Google Gemini agent memory

### Usage

1. Launch the app on macOS or iOS.
2. The app automatically discovers and indexes AI agent memory files from known paths.
3. Browse memory files organized by agent in a native SwiftUI interface.
4. View rendered Markdown content for each memory file.
5. Use the app to audit, review, or understand what your AI agents have stored.

### Key Features

- **Native experience** — built with SwiftUI for macOS and iOS
- **Multi-agent support** — browse memory from Claude Code, Codex, Cursor, Gemini, and more
- **Markdown rendering** — view `.md` memory files with proper formatting
- **Auto-discovery** — finds memory files in standard agent directories
- **Read-only** — safely browse without risk of modifying agent memory

## References

- Source: [nvwalj/ai-memory-reader](https://github.com/nvwalj/ai-memory-reader)
- Language: Swift / SwiftUI
- Platforms: macOS, iOS
