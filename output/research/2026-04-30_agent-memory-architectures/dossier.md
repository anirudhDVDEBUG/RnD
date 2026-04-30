# Agent Memory Architectures — Research Dossier

*Audience: JNTU students • Talk length: ~30 minutes • Date: 2026-04-30*

> **Note on sourcing.** WebSearch was not granted in this session, so the "fresh authoritative sources" requirement is filled from canonical, well-established URLs (arXiv preprints, primary GitHub repos) that I am confident exist and are widely referenced in the agent-memory literature through early 2026. The local DB hits are mostly tangential (Claude skill scaffolds and unrelated MCP servers); I cite only the few that genuinely connect to the topic.

---

## 1. Executive Summary

LLMs are stateless function calls. An "agent" is the software wrapper that pretends otherwise — and that pretense is what we call **memory**. Over the last 24 months the field has converged on a fairly clear picture: a single context window cannot be the whole answer, and every serious framework now layers some form of *external* memory on top of the model. The interesting disagreement is *how* to organize that external store.

Four design families dominate as of April 2026:

1. **Tiered / OS-style memory** — treat context as RAM and external stores as disk, paging facts in and out. MemGPT (https://arxiv.org/abs/2310.08560) introduced this metaphor; its production successor is the Letta runtime (https://github.com/letta-ai/letta).
2. **Extract-and-retrieve memory** — distill conversation turns into atomic "memories," embed them, and retrieve top-k by similarity. Mem0 (https://github.com/mem0ai/mem0, paper https://arxiv.org/abs/2504.19413) is the canonical example.
3. **Temporal knowledge graphs** — store facts as time-stamped triples in a graph so the agent can reason about *when* something was true, not just *whether*. Zep/Graphiti (https://github.com/getzep/graphiti, https://arxiv.org/abs/2501.13956) leads here.
4. **Cognitive-inspired hierarchies** — explicitly model episodic, semantic, and procedural memory and add a "reflection" loop that compresses recent experience into higher-level beliefs. Park et al.'s Generative Agents paper (https://arxiv.org/abs/2304.03442) is the seed; most 2025 systems borrow its reflect-summarize-retrieve loop.

Two benchmarks now anchor empirical comparison: **LongMemEval** (https://arxiv.org/abs/2410.10813), which stress-tests recall across 5 reasoning skills over very long histories, and **LoCoMo** (https://arxiv.org/abs/2402.17753), a 600-turn multi-session conversational benchmark. Mem0's own evaluation reports it beats a full-context baseline on LoCoMo while using ~90% fewer tokens (https://arxiv.org/abs/2504.19413) — the headline result that has driven a lot of 2025 production adoption.

The practitioner take-away for students: **pick the memory shape that matches your task's failure mode**. Chatbots that hallucinate user preferences need extract-and-retrieve. Agents that confuse "what is true now" with "what was true last week" need a temporal graph. Long-running coding/ops agents that exhaust context need OS-style paging. The Claude Skills ecosystem (https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder, https://antigravity.google/docs/skills) is also worth understanding as a form of *procedural* memory — reusable behavioral packs the agent loads on demand.

A talk-friendly framing: **"Memory is not a database problem; it is a forgetting problem."** What the agent throws away is what determines whether it scales.

---

## 2. Landscape Map — Taxonomy of Approaches

A useful way to organize the space is along two axes: *what is stored* (raw text vs. structured facts vs. learned skills) and *how it is recalled* (ranked retrieval vs. graph traversal vs. paged into context).

```
                      RAW TEXT          STRUCTURED FACTS        SKILLS / PROCEDURES
                  ┌────────────────┬──────────────────────┬──────────────────────┐
  RANKED          │ Vector RAG     │ Mem0                 │ Tool/skill registries│
  RETRIEVAL       │ (chunks+embed) │ (extracted memories) │ (Anthropic Skills,   │
                  │                │                      │  voltagent)          │
                  ├────────────────┼──────────────────────┼──────────────────────┤
  GRAPH           │ —              │ Zep / Graphiti       │ DecisionGraph        │
  TRAVERSAL       │                │ (temporal KG)        │ (decision memory)    │
                  ├────────────────┼──────────────────────┼──────────────────────┤
  PAGED INTO      │ MemGPT / Letta │ Generative Agents    │ Reflection / self-   │
  CONTEXT         │ (OS metaphor)  │ (reflect→summary)    │ editing memory       │
                  └────────────────┴──────────────────────┴──────────────────────┘
```

Cross-cutting concerns that any architecture must answer:

- **Write policy** — when to commit something to long-term memory (every turn? after summarization? on user signal?).
- **Forgetting / consolidation** — TTLs, decay scores, summarization passes, contradiction resolution.
- **Indexing modality** — dense vectors, BM25, graph edges, or hybrid.
- **Query rewriting** — does the agent retrieve from the raw user message, or from a model-rewritten query?
- **Provenance & trust** — can the agent cite *why* it believes a fact, and override stale entries?

The cognitive-science taxonomy of **episodic** (specific events), **semantic** (general facts), and **procedural** (how-to skills) memory is the most common pedagogical scaffold, and maps cleanly to: chat-history snippets, extracted user-profile facts, and skill packs respectively.

---

## 3. Deep-Dives

### 3.1 Tiered, OS-style memory: MemGPT → Letta

MemGPT (Packer et al., 2023; https://arxiv.org/abs/2310.08560) is the architectural ancestor of every "agent has a hard drive" design. Its central move is to treat the model's context window as **main memory** and to expose tool calls — `core_memory_append`, `archival_memory_search`, `recall_memory_search` — that the LLM itself uses to page facts in and out. The OS analogy is not just rhetorical: there is a fixed-size "core memory" (system-prompt-like, always in context), a recall buffer (recent messages), and an unbounded archival store (vector-indexed). The model decides what to evict.

Letta (https://github.com/letta-ai/letta) is the production-grade rewrite of MemGPT by the same team. It generalizes the idea into a **stateful agent server** with sleep-time compute (background memory consolidation while the agent is idle) and a typed schema for memory blocks. The pedagogically interesting bit for students is the *self-editing* property: the agent's behavior next turn depends on edits it made to its own core-memory block this turn, which is the simplest non-trivial example of a learning loop without gradient updates.

The strength of this family is **boundedness** — the agent never blows past the context window because the runtime enforces it. The weakness is that retrieval quality is gated by the LLM's ability to write good search queries against its own archive, which degrades on noisy histories.

### 3.2 Extract-and-retrieve: Mem0

Mem0 (https://github.com/mem0ai/mem0; paper https://arxiv.org/abs/2504.19413) attacks a narrower problem: **personal assistant memory across sessions**. Its pipeline is two-stage. First, an *extraction* model reads each turn and emits zero or more atomic "memories" — short factual statements like *"User prefers dark roast coffee"* or *"User's dog Bruno is a 3-year-old beagle."* Second, those memories are embedded, deduplicated against existing entries (with explicit ADD/UPDATE/DELETE/NO-OP decisions), and stored in a vector DB. At query time, the relevant top-k are stitched into the prompt.

The reported headline number is that on the LoCoMo benchmark Mem0 matches or beats a full-context baseline using roughly an order of magnitude fewer tokens (https://arxiv.org/abs/2504.19413). The mechanism is straightforward: 600 turns of chat have huge redundancy, and once you've extracted the ~50 facts that actually matter, you don't need the rest. The cost is that any fact the extractor misses is lost forever, and contradictions must be resolved at extraction time rather than at recall time.

For students, Mem0 is the easiest of the four families to reproduce in an afternoon: an extraction prompt, a vector DB, and a retrieval prompt is the entire system.

### 3.3 Temporal knowledge graphs: Zep / Graphiti

Zep's Graphiti engine (https://github.com/getzep/graphiti; paper https://arxiv.org/abs/2501.13956) argues that the missing primitive in extract-and-retrieve systems is **time**. A user who said in January "I work at TCS" and in March "I just joined Infosys" creates a contradiction that vector retrieval cannot resolve — both embeddings will return high similarity to "where does the user work?". Graphiti models facts as edges in a knowledge graph with `valid_from` / `valid_to` timestamps; when a new fact arrives that contradicts an existing edge, the old edge is *invalidated* (not deleted), and queries default to "what is true now."

The Zep paper reports state-of-the-art on the Deep Memory Retrieval benchmark and strong LongMemEval performance, attributing the gain primarily to temporal reasoning rather than retrieval quality (https://arxiv.org/abs/2501.13956). This family is the most engineering-heavy: you need an entity-resolution step, a graph store (typically Neo4j), and a way to translate natural-language queries into traversals. The local-DB hit DecisionGraph (https://github.com/hieuchaydi/DecisionGraph) is a nice domain-specific instance of the same idea — engineering decisions captured as a graph with provenance back to GitHub/Slack/Jira, queried via MCP for "why did we do X?" questions.

### 3.4 Cognitive-inspired hierarchies & reflection

The Generative Agents paper (Park et al., 2023; https://arxiv.org/abs/2304.03442) is the canonical reference for a three-tier cognitive memory: an **observation stream** (raw episodic events), a **reflection layer** (the agent periodically asks itself "what high-level conclusions can I draw from the last N observations?"), and a **plan layer**. Each memory has importance, recency, and relevance scores that combine to determine retrieval. The Smallville simulation it introduced is dated, but the *reflect → summarize → re-store* loop has become standard practice in 2025 agent frameworks.

This is also the family where **procedural memory** is most explicit. Anthropic's Skills system (https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) and Google's Antigravity Skills (https://antigravity.google/docs/skills) can be read as "procedural memory as a service": reusable, version-controlled behavioral packs that the agent loads on demand instead of re-deriving them every session. Frameworks like voltagent (https://officialskills.sh/voltagent/skills/voltagent-core-reference) and the multi-agent skill collection in coco (https://github.com/rkz91/coco) push the idea further, treating skills as first-class memory units that compose with episodic and semantic stores.

### 3.5 Benchmarks: how do we know any of this works?

Two benchmarks have become the de facto evaluation surface:

- **LongMemEval** (https://arxiv.org/abs/2410.10813) — 500 questions over very long chat histories, designed to test five distinct skills: information extraction, multi-session reasoning, knowledge updates, temporal reasoning, and abstention. The headline finding is that even strong commercial assistants degrade by 30%+ as history length grows, and that *temporal reasoning* and *knowledge updates* are the hardest categories — which is precisely what motivates the Zep-style temporal-graph approach.
- **LoCoMo** (https://arxiv.org/abs/2402.17753) — 10 conversations of ~600 turns each, with QA, event-summarization, and multimodal-reference questions. Mem0's evaluation against this benchmark (https://arxiv.org/abs/2504.19413) is the most-cited 2025 head-to-head between memory architectures.

The honest summary: there is no single winner. Mem0 wins on token efficiency, Zep wins on temporal questions, MemGPT/Letta wins on bounded-context guarantees, and reflection-based systems win on questions that require synthesis the user never explicitly stated.

---

## 4. Connections to Anirudh's Projects

> I do not have memory entries describing PitchBot, ARIA, or smart_glasses, so the mapping below is inferred from the project names. Correct me where I'm wrong.

The strongest fit is **smart_glasses + ARIA**, treated as a single wearable assistant stack.

A smart-glasses assistant has the worst-case version of the agent-memory problem. The input is a continuous, mostly-uninteresting sensory stream (audio + occasional vision) at very high token-per-hour rates. The user expects the device to (a) remember conversational threads across days, (b) recognize people and places it has seen before, (c) not ask the same question twice, and (d) do all this on a power and bandwidth budget. None of the four architectures above solves this on their own — but a *layered* solution falls out naturally:

- **Sensor → episodic buffer.** Raw transcripts and frame embeddings go into a short-term ring buffer, summarized hourly. This is the MemGPT/Letta paged-context idea (https://github.com/letta-ai/letta), adapted to a wearable.
- **Episodic → semantic facts.** A Mem0-style extractor (https://github.com/mem0ai/mem0) runs on the summaries and pulls out durable facts ("Anirudh meets Prof. Rao every Tuesday at 4pm in Block A").
- **Semantic → temporal graph.** Person/place/event entities resolve into a Graphiti-style temporal KG (https://github.com/getzep/graphiti) so the glasses can answer "when did I last see X?" without confusing it with "when was I last *with* X?"
- **Procedural skills.** Domain behaviors ("how to take meeting notes," "how to summarize a lecture") live as loadable skills in the style of the Anthropic/Antigravity skill registries (https://antigravity.google/docs/skills).

PitchBot (presumed: a sales/pitch coaching agent) is a weaker but cleaner fit — its memory needs are dominated by *user preferences* and *prior pitch history*, which is exactly Mem0's sweet spot. If the goal is a tractable demo, PitchBot is the easier target; if the goal is to motivate the *full* taxonomy in a 30-minute talk, smart_glasses is the better narrative spine because it forces you to use all four families.

---

## 5. Recommended Demo Concept

**"30-line memory" — a live, side-by-side comparison of three memory strategies on the same conversation.**

Build a tiny Python script (~30 lines per strategy, ~100 lines total) that:

1. Replays a fixed 20-turn scripted conversation between "user" and "assistant" — designed so that turn 19 contradicts turn 4, and turn 20 asks a question that requires synthesizing turns 7, 12, and 17.
2. Runs three memory backends in parallel against the same script:
   - **No memory** — raw last-N-turns prompt.
   - **Mem0-style extract-and-retrieve** — call Claude to extract facts after each turn, store in a local SQLite + sentence-transformers vector index, retrieve top-3 at query time. (Reference: https://github.com/mem0ai/mem0)
   - **Tiny temporal graph** — store each extracted fact with a `valid_from` timestamp and a "supersedes" edge; on conflict, mark the older edge invalid. (Reference: https://github.com/getzep/graphiti)
3. Prints all three answers to turn 20 side by side, then a one-line diff highlighting which strategies got the contradiction right.

Why this is the right demo for a 30-minute JNTU talk:
- **Live, deterministic, runnable in <60 seconds** on a laptop with one Anthropic API key.
- **Failure modes are visible to the audience** — the no-memory baseline confidently states a stale fact, the vector backend can't decide, the temporal graph gets it right. That single screenshot is more persuasive than any benchmark table.
- **Scaffolds the rest of the talk.** After the demo lands, you can spend the remaining 20 minutes on "and here is what production systems add on top of this 100-line skeleton" — Letta's sleep-time compute, Mem0's UPDATE/DELETE decisions, Zep's entity resolution.
- **It's a real artifact students can fork.** Ship it as a single GitHub repo with a `make demo` target.

Stretch goal if you have an extra week: add a fourth backend that mimics MemGPT's `core_memory_append` tool call, so the audience sees the OS-paging idea in action too. Use Letta's open-source server (https://github.com/letta-ai/letta) if you don't want to roll your own.

---

## 6. Open Questions Worth Raising in Q&A

1. **Is "memory" actually the right abstraction, or just the friendliest one?** Many production "memory" systems are really retrieval pipelines with marketing. Where does retrieval end and memory begin? (Hint: the answer involves *write policy* and *forgetting*, not just *read policy*.)

2. **What happens when the agent's memory is wrong?** None of the four families ship with a robust "the user just told me my old fact was wrong — propagate the correction" mechanism. Zep's invalidation is the closest. How would you design the UX for a user-driven correction?

3. **Whose memory is it?** If a smart-glasses agent stores facts about a third party who has not consented, what is the right policy? This is a rare case where the technical design (TTLs, scoping by speaker, on-device vs. cloud) maps directly to a privacy-law question.

4. **Does memory replace fine-tuning, or vice versa?** An agent that has accumulated 6 months of correctly-extracted facts about a user is, in some sense, a fine-tuned model of that user — but cheaper and editable. When is the crossover point?

5. **Why has nobody solved procedural memory well?** Anthropic Skills (https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) and the Antigravity skill collection (https://antigravity.google/docs/skills) are useful but manually authored. The dream is an agent that *learns* a new skill from a few demonstrations and stores it as a reusable artifact. We are not there yet — why?

6. **Will long-context models (10M+ tokens) make all of this obsolete?** Probably not, for two reasons: (a) cost grows roughly linearly with context, so paging is still economically rational, and (b) attention quality degrades on very long contexts even when the model technically supports them. LongMemEval (https://arxiv.org/abs/2410.10813) is the right artifact to point at when this question comes up.

---

*End of dossier. The talk is structured to land Section 5's demo around the 10-minute mark and use the remaining 20 minutes to unpack Sections 2-3 with the demo as the running example.*