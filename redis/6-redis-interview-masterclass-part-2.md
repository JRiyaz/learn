# Redis Interview Masterclass - Part 2

## Introduction

In Part 1, we covered:

- Redis fundamentals
- Architecture
- Data structures
- Caching
- Transactions
- Pub/Sub
- Streams
- Persistence

This chapter focuses on **Senior Backend Engineer** interview topics.

Topics include:

- Redis internals
- Memory management
- Expiration algorithms
- Internal data structures
- Replication
- Sentinel
- Cluster
- Distributed Locks
- Redlock
- Performance tuning
- Debugging scenarios
- System design discussions
- Rapid-fire questions

______________________________________________________________________

# Redis Internals

## 1. How Does Redis Store Strings?

### Answer

Redis does **not** store strings as plain C strings.

Internally, Redis uses a data structure called **SDS (Simple Dynamic String)**.

Advantages:

- Stores string length explicitly.
- Binary safe.
- O(1) length retrieval.
- Reduces repeated memory scans.
- Supports embedded null bytes.

Diagram

```text id="rii001"
SDS

↓

Length

↓

Allocated Size

↓

Character Buffer
```

______________________________________________________________________

## 2. Why Not Use C Strings?

Traditional C strings require scanning until a null terminator to determine length.

```text id="rii002"
Hello

↓

'\0'
```

Length calculation becomes O(N).

SDS stores the length separately, making length retrieval O(1).

______________________________________________________________________

## 3. How Are Hashes Stored?

Redis automatically chooses an internal encoding depending on the size of the hash.

Modern Redis versions primarily use:

- Listpack (small hashes)
- Hash table (larger hashes)

This optimization reduces memory usage while maintaining performance.

______________________________________________________________________

## 4. How Are Sorted Sets Implemented?

Internally,

Redis combines:

```text id="rii003"
Hash Table

+

Skip List
```

Hash Table

↓

Fast lookup

Skip List

↓

Ordered traversal

This combination provides efficient lookups and ranking operations.

______________________________________________________________________

## 5. What is a Skip List?

A probabilistic data structure that maintains ordered elements.

```text id="rii004"
Level 3

↓

Level 2

↓

Level 1

↓

Data
```

Search complexity is approximately:

```text id="rii005"
O(log N)
```

______________________________________________________________________

# Memory Management

## 6. What Happens When Redis Runs Out of Memory?

Behavior depends on the configured eviction policy.

Examples:

- Reject writes
- Remove old keys
- Remove least frequently used keys
- Remove least recently used keys

______________________________________________________________________

## 7. LRU vs LFU

| LRU | LFU |
| -------------------------------- | ----------------------------------- |
| Removes least recently used keys | Removes least frequently used keys |
| Based on recent access | Based on long-term access frequency |

______________________________________________________________________

## 8. Memory Fragmentation

Sometimes Redis reports:

```text id="rii006"
Used Memory

↓

500 MB
```

Operating system usage:

```text id="rii007"
800 MB
```

The difference may be due to memory fragmentation.

Redis provides metrics such as `mem_fragmentation_ratio` to help diagnose this.

______________________________________________________________________

## 9. How Do You Check Memory?

CLI

```bash id="rii008"
INFO memory
```

Python

```python id="rii009"
client.info("memory")
```

______________________________________________________________________

# Expiration

## 10. How Does Redis Expire Keys?

Redis uses two complementary strategies.

### Passive Expiration

When a client accesses an expired key,

Redis removes it before returning a value.

______________________________________________________________________

### Active Expiration

A background process periodically samples keys with expiration times and removes expired entries.

This prevents expired keys from remaining in memory indefinitely.

______________________________________________________________________

## 11. Why Not Scan Every Key?

Suppose Redis stores

```text id="rii010"
100 Million Keys
```

Scanning every key continuously would be too expensive.

Sampling provides a practical balance between CPU usage and memory cleanup.

______________________________________________________________________

# Replication

## 12. Explain Replication

```text id="rii011"
Primary

↓

Replica

↓

Replica
```

Writes go to the primary.

Replicas receive replicated updates.

______________________________________________________________________

## 13. Benefits

- Read scaling
- High availability
- Disaster recovery
- Backup replicas

______________________________________________________________________

# Sentinel

## 14. What Does Sentinel Do?

Responsibilities:

- Monitor Redis instances
- Detect failures
- Elect a new primary
- Notify clients

Diagram

```text id="rii012"
Sentinel

↓

Primary Fails

↓

Replica Promoted

↓

Clients Reconnect
```

______________________________________________________________________

## 15. Does Sentinel Shard Data?

No.

Sentinel provides:

- Monitoring
- Failover

It does **not** distribute data across nodes.

______________________________________________________________________

# Redis Cluster

## 16. Explain Redis Cluster

Redis Cluster distributes keys using

```text id="rii013"
16384

Hash Slots
```

Each node owns a subset of the slots.

______________________________________________________________________

## 17. Why Hash Slots?

Instead of assigning keys directly to servers,

Redis maps keys to slots first.

Benefits:

- Easier rebalancing
- Simpler scaling
- Predictable distribution

______________________________________________________________________

## 18. Cluster vs Sentinel

| Sentinel | Cluster |
| ----------------- | -------------------------------------- |
| High Availability | High Availability + Horizontal Scaling |
| One Primary | Multiple Primaries |
| No Sharding | Automatic Sharding |

______________________________________________________________________

# Distributed Locks

## 19. Why Use Distributed Locks?

Suppose

Five application servers

↓

Same scheduled job

↓

Executed five times.

A distributed lock ensures only one server performs the work.

______________________________________________________________________

## 20. SET NX

CLI

```bash id="rii014"
SET lock:job worker1 NX EX 30
```

Python

```python id="rii015"
client.set(
    "lock:job",
    "worker1",
    nx=True,
    ex=30
)
```

______________________________________________________________________

## 21. Why Is EX Important?

Without expiration,

a crashed worker might leave the lock forever,

blocking future work.

______________________________________________________________________

## 22. Redlock

Redlock is a distributed locking algorithm designed for multiple independent Redis instances.

Interview Tip

Know that:

- Redlock exists.
- It attempts to improve fault tolerance.
- It is sometimes debated in the distributed systems community.

For most interviews, understanding its purpose and trade-offs is sufficient.

______________________________________________________________________

# Performance Questions

## 23. Why Is Redis Slow?

Possible reasons:

- Large values
- Network latency
- Slow client
- Blocking commands
- Memory pressure
- Poor key design

______________________________________________________________________

## 24. Why Avoid KEYS?

```bash id="rii016"
KEYS *
```

Scans the full keyspace.

May block Redis.

Instead

```bash id="rii017"
SCAN 0
```

returns results incrementally.

______________________________________________________________________

## 25. Why Use Pipelines?

Without pipelines

```text id="rii018"
1000 Commands

↓

1000 Network Trips
```

With pipelines

```text id="rii019"
1000 Commands

↓

1 Network Trip
```

______________________________________________________________________

## 26. Why Keep Values Small?

Smaller values:

- Consume less memory
- Reduce network transfer time
- Improve cache efficiency

______________________________________________________________________

# Production Debugging

## Scenario 1

API latency suddenly doubles.

Checklist:

- Redis CPU
- Memory usage
- Slow log
- Network latency
- Cache hit ratio

______________________________________________________________________

## Scenario 2

Redis memory reaches 95%.

Possible actions:

- Review TTL strategy
- Inspect largest keys
- Adjust eviction policy
- Increase memory if appropriate

______________________________________________________________________

## Scenario 3

Redis crashes.

Questions to ask:

- Was persistence enabled?
- Was replication configured?
- Was Sentinel or Cluster available?
- How quickly can the application recover?

______________________________________________________________________

## Scenario 4

Cache hit ratio falls sharply.

Investigate:

- Key naming
- TTL changes
- Evictions
- Deployment changes

______________________________________________________________________

## Scenario 5

Orders are missing from a Stream.

Check:

- Consumer Group
- Pending Entries List
- `XACK`
- Worker logs

______________________________________________________________________

# System Design Discussions

## Redis for Sessions

```text id="rii020"
User

↓

FastAPI

↓

Redis

↓

Session
```

Advantages

- Fast lookups
- Shared across application instances
- Easy expiration

______________________________________________________________________

## Redis for Rate Limiting

Use atomic counters.

```python id="rii021"
count = client.incr(
    "rate:user:42"
)

if count == 1:
    client.expire(
        "rate:user:42",
        60
    )
```

______________________________________________________________________

## Redis for Leaderboards

Use Sorted Sets.

```python id="rii022"
client.zadd(
    "leaderboard",
    {
        "Alice": 100
    }
)
```

______________________________________________________________________

## Redis for Background Jobs

Prefer Streams.

Worker Pool

↓

Consumer Group

↓

Reliable Processing

______________________________________________________________________

# Rapid Fire

1. Redis vs Memcached
1. Redis vs PostgreSQL
1. Pub/Sub vs Streams
1. List vs Stream
1. Set vs Sorted Set
1. Hash vs JSON String
1. LRU vs LFU
1. RDB vs AOF
1. Sentinel vs Cluster
1. Pipeline vs Transaction
1. WATCH vs Lua Script
1. SCAN vs KEYS
1. Passive vs Active Expiration
1. Replication vs Sharding
1. Cache-Aside vs Write-Through
1. Hash Table vs Skip List
1. SDS vs C String
1. Connection Pool vs New Connection
1. Distributed Lock vs Database Lock
1. Redis Stream vs Kafka (high level)

______________________________________________________________________

# Common Interview Mistakes

- Saying Redis is only a cache.
- Confusing Sentinel with Cluster.
- Using `KEYS *` in production.
- Ignoring TTL.
- Assuming Redis transactions support SQL-style rollbacks.
- Forgetting that Streams require acknowledgements.
- Believing Redis can safely replace every relational database.

______________________________________________________________________

# Final Interview Checklist

You should now be able to explain:

- Redis architecture
- Why Redis is fast
- Redis internals
- SDS
- Skip Lists
- Internal encodings
- Data structures
- Caching strategies
- Pub/Sub
- Streams
- Transactions
- Pipelines
- Lua scripts
- Memory management
- Expiration
- Persistence
- Replication
- Sentinel
- Cluster
- Distributed locks
- Redlock
- Performance tuning
- Production deployment
- Monitoring
- Debugging scenarios

______________________________________________________________________

# Final Redis Cheat Sheet

```text id="rii023"
Redis

↓

Strings

↓

Hashes

↓

Lists

↓

Sets

↓

Sorted Sets

↓

Bitmaps

↓

HyperLogLog

↓

Geospatial

↓

Streams

↓

Caching

↓

TTL

↓

Transactions

↓

Pipelines

↓

Lua

↓

Persistence

↓

Replication

↓

Sentinel

↓

Cluster

↓

Distributed Locks

↓

Monitoring

↓

Performance
```

______________________________________________________________________

# Summary

After completing the Redis section, you should be comfortable discussing Redis from both an implementation and
production perspective. You should understand not only how to use Redis commands and the `redis-py` client, but also the
internal design decisions that make Redis fast, scalable, and widely adopted in modern backend systems.

This knowledge prepares you for Redis-related questions in backend engineering interviews ranging from mid-level to
senior roles.

______________________________________________________________________

## Next File

[7-redis-url-shortener-project-part-1.md](7-redis-url-shortener-project-part-1.md)
