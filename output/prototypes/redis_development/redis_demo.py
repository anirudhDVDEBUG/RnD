#!/usr/bin/env python3
"""
Redis Development Patterns Demo
Demonstrates core Redis data structures, Redis Stack modules, and common
application patterns using fakeredis (no real Redis server needed).
"""

import json
import time
import hashlib
from datetime import datetime

try:
    import fakeredis
except ImportError:
    print("ERROR: fakeredis not installed. Run: pip install fakeredis")
    raise SystemExit(1)


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_basic_data_structures(r: fakeredis.FakeRedis):
    """Demonstrate core Redis data structures."""
    section("1. Core Data Structures")

    # Strings
    print("--- Strings (key-value) ---")
    r.set("app:config:max_retries", "3")
    r.set("app:config:timeout_ms", "5000")
    r.incr("stats:page_views")
    r.incr("stats:page_views")
    r.incr("stats:page_views")
    print(f"  max_retries  = {r.get('app:config:max_retries')}")
    print(f"  timeout_ms   = {r.get('app:config:timeout_ms')}")
    print(f"  page_views   = {r.get('stats:page_views')}")

    # Hashes
    print("\n--- Hashes (object storage) ---")
    r.hset("user:1001", mapping={
        "name": "Alice Chen",
        "email": "alice@example.com",
        "role": "engineer",
        "login_count": "0",
    })
    r.hincrby("user:1001", "login_count", 1)
    user = r.hgetall("user:1001")
    print(f"  user:1001 = {json.dumps(user, indent=4)}")

    # Lists
    print("\n--- Lists (ordered queue) ---")
    for task in ["send_email", "resize_image", "generate_report"]:
        r.rpush("queue:tasks", task)
    next_task = r.lpop("queue:tasks")
    remaining = r.lrange("queue:tasks", 0, -1)
    print(f"  Dequeued: {next_task}")
    print(f"  Remaining: {remaining}")

    # Sets
    print("\n--- Sets (unique collections) ---")
    r.sadd("user:1001:tags", "python", "redis", "docker", "python")  # dup ignored
    r.sadd("user:1002:tags", "redis", "kubernetes", "go")
    common = r.sinter("user:1001:tags", "user:1002:tags")
    print(f"  user:1001 tags: {r.smembers('user:1001:tags')}")
    print(f"  user:1002 tags: {r.smembers('user:1002:tags')}")
    print(f"  Common tags:    {common}")

    # Sorted Sets
    print("\n--- Sorted Sets (leaderboard) ---")
    r.zadd("leaderboard:game1", {"alice": 4500, "bob": 3200, "charlie": 5100, "diana": 4800})
    top3 = r.zrevrange("leaderboard:game1", 0, 2, withscores=True)
    print("  Top 3 players:")
    for rank, (player, score) in enumerate(top3, 1):
        print(f"    #{rank}  {player:10s}  {int(score)} pts")


def demo_caching_pattern(r: fakeredis.FakeRedis):
    """Demonstrate cache-aside pattern with TTL."""
    section("2. Caching Pattern (Cache-Aside + TTL)")

    def get_user_profile(user_id: str) -> dict:
        cache_key = f"cache:user:{user_id}"
        cached = r.get(cache_key)
        if cached:
            print(f"  [HIT]  cache key={cache_key}")
            return json.loads(cached)
        # Simulate DB fetch
        print(f"  [MISS] cache key={cache_key} -> fetching from DB...")
        profile = {"id": user_id, "name": "Alice Chen", "email": "alice@example.com"}
        r.set(cache_key, json.dumps(profile), ex=300)  # TTL 5 min
        ttl = r.ttl(cache_key)
        print(f"  [SET]  cached with TTL={ttl}s")
        return profile

    profile1 = get_user_profile("1001")
    profile2 = get_user_profile("1001")  # should hit cache
    print(f"  Result: {profile1}")


def demo_session_store(r: fakeredis.FakeRedis):
    """Demonstrate session storage with hashes."""
    section("3. Session Storage")

    session_id = hashlib.sha256(b"user1001-session").hexdigest()[:32]
    session_key = f"session:{session_id}"

    r.hset(session_key, mapping={
        "user_id": "1001",
        "username": "alice",
        "ip": "192.168.1.42",
        "created_at": datetime.now().isoformat(),
    })
    r.expire(session_key, 1800)  # 30 min TTL

    session = r.hgetall(session_key)
    ttl = r.ttl(session_key)
    print(f"  Session ID: {session_id}")
    print(f"  Data:       {json.dumps(session, indent=4)}")
    print(f"  TTL:        {ttl}s")


def demo_rate_limiter(r: fakeredis.FakeRedis):
    """Demonstrate sliding-window rate limiter with sorted sets."""
    section("4. Rate Limiting (Sliding Window)")

    def check_rate_limit(user_id: str, max_requests: int = 5, window_sec: int = 60) -> bool:
        key = f"ratelimit:{user_id}"
        now = time.time()
        pipe = r.pipeline()
        pipe.zremrangebyscore(key, 0, now - window_sec)  # prune old entries
        pipe.zadd(key, {f"{now}-{id(pipe)}": now})
        pipe.zcard(key)
        pipe.expire(key, window_sec)
        results = pipe.execute()
        count = results[2]
        return count <= max_requests

    print(f"  Simulating 7 requests (limit=5/60s):")
    for i in range(1, 8):
        allowed = check_rate_limit("user:1001", max_requests=5)
        status = "ALLOWED" if allowed else "BLOCKED"
        print(f"    Request #{i}: {status}")


def demo_distributed_lock(r: fakeredis.FakeRedis):
    """Demonstrate distributed lock with SET NX PX."""
    section("5. Distributed Lock (SET NX PX)")

    lock_key = "lock:order:process"
    lock_value = "worker-abc-123"

    # Acquire
    acquired = r.set(lock_key, lock_value, nx=True, px=10000)
    print(f"  Acquire lock: {'SUCCESS' if acquired else 'FAILED'}")

    # Try again (should fail - already held)
    acquired2 = r.set(lock_key, lock_value, nx=True, px=10000)
    print(f"  Re-acquire:   {'SUCCESS' if acquired2 else 'FAILED (lock held)'}")

    # Release (only if we hold it)
    current = r.get(lock_key)
    if current == lock_value:
        r.delete(lock_key)
        print(f"  Released lock (value matched)")

    # Now acquire again
    acquired3 = r.set(lock_key, lock_value, nx=True, px=10000)
    print(f"  Post-release:  {'SUCCESS' if acquired3 else 'FAILED'}")


def demo_pub_sub_simulation(r: fakeredis.FakeRedis):
    """Simulate pub/sub messaging pattern."""
    section("6. Pub/Sub Messaging (Simulated)")

    # Use a list-based queue to simulate since fakeredis pub/sub is limited
    channel = "notifications:user:1001"

    messages = [
        {"type": "order_shipped", "order_id": "ORD-9921", "ts": datetime.now().isoformat()},
        {"type": "payment_received", "amount": 49.99, "ts": datetime.now().isoformat()},
        {"type": "review_request", "product": "Redis Handbook", "ts": datetime.now().isoformat()},
    ]

    print("  Publishing messages:")
    for msg in messages:
        r.rpush(channel, json.dumps(msg))
        print(f"    -> {msg['type']}")

    print("\n  Consuming messages:")
    while r.llen(channel) > 0:
        raw = r.lpop(channel)
        msg = json.loads(raw)
        print(f"    <- {msg['type']}: {json.dumps({k:v for k,v in msg.items() if k != 'type'})}")


def demo_redis_stack_commands():
    """Show Redis Stack commands (JSON, Search, TimeSeries) as reference."""
    section("7. Redis Stack Commands Reference")

    print("  These commands require Redis Stack (redis-stack-server).\n")

    examples = [
        ("RedisJSON", [
            "JSON.SET user:1 $ '{\"name\":\"Alice\",\"age\":30,\"skills\":[\"python\",\"redis\"]}'",
            "JSON.GET user:1 $.name",
            "JSON.NUMINCRBY user:1 $.age 1",
            "JSON.ARRAPPEND user:1 $.skills '\"docker\"'",
        ]),
        ("RediSearch", [
            "FT.CREATE idx:users ON JSON PREFIX 1 user: SCHEMA $.name AS name TEXT $.age AS age NUMERIC",
            "FT.SEARCH idx:users '@name:Alice'",
            "FT.SEARCH idx:users '@age:[25 35]'",
            "FT.AGGREGATE idx:users '*' GROUPBY 1 @age REDUCE COUNT 0 AS count",
        ]),
        ("Vector Search", [
            "FT.CREATE idx:docs ON HASH PREFIX 1 doc: SCHEMA content TEXT embedding VECTOR FLAT 6 TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE",
            "FT.SEARCH idx:docs '*=>[KNN 5 @embedding $vec AS score]' PARAMS 2 vec '<blob>' DIALECT 2",
        ]),
        ("RedisTimeSeries", [
            "TS.CREATE sensor:temp RETENTION 86400000 LABELS type temperature location office",
            "TS.ADD sensor:temp * 23.5",
            "TS.RANGE sensor:temp - + AGGREGATION avg 3600000",
            "TS.MRANGE - + FILTER type=temperature",
        ]),
        ("Probabilistic (Bloom Filter)", [
            "BF.RESERVE seen_urls 0.001 1000000",
            "BF.ADD seen_urls 'https://example.com/page1'",
            "BF.EXISTS seen_urls 'https://example.com/page1'  # -> 1",
            "BF.EXISTS seen_urls 'https://example.com/page2'  # -> 0",
        ]),
    ]

    for module, commands in examples:
        print(f"  [{module}]")
        for cmd in commands:
            print(f"    > {cmd}")
        print()


def demo_pipeline_performance(r: fakeredis.FakeRedis):
    """Demonstrate pipelining for batch operations."""
    section("8. Pipelining (Batch Operations)")

    n = 1000

    # Without pipeline
    start = time.time()
    for i in range(n):
        r.set(f"bench:nopipe:{i}", f"value-{i}")
    no_pipe_ms = (time.time() - start) * 1000

    # With pipeline
    start = time.time()
    pipe = r.pipeline()
    for i in range(n):
        pipe.set(f"bench:pipe:{i}", f"value-{i}")
    pipe.execute()
    pipe_ms = (time.time() - start) * 1000

    print(f"  {n} SET commands:")
    print(f"    Without pipeline: {no_pipe_ms:.1f}ms")
    print(f"    With pipeline:    {pipe_ms:.1f}ms")
    if no_pipe_ms > 0:
        print(f"    Speedup:          {no_pipe_ms/max(pipe_ms, 0.01):.1f}x")
    print()
    print("  Note: With a real Redis server over the network,")
    print("  pipelining reduces round-trip overhead dramatically.")


def main():
    print("=" * 60)
    print("  Redis Development Patterns Demo")
    print("  Using fakeredis (no server required)")
    print("=" * 60)

    r = fakeredis.FakeRedis(decode_responses=True)

    demo_basic_data_structures(r)
    demo_caching_pattern(r)
    demo_session_store(r)
    demo_rate_limiter(r)
    demo_distributed_lock(r)
    demo_pub_sub_simulation(r)
    demo_redis_stack_commands()
    demo_pipeline_performance(r)

    # Summary stats
    section("Summary")
    info = r.info()
    db_keys = r.dbsize()
    print(f"  Total keys in demo database: {db_keys}")
    print(f"  Redis version (fakeredis):   {info.get('redis_version', 'N/A')}")
    print()
    print("  Patterns demonstrated:")
    print("    1. Core data structures (String, Hash, List, Set, Sorted Set)")
    print("    2. Cache-aside with TTL")
    print("    3. Session storage")
    print("    4. Sliding-window rate limiting")
    print("    5. Distributed locking (SET NX PX)")
    print("    6. Pub/Sub messaging (list-based)")
    print("    7. Redis Stack commands reference")
    print("    8. Pipeline batching")
    print()
    print("  Next step: Install the Claude skill for AI-assisted Redis development.")
    print("  See HOW_TO_USE.md for details.")


if __name__ == "__main__":
    main()
