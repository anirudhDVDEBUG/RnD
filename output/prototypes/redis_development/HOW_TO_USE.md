# How to Use

## Option A: Install as a Claude Code Skill

### 1. Copy the skill folder

```bash
mkdir -p ~/.claude/skills/redis_development
cp SKILL.md ~/.claude/skills/redis_development/SKILL.md
```

### 2. Verify it loaded

Open Claude Code and type any trigger phrase (see below). Claude will use the skill automatically — no config file edits needed.

### Trigger phrases

Any of these activates the skill:

- "Help me design a Redis data model for …"
- "How do I use RediSearch to query JSON documents?"
- "Set up Redis as a vector database"
- "What Redis data structure should I use for …?"
- "Write a Redis pipeline in Python"
- Any mention of RedisJSON, RediSearch, RedisTimeSeries, Bloom filters + Redis

## Option B: Run the standalone demo

### Prerequisites

- Python 3.9+
- No Redis server required (uses `fakeredis`)

### Install & run

```bash
git clone <this-repo> && cd redis_development
pip install -r requirements.txt   # just fakeredis
python3 redis_demo.py
```

Or all-in-one:

```bash
bash run.sh
```

### First 60 seconds

**Input:**
```bash
bash run.sh
```

**Output (abbreviated):**
```
============================================================
  Redis Development Patterns Demo
  Using fakeredis (no server required)
============================================================

============================================================
  1. Core Data Structures
============================================================

--- Strings (key-value) ---
  max_retries  = 3
  page_views   = 3

--- Hashes (object storage) ---
  user:1001 = {"name": "Alice Chen", "email": "alice@example.com", ...}

--- Sorted Sets (leaderboard) ---
  Top 3 players:
    #1  charlie     5100 pts
    #2  diana       4800 pts
    #3  alice       4500 pts

============================================================
  4. Rate Limiting (Sliding Window)
============================================================
  Simulating 7 requests (limit=5/60s):
    Request #1: ALLOWED
    ...
    Request #6: BLOCKED

============================================================
  8. Pipelining (Batch Operations)
============================================================
  1000 SET commands:
    Without pipeline: 12.3ms
    With pipeline:    3.1ms
    Speedup:          4.0x
```

All 8 patterns run in < 2 seconds with zero network calls.
