# Technical Details

## What It Does

This is a single-page browser tool that lets you write arbitrary HTML/JS in an editor and run it inside a sandboxed `<iframe>` governed by a strict Content-Security-Policy. The CSP starts with `default-src 'none'` -- blocking all network requests. When code inside the iframe tries to `fetch()` an external origin, the tool intercepts the failure, pops up a confirmation dialog, and -- if approved -- adds that origin to the CSP `connect-src` directive and reloads the iframe. This creates an interactive, incremental allow-list workflow for exploring what origins untrusted code needs.

## Architecture

```
+---------------------+       postMessage        +----------------------------+
|   Parent window     | <----------------------- |   Sandboxed iframe         |
|   (index.html)      |                          |   (blob: URL)              |
|                     |                          |                            |
|  - Editor textarea  |   builds CSP + injects   |  - <meta> CSP header       |
|  - Allow-list UI    | -----------------------> |  - Patched fetch()         |
|  - CSP display      |                          |  - securitypolicyviolation |
|  - Event log        |                          |    event listener          |
+---------------------+                          +----------------------------+
        |
        v
   localStorage (persist allow-list)
```

### Key Files

| File | Role |
|---|---|
| `index.html` | Layout: editor panel, preview iframe, toolbar, allow-list tags, log |
| `app.js` | All logic: CSP builder, blob URL injection, `postMessage` listener, localStorage, UI wiring |
| `style.css` | Two-panel dark theme (Catppuccin Mocha palette) |
| `server.js` | Zero-dependency static file server (Node built-in `http`) |

### Data Flow

1. User edits HTML in the textarea.
2. On "Refresh Preview", `app.js` reads the allow-list from `localStorage`, builds a CSP string, and wraps the user's HTML with a `<meta http-equiv="Content-Security-Policy">` tag plus a patched `fetch()`.
3. The wrapped HTML is turned into a `blob:` URL and assigned to the iframe's `src`.
4. The iframe has `sandbox="allow-scripts"` (no `allow-same-origin`), providing an additional isolation layer.
5. When `fetch()` fails inside the iframe (CSP blocks it), the patched function sends a `postMessage` to the parent with the blocked origin.
6. The parent's message listener shows a `confirm()` dialog. If accepted, the origin is added to the allow-list, persisted, and the preview refreshes with the updated CSP.
7. The iframe also listens for `securitypolicyviolation` DOM events as a fallback detection mechanism.

### Dependencies

**None.** The server uses Node's built-in `http` and `fs` modules. The frontend is vanilla HTML/CSS/JS with no build step, no frameworks, no npm packages.

## Limitations

- **`connect-src` only.** The allow-list only controls `fetch()`/XHR destinations. It does not manage `img-src`, `script-src`, `font-src`, or other CSP directives. Extending to those would require parsing the violation's `effectiveDirective`.
- **`confirm()` UX.** The browser's native `confirm()` dialog is modal and blocks. A production tool would use a non-blocking toast/banner UI.
- **No server-side CSP.** The CSP is applied via a `<meta>` tag inside the iframe, not via an HTTP response header. Some CSP directives (like `frame-ancestors`) don't work in `<meta>` tags. For this use case (`connect-src`), `<meta>` is sufficient.
- **`blob:` URL origin.** Because the iframe loads from a `blob:` URL and lacks `allow-same-origin`, its effective origin is `null`. This means it cannot use cookies, `localStorage`, or other origin-scoped APIs itself.
- **No `XMLHttpRequest` patching.** Only `fetch()` is patched. Legacy XHR calls would still be blocked but wouldn't trigger the allow-list prompt (the `securitypolicyviolation` event provides partial coverage).

## Why It Matters for Claude-Driven Products

- **Agent sandboxing.** If you're building an agent that generates and runs code (e.g., an "agent factory" that outputs HTML dashboards or ad creatives), this pattern lets you sandbox the agent's output while giving users fine-grained control over what external services it can reach.
- **Lead-gen / marketing tool previews.** Preview user-submitted landing pages or email templates safely. The CSP sandbox prevents exfiltration while the allow-list lets legitimate analytics or API calls through.
- **Ad creative testing.** Run ad HTML in a sandbox, see which tracking pixels and APIs it tries to call, and approve them one by one before going live.
- **Security research.** Quickly test what network calls an untrusted snippet makes without risking your browsing context.
