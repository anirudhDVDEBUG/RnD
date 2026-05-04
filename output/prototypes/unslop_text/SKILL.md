---
name: unslop_text
description: |
  Remove AI "slop" from text — overused filler words, cliched phrases, and hollow transitions that make writing sound machine-generated.
  TRIGGER when: user says "unslop", "remove slop", "de-slop", "make it sound less AI", "remove AI-isms", "less robotic", "too flowery", "sounds like ChatGPT", "remove filler", "tighten prose", "humanize this text", "natural writing", "clean up AI writing"
---

# Unslop Text

Detect and remove AI-generated "slop" -- the overused words, hollow transitions, and cliched phrases that make writing sound machine-generated. Based on [MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop).

## When to use

- "Unslop this paragraph" or "remove the slop"
- "This sounds too much like AI / ChatGPT -- make it natural"
- "Remove filler words and tighten the prose"
- "Humanize this text" or "make it less robotic"
- "Clean up AI writing" or "de-slop my draft"

## How to use

### Step 1: Identify slop patterns

Scan the text for these categories of AI slop:

**Overused intensifiers and filler adverbs:**
seamlessly, arguably, notably, importantly, crucially, frankly, undeniably, essentially, fundamentally, ultimately, remarkably, incredibly, moreover, furthermore, additionally, consequently, subsequently, accordingly, nevertheless, nonetheless, straightforward, straightforwardly

**Hollow adjectives and hyperbole:**
groundbreaking, game-changing, cutting-edge, revolutionary, transformative, innovative, world-class, best-in-class, state-of-the-art, next-generation, holistic, robust, scalable, leveraged, synergistic, unparalleled, unprecedented, pivotal, invaluable, indispensable, comprehensive, meticulous

**Cliched phrases and transitions (remove or rephrase entirely):**
- "It's worth noting that..." / "It's important to note..."
- "In today's [rapidly evolving/fast-paced/digital] landscape..."
- "Let's dive in" / "Let's dive deep" / "Let's unpack"
- "At the end of the day..."
- "This is where X comes in" / "Enter X"
- "The beauty of X is..."
- "Think of it as..."
- "Here's the thing:" / "Here's the kicker:"
- "Not just X, but Y" (when used as empty emphasis)
- "Take it to the next level"
- "By the same token"
- "In a nutshell" / "At its core"
- "The landscape of X" / "Navigate the landscape"
- "Unlock the power/potential of..."
- "Delve into" / "Delve deeper"
- "Realm" / "in the realm of"
- "Tapestry" / "rich tapestry"
- "Embark on a journey"
- "Foster innovation/growth/collaboration"
- "It's not just about X -- it's about Y"
- "Imagine a world where..."
- "In an era where..."
- "Peeling back the layers"
- "The secret sauce"

**Sycophantic openers (remove completely):**
- "Great question!"
- "That's a really interesting point"
- "Absolutely!"
- "What a fantastic..."

**Hollow conclusions:**
- "In conclusion, ..." (just state the conclusion)
- "To sum up / To summarize" (just summarize)
- "As we've seen..." (the reader was there)

### Step 2: Apply fixes

For each slop instance found:

1. **Delete** if the word/phrase adds no meaning (most filler adverbs, sycophantic openers, hollow transitions)
2. **Replace** with a specific, concrete word if meaning would be lost (e.g., "groundbreaking" -> describe what actually changed; "robust" -> "handles X and Y edge cases")
3. **Restructure** the sentence if removing the slop makes it awkward

### Step 3: Verify

- Re-read the cleaned text to ensure it still flows naturally
- Check that no actual meaning was lost
- Ensure the tone matches the intended audience (technical, casual, formal)
- The goal is clear, direct writing -- not robotic or stripped-down writing

### Principles

- **Show, don't tell**: Replace vague praise ("innovative solution") with specifics ("reduces latency by 40%")
- **Cut the warm-up**: Get to the point. Remove throat-clearing intros.
- **One idea per sentence**: If a sentence has multiple filler words, it's probably trying to say too much.
- **Prefer plain language**: "use" over "leverage/utilize", "help" over "empower", "improve" over "revolutionize" (unless it literally is a revolution)
- **Trust the reader**: Don't over-explain or over-emphasize. If it's important, the content shows it.

## References

- Source: [MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop)
- Curated from: [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
