# Redis Development Skill — Demo

A Claude Code skill that teaches Claude how to design Redis data models, pick the right data structures, use Redis Stack modules (JSON, Search, TimeSeries, Bloom), and write production-grade client code in Python and Node.js.

**Headline result:** Ask Claude _"design a Redis data model for a real-time leaderboard with player profiles"_ and it produces working `redis-py` code with sorted sets, hashes, pipelining, and TTL — no Redis docs tab required.

```
bash run.sh   # 8 live pattern demos, no Redis server needed
```

- [HOW_TO_USE.md](HOW_TO_USE.md) — install the skill, trigger phrases, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — what the skill covers, architecture, limitations
