---
name: qr_code_generator
description: |
  Build a self-contained, single-file HTML QR code generator that creates scannable codes for URLs, text, and WiFi networks.
  TRIGGER when: user asks to generate QR codes, create a QR code tool, build a WiFi QR code, make a scannable code, or create a QR code web page.
  DO NOT TRIGGER when: user wants to read/decode existing QR codes, or needs server-side QR generation in Python/Node.
---

# QR Code Generator

Create a single-file HTML tool that generates QR codes for URLs, plain text, and WiFi network credentials — entirely client-side with no server required.

## When to use

- "Build me a QR code generator"
- "Create a web tool that makes QR codes for WiFi networks"
- "Generate a scannable QR code for a URL"
- "I need an HTML page that creates QR codes client-side"
- "Make a WiFi QR code so guests can connect easily"

## How to use

1. **Create a single HTML file** (e.g. `qr-code-generator.html`) that includes all markup, styles, and scripts inline.

2. **Include a QR code library.** Use the `qrcode-generator` library (also known as `qrcode.js` by kazuhikoarase) via a CDN `<script>` tag, or use a self-contained JS QR encoder. A good CDN option:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js"></script>
   ```

3. **Build two modes via a segmented toggle:**
   - **URL / Text mode** — a single textarea/input for arbitrary text or a URL.
   - **WiFi mode** — fields for:
     - Network name (SSID)
     - Password (with show/hide toggle)
     - Security dropdown: `WPA/WPA2/WPA3 (most common)`, `WEP`, `None`
     - Hidden network checkbox
   - WiFi QR string format: `WIFI:T:<security>;S:<ssid>;P:<password>;H:<hidden>;;`
     - Security values: `WPA`, `WEP`, or `nopass`
     - Hidden: `true` or `false`
     - Special characters in SSID/password (`;`, `,`, `:`, `\`, `"`) must be escaped with a backslash.

4. **Add style options:**
   - Module style: Square (default) or Rounded
   - Border: checkbox to add/remove quiet zone
   - Size: Small / Medium / Large (map to QR `cellSize` values like 4, 6, 10)
   - Color: color picker for foreground (default black), background always white

5. **Render the QR code** onto a `<canvas>` element when the user clicks "Generate QR code". Steps:
   - Determine the input string (plain text or WiFi-formatted string).
   - Choose an appropriate error correction level (M is a good default).
   - Auto-detect the minimum QR version (type number) that fits the data, or use `0` for auto.
   - Draw modules onto canvas, respecting chosen cell size, color, and border.

6. **Provide a download button** that exports the canvas as a PNG via `canvas.toDataURL('image/png')`.

7. **Styling guidelines:**
   - Clean, minimal design with a readable sans-serif font.
   - Use a segmented control (not tabs) for mode switching.
   - Group style options (style, border, size, color) visually below the input fields.
   - Mobile-friendly: responsive layout, minimum touch target sizes.

### Example WiFi string generation

```javascript
function buildWifiString(ssid, password, security, hidden) {
  const esc = (s) => s.replace(/([\\;,:"\\])/g, '\\$1');
  const secMap = { wpa: 'WPA', wep: 'WEP', none: 'nopass' };
  const sec = secMap[security] || 'WPA';
  return `WIFI:T:${sec};S:${esc(ssid)};P:${esc(password)};H:${hidden ? 'true' : 'false'};;`;
}
```

### Example QR rendering

```javascript
function generateQR(text, cellSize, color) {
  const qr = qrcode(0, 'M');
  qr.addData(text);
  qr.make();
  const count = qr.getModuleCount();
  const canvas = document.getElementById('qr-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.height = count * cellSize;
  for (let row = 0; row < count; row++) {
    for (let col = 0; col < count; col++) {
      ctx.fillStyle = qr.isDark(row, col) ? color : '#ffffff';
      ctx.fillRect(col * cellSize, row * cellSize, cellSize, cellSize);
    }
  }
}
```

## References

- Inspiration: [QR code generator by Simon Willison](https://simonwillison.net/2026/May/15/qr-code-generator/#atom-everything)
- Live demo: [tools.simonwillison.net/qr-code-generator](https://tools.simonwillison.net/qr-code-generator)
- WiFi QR code spec: `WIFI:T:<type>;S:<ssid>;P:<password>;H:<hidden>;;`
- QR library: [qrcode-generator on npm](https://www.npmjs.com/package/qrcode-generator)
