# Technical Details

## What It Does

Appshot is a code-first tool that turns a declarative TypeScript config into production-ready App Store and Google Play marketing assets. You define scenes (screenshot + caption + background + device frame), and Appshot renders them through Remotion's React-based video pipeline into static PNGs or animated MP4s with transitions. The Claude Code skill layer adds natural-language control — scanning app source to auto-generate configs, iterating on creative direction, and triggering renders from conversation.

## Architecture

```
appshot.config.ts  -->  Remotion Compositions  -->  Renderer  -->  PNG / MP4
       |                       |                       |
  TypeScript DSL         React + Tailwind         Puppeteer/FFmpeg
       |                       |
  Claude Skill          Device Frames + Layouts
  (config gen)          (bundled SVG assets)
```

**Key files in the appshot repo:**
- `src/config/schema.ts` — Zod schema for config validation
- `src/compositions/` — Remotion React components (device frames, captions, backgrounds)
- `src/renderer/` — Orchestrates Remotion's `renderMedia` and `renderStill` APIs
- `src/cli/` — CLI commands (`init`, `preview`, `render`)
- `src/skills/` — Claude Code skill definitions for AI-assisted workflows

**Dependencies:**
- Remotion (React video framework) — handles frame-by-frame rendering
- React + Tailwind — component styling
- Puppeteer (via Remotion) — headless Chrome for screenshot capture
- FFmpeg (via Remotion) — video encoding

**Data flow:**
1. CLI parses config, validates with Zod
2. Remotion compositions receive scene data as props
3. For PNG: `renderStill()` captures each scene at target resolution
4. For MP4: `renderMedia()` renders full sequence with transitions at 30fps

## Limitations

- Requires Node.js 18+ and ~500MB disk for Remotion/Chromium deps
- No real-time preview on headless servers (Studio needs a browser)
- Device frame library is finite — custom frames require SVG work
- Video render times scale linearly with scene count (~5-10s per scene)
- Claude skill depends on having screenshots already captured (doesn't take screenshots of running apps)
- No direct App Store Connect / Google Play Console upload integration

## Why It Matters for Claude-Driven Products

**Marketing automation:** Any agent that builds apps (agent factories, no-code builders) can auto-generate store listings as a final step — config generation is trivially LLM-friendly.

**Ad creative pipelines:** The config-to-render pattern maps directly to programmatic ad generation. Swap "app screenshots" for "product shots" and you have a templated creative engine controllable via Claude.

**ASO at scale:** For teams managing multiple apps, Claude can batch-generate and A/B test different caption/background combinations by iterating configs.

**Skill composability:** Demonstrates the "scan → direct → render" pattern where Claude Code skills chain together — useful reference for building multi-step agent workflows in any domain.
