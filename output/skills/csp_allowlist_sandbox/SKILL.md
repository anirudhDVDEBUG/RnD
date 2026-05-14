---
name: csp_allowlist_sandbox
description: |
  Build a CSP-protected sandboxed iframe playground that intercepts blocked fetch requests,
  prompts the user to allow-list origins, and refreshes with updated Content-Security-Policy headers.
  Triggers: "csp sandbox", "iframe allow-list", "fetch intercept csp", "sandboxed iframe security",
  "content security policy allow-list"
---

# CSP Allow-list Sandbox

Create a browser-based tool that runs untrusted HTML/JS inside a CSP-protected sandboxed iframe, intercepts CSP-blocked network requests, and lets the user interactively build an origin allow-list.

## When to use

- "Build a CSP sandbox that lets users allow-list domains"
- "Create an iframe playground with Content-Security-Policy protection"
- "Intercept blocked fetch requests and prompt the user to allow them"
- "Set up a sandboxed preview with dynamic CSP connect-src management"
- "Build a tool like Simon Willison's CSP Allow-list Experiment"

## How to use

### Architecture

The tool has two layers:

1. **Parent window** — hosts the editor, preview controls, allow-list UI, and constructs the CSP header.
2. **Sandboxed iframe** — renders the user's HTML with a strict CSP applied; contains a patched `fetch()` that catches CSP violations.

### Step-by-step implementation

1. **Create the parent page** with:
   - A source-code editor panel (left) for the user's HTML.
   - A preview panel (right) containing a sandboxed `<iframe>`.
   - An allow-list manager: an input field, Add button, and tag list of allowed origins.
   - Buttons: *Reset sample*, *Clear allow-list*, *Refresh preview*.

2. **Build the CSP header string** dynamically from the allow-list:
   ```js
   function buildCSP(allowedOrigins) {
     const connectSrc = allowedOrigins.length
       ? `connect-src ${allowedOrigins.join(' ')};`
       : '';
     return [
       "default-src 'none'",
       "script-src 'unsafe-inline'",
       "style-src 'unsafe-inline'",
       connectSrc
     ].filter(Boolean).join('; ');
   }
   ```

3. **Inject the user's HTML into the iframe** using a `blob:` URL or `srcdoc`, prepending a `<meta http-equiv="Content-Security-Policy">` tag with the constructed policy:
   ```js
   function refreshPreview(html, allowedOrigins) {
     const csp = buildCSP(allowedOrigins);
     const wrapped = `<meta http-equiv="Content-Security-Policy" content="${csp}">
   <script>
   // Patch fetch to catch CSP blocks
   const _fetch = window.fetch;
   window.fetch = async function(url, opts) {
     try {
       return await _fetch(url, opts);
     } catch (err) {
       const origin = new URL(url).origin;
       window.parent.postMessage(
         { type: 'fetch-blocked', url: String(url), origin },
         '*'
       );
       throw err;
     }
   };
   <\/script>
   ${html}`;
     const blob = new Blob([wrapped], { type: 'text/html' });
     iframe.src = URL.createObjectURL(blob);
   }
   ```

4. **Listen for messages from the iframe** in the parent window:
   ```js
   window.addEventListener('message', (e) => {
     if (e.data?.type === 'fetch-blocked') {
       const allow = confirm(
         `The sandbox tried to connect to: ${e.data.origin}\n\n` +
         `Add this origin to the CSP connect-src allow-list and refresh?`
       );
       if (allow) {
         addToAllowList(e.data.origin);
         refreshPreview(getSource(), getAllowedOrigins());
       }
     }
   });
   ```

5. **Persist the allow-list** in `localStorage` so it survives reloads:
   ```js
   function getAllowedOrigins() {
     return JSON.parse(localStorage.getItem('csp-allow-list') || '[]');
   }
   function addToAllowList(origin) {
     const list = getAllowedOrigins();
     if (!list.includes(origin)) {
       list.push(origin);
       localStorage.setItem('csp-allow-list', JSON.stringify(list));
       renderAllowListUI();
     }
   }
   ```

6. **Set iframe sandbox attributes** for defense-in-depth:
   ```html
   <iframe sandbox="allow-scripts" id="preview"></iframe>
   ```
   The `sandbox` attribute without `allow-same-origin` ensures the iframe cannot access the parent's cookies or storage.

### Security considerations

- Start with `default-src 'none'` — deny everything by default.
- Only add `script-src 'unsafe-inline'` and `style-src 'unsafe-inline'` so user code can run inline scripts/styles.
- Each allowed origin is added **only** to `connect-src`, not to `script-src` or other directives.
- The `sandbox` attribute on the iframe provides an additional security layer beyond CSP.
- Always validate that origins added to the allow-list are well-formed URLs.

### Key files to produce

| File | Purpose |
|---|---|
| `index.html` | Single-page app with editor, preview iframe, and allow-list UI |
| `style.css` | Two-panel layout styling (optional — can be inline) |
| `app.js` | CSP builder, iframe injection, message listener, localStorage persistence |

## References

- [CSP Allow-list Experiment — Simon Willison](https://simonwillison.net/2026/May/13/csp-allow/#atom-everything)
- [Live tool](https://tools.simonwillison.net/csp-allow)
- [Earlier CSP iframe escape test](https://simonwillison.net/2026/Apr/3/test-csp-iframe-escape/)
- [MDN: Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
- [MDN: iframe sandbox attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox)
