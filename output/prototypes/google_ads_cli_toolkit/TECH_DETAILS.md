# Tech Details — Google Ads CLI Toolkit

## What It Does

The google-ads-cli-toolkit is a Python-based CLI that wraps three Google marketing APIs — Google Ads, Google Tag Manager (GTM), and Google Analytics 4 (GA4) — into a single terminal interface. It lets you list campaigns, pull performance metrics, execute GAQL (Google Ads Query Language) queries, manage GTM tags/triggers/variables, and retrieve GA4 analytics reports without ever opening a browser. The toolkit includes a Claude Code playbook so Claude can compose queries, interpret results, and automate bulk PPC operations through natural language.

The demo prototype in this repo simulates the full CLI surface using realistic mock data, so you can evaluate the workflow and output format without configuring API credentials.

## Architecture

```
google_ads_cli.py          # Main CLI entry point (argparse subcommands)
├── cmd: status            # Account-level summary across all services
├── cmd: campaigns         # Google Ads campaign listing + metrics
├── cmd: query <GAQL>      # GAQL query executor (parses & routes)
├── cmd: gtm               # GTM container listing
└── cmd: ga4               # GA4 source/medium traffic report

run.sh                     # End-to-end demo runner
requirements.txt           # Dependencies (stdlib-only for demo)
SKILL.md                   # Claude Code skill definition
```

### Data Flow (Full Toolkit)

```
User / Claude Code
    │
    ▼
google_ads_cli.py (argparse CLI)
    │
    ├── google-ads.yaml ──► Google Ads API (REST/gRPC)
    │                        └─ GAQL queries ──► campaign/ad_group/keyword data
    │
    ├── OAuth2 creds ──────► GTM API v2 (REST)
    │                        └─ containers, workspaces, tags, triggers, variables
    │
    └── Service account ───► GA4 Data API v1 (REST)
                             └─ runReport() ──► dimensions + metrics
```

### Key Dependencies (Full Toolkit)

| Package | Purpose |
|---------|---------|
| `google-ads` (v24+) | Official Google Ads API client; handles GAQL queries, campaign CRUD, bid management |
| `google-api-python-client` | GTM API v2 access via discovery-based client |
| `google-analytics-data` | GA4 Data API client for analytics reports |
| `google-auth` / `google-auth-oauthlib` | OAuth2 and service account authentication |
| `pyyaml` | Parses `google-ads.yaml` configuration |

### Model Calls

The toolkit itself makes **no LLM API calls**. It's designed as a tool layer that Claude Code invokes. Claude composes the GAQL queries, interprets the tabular output, and decides what operations to run next. The Claude Code playbook (SKILL.md) teaches Claude how to use each subcommand and what safety checks to perform (e.g., confirming customer ID before writes, using `--dry-run`).

## Limitations

- **Authentication complexity**: Each of the three APIs requires separate credential setup (developer token + OAuth for Ads, OAuth for GTM, service account for GA4). Initial setup takes 15-30 minutes per API.
- **Read-heavy**: The toolkit is strongest at querying and reporting. Write operations (create campaigns, modify bids, publish GTM versions) exist but require careful guardrails — there's no built-in undo.
- **No real-time bidding**: This is a management/reporting CLI, not a real-time bid optimizer. It queries snapshot data, not streaming auction signals.
- **Single-account**: Works with one Google Ads customer ID at a time. MCC (manager account) support for cross-account queries is limited.
- **GAQL learning curve**: Composing efficient GAQL queries requires understanding Google Ads resource relationships — this is where Claude Code integration adds the most value.
- **Rate limits**: Google Ads API has daily quota limits (~15,000 requests/day for basic access). Heavy automation needs a Standard access developer token.

## Why It Matters

**For Claude-driven ad operations**: This is the missing CLI layer between Claude Code and the Google Ads ecosystem. Instead of clicking through the Google Ads UI, a Claude agent can query campaign performance, identify underperformers, adjust bids, and generate reports — all from a terminal session. Combined with Claude's ability to compose GAQL queries from natural language, it dramatically lowers the barrier to programmatic ad management.

**For marketing/lead-gen teams**: Pull cross-platform reports (Ads + GA4 + GTM) into a single terminal workflow. Claude can interpret the data and suggest budget reallocations, keyword expansions, or audience adjustments without needing a dedicated PPC analyst.

**For agent factories**: This toolkit is a good template for wrapping any REST API behind a CLI that Claude can call. The pattern — argparse subcommands, YAML config, tabular output — works for any API-driven domain (CRM, email, social ads).
