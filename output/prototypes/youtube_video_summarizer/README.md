# YouTube Video Summarizer

**Turn any YouTube video into structured markdown notes in seconds** -- TL;DR, key takeaways, chapter breakdowns, notable quotes, and action items.

## Headline Result

Given a YouTube URL, produces output like:

```
# How Transformers Work - A Detailed Explanation

**Channel:** AI Academy
**Duration:** 18:42

## TL;DR
Transformers replaced RNNs by using self-attention to process all tokens simultaneously.
The architecture uses multi-head attention and positional encoding stacked into deep blocks.

## Key Takeaways
- Transformers solved RNN's sequential bottleneck with self-attention
- Query/Key/Value mechanism computes token relationships in parallel
- Multi-head attention captures different linguistic patterns simultaneously
- Positional encoding (sinusoidal or RoPE) preserves word order
...
```

## Quick Start

```bash
bash run.sh          # demo with mock data, no dependencies needed
```

For real videos:
```bash
pip install yt-dlp
python3 summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- Installation, Claude skill setup, trigger phrases
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- Architecture, data flow, limitations
