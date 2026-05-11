---
name: deliberate_wheel_reinvention
description: |
  Guides deliberate reimplementation of existing tools/algorithms as a structured learning exercise.
  TRIGGER: user wants to learn by rebuilding something, asks "should I reinvent X", wants to deeply understand a library/tool/algorithm by implementing it from scratch, or asks about learning-by-doing vs studying.
---

# Deliberate Wheel Reinvention

A skill for structured learning through intentional reimplementation. Based on Andrew Quinn's insight that reinventing 4-5 wheels in a domain propels you to the frontier faster than idle study — but you need to pick the *right* wheels.

## When to use

- "I want to truly understand how X works by building it myself"
- "Should I reimplement this or just use the existing library?"
- "Help me learn [domain] by building something from scratch"
- "I keep using X but don't understand the internals"
- "What's the best way to deeply learn [topic] through practice?"

## How to use

### Step 1: Identify the wheel worth reinventing

Ask the user what domain they want to deepen expertise in. Help them pick a reimplementation target that:
- Covers a **foundational concept** (not a trivial wrapper or glue code)
- Is **bounded enough** to finish in days, not months
- Will teach **transferable principles** (e.g., building a simple SQLite teaches B-trees, query parsing, file I/O — applicable everywhere)
- Isn't already well-understood by the user (no value re-treading known ground)

### Step 2: Scope the minimal version

Define a stripped-down version that captures the core insight without incidental complexity:
- List the 3-5 **essential behaviors** the reimplementation must exhibit
- Explicitly list what to **leave out** (production error handling, edge cases, performance optimizations)
- Set a **done condition**: what proves you've internalized the concept?

### Step 3: Build with directed questions

During implementation, encourage the user to:
1. **Attempt first** before looking at reference implementations
2. **Ask targeted questions** when stuck — "How does X handle Y?" beats reading the full source
3. **Compare their solution** against the real implementation after completing each component
4. **Note the delta** — where their intuition was right, where it was wrong, and why

### Step 4: Extract the lesson

After building, help the user articulate:
- What they now understand that they didn't before
- What class of problems this knowledge unlocks
- Whether this wheel connects to another worth reinventing next

### Example targets by domain

| Domain | Good wheels to reinvent |
|--------|------------------------|
| Databases | B-tree, simple query parser, WAL journaling |
| Networking | HTTP/1.1 server, DNS resolver, TCP over UDP |
| Compilers | Lexer, recursive descent parser, register allocator |
| Search | Inverted index, TF-IDF, finite state transducer |
| OS | Memory allocator, simple filesystem, shell |
| Web | Template engine, router, form validator |

## Key principle

> You *need* to reinvent a couple of wheels to get to the edge of what we know about wheel-making — not a thousand wheels, and not zero; probably four or five is sufficient in most domains. Each wheel you reinvent, and every directed question you ask along the way, will propel you faster to the true frontier than that same amount of time spent in idle study, or even five times that amount.
>
> — Andrew Quinn

## References

- [Quoting Andrew Quinn](https://simonwillison.net/2026/May/10/andrew-quinn/#atom-everything) — Simon Willison's Weblog
- [Replacing a 3 GB SQLite database with a 10 MB FST binary](https://til.andrew-quinn.me/posts/replacing-a-3-gb-sqlite-database-with-a-7-mb-fst-finite-state-trandsucer-binary/#fn:5) — Andrew Quinn (original source)
