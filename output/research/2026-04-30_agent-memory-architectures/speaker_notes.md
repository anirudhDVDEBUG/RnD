# Speaker notes — Agent Memory Architectures

## Slide 2: 1. Executive Summary
LLMs are stateless function calls. An "agent" is the software wrapper that pretends otherwise — and that pretense is what we call **memory**. Over the last 24 months the field has converged on a fairly clear picture: a single context window cannot be the whole answer, and every serious framework now layers some form of *external* memory on top of the model. The interesting disagreement is *how* to organize that external store.

Four design families dominate as of April 2026:

1. **Tiered / OS-style memory** — treat context as RAM and external stores as disk, paging facts in and out. MemGPT (https://arxiv.org/abs/2310.08560) introduced this metaphor; its production successor is the Letta runtime (https://github.com/letta-ai/letta).
2. **Extract-and-retrieve memory** — distill conversation turns into atomic "memories," embed them, and retrieve top-k by similarity. Mem0 (https://github.com/mem0ai/mem0, paper https://arxiv.org/abs/2504.19413) is the canonical example.
3. **Temporal knowledge graphs** — store facts as time-stamped triples in a graph so the agent can reason about *when* something was true, not just *whether*. Zep/Graphiti (https://github.com/getzep/graphiti, https://arxi

## Slide 3: 2. Landscape Map — Taxonomy of Approaches
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
                  └────────────────┴──────────────────────┴────────────

## Slide 4: 3. Deep-Dives


## Slide 5: 3.1 Tiered, OS-style memory: MemGPT → Letta
MemGPT (Packer et al., 2023; https://arxiv.org/abs/2310.08560) is the architectural ancestor of every "agent has a hard drive" design. Its central move is to treat the model's context window as **main memory** and to expose tool calls — `core_memory_append`, `archival_memory_search`, `recall_memory_search` — that the LLM itself uses to page facts in and out. The OS analogy is not just rhetorical: there is a fixed-size "core memory" (system-prompt-like, always in context), a recall buffer (recent messages), and an unbounded archival store (vector-indexed). The model decides what to evict.

Letta (https://github.com/letta-ai/letta) is the production-grade rewrite of MemGPT by the same team. It generalizes the idea into a **stateful agent server** with sleep-time compute (background memory consolidation while the agent is idle) and a typed schema for memory blocks. The pedagogically interesting bit for students is the *self-editing* property: the agent's behavior next turn depends on edits it made to its own core-memory block this turn, which is the simplest non-trivial example of a learning loop without gradient updates.

The strength of this family is **boundedness** — the agent nev

## Slide 6: 3.2 Extract-and-retrieve: Mem0
Mem0 (https://github.com/mem0ai/mem0; paper https://arxiv.org/abs/2504.19413) attacks a narrower problem: **personal assistant memory across sessions**. Its pipeline is two-stage. First, an *extraction* model reads each turn and emits zero or more atomic "memories" — short factual statements like *"User prefers dark roast coffee"* or *"User's dog Bruno is a 3-year-old beagle."* Second, those memories are embedded, deduplicated against existing entries (with explicit ADD/UPDATE/DELETE/NO-OP decisions), and stored in a vector DB. At query time, the relevant top-k are stitched into the prompt.

The reported headline number is that on the LoCoMo benchmark Mem0 matches or beats a full-context baseline using roughly an order of magnitude fewer tokens (https://arxiv.org/abs/2504.19413). The mechanism is straightforward: 600 turns of chat have huge redundancy, and once you've extracted the ~50 facts that actually matter, you don't need the rest. The cost is that any fact the extractor misses is lost forever, and contradictions must be resolved at extraction time rather than at recall time.

For students, Mem0 is the easiest of the four families to reproduce in an afternoon: an extraction p

## Slide 7: 3.3 Temporal knowledge graphs: Zep / Graphiti
Zep's Graphiti engine (https://github.com/getzep/graphiti; paper https://arxiv.org/abs/2501.13956) argues that the missing primitive in extract-and-retrieve systems is **time**. A user who said in January "I work at TCS" and in March "I just joined Infosys" creates a contradiction that vector retrieval cannot resolve — both embeddings will return high similarity to "where does the user work?". Graphiti models facts as edges in a knowledge graph with `valid_from` / `valid_to` timestamps; when a new fact arrives that contradicts an existing edge, the old edge is *invalidated* (not deleted), and queries default to "what is true now."

The Zep paper reports state-of-the-art on the Deep Memory Retrieval benchmark and strong LongMemEval performance, attributing the gain primarily to temporal reasoning rather than retrieval quality (https://arxiv.org/abs/2501.13956). This family is the most engineering-heavy: you need an entity-resolution step, a graph store (typically Neo4j), and a way to translate natural-language queries into traversals. The local-DB hit DecisionGraph (https://github.com/hieuchaydi/DecisionGraph) is a nice domain-specific instance of the same idea — engineering decisio

## Slide 8: 3.4 Cognitive-inspired hierarchies & reflection
The Generative Agents paper (Park et al., 2023; https://arxiv.org/abs/2304.03442) is the canonical reference for a three-tier cognitive memory: an **observation stream** (raw episodic events), a **reflection layer** (the agent periodically asks itself "what high-level conclusions can I draw from the last N observations?"), and a **plan layer**. Each memory has importance, recency, and relevance scores that combine to determine retrieval. The Smallville simulation it introduced is dated, but the *reflect → summarize → re-store* loop has become standard practice in 2025 agent frameworks.

This is also the family where **procedural memory** is most explicit. Anthropic's Skills system (https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) and Google's Antigravity Skills (https://antigravity.google/docs/skills) can be read as "procedural memory as a service": reusable, version-controlled behavioral packs that the agent loads on demand instead of re-deriving them every session. Frameworks like voltagent (https://officialskills.sh/voltagent/skills/voltagent-core-reference) and the multi-agent skill collection in coco (https://github.com/rkz91/coco) push the idea fur

## Slide 9: 3.5 Benchmarks: how do we know any of this works?
Two benchmarks have become the de facto evaluation surface:

- **LongMemEval** (https://arxiv.org/abs/2410.10813) — 500 questions over very long chat histories, designed to test five distinct skills: information extraction, multi-session reasoning, knowledge updates, temporal reasoning, and abstention. The headline finding is that even strong commercial assistants degrade by 30%+ as history length grows, and that *temporal reasoning* and *knowledge updates* are the hardest categories — which is precisely what motivates the Zep-style temporal-graph approach.
- **LoCoMo** (https://arxiv.org/abs/2402.17753) — 10 conversations of ~600 turns each, with QA, event-summarization, and multimodal-reference questions. Mem0's evaluation against this benchmark (https://arxiv.org/abs/2504.19413) is the most-cited 2025 head-to-head between memory architectures.

The honest summary: there is no single winner. Mem0 wins on token efficiency, Zep wins on temporal questions, MemGPT/Letta wins on bounded-context guarantees, and reflection-based systems win on questions that require synthesis the user never explicitly stated.

---

## Slide 10: 4. Connections to Anirudh's Projects
> I do not have memory entries describing PitchBot, ARIA, or smart_glasses, so the mapping below is inferred from the project names. Correct me where I'm wrong.

The strongest fit is **smart_glasses + ARIA**, treated as a single wearable assistant stack.

A smart-glasses assistant has the worst-case version of the agent-memory problem. The input is a continuous, mostly-uninteresting sensory stream (audio + occasional vision) at very high token-per-hour rates. The user expects the device to (a) remember conversational threads across days, (b) recognize people and places it has seen before, (c) not ask the same question twice, and (d) do all this on a power and bandwidth budget. None of the four architectures above solves this on their own — but a *layered* solution falls out naturally:

- **Sensor → episodic buffer.** Raw transcripts and frame embeddings go into a short-term ring buffer, summarized hourly. This is the MemGPT/Letta paged-context idea (https://github.com/letta-ai/letta), adapted to a wearable.
- **Episodic → semantic facts.** A Mem0-style extractor (https://github.com/mem0ai/mem0) runs on the summaries and pulls out durable facts ("Anirudh meets Prof. Rao every Tuesda

## Slide 11: 5. Recommended Demo Concept
**"30-line memory" — a live, side-by-side comparison of three memory strategies on the same conversation.**

Build a tiny Python script (~30 lines per strategy, ~100 lines total) that:

1. Replays a fixed 20-turn scripted conversation between "user" and "assistant" — designed so that turn 19 contradicts turn 4, and turn 20 asks a question that requires synthesizing turns 7, 12, and 17.
2. Runs three memory backends in parallel against the same script:
   - **No memory** — raw last-N-turns prompt.
   - **Mem0-style extract-and-retrieve** — call Claude to extract facts after each turn, store in a local SQLite + sentence-transformers vector index, retrieve top-3 at query time. (Reference: https://github.com/mem0ai/mem0)
   - **Tiny temporal graph** — store each extracted fact with a `valid_from` timestamp and a "supersedes" edge; on conflict, mark the older edge invalid. (Reference: https://github.com/getzep/graphiti)
3. Prints all three answers to turn 20 side by side, then a one-line diff highlighting which strategies got the contradiction right.

Why this is the right demo for a 30-minute JNTU talk:
- **Live, deterministic, runnable in <60 seconds** on a laptop with one Anthropic A

## Slide 12: 6. Open Questions Worth Raising in Q&A
1. **Is "memory" actually the right abstraction, or just the friendliest one?** Many production "memory" systems are really retrieval pipelines with marketing. Where does retrieval end and memory begin? (Hint: the answer involves *write policy* and *forgetting*, not just *read policy*.)

2. **What happens when the agent's memory is wrong?** None of the four families ship with a robust "the user just told me my old fact was wrong — propagate the correction" mechanism. Zep's invalidation is the closest. How would you design the UX for a user-driven correction?

3. **Whose memory is it?** If a smart-glasses agent stores facts about a third party who has not consented, what is the right policy? This is a rare case where the technical design (TTLs, scoping by speaker, on-device vs. cloud) maps directly to a privacy-law question.

4. **Does memory replace fine-tuning, or vice versa?** An agent that has accumulated 6 months of correctly-extracted facts about a user is, in some sense, a fine-tuned model of that user — but cheaper and editable. When is the crossover point?

5. **Why has nobody solved procedural memory well?** Anthropic Skills (https://github.com/anthropics/skills/tree/main/
