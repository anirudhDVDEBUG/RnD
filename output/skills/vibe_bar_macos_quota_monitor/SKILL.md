---
name: vibe_bar_macos_quota_monitor
description: |
  Build and configure Vibe Bar, a native macOS menu-bar app for monitoring Claude Code and Codex subscription quota, usage pace, local token cost, and service status.
  Triggers: vibe bar, quota monitor, usage tracker, menu bar app, subscription usage
---

# Vibe Bar — macOS Quota Monitor

A native macOS SwiftUI menu-bar app that lets Claude Code and OpenAI Codex users track subscription quota consumption, usage pace, estimated local token cost, and live service status — all from the menu bar.

## When to use

- "Set up a menu bar app to track my Claude Code quota usage"
- "Monitor my Codex subscription usage and pace from the macOS menu bar"
- "Build a native macOS quota tracker for AI coding tools"
- "I want to see my Claude Code token spend and service status at a glance"
- "Help me configure Vibe Bar for quota monitoring"

## How to use

### 1. Clone and build

```bash
git clone https://github.com/AstroQore/vibe-bar.git
cd vibe-bar
open VibeBar.xcodeproj   # or the .xcworkspace if present
```

Build and run in Xcode (⌘R). The app appears as a menu-bar icon.

### 2. Core features

- **Quota tracking** — See how much of your Claude Code or Codex subscription quota you've consumed.
- **Usage pace** — Visual indicator of your burn rate so you can pace usage across the billing period.
- **Local token cost** — Estimates token spend for local coding sessions.
- **Service status** — Live status checks for Anthropic and OpenAI services.

### 3. Configuration

On first launch, configure your provider credentials and billing period in the app's preferences (click the menu-bar icon → Settings).

### 4. Development notes

- Written in **Swift / SwiftUI**, targeting macOS.
- Local-first design — data stays on your machine.
- Topics: `macos`, `menubar`, `swift`, `swiftui`, `claude-code`, `codex`, `quota-tracker`, `usage-monitor`.

## References

- Source repository: https://github.com/AstroQore/vibe-bar
