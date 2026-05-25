# Technical Details: Retro Book Game Converter

## What It Does

This is a Claude Code skill that instructs Claude to analyze vintage BASIC game listings (from 1980s books like Usborne's series) and faithfully recreate them as self-contained HTML/JS browser games. The skill provides Claude with a structured approach: parse the original game logic (movement, scoring, win/lose conditions), map BASIC constructs to modern equivalents, and output a single `index.html` with retro styling.

The key insight is that 1980s type-in games have simple, well-defined mechanics that map cleanly to vanilla JavaScript — no game engine needed. The skill ensures Claude maintains fidelity to the original while adding modern affordances (touch controls, responsive layout).

## Architecture

```
~/.claude/skills/retro_book_game_converter/
└── SKILL.md          # The skill definition (instructions for Claude)

Output per conversion:
└── index.html        # Self-contained game (HTML + CSS + JS, no deps)
```

**Data flow:**
1. User provides game description or BASIC listing (text, PDF reference, or description)
2. Skill triggers on keywords like "retro game", "BASIC listing", "Usborne"
3. Claude analyzes game mechanics from the source material
4. Claude generates a single HTML file with embedded CSS and JS
5. User opens in browser — game is immediately playable

**No external dependencies.** No build step, no framework, no API calls. The output is a static HTML file.

## Key Design Decisions

- **Single-file output**: Everything in one `index.html` — easy to share, host, or embed
- **Vanilla JS only**: No React, no Canvas libraries, no game engines. Text-mode rendering using monospace pre-formatted text
- **ASCII graphics**: Uses Unicode block characters and symbols, matching the spirit of the original text-mode games
- **CRT aesthetic**: CSS scanline overlay, green-on-black coloring, monospace fonts
- **Mobile-first controls**: On-screen directional buttons alongside keyboard support

## Limitations

- **No OCR**: Cannot read scanned PDFs directly. User must provide the game description or transcribed listing
- **Simple games only**: Best suited for text-mode, turn-based, or simple real-time games. Not appropriate for complex graphical games
- **No sound**: Original games often had BEEP commands; this doesn't recreate audio
- **Interpretation required**: If the original BASIC listing has platform-specific commands (PEEK/POKE, hardware sprites), Claude approximates the behavior rather than emulating the hardware
- **Single-page limit**: Very complex multi-screen games may exceed what fits cleanly in one file

## Why This Matters for Claude-Driven Products

**Content marketing / Lead gen**: Retro game recreations are highly shareable nostalgic content. A marketing agency could use this skill to generate playable retro games as interactive content pieces — embed them in blog posts, landing pages, or email campaigns. The games are self-contained HTML that works anywhere.

**Agent factories**: This demonstrates a pattern where a skill turns Claude into a specialized code generator with domain expertise. The same pattern applies to generating ad creatives, email templates, or interactive demos from specifications.

**Educational products**: Converting old programming books into playable demos bridges generations of learners. Schools teaching programming history can instantly demonstrate what 1980s code produced.

**Ad creatives**: Interactive retro-styled mini-games make compelling ad units. A single prompt produces a deployable game that could serve as a playable ad or engagement piece.

## Source

- [Simon Willison: Mad House — Usborne Creepy Computer Games](https://simonwillison.net/2026/May/24/usborne-mad-house/#atom-everything)
- [Usborne Free Computer Book PDFs](https://usborne.com/us/books/computer-and-coding-books)
