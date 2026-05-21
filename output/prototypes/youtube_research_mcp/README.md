# YouTube Research MCP

**MCP server that turns YouTube into a structured AI research source** — extract transcripts, pull comments, analyze channels, and search videos, all callable from Claude via the Model Context Protocol.

## Headline Result

```
$ bash run.sh

1. GET TRANSCRIPT
Video ID : dQw4w9WgXcQ   |   Segments: 10   |   Source: youtube_transcript_api
Full text: "Welcome to this deep dive on large language models. Today we'll
cover how transformer architectures work..."

2. GET COMMENTS
[234 likes] @AIResearcher42: Great explanation of attention!
[187 likes] @MLEngineer: Would love a follow-up on MoE architectures.

3. ANALYZE CHANNEL
Channel: AI Explained  |  542,000 subs  |  187 videos  |  28.4M views
Top topics: transformers, LLMs, benchmarks, RAG, scaling laws

4. SEARCH VIDEOS
[dQw4w9WgXcQ] How Transformers Work — Visual Guide (320,000 views)
```

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure as MCP server, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, product relevance
