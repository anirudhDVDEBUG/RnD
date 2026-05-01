---
name: rewrite_tool_descriptions
description: |
  Rewrite and optimize tool/API descriptions so LLM-based agents can select and invoke them more reliably, especially at scale (100+ tools). Applies principles from the Trace-Free+ curriculum-learning framework.
  TRIGGER when: user wants to improve tool descriptions for agent consumption, optimize API catalogs for LLM tool-use, reduce tool-selection errors at scale, or make function/tool interfaces less ambiguous for AI agents.
  DO NOT TRIGGER when: user is building tools from scratch, writing human-facing API docs, or doing general prompt engineering unrelated to tool interfaces.
---

# Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use

Apply research-backed principles from the Trace-Free+ framework to rewrite tool and API descriptions so that LLM-based agents select and call them correctly, especially as tool catalogs grow large.

## When to use

- "These tool descriptions are confusing the agent — it keeps picking the wrong one"
- "Optimize my tool catalog so the LLM can distinguish between similar functions"
- "Rewrite these API descriptions for better agent tool selection"
- "My agent's accuracy drops as I add more tools — help fix the descriptions"
- "Make these function descriptions less ambiguous for LLM consumption"

## How to use

### Step 1 — Audit existing descriptions

Collect all tool/function descriptions the agent consumes. Identify:
- **Ambiguous phrasing**: terms that overlap between tools (e.g., "get data" used by multiple tools)
- **Missing constraints**: parameter types, valid ranges, required formats not stated
- **Human-oriented shorthand**: abbreviations, implicit context, or jargon a human dev would resolve but an LLM cannot
- **Redundant tools**: near-duplicates that confuse selection

### Step 2 — Rewrite each description using these principles

For each tool, produce a rewritten description that follows these rules:

1. **Lead with a unique, discriminative verb-object phrase.** e.g., "Search restaurant reviews by location and cuisine" not "Get data from the restaurant API."
2. **State what the tool does NOT do.** When two tools are similar, explicitly note the boundary. e.g., "Returns restaurant metadata only — does NOT place orders. For orders, use `place_order`."
3. **Enumerate parameters with types, defaults, and constraints inline.** e.g., `location (string, required): City name or lat/lng pair. Must not be empty.`
4. **Specify the return schema concisely.** e.g., "Returns a JSON array of objects with fields: `name` (string), `rating` (float 0-5), `address` (string)."
5. **Include a single canonical example** showing a realistic invocation and expected output shape.
6. **Keep total length under 200 words per tool.** Longer descriptions degrade selection accuracy at scale.

### Step 3 — Differentiate across the catalog

After rewriting individually, review the full set together:

- Ensure no two descriptions share the same leading verb-object phrase
- Add explicit cross-references between commonly confused tools ("See also: X for Y use-case")
- Group tools by domain/namespace if the catalog exceeds ~50 tools
- Remove or merge truly redundant tools

### Step 4 — Validate with contrastive queries

Test the rewritten catalog by prompting the agent with:
- Queries that should match exactly one tool
- Queries that are deliberately ambiguous to see if the agent asks for clarification
- Queries that require chaining two tools, verifying correct ordering

Fix any remaining selection errors by tightening the discriminative phrasing.

### Template for a rewritten tool description

```
Name: <tool_name>
Description: <Unique verb-object phrase>. <One sentence elaborating scope>. Does NOT <common misconception>.
Parameters:
  - <param> (<type>, <required|optional>): <Constraint and semantics>.
Returns: <Concise schema description>.
Example:
  Input: <realistic example input>
  Output: <abbreviated realistic output>
```

## Key insights from the research

- Tool descriptions written for human developers tolerate ambiguity that agents cannot resolve — rewriting for agents is a distinct task from writing docs.
- Accuracy degrades significantly as catalogs grow past ~50 tools; discriminative descriptions reduce this degradation by ~29%.
- Optimizing descriptions across the catalog (not per-tool in isolation) captures inter-tool contrasts that matter for selection.
- These gains are complementary to agent fine-tuning — you get improvements on top of better models.

## References

- Paper: [Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use](https://arxiv.org/abs/2602.20426) — Trace-Free+ curriculum learning framework for scalable tool-description optimization.
