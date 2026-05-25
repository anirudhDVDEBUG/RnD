---
name: retro_book_game_converter
description: |
  Converts classic computer games from vintage programming books (1980s-era BASIC listings, PDFs, scans) into modern, playable browser games using vanilla JavaScript and HTML.
  Triggers: retro game, vintage code, BASIC listing, old computer book, Usborne, type-in game, 8-bit game recreation, convert old game
---

# Retro Book Game Converter

Recreate classic games from vintage computer books (like Usborne's 1980s series) as modern, playable browser games in vanilla JavaScript and HTML with a retro aesthetic.

## When to use

- "Convert this old BASIC game listing into a playable web game"
- "Recreate this retro computer book game in JavaScript"
- "Build a browser version of this 1980s type-in game from a PDF"
- "Turn this Usborne / Commodore 64 / ZX Spectrum game into HTML"
- "Make a mobile-friendly retro game from this vintage code listing"

## How to use

1. **Obtain the source material**: Get the PDF, scan, or text of the original game listing from the vintage book. Usborne published free PDFs of their 1980s computer books at https://usborne.com/us/books/computer-and-coding-books.

2. **Analyze the original game logic**: Read through the original BASIC (or other language) listing and identify:
   - Core game mechanics (movement, scoring, win/lose conditions)
   - Text-based UI elements (ASCII art, status displays)
   - Input controls (keyboard mappings)
   - Any randomization or timing elements

3. **Build the HTML/JS game**: Create a single `index.html` file with:
   - Vanilla JavaScript (no frameworks)
   - Retro aesthetic: green-on-black or amber-on-black terminal style, monospace fonts, CRT-like effects
   - Mobile-friendly controls: touch-friendly buttons mirroring keyboard inputs
   - Responsive layout that works on both desktop and mobile

4. **Structure the game code**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>GAME TITLE — Book Title</title>
     <style>
       /* Retro terminal aesthetic */
       body { background: #000; color: #0f0; font-family: 'Courier New', monospace; }
       /* CRT scanline effect (optional) */
       /* Mobile-friendly button sizing */
     </style>
   </head>
   <body>
     <div id="game"><!-- game UI --></div>
     <script>
       // Game logic faithfully recreated from the original listing
     </script>
   </body>
   </html>
   ```

5. **Credit the original source**: Include a visible credit line linking to the original book or publisher. Example:
   ```html
   <footer>
     Based on "Game Name" from <em>Book Title</em> (Year) by Publisher.
     <a href="https://example.com">Free PDFs available here</a>
   </footer>
   ```

6. **Key design principles**:
   - Stay faithful to the original game mechanics — don't over-modernize
   - Use ASCII-style graphics (asterisks, pipes, dashes) to match the original feel
   - Keep controls simple and clearly labeled
   - Add a START/RESTART button for easy replay
   - Display score/status prominently like the original

## References

- Source: [Mad House — Usborne Creepy Computer Games](https://simonwillison.net/2026/May/24/usborne-mad-house/#atom-everything) by Simon Willison
- [Usborne Free Computer Book PDFs](https://usborne.com/us/books/computer-and-coding-books)
