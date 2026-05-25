# How to Use: Retro Book Game Converter

## What This Is

A **Claude Code skill** (not an MCP server, not a CLI tool). You install a `SKILL.md` file and Claude Code gains the ability to convert old BASIC game listings into playable browser games on demand.

## Installation

```bash
# Clone this repo
git clone <this-repo> retro_book_game_converter
cd retro_book_game_converter

# Copy the skill into Claude Code's skills directory
mkdir -p ~/.claude/skills/retro_book_game_converter
cp skill/SKILL.md ~/.claude/skills/retro_book_game_converter/SKILL.md
```

That's it. No pip install, no npm install, no API keys.

## Trigger Phrases

Once the skill is installed, say any of these to Claude Code:

- "Convert this old BASIC game listing into a playable web game"
- "Recreate this retro computer book game in JavaScript"
- "Build a browser version of this 1980s type-in game from a PDF"
- "Turn this Usborne game into HTML"
- "Make a mobile-friendly retro game from this vintage code listing"

Claude will produce a single `index.html` file with the complete game.

## First 60 Seconds

**Input:**
> "Convert Mad House from Usborne Creepy Computer Games into a playable browser game. It's a maze game where you avoid ghosts and collect treasures to escape a haunted house."

**Output:** A single `index.html` file containing:
- Green-on-black terminal aesthetic with CRT scanlines
- Arrow key + touch-friendly button controls
- Ghost AI that chases the player
- Treasure collection and escape mechanics
- Score tracking
- Mobile-responsive layout

**To play immediately:**
```bash
bash run.sh
# Opens at http://localhost:8973
```

Or just open `index.html` directly in any browser.

## Running the Demo

```bash
bash run.sh
```

This will:
1. Print a text-mode preview of the game
2. Start a local HTTP server on port 8973
3. Verify the game is being served correctly
4. Print the URL to open in your browser

No dependencies required beyond Python 3 (for the HTTP server) and a web browser.

## What You Get Per Conversion

Each game conversion produces:
- A single `index.html` (fully self-contained, no external deps)
- Retro terminal aesthetic (green/amber on black, monospace, scanlines)
- Mobile-friendly touch controls
- Credit footer linking to the original source
- Faithful recreation of original game mechanics
