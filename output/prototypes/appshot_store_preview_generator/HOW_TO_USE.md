# How to Use Appshot

## Install

```bash
# Option A: Scaffold a new appshot project
npx appshot@latest init

# Option B: Add to existing project
npm install appshot
```

Requires Node.js 18+ and npm.

## Claude Code Skill Setup

Drop the skill file so Claude Code can trigger appshot workflows via natural language:

```bash
mkdir -p ~/.claude/skills/appshot_store_preview_generator
cp SKILL.md ~/.claude/skills/appshot_store_preview_generator/SKILL.md
```

**Trigger phrases:**
- "app store screenshots"
- "play store preview video"
- "appshot"
- "store listing assets"
- "app preview render"
- "ASO screenshots"
- "mobile app marketing video"

## First 60 Seconds

```bash
# 1. Init project
npx appshot@latest init
cd my-appshot-project

# 2. Edit appshot.config.ts (or use the default demo config)

# 3. Preview in browser
npx appshot preview

# 4. Render screenshots
npx appshot render --format png
# Output: ./output/scene-01.png, scene-02.png, ...

# 5. Render video
npx appshot render --format mp4
# Output: ./output/preview.mp4
```

**Input:** A TypeScript config with scene definitions (screenshot path, caption, background, device frame).

**Output:** Store-ready PNGs at 1290x2796 (iOS) or 1080x1920 (Android), plus an MP4 with slide/fade/zoom transitions.

## AI-Assisted Workflow (Claude Code)

With the skill installed, just ask Claude:

```
> Scan my React Native app in ./src/screens and generate appshot scenes
> Make backgrounds use a blue-to-purple gradient theme
> Render screenshots for the App Store
```

Claude will generate/update your `appshot.config.ts` and trigger renders.

## Local Demo (No Dependencies)

```bash
bash run.sh
```

This runs a self-contained Node.js demo that generates HTML-based preview mockups in `./demo_output/`, demonstrating the config-to-screenshot pipeline without needing Remotion installed.
