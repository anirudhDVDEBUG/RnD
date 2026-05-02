# LangChain Agent Platform — Mini-Repo

**TL;DR:** Demonstrates LangChain's core patterns — LCEL chains, tool-calling agents, RAG pipelines, and structured output — all runnable locally with mock data and no API keys required.

## Headline Result

```
$ bash run.sh

=== LCEL Chain Demo ===
Q: What are Python decorators?
A: Decorators are functions that modify the behavior of other functions...

=== Tool-Calling Agent Demo ===
Agent called: calculator("42 * 17") -> 714
Final answer: 42 * 17 = 714

=== RAG Pipeline Demo ===
Indexed 4 documents into FAISS vector store
Q: What is LangChain?
A: LangChain is an agent engineering platform for composing LLMs, tools, and retrieval...

=== Structured Output Demo ===
MovieReview(title='Inception', rating=9, summary='A mind-bending thriller...')
```

## Next Steps

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, configure, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations
