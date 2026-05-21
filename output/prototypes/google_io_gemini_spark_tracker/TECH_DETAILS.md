# Technical Details

## What it does

This skill provides Claude Code with structured context about Google I/O 2026 announcements so it can answer questions about Gemini Spark, the Antigravity platform, and related competitive dynamics without hallucinating details. The standalone `tracker.py` script generates a summary report and machine-readable JSON export from curated announcement data -- no API keys or network access required.

The core value is **availability triage**: clearly separating what Google has actually shipped (GA) from what was demoed but isn't available yet (Preview/Coming Soon). This distinction matters because Google I/O historically announces products that take months to ship, and Simon Willison's coverage specifically calls this out.

## Architecture

```
SKILL.md                  # Claude Code skill definition (trigger rules + knowledge)
tracker.py                # Standalone report generator
  +-- Announcement        # Dataclass: name, category, description, status, model, tags
  +-- ANNOUNCEMENTS[]     # Curated list of 7 items from Google I/O 2026
  +-- summarize_all()     # Status breakdown + table view
  +-- detail_view()       # Per-item cards with URLs and tags
  +-- competitive_comparison()  # Gemini Spark vs OpenClaw vs Claude Code
  +-- export_json()       # Writes google_io_2026_tracker.json
```

**Dependencies:** Python 3.10+ standard library only (`json`, `textwrap`, `dataclasses`, `enum`). Zero third-party packages.

**Data flow:** All data is embedded in `tracker.py` as a Python list. No network calls, no API keys, no database. The JSON export is a flat file written to the current directory.

## Limitations

- **Static data**: Announcements are hardcoded from Simon Willison's May 20, 2026 blog post. As Google ships features or changes plans, the data goes stale. You must manually update `ANNOUNCEMENTS` in `tracker.py`.
- **No live checking**: The script does not verify whether URLs are live or whether GA status has changed. It's a snapshot, not a monitor.
- **Competitive comparison is approximate**: The Gemini Spark vs OpenClaw vs Claude Code table is a rough feature-parity snapshot, not a benchmark.
- **Prompt injection section is informational only**: The skill points users to the Google Cloud blog for security details but does not implement or test any guardrails.

## Why it matters for Claude-driven products

1. **Agent factories**: Gemini Spark is a direct competitor to Claude Code's agent capabilities. Tracking its feature set helps teams building agent orchestration decide which platform to target or integrate with.

2. **Lead-gen / marketing**: Knowing what Google announced (and what's actually available) lets content teams write accurate comparison pieces and avoid "coming soon" traps that age poorly.

3. **Ad creatives**: The Antigravity SDK's open-source Python wrapper is a real integration surface. Teams building multi-model ad pipelines may want to evaluate it alongside Anthropic's SDK.

4. **Voice AI**: Gemini Spark's native Google ecosystem integrations (Calendar, Gmail, Maps) make it relevant for voice-agent builders who need appointment scheduling or navigation -- areas where Claude currently relies on MCP servers.

5. **Security posture**: The prompt injection guardrails documentation is directly relevant to anyone shipping user-facing agents, regardless of model provider. Google's enterprise approach is worth studying as a comparison point.
