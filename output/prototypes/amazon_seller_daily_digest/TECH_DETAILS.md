# Technical Details: Amazon Seller Daily Digest

## What It Does

This skill implements a multi-source intelligence aggregation pipeline for Amazon sellers. It scrapes/fetches signals from four source categories (official Amazon announcements, seller community forums, podcast transcripts, and newsletter archives), then passes the raw signals through Claude for synthesis into a structured, bilingual digest. The output is formatted into five actionable sections (Policy, Tools, Buzz, Signals, Actions) and routed to the configured delivery channel.

The key value is **signal compression**: a seller would need to monitor 10+ sources daily; this condenses them into a 2-minute read with explicit action items.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   index.js (orchestrator)            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌──────┐ │
│  │ Official │  │Community │  │Podcast │  │News- │ │
│  │ Fetcher  │  │ Fetcher  │  │Fetcher │  │letter│ │
│  └────┬─────┘  └────┬─────┘  └───┬────┘  └──┬───┘ │
│       │              │            │           │     │
│       └──────────────┴────────────┴───────────┘     │
│                       │                             │
│              ┌────────▼────────┐                    │
│              │  Claude Synth   │                    │
│              │  (remix/rank)   │                    │
│              └────────┬────────┘                    │
│                       │                             │
│              ┌────────▼────────┐                    │
│              │   Formatter     │                    │
│              │  (zh/en/both)   │                    │
│              └────────┬────────┘                    │
│                       │                             │
│    ┌─────────┬────────┼────────┬──────────┐        │
│    │stdout   │Telegram│ Email  │  Feishu  │        │
│    └─────────┴────────┴────────┴──────────┘        │
└─────────────────────────────────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `index.js` | Main orchestrator — runs fetchers, calls synthesis, routes output |
| `src/fetchers/` | Source-specific scrapers (official, community, podcast, newsletter) |
| `src/synthesizer.js` | Claude API call to remix raw signals into structured digest |
| `src/formatter.js` | Bilingual formatting (zh/en sections with category tags) |
| `src/delivery/` | Output channel adapters (stdout, telegram, email, feishu) |
| `config.js` | Source URLs, language settings, delivery config |

### Dependencies

- **node-fetch** / built-in fetch — HTTP requests to source URLs
- **@anthropic-ai/sdk** — Claude API for synthesis step
- **nodemailer** — Email delivery (optional)
- **node-telegram-bot-api** — Telegram delivery (optional)

### Data Flow

1. **Fetch** (parallel): Each fetcher hits its sources, extracts headlines/summaries
2. **Normalize**: Raw items tagged with `{source, category, title, summary, url, date}`
3. **Synthesize**: All normalized items sent to Claude with a structured prompt requesting bilingual digest in 5 categories
4. **Format**: Claude output parsed into sections, wrapped with delivery-specific formatting (Markdown for Telegram, HTML for email)
5. **Deliver**: Routed to configured channel(s)

## Limitations

- **Source freshness depends on scraping**: If Amazon changes their announcement page structure, the official fetcher breaks until updated.
- **No historical storage**: Each run is stateless; doesn't deduplicate against yesterday's digest.
- **Claude dependency for synthesis**: Without an API key, you only get raw fetched items (or mock data in demo mode).
- **Rate limits**: Community forum scraping may be throttled; no built-in retry/backoff beyond simple timeout.
- **Language quality**: Chinese translations are Claude-generated, not human-reviewed.

## Why This Matters for Claude-Driven Products

- **Lead-gen / Marketing**: Daily digests are a proven newsletter format — this is a template for building "daily brief" products in any vertical (not just Amazon). Swap the fetchers for any niche's sources.
- **Agent Factories**: Demonstrates the fetch-synthesize-deliver pattern that's reusable across any "monitoring agent" use case. The architecture cleanly separates concerns for easy customization.
- **Ad Creatives**: The "Action Items" section could feed directly into ad copy generation — "New FBA fees? Here's how our tool saves you $X/month."
- **Voice AI**: The structured digest format (short tagged items) maps well to voice briefings — each section is a natural "segment" for a morning audio digest.
