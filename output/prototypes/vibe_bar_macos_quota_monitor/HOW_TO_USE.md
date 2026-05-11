# How to Use

## Option A: Terminal Demo (this repo)

### Install

```bash
# No dependencies beyond Python 3.6+
git clone <this-repo>
cd vibe_bar_macos_quota_monitor
bash run.sh
```

### First 60 Seconds

1. Run `bash run.sh` — the terminal dashboard prints immediately with mock data.
2. Review quota bars, pace indicators, and projected spend for both Claude Code and Codex.
3. Run `python3 quota_monitor.py --json` for machine-readable output you can pipe into other tools.

**Input:** (none — mock data auto-generated)

**Output:**
```
  Claude Code (Max)  [Max $200/mo]
  Quota used:  $94.17 / $200.00  (47.1%)
  [##############................]
  Pace:        =  ON PACE   (good)
  Today:       11 sessions, 182.3K in / 45.1K out
  Est. cost:   $1.2233 today

  SERVICE STATUS
  [OK]  Anthropic API         operational
  [OK]  Claude Code           operational
  [!!]  OpenAI API            degraded
```

---

## Option B: Claude Code Skill

This prototype ships a skill definition. To install it:

```bash
mkdir -p ~/.claude/skills/vibe_bar_macos_quota_monitor
cp SKILL.md ~/.claude/skills/vibe_bar_macos_quota_monitor/SKILL.md
```

### Trigger Phrases

Say any of these to Claude Code and the skill activates:

- "Set up a menu bar app to track my Claude Code quota usage"
- "Monitor my Codex subscription usage and pace"
- "Build a native macOS quota tracker for AI coding tools"
- "Help me configure Vibe Bar for quota monitoring"
- "vibe bar" / "quota monitor" / "usage tracker"

The skill guides Claude through cloning, building, and configuring the real macOS app.

---

## Option C: Real macOS App

```bash
git clone https://github.com/AstroQore/vibe-bar.git
cd vibe-bar
open VibeBar.xcodeproj
# Build & Run (Cmd+R) in Xcode
```

On first launch, click the menu-bar icon and open Settings to enter your provider credentials and billing period.

### Requirements

- macOS 13+ (Ventura or later)
- Xcode 15+
- Swift 5.9+
