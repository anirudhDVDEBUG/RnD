---
name: redis_development
description: |
  Guide for developing applications with Redis, including data modeling, querying, Redis Stack modules (JSON, Search, TimeSeries, Probabilistic), and best practices.
  TRIGGER: when the user asks about Redis data modeling, Redis queries, Redis Stack, RedisJSON, RediSearch, Redis commands, Redis client libraries, or building applications that use Redis as a database or cache.
---

# Redis Development Skill

This skill provides guidance for developing applications with Redis, covering data modeling, querying patterns, Redis Stack modules, and best practices.

## When to use

- "Help me design a Redis data model for my application"
- "How do I use RediSearch to query JSON documents?"
- "Set up Redis as a vector database for semantic search"
- "What Redis data structure should I use for this use case?"
- "Help me write Redis commands or use a Redis client library"

## How to use

### 1. Understand Redis Data Structures

Redis provides core data structures. Choose the right one for your use case:

- **Strings** — Simple key-value pairs, counters, cached serialized objects
- **Hashes** — Object-like storage with individual field access (e.g., user profiles)
- **Lists** — Ordered collections, queues, activity feeds
- **Sets** — Unique collections, tags, relationships
- **Sorted Sets** — Ranked data, leaderboards, time-based indexes
- **Streams** — Event logs, message queues, activity streams

### 2. Use Redis Stack Modules

Redis Stack extends Redis with powerful modules:

- **RedisJSON** — Store, query, and manipulate JSON documents natively
  ```redis
  JSON.SET user:1 $ '{"name":"Alice","age":30,"email":"alice@example.com"}'
  JSON.GET user:1 $.name
  ```

- **RediSearch** — Full-text search and secondary indexing
  ```redis
  FT.CREATE idx:users ON JSON PREFIX 1 user: SCHEMA $.name AS name TEXT $.age AS age NUMERIC
  FT.SEARCH idx:users "@name:Alice"
  ```

- **RedisTimeSeries** — Time-series data ingestion and querying
  ```redis
  TS.CREATE sensor:temp RETENTION 86400000 LABELS type temperature
  TS.ADD sensor:temp * 23.5
  TS.RANGE sensor:temp - + AGGREGATION avg 3600000
  ```

- **Redis Probabilistic** — Bloom filters, Count-Min Sketch, Top-K, HyperLogLog
  ```redis
  BF.ADD seen_urls "https://example.com"
  BF.EXISTS seen_urls "https://example.com"
  ```

### 3. Vector Search (AI/ML Use Cases)

Redis supports vector similarity search for RAG, recommendation engines, and semantic search:

```redis
FT.CREATE idx:docs ON HASH PREFIX 1 doc: SCHEMA
  content TEXT
  embedding VECTOR FLAT 6 TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE

FT.SEARCH idx:docs "*=>[KNN 5 @embedding $query_vec AS score]"
  PARAMS 2 query_vec "<binary_vector>" SORTBY score DIALECT 2
```

### 4. Client Library Patterns

Use official Redis client libraries:

**Python (redis-py):**
```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Basic operations
r.set('key', 'value')
r.hset('user:1', mapping={'name': 'Alice', 'age': 30})

# JSON
from redis.commands.json.path import Path
r.json().set('user:1', Path.root_path(), {"name": "Alice", "age": 30})

# Search
from redis.commands.search.query import Query
results = r.ft('idx:users').search(Query('@name:Alice'))
```

**Node.js (node-redis):**
```javascript
import { createClient, SchemaFieldTypes } from 'redis';

const client = createClient();
await client.connect();

// JSON
await client.json.set('user:1', '$', { name: 'Alice', age: 30 });

// Search
await client.ft.create('idx:users', {
  '$.name': { type: SchemaFieldTypes.TEXT, AS: 'name' },
  '$.age': { type: SchemaFieldTypes.NUMERIC, AS: 'age' }
}, { ON: 'JSON', PREFIX: 'user:' });

const results = await client.ft.search('idx:users', '@name:Alice');
```

### 5. Best Practices

- **Key naming**: Use colon-separated namespaces (e.g., `user:1:profile`, `order:2024:items`)
- **Expiration**: Set TTL on cache keys with `EXPIRE` or `SET key value EX seconds`
- **Pipelining**: Batch multiple commands to reduce round trips
- **Transactions**: Use `MULTI`/`EXEC` for atomic operations or Lua scripts for complex logic
- **Memory**: Monitor with `INFO memory`; use appropriate data structures to minimize overhead
- **Persistence**: Configure RDB snapshots and/or AOF for durability requirements
- **Connection pooling**: Always use connection pools in production applications

### 6. Common Patterns

- **Caching**: SET/GET with TTL for database query caching
- **Session storage**: Hashes with expiration for user sessions
- **Rate limiting**: INCR + EXPIRE or sliding window with Sorted Sets
- **Pub/Sub**: Real-time messaging between services
- **Distributed locks**: SET with NX and PX flags (Redlock algorithm)
- **Leaderboards**: Sorted Sets with ZADD/ZRANGE

## References

- Source: [redis/agent-skills — redis-development](https://github.com/redis/agent-skills/tree/main/skills/redis-development)
- [Redis Documentation](https://redis.io/docs/)
- [Redis Stack](https://redis.io/docs/stack/)
- [Redis Clients](https://redis.io/docs/clients/)
