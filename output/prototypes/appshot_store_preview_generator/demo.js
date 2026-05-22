#!/usr/bin/env node
/**
 * Appshot Store Preview Generator — Local Demo
 * Generates HTML-based store preview mockups from a config,
 * demonstrating the config-to-screenshot pipeline.
 */

const fs = require("fs");
const path = require("path");

// --- Mock appshot config (equivalent to appshot.config.ts) ---
const config = {
  platform: "ios",
  device: "iphone-15-pro",
  outputDir: "./demo_output",
  transitions: "slide",
  fps: 30,
  scenes: [
    {
      title: "Welcome Screen",
      caption: "Get started in seconds",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      mockContent: "Welcome to MyApp",
    },
    {
      title: "Dashboard",
      caption: "Track everything at a glance",
      background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
      mockContent: "Dashboard: 12 tasks, 3 projects",
    },
    {
      title: "Analytics",
      caption: "Insights that drive growth",
      background: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
      mockContent: "Revenue: $12.4k | Users: 2.3k",
    },
    {
      title: "Settings",
      caption: "Your app, your way",
      background: "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
      mockContent: "Profile | Notifications | Theme",
    },
    {
      title: "Share",
      caption: "Collaborate with your team",
      background: "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
      mockContent: "Invite 3 teammates",
    },
  ],
};

// --- Device frame dimensions ---
const devices = {
  "iphone-15-pro": { width: 1290, height: 2796, radius: 120, name: "iPhone 15 Pro" },
  "pixel-8": { width: 1080, height: 1920, radius: 80, name: "Pixel 8" },
};

const device = devices[config.device] || devices["iphone-15-pro"];

// --- Generate HTML preview for a single scene ---
function generateSceneHTML(scene, index, deviceInfo) {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>${scene.title} — Store Preview</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: ${deviceInfo.width}px;
  height: ${deviceInfo.height}px;
  background: ${scene.background};
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  overflow: hidden;
}
.caption {
  color: white;
  font-size: 72px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 80px;
  text-shadow: 0 2px 20px rgba(0,0,0,0.3);
  padding: 0 60px;
}
.device-frame {
  width: 740px;
  height: 1560px;
  background: #1a1a1a;
  border-radius: ${deviceInfo.radius}px;
  border: 12px solid #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 40px 80px rgba(0,0,0,0.4);
  position: relative;
  overflow: hidden;
}
.device-frame::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 36px;
  background: #000;
  border-radius: 18px;
}
.screen-content {
  color: white;
  font-size: 42px;
  text-align: center;
  padding: 40px;
  opacity: 0.9;
}
.scene-number {
  position: absolute;
  top: 40px;
  right: 40px;
  color: rgba(255,255,255,0.5);
  font-size: 32px;
}
</style>
</head>
<body>
  <div class="scene-number">${index + 1} / ${config.scenes.length}</div>
  <div class="caption">${scene.caption}</div>
  <div class="device-frame">
    <div class="screen-content">${scene.mockContent}</div>
  </div>
</body>
</html>`;
}

// --- Generate storyboard overview ---
function generateStoryboardHTML(scenes, deviceInfo) {
  const sceneCards = scenes
    .map(
      (scene, i) => `
    <div class="scene-card">
      <div class="scene-preview" style="background: ${scene.background}">
        <div class="mini-caption">${scene.caption}</div>
        <div class="mini-device">
          <div class="mini-content">${scene.mockContent}</div>
        </div>
      </div>
      <div class="scene-label">${i + 1}. ${scene.title}</div>
    </div>`
    )
    .join("\n");

  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Appshot Storyboard — ${config.platform.toUpperCase()} ${deviceInfo.name}</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0f0f0f;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  padding: 60px;
}
h1 { font-size: 36px; margin-bottom: 8px; }
.subtitle { color: #888; font-size: 18px; margin-bottom: 40px; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}
.scene-card {
  border-radius: 16px;
  overflow: hidden;
  background: #1a1a1a;
}
.scene-preview {
  aspect-ratio: 9/16;
  max-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.mini-caption {
  color: white;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 16px;
  text-shadow: 0 1px 8px rgba(0,0,0,0.3);
}
.mini-device {
  width: 120px;
  height: 220px;
  background: #1a1a1a;
  border-radius: 16px;
  border: 3px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
}
.mini-content {
  color: #ccc;
  font-size: 9px;
  text-align: center;
  padding: 8px;
}
.scene-label {
  padding: 16px;
  font-size: 14px;
  font-weight: 500;
}
.config-block {
  margin-top: 50px;
  background: #1a1a1a;
  border-radius: 12px;
  padding: 24px;
}
.config-block h2 { font-size: 20px; margin-bottom: 12px; }
.config-block pre {
  color: #a8e6cf;
  font-size: 13px;
  line-height: 1.5;
  overflow-x: auto;
}
</style>
</head>
<body>
  <h1>Appshot Preview Storyboard</h1>
  <div class="subtitle">Platform: ${config.platform.toUpperCase()} | Device: ${deviceInfo.name} | Scenes: ${scenes.length} | Transitions: ${config.transitions}</div>
  <div class="grid">
    ${sceneCards}
  </div>
  <div class="config-block">
    <h2>Generated Config</h2>
    <pre>${JSON.stringify(config, null, 2)}</pre>
  </div>
</body>
</html>`;
}

// --- Main ---
function main() {
  const outputDir = path.resolve(config.outputDir);

  // Create output directory
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log("=== Appshot Store Preview Generator (Demo) ===\n");
  console.log(`Platform:    ${config.platform.toUpperCase()}`);
  console.log(`Device:      ${device.name} (${device.width}x${device.height})`);
  console.log(`Scenes:      ${config.scenes.length}`);
  console.log(`Transitions: ${config.transitions}`);
  console.log(`Output:      ${outputDir}\n`);

  // Generate individual scene HTMLs
  config.scenes.forEach((scene, i) => {
    const html = generateSceneHTML(scene, i, device);
    const filename = `scene-${String(i + 1).padStart(2, "0")}-${scene.title.toLowerCase().replace(/\s+/g, "-")}.html`;
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, html);
    console.log(`  [PNG mock] ${filename}  "${scene.caption}"`);
  });

  // Generate storyboard overview
  const storyboard = generateStoryboardHTML(config.scenes, device);
  const storyboardPath = path.join(outputDir, "storyboard.html");
  fs.writeFileSync(storyboardPath, storyboard);
  console.log(`\n  [Storyboard] storyboard.html`);

  // Generate config file (as it would appear in a real project)
  const configTS = `import { defineConfig } from "appshot";

export default defineConfig({
  platform: "${config.platform}",
  device: "${config.device}",
  transitions: "${config.transitions}",
  fps: ${config.fps},
  scenes: ${JSON.stringify(config.scenes.map(s => ({
    title: s.title,
    screenshot: `./screenshots/${s.title.toLowerCase().replace(/\s+/g, "-")}.png`,
    caption: s.caption,
    background: s.background,
  })), null, 4).replace(/\n/g, "\n  ")},
});
`;
  const configPath = path.join(outputDir, "appshot.config.ts");
  fs.writeFileSync(configPath, configTS);
  console.log(`  [Config]     appshot.config.ts`);

  console.log("\n--- Summary ---");
  console.log(`Generated ${config.scenes.length} scene previews + storyboard + config`);
  console.log(`Open ${storyboardPath} in a browser to see the full preview.`);
  console.log("\nIn production, 'npx appshot render --format png' converts these to pixel-perfect store screenshots.");
  console.log("'npx appshot render --format mp4' produces a preview video with transitions.\n");
}

main();
