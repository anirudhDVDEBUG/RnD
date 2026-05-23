# Technical Details

## What This Does

This is a Claude Code **skill** (a markdown knowledge file) paired with a standalone Python analyzer. The skill gives Claude structured context about the FTC's May 2026 enforcement action against Cox Media Group, MindSift, and 1010 Digital Works for marketing an "Active Listening" AI ad-targeting service that falsely claimed to use smart-device microphone data. The Python analyzer demonstrates the same analysis as a runnable script, outputting a structured report from bundled case data.

The core value is **regulatory intelligence**: translating an FTC enforcement action into actionable compliance guidance for teams building or marketing AI products, especially in ad-tech and marketing automation.

## Architecture

```
ftc_active_listening_settlement/
  SKILL.md          -- Claude Code skill definition (drop into ~/.claude/skills/)
  analyzer.py       -- Standalone analysis script (Python 3, stdlib only)
  case_data.json    -- Structured case facts, penalties, timeline, lessons
  run.sh            -- Entry point: runs analyzer.py
  requirements.txt  -- Empty (stdlib only)
```

**Data flow:**
1. `case_data.json` contains structured facts about the settlement (parties, claims, reality, penalties, timeline, lessons)
2. `analyzer.py` loads the JSON, formats it into a human-readable report or JSON output
3. CLI flags (`--section`, `--format`) allow filtering to specific aspects

**No model calls, no API keys, no external dependencies.** The skill file is consumed by Claude Code's skill-loading mechanism; the Python script is a self-contained demo.

## Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Injected into Claude's context when trigger phrases match |
| `analyzer.py` | CLI tool that parses `case_data.json` and prints analysis |
| `case_data.json` | All case facts in structured format |

## Dependencies

- Python 3.6+ (standard library only: `json`, `argparse`, `textwrap`)
- No pip packages required

## Limitations

- **Static data only.** The case data is a snapshot of the May 2026 settlement. It does not update automatically if further enforcement actions or appeals occur.
- **No legal advice.** The compliance lessons are informational. Consult legal counsel for actual regulatory guidance.
- **Skill triggers are keyword-based.** Claude Code matches on phrases in the skill description; edge-case queries may not activate it.
- **No primary source fetching.** The analyzer does not scrape the FTC website or court filings. All data is pre-bundled.

## Why This Matters for Claude-Driven Products

- **Lead-gen / marketing teams:** If you're building AI-powered marketing tools, this case is a direct warning. Overstating what your AI does in pitch decks or sales materials is an FTC enforcement target.
- **Ad creatives / ad-tech:** The "Active Listening" pitch is a case study in how rebranding commodity ad-tech with AI buzzwords backfires.
- **Agent factories:** If your agents make claims about data sources or capabilities, those claims need to be verifiable. The FTC treats AI capability claims the same as any other advertising claim.
- **Voice AI:** This case confirms that despite widespread consumer fear, mainstream ad targeting does NOT use ambient microphone data. Voice AI builders can reference this settlement to differentiate real voice-data products from fraudulent claims.

## References

- [FTC Press Release (May 2026)](https://www.ftc.gov/news-events/news/press-releases/2026/05/ftc-require-cox-media-group-two-other-firms-pay-nearly-1-million-settle-charges-they-deceived)
- [Simon Willison's Analysis](https://simonwillison.net/2026/May/22/ftc-active-listening/#atom-everything)
- [Simon Willison's 2024 Coverage](https://simonwillison.net/2024/Sep/2/facebook-cmg/)
- [CMG Pitch Deck (DocumentCloud)](https://www.documentcloud.org/documents/25051283-cmg-pitch-deck-on-voice-data-advertising-active-listening/)
