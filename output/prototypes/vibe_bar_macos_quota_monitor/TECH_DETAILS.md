# Technical Details

## What It Does

Vibe Bar is a native macOS menu-bar application written in Swift/SwiftUI that polls subscription usage data for Claude Code (Anthropic) and Codex (OpenAI), computes quota consumption rates, projects end-of-period spend, and surfaces live service-status indicators. The terminal demo in this repo (`quota_monitor.py`) replicates the same dashboard logic using mock data so the concept can be evaluated without macOS or API credentials.

The core computation is straightforward: given a billing period (start/end dates) and current cumulative spend, it derives the time-fraction elapsed, the usage-fraction consumed, and a pace ratio (usage/time). A ratio above 1.0 means you're spending faster than the billing period allows — the app flags this visually so you can throttle usage before hitting the cap.

## Architecture

### Real macOS App (Swift)

```
VibeBar.xcodeproj/
  VibeBarApp.swift        — App entry, NSStatusItem menu-bar setup
  QuotaService.swift      — Polls provider APIs for usage data
  StatusService.swift     — Checks api.anthropic.com / api.openai.com health
  DashboardView.swift     — SwiftUI popover with quota bars, pace, cost
  SettingsView.swift      — Credential & billing config (stored in Keychain)
  Models/
    Provider.swift        — Billing period, quota, usage structs
    TokenCost.swift       — Per-model token pricing tables
```

**Data flow:** Timer fires every ~60s -> QuotaService fetches usage -> Model computes pace & projection -> SwiftUI view updates -> menu-bar icon color changes (green/yellow/red).

### Terminal Demo (Python)

```
quota_monitor.py          — Single-file demo, stdlib only
  generate_mock_usage()   — Produces realistic billing/usage dicts
  check_service_status()  — Simulated status endpoint results
  render_dashboard()      — Terminal or JSON output
```

No external dependencies. Python 3.6+.

## Key Dependencies

| Component        | Dependency       | Purpose                    |
|------------------|------------------|----------------------------|
| macOS app        | SwiftUI          | Native menu-bar UI         |
| macOS app        | Keychain         | Secure credential storage  |
| macOS app        | URLSession       | HTTP polling               |
| Terminal demo    | Python stdlib    | Zero-dep demo              |

## Limitations

- **No real API integration in the demo.** The terminal version uses randomized mock data. The real app requires macOS, Xcode, and valid provider credentials.
- **Quota APIs are unofficial.** Neither Anthropic nor OpenAI expose a formal "quota remaining" REST endpoint for consumer plans. The real app likely scrapes usage dashboards or uses undocumented endpoints, which may break.
- **macOS only.** The native app is SwiftUI-based; there is no Linux/Windows port.
- **No alerting.** The app shows status but does not send push notifications or Slack messages when thresholds are crossed (an obvious extension).
- **Single-user.** No team/org-level quota aggregation.

## Why It Matters

For anyone building Claude-driven products (agent factories, marketing automation, ad-creative pipelines, voice AI), quota management is a real operational concern:

- **Cost visibility** — Subscription tiers with soft caps mean surprise throttling. Knowing your burn rate in real time prevents mid-sprint slowdowns.
- **Pacing for teams** — If multiple agents share a quota, a dashboard like this (extended to team view) becomes essential infrastructure.
- **Multi-provider arbitrage** — Seeing Claude and Codex usage side-by-side lets you shift workloads to whichever provider has more headroom.
- **Build-vs-buy signal** — This app is ~500 lines of Swift. If you need quota monitoring in your own agent platform, the pattern (poll + compute pace + traffic-light UI) is easy to replicate.
