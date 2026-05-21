---
name: token_speed_visualizer
description: |
  Build an interactive HTML demo that simulates LLM token output at various speeds (tokens per second), helping users visualize what advertised inference speeds actually look like in practice.
  TRIGGER when: user asks to visualize token speed, simulate LLM output speed, compare tokens per second, build a token throughput demo, or wants to understand what "X tokens/second" looks like.
  DO NOT TRIGGER when: user asks about optimizing inference performance, benchmarking actual models, or measuring real token throughput.
---

# Token Speed Visualizer

Create an interactive HTML application that simulates LLM token output at configurable speeds, so users can see and feel what different tokens-per-second rates look like in real time.

## When to use

- "What does 30 tokens per second look like?"
- "Build a demo that simulates LLM output speed"
- "Compare token throughput speeds visually"
- "I want to visualize the difference between 10 and 100 tokens per second"
- "Create an interactive token speed simulator"

## How to use

1. **Create a single self-contained HTML file** (no external dependencies) with the following features:
   - A text area or output div where tokens are streamed character-by-character or word-by-word to simulate LLM output.
   - A speed control (slider or input) allowing the user to set tokens per second, ranging from **5 to 800 tokens/sec**.
   - Preset speed buttons for common values: 5, 10, 30, 50, 100, 200, 400, 800 tokens/sec.
   - A start/stop/reset button to control the simulation.
   - A real-time counter showing tokens emitted and elapsed time.

2. **Token simulation logic:**
   - Use a sample paragraph of realistic LLM-style output text (at least 500 words).
   - Treat each word (whitespace-delimited) as roughly one token (a reasonable approximation for English text; note real tokenizers average ~0.75 words per token, but word-level is more visually intuitive).
   - Use `requestAnimationFrame` or `setInterval` with precise timing to emit tokens at the configured rate.
   - Accumulate tokens in the output area with smooth scrolling.

3. **Styling:**
   - Clean, minimal design with a monospace font for the output area.
   - Dark mode support via `prefers-color-scheme`.
   - Mobile-responsive layout.
   - Visually highlight the most recently emitted token briefly (e.g., a subtle background flash).

4. **Save the file** as `token_speed_demo.html` in the current directory and inform the user they can open it in any browser.

## Example output structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Token Speed Visualizer</title>
  <!-- All CSS inline -->
</head>
<body>
  <!-- Speed controls, output area, counters -->
  <!-- All JS inline -->
</body>
</html>
```

## References

- Original app by Mike Veerman: https://mikeveerman.github.io/tokenspeed/
- Source code: https://github.com/MikeVeerman/tokenspeed/blob/master/index.html
- Via Simon Willison: https://simonwillison.net/2026/May/20/tokens-per-second/#atom-everything
- Hacker News discussion: https://news.ycombinator.com/item?id=48174920
