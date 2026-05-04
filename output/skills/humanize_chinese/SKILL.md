---
name: humanize_chinese
description: |
  Rewrites AI-generated Chinese text so it reads naturally and sounds human-written.
  TRIGGER: user asks to "humanize Chinese text", "make Chinese output natural",
  "rewrite Chinese to sound human", "polish Chinese writing", or "remove AI tone from Chinese".
---

# Humanize Chinese Text

Transform AI-generated Chinese text into natural, human-sounding Chinese prose. Applies idiomatic phrasing, varied sentence structure, and culturally appropriate tone to eliminate the robotic quality of machine-generated Chinese.

## When to use

- "Humanize this Chinese text"
- "Make this Chinese paragraph sound more natural"
- "Rewrite this Chinese so it doesn't sound like AI wrote it"
- "Polish my Chinese writing to sound more authentic"
- "Remove the AI tone from this Chinese content"

## How to use

1. **Provide the Chinese text** you want to humanize — paste it directly or point to a file containing Chinese content.

2. **Apply humanization rules** to the text:
   - Replace overly formal or stiff phrasing (e.g., 此外/furthermore → 另外/also, 需要注意的是 → 值得一提)
   - Vary sentence length — mix short punchy sentences with longer ones instead of uniform structure
   - Use colloquial connectors (而且, 不过, 其实, 说实话) instead of rigid academic ones (然而, 因此, 综上所述)
   - Remove unnecessary hedging phrases (如前所述, 总的来说, 从某种程度上讲)
   - Add natural discourse markers and filler appropriate to the register (嗯, 对了, 话说回来)
   - Prefer active voice and concrete subjects over passive constructions
   - Use contractions and spoken forms where appropriate (别 vs 不要, 挺好的 vs 非常好)
   - Ensure punctuation follows natural Chinese conventions (、for serial commas, ！for emphasis)

3. **Preserve meaning and intent** — the humanized version must convey the same information; only the style changes.

4. **Match the target register**:
   - **Casual/social media**: Use internet slang, emoji-friendly tone, shorter sentences
   - **Professional/business**: Natural but polished, avoid slang, keep appropriate formality
   - **Creative/narrative**: Varied rhythm, literary devices, emotional resonance
   - Default to a natural conversational register if unspecified.

5. **Output the rewritten text** with a brief note on key changes made.

## Example

**Input (AI-generated):**
> 人工智能技术在近年来取得了显著的进展。它在各个领域都有着广泛的应用，包括医疗、教育和金融等。需要注意的是，人工智能的发展也带来了一些挑战。

**Output (humanized):**
> 这几年AI发展得特别快，医疗、教育、金融这些领域都用上了。不过话说回来，发展快归快，问题也不少。

## References

- Source repository: [voidborne-d/humanize-chinese](https://github.com/voidborne-d/humanize-chinese)
- Discovered via: [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
