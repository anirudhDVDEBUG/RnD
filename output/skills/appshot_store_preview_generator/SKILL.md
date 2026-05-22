---
name: appshot_store_preview_generator
description: |
  Generate App Store and Google Play preview videos and screenshots using Appshot (Remotion + React + Tailwind).
  Triggers: "app store screenshots", "play store preview video", "appshot", "store listing assets", "app preview render", "ASO screenshots", "mobile app marketing video"
---

# Appshot — App Store & Google Play Preview Generator

Generate professional App Store and Google Play preview videos and screenshots from a simple TypeScript config. Built on Remotion + React + Tailwind.

## When to use

- "Generate App Store screenshots for my iOS app"
- "Create a Google Play preview video from my app screens"
- "Set up appshot to produce store listing assets"
- "Render app marketing videos with device frames and captions"
- "Build ASO preview screenshots with text overlays and backgrounds"

## How to use

### 1. Install Appshot

```bash
npx appshot@latest init
```

This scaffolds the project with default templates, configs, and Remotion dependencies.

If adding to an existing project:

```bash
npm install appshot
```

### 2. Configure your scenes

Edit the TypeScript config file (typically `appshot.config.ts` at the project root) to define your scenes:

```typescript
import { defineConfig } from "appshot";

export default defineConfig({
  platform: "ios", // or "android"
  device: "iphone-15-pro", // device frame to use
  scenes: [
    {
      title: "Welcome Screen",
      screenshot: "./screenshots/welcome.png",
      caption: "Get started in seconds",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    },
    {
      title: "Dashboard",
      screenshot: "./screenshots/dashboard.png",
      caption: "Track everything at a glance",
      background: "#1a1a2e",
    },
  ],
});
```

### 3. Preview in browser

```bash
npx appshot preview
```

Opens a Remotion Studio preview in the browser where you can inspect each scene, adjust timing, and iterate on design.

### 4. Render screenshots

```bash
npx appshot render --format png
```

Renders each scene as a static screenshot sized for the target store (App Store or Google Play).

### 5. Render preview video

```bash
npx appshot render --format mp4
```

Renders the full sequence as an MP4 preview video with transitions between scenes.

### 6. AI-assisted workflow (Claude Code integration)

Appshot ships with built-in Claude Code agent skills. Use natural language to:

- **Scan your app**: Point appshot at your project to automatically detect screens and generate a config.
- **Direct the creative**: Describe the look and feel you want (colors, copy, layout) and let the agent update the config.
- **Render**: Trigger renders directly from the conversation.

Example workflow:
```
> Scan my React Native app in ./src/screens and generate appshot scenes
> Make the backgrounds more vibrant, use a blue-to-purple gradient theme
> Add captions that highlight the key feature of each screen
> Render screenshots for the App Store
```

### Key configuration options

| Option | Description |
|---|---|
| `platform` | `"ios"` or `"android"` — determines output sizes and device frames |
| `device` | Device frame model (e.g., `"iphone-15-pro"`, `"pixel-8"`) |
| `scenes[]` | Array of scene objects with screenshot, caption, background |
| `transitions` | Transition style between scenes for video (`"slide"`, `"fade"`, `"zoom"`) |
| `fps` | Frames per second for video output (default: 30) |
| `outputDir` | Directory for rendered output (default: `./output`) |

### Output sizes

- **App Store (iOS)**: 1290x2796 (6.7"), 1242x2688 (6.5"), 1242x2208 (5.5")
- **Google Play (Android)**: 1080x1920, custom sizes supported

## References

- **Repository**: https://github.com/trunghaiy/appshot
- **Built with**: [Remotion](https://www.remotion.dev/) + React + Tailwind CSS
- **License**: See repository for license details
