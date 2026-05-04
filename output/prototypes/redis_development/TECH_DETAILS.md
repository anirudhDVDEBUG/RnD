# Technical Details

## What this is

`redis_development` is a **Claude Code skill** — a markdown file dropped into `~/.claude/skills/` that gives Claude deep knowledge of Redis application development. When triggered, Claude can:

- Recommend the right Redis data structure for a use case (strings vs hashes vs sorted sets vs streams)
- Generate working client code in Python (`redis-py`) or Node.js (`node-redis`)
- Design Redis Stack queries: RedisJSON paths, RediSearch full-text and vector indexes, TimeSeries aggregations, Bloom filter sizing
- Apply production patterns: cache-aside + TTL, sliding-window rate limiting, distributed locks (SET NX PX / Redlock), pipelining, pub/sub

The companion `redis_demo.py` script demonstrates 8 of these patterns live using `fakeredis` — no server or API keys required.

## Architecture

```
SKILL.md              Claude skill definition (trigger rules + reference material)
redis_demo.py         Standalone demo: 8 patterns against fakeredis
requirements.txt      fakeredis>=2.21.0
run.sh                One-command setup + run
```

**Data flow (skill):** User prompt -> Claude detects Redis-related intent -> skill context injected -> Claude generates Redis commands / client code informed by the skill's best-practice reference.

**Data flow (demo):** `run.sh` -> venv + pip install -> `redis_demo.py` -> `fakeredis.FakeRedis` (in-memory, no I/O) -> stdout.

### Key dependencies

| Dependency | Role |
|---|---|
| `fakeredis` | In-process Redis emulator for demo; supports core commands, pipelines, transactions |
| `redis-py` (production) | Official Python client referenced in skill guidance |
| `node-redis` (production) | Official Node.js client referenced in skill guidance |

No model calls, no API keys, no network access required for the demo.

## Limitations

- **fakeredis does not support Redis Stack modules.** The demo prints JSON/Search/TimeSeries/Bloom commands as reference text rather than executing them. For live module testing, install `redis-stack-server` via Docker: `docker run -p 6379:6379 redis/redis-stack-server:latest`.
- The skill is **read-only guidance** — it does not connect to or manage a Redis instance. Claude generates code; the user runs it.
- No coverage of Redis Cluster sharding, Sentinel HA, or Redis Streams consumers in the current skill text.
- Vector search examples use placeholder binary blobs; real embeddings require an embedding model (OpenAI, Cohere, etc.).

## Why this matters for Claude-driven products

| Use case | Redis role |
|---|---|
| **Lead-gen / marketing** | Session storage, form-submission dedup (Bloom), real-time visitor counters |
| **Ad creatives** | Cache rendered assets with TTL, rate-limit API calls to creative generation models |
| **Agent factories** | Shared state between agents (hashes), task queues (lists/streams), distributed locks for idempotent tool calls |
| **Voice AI** | Sub-millisecond context lookup (JSON + Search), conversation history with TTL, rate limiting per caller |
| **RAG pipelines** | Vector similarity search (FT.SEARCH KNN), document chunk caching, embedding dedup |

Redis is the most common "fast layer" in production AI stacks. A Claude skill that generates correct Redis code on first ask eliminates round-trips to docs and reduces integration time from hours to minutes.
