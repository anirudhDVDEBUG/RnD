# Technical Details

## What it does

A single self-contained HTML file (~200 lines) that simulates LLM token generation at user-specified speeds. It splits a ~600-word sample text into whitespace-delimited tokens and emits them into a scrolling output area using `requestAnimationFrame` with precise time-delta accumulation. This gives users a visceral sense of what advertised inference speeds (tokens/second) actually feel like during real interaction.

## Architecture

```
token_speed_demo.html   (single file, zero dependencies)
├── CSS: responsive layout, dark mode via prefers-color-scheme
├── HTML: preset buttons, range slider, start/stop/reset, output div, stats bar
└── JS:  rAF loop with fractional token accumulator for accurate pacing
```

**Data flow:**
1. Sample text is split into tokens (words + whitespace segments)
2. Each animation frame calculates `elapsed * speed` to determine tokens to emit
3. Non-whitespace tokens get a brief highlight class; whitespace is inserted as text nodes
4. Stats (count, elapsed, actual rate) update every frame

**Key implementation details:**
- Fractional accumulator prevents drift at high speeds (e.g., 800 t/s = ~1.25ms/token, below rAF resolution, so multiple tokens emit per frame)
- Token highlighting uses CSS transitions for subtle visual feedback
- No external fonts, frameworks, or network requests

## Limitations

- Treats words as tokens; real BPE tokenizers average ~0.75 words/token (so actual throughput in words is ~75% of stated t/s). This is intentional for visual clarity.
- No latency simulation (time-to-first-token / prefill delay)
- Cannot simulate actual model quality differences at different speeds
- Single fixed sample text (not configurable without editing source)
- Browser tab throttling may reduce accuracy when tab is background

## Why it matters for Claude-driven products

- **Lead-gen / marketing sites:** Demonstrates streaming UX quality at different price points. Helps product teams decide minimum acceptable speed for their chat widget.
- **Agent factories:** Multi-step agents make sequential LLM calls. Understanding per-call latency budget (e.g., 5 calls at 50 t/s vs 200 t/s) directly impacts UX design.
- **Voice AI:** Text-to-speech pipelines need tokens fast enough to maintain natural speech cadence (~3 words/sec). This tool shows that 15+ t/s is the bare minimum for real-time voice.
- **Ad creative generation:** Batch speed matters for cost. Visualizing 400 t/s helps stakeholders understand why Groq/Cerebras claims matter for high-volume generation.

## References

- Original app: [mikeveerman.github.io/tokenspeed](https://mikeveerman.github.io/tokenspeed/)
- Source: [github.com/MikeVeerman/tokenspeed](https://github.com/MikeVeerman/tokenspeed/blob/master/index.html)
- Simon Willison writeup: [simonwillison.net/2026/May/20/tokens-per-second](https://simonwillison.net/2026/May/20/tokens-per-second/#atom-everything)
