# Technical Details

## What it does

CosmoBlk email-design is a Claude Code skill that turns natural-language email requests into production-ready MJML/HTML. It enforces six opinionated archetypes (Welcome, Promotional, Newsletter, Transactional, Re-engagement, Announcement) and "anti-slop" rules — no lorem ipsum, no placeholder images, no missing footers. When Claude loads the skill, it gains structured knowledge of email archetypes, brand briefs, MJML component patterns, and ESP-specific merge tags so it can generate emails that are ready to send, not just look at.

The prototype in this repo extracts the core logic into a standalone Node.js module: you provide a brand brief + archetype → it outputs compiled MJML and responsive HTML.

## Architecture

```
archetypes.js     Six archetype definitions + ESP merge-tag maps
    ↓
builder.js        Takes (archetype, brand, esp) → produces MJML string → compiles via mjml → returns { mjml, html, errors }
    ↓
index.js          CLI entry point: parses args, calls builder, writes output/
generate_all.js   Batch: generates all six archetypes in one pass
```

### Key files

| File | Purpose |
|------|---------|
| `archetypes.js` | Archetype definitions (sections, defaults), ESP merge-tag mappings |
| `builder.js` | MJML template assembly and compilation |
| `index.js` | Single-archetype CLI |
| `generate_all.js` | Batch generation CLI |
| `run.sh` | End-to-end demo runner |

### Dependencies

- **mjml** (v4.x) — Framework for responsive email markup. Compiles MJML XML to battle-tested HTML that renders correctly in Outlook, Gmail, Apple Mail, and other clients.
- **Node.js >= 16** — Runtime.

No AI model calls, no API keys, no network requests at runtime (except the `placehold.co` image URLs in the demo brand brief).

## Limitations

- **No AI generation at runtime.** This prototype demonstrates the archetype/templating system. In real use, Claude Code itself writes the copy and selects imagery based on the skill instructions — the skill is a prompt, not a running service.
- **No actual ESP delivery.** The MCP integration (pushing templates to Klaviyo, Mailchimp, etc.) requires a configured MCP server for that ESP. This demo only generates the HTML files locally.
- **Placeholder images.** The demo uses `placehold.co` URLs. In production use, Claude would use real brand assets or URLs provided by the user.
- **Static templates.** The archetype layouts are fixed. Claude Code can deviate from them when the skill is loaded, but this standalone prototype always produces the same structure per archetype.
- **No dark-mode support.** The generated HTML does not include `@media (prefers-color-scheme: dark)` overrides.

## Why it matters

For teams building Claude-driven products in **marketing and lead-gen**:

- **Anti-slop by design.** Most AI email generators produce generic output. The archetype system forces structure and real content, reducing the edit-before-send cycle.
- **ESP-portable.** Merge tags auto-adapt to the target platform, so the same generation logic works across Klaviyo, Mailchimp, ActiveCampaign, and Nitrosend.
- **Skill-based architecture.** Demonstrates how to package domain expertise (email design best practices, CAN-SPAM compliance, responsive layout) as a reusable Claude Code skill — the same pattern applies to ad creative, landing pages, or any structured content.
- **MCP-ready.** When paired with an ESP's MCP server, Claude can go from "design me a welcome email" to a live campaign with no human touching HTML.
