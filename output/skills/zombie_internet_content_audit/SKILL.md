---
name: zombie_internet_content_audit
description: |
  Audit text, web pages, or content feeds for signs of AI-generated "slop" and zombie internet patterns.
  TRIGGER when: user asks to check if content is AI-generated, detect LLM slop, audit content authenticity, scan for zombie internet patterns, or evaluate writing for AI tells.
  DO NOT TRIGGER when: user wants to generate content with AI, or is asking about AI models themselves.
---

# Zombie Internet Content Audit

Audit text and content for hallmarks of AI-generated writing ("slop") and zombie internet patterns, based on the framework described by Jason Koebler (404 Media) and highlighted by Simon Willison.

## When to use

- "Does this look AI-generated?"
- "Check this article/post/comment for LLM slop"
- "Audit this content for authenticity"
- "Scan this feed/page for zombie internet patterns"
- "Is this real human writing or AI output?"

## How to use

1. **Collect the content** — accept raw text, a URL (use `WebFetch`), or a file path (use `Read`).
2. **Run the slop signal scan.** Check for these common AI-writing indicators:
   - **Lexical tells**: overuse of "delve", "landscape", "arguably", "It's important to note", "game-changer", "in today's fast-paced world", "comprehensive", "cutting-edge", "straightforward", "I'd be happy to", "Great question!"
   - **Structural tells**: listicle padding, formulaic intro → body → hopeful conclusion, every paragraph the same length, excessive hedging, hollow superlatives.
   - **Zombie internet patterns**: heartfelt advice from marketing accounts, AI-summarized books sold as originals, automated blog/social posts optimized purely for ad revenue, engagement-bait phrasing.
   - **Metadata tells**: generic author bios, stock-photo avatars, publication timestamps clustering at regular intervals, suspiciously high output volume.
3. **Score and report.** Provide:
   - A confidence estimate (low / medium / high) that the content is AI-generated.
   - Specific passages or patterns that triggered the assessment, with line references.
   - A brief note on which category applies: pure bot output, human-edited AI draft, AI-augmented human writing, or likely authentic human writing.
4. **Offer next steps:**
   - For content creators: suggest how to revise flagged passages to sound more authentic.
   - For content consumers: flag which parts to verify independently.
   - For feed/platform operators: recommend filtering heuristics.

## Key concepts

- **Dead Internet**: bots talking to bots — fully automated, no humans involved.
- **Zombie Internet** (Koebler's term): the more insidious reality where humans use AI to talk to other humans, AI agents interact on behalf of people, hustlebro influencers spin up automated channels, and the line between human and machine authorship is deliberately blurred.
- **Slop**: low-quality AI-generated content published without meaningful human review or editing.

## Limitations

- No detector is 100% accurate. This skill identifies *patterns consistent with* AI generation, not proof.
- Skilled human editors can remove AI tells; conversely, some human writers naturally use phrases common in LLM output.
- Always pair automated detection with human judgment.

## References

- Jason Koebler, "Your AI Use Is Breaking My Brain" — [404 Media](https://www.404media.co/your-ai-use-is-breaking-my-brain/)
- Simon Willison's commentary — [simonwillison.net](https://simonwillison.net/2026/May/11/zombie-internet/#atom-everything)
