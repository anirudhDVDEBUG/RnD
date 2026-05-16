# How to Use

## Prerequisites

- Any modern browser (Chrome, Firefox, Safari, Edge)
- Python 3 (only for the local dev server in `run.sh`; you can also just double-click the HTML file)

## Quick start

```bash
git clone <this-repo>
cd qr_code_generator
bash run.sh
# Opens http://localhost:8765/qr-code-generator.html
```

Or simply open `qr-code-generator.html` directly in your browser — no server needed.

## Using this as a Claude Code Skill

This repo includes a `SKILL.md` that teaches Claude Code how to build QR code generators on demand.

1. Copy the skill folder into your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/qr_code_generator
   cp SKILL.md ~/.claude/skills/qr_code_generator/SKILL.md
   ```

2. **Trigger phrases** that activate the skill:
   - "Build me a QR code generator"
   - "Create a web tool that makes QR codes for WiFi networks"
   - "Generate a scannable QR code for a URL"
   - "Make a WiFi QR code so guests can connect easily"

3. Claude Code will produce a self-contained HTML file with all markup, styles, and scripts inline.

## First 60 seconds

1. Run `bash run.sh` (or open the HTML file directly).
2. You see two modes: **URL / Text** and **WiFi**.
3. **URL / Text mode:** type `https://example.com` and click **Generate QR Code**. A QR code appears. Click **Download PNG** to save it.
4. **WiFi mode:** switch to WiFi, enter your network name and password, pick security type, click **Generate QR Code**. Hand the PNG to guests — they scan it with their phone camera and connect automatically.
5. Customize: change module style (square/rounded), toggle the quiet zone border, pick a size, or change the foreground color.

## Configuration

| Environment variable | Default | Description |
|---|---|---|
| `PORT` | `8765` | Port for the local dev server |
