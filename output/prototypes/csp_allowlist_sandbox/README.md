# CSP Allow-list Sandbox

A browser-based tool that runs untrusted HTML/JS inside a CSP-protected sandboxed iframe, intercepts blocked network requests, and lets you interactively build an origin allow-list. Inspired by [Simon Willison's CSP Allow-list Experiment](https://simonwillison.net/2026/May/13/csp-allow/#atom-everything).

**Headline result:** Type any HTML+JS in the editor, hit Refresh -- blocked `fetch()` calls trigger a prompt asking if you want to allow that origin. Accept, and the iframe auto-reloads with an updated `Content-Security-Policy` header that now permits the request.

- [HOW_TO_USE.md](HOW_TO_USE.md) -- install, run, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) -- architecture, data flow, limitations
