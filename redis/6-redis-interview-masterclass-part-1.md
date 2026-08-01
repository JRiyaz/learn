# Redis Interview Masterclass - Part 1

## Introduction

This chapter is a comprehensive Redis interview guide.

Unlike previous lectures, this file focuses on:

- Interview questions
- Internal concepts
- Coding questions
- Production discussions
- Common mistakes
- Best practices

If you can answer the questions in this chapter confidently, you'll be well prepared for Redis interviews ranging from
junior to senior backend roles.

______________________________________________________________________

# Beginner Questions

## 1. What is Redis?

### Answer

Redis (REmote DIctionary Server) is an open-source, in-memory data structure store that can be used as:

- Cache
- Database
- Message Broker
- Session Store
- Queue
- Leaderboard Engine

Redis stores most working data in RAM, making it extremely fast.

______________________________________________________________________

## 2. Why is Redis Fast?

### Answer

Main reasons:

- In-memory storage
- Efficient C implementation
- Optimized data structures
- Minimal network overhead
- Mostly O(1) operations
- Single-threaded command execution (avoids lock contention)

Diagram

```text id="ri001"
Application

↓

Redis

↓

RAM
```

______________________________________________________________________

## 3. Is Redis a Database?

### Answer

Yes.

Redis is a NoSQL database.

However,

it is commonly used as:

- Cache
- Session Store
- Queue

instead of replacing PostgreSQL or MySQL.

______________________________________________________________________

## 4. Why Not Replace PostgreSQL with Redis?

### Answer

Redis lacks many relational database features.

Examples:

- SQL
- JOINs
- Rich query language
- Strong relational modeling

Redis excels at speed.

PostgreSQL excels at durable relational storage.

______________________________________________________________________

## 5. Redis vs Memcached

| Redis | Memcached |
| ------------------------ | ---------------- |
| Multiple data structures | Strings only |
| Persistence | No persistence |
| Replication | Limited features |
| Pub/Sub | Not supported |
| Streams | Not supported |
| Lua Scripts | Not supported |

Interview Tip

Redis has become the preferred choice for most new applications.

______________________________________________________________________

# Architecture Questions

## 6. Explain Redis Architecture

```text id="ri002"
Application

↓

TCP

↓

Redis

↓

RAM

↓

(Optional)

Disk
```

Redis processes commands received over TCP, operates on in-memory data structures, and can optionally persist data to
disk.

______________________________________________________________________

## 7. Why is Redis Single Threaded?

### Answer

Historically,

Redis processes commands using one main execution thread.

Benefits:

- No locks
- No race conditions inside Redis command execution
- Simpler design
- Lower overhead

Redis is fast enough that a single thread can process a very large number of operations per second on modern hardware.

______________________________________________________________________

## 8. Is Redis Really Single Threaded?

### Answer

Not entirely.

Modern Redis versions use additional threads for tasks such as networking and background work.

The main command execution path remains single-threaded, which preserves simplicity and predictable behavior.

______________________________________________________________________

## 9. Why Doesn't Redis Need Locks?

Commands execute one at a time on the main execution thread.

Example

```bash id="ri003"
INCR counter
```

Even if thousands of clients call it simultaneously,

Redis executes them sequentially,

making the increment operation atomic.

______________________________________________________________________

# Data Structure Questions

## 10. Which Redis Data Structure Would You Use for User Profiles?

### Answer

Hashes.

Example

CLI

```bash id="ri004"
HSET user:1 \
name Alice \
age 25
```

Python

```python id="ri005"
client.hset(
    "user:1",
    mapping={
        "name": "Alice",
        "age": 25
    }
)
```

______________________________________________________________________

## 11. Which Data Structure for Leaderboards?

Answer

Sorted Sets.

CLI

```bash id="ri006"
ZADD leaderboard \
100 Alice
```

Python

```python id="ri007"
client.zadd(
    "leaderboard",
    {
        "Alice":100
    }
)
```

______________________________________________________________________

## 12. Which Data Structure for Queues?

Answer

Lists

or

Streams

depending on reliability requirements.

______________________________________________________________________

## 13. Difference Between Set and Sorted Set

| Set | Sorted Set |
| --------------- | ------------------------- |
| Unique values | Unique values with scores |
| No order | Score-based ordering |
| Fast membership | Ranking support |

______________________________________________________________________

## 14. HyperLogLog Use Case

Answer

Approximate counting of unique values.

Examples

- Daily visitors
- Unique IPs
- Analytics

Memory usage remains very small even for large datasets.

______________________________________________________________________

# Caching Questions

## 15. What is a Cache?

Answer

A fast storage layer that avoids expensive database queries.

______________________________________________________________________

## 16. Explain Cache-Aside

```text id="ri008"
Redis

↓

Miss

↓

Database

↓

Redis

↓

Return
```

The application loads data into Redis only after a cache miss.

______________________________________________________________________

## 17. Cache Hit vs Cache Miss

Cache Hit

Redis returns data immediately.

Cache Miss

Database must be queried.

______________________________________________________________________

## 18. Why Use TTL?

Without TTL,

cache entries may become stale.

CLI

```bash id="ri009"
SET product:1 Laptop EX 300
```

Python

```python id="ri010"
client.set(
    "product:1",
    "Laptop",
    ex=300
)
```

______________________________________________________________________

## 19. What is Cache Stampede?

Thousands of requests

↓

Cache expires

↓

All hit database

↓

Database overload.

Solutions

- Random TTL
- Distributed Lock
- Cache warming

______________________________________________________________________

## 20. Cache Penetration

Repeated requests for nonexistent keys.

Solution

Cache negative results.

______________________________________________________________________

## 21. Cache Avalanche

Many cache entries expire simultaneously.

Solution

Randomized expiration.

______________________________________________________________________

# Transactions

## 22. Does Redis Support Transactions?

Yes.

Commands

```text id="ri011"
MULTI

↓

EXEC
```

______________________________________________________________________

## 23. Are Redis Transactions ACID?

Answer

No.

Redis transactions provide command grouping and sequential execution but do not offer the same rollback semantics as
relational database transactions.

______________________________________________________________________

## 24. What Does WATCH Do?

WATCH provides optimistic locking.

If a watched key changes before `EXEC`, the transaction is aborted.

______________________________________________________________________

## 25. Pipeline vs Transaction

| Pipeline | Transaction |
| ----------------------- | ---------------------------- |
| Reduce network overhead | Group commands atomically |
| Performance | Consistency |
| Faster | Safer for related operations |

______________________________________________________________________

# Pub/Sub

## 26. Explain Pub/Sub

Publisher

↓

Redis

↓

Subscribers

Messages are delivered only to currently connected subscribers.

______________________________________________________________________

## 27. Pub/Sub vs Streams

| Pub/Sub | Streams |
| ------------------- | ---------------- |
| No persistence | Persistent |
| Broadcast | Event log |
| No replay | Replay supported |
| No acknowledgements | Acknowledgements |

______________________________________________________________________

## 28. When Would You Use Streams?

Examples

- Orders
- Payments
- Email processing
- Event processing

______________________________________________________________________

# Persistence

## 29. Explain RDB

Redis periodically writes snapshots of its in-memory data to disk.

______________________________________________________________________

## 30. Explain AOF

Redis appends write operations to a log file so they can be replayed during recovery.

______________________________________________________________________

## 31. RDB vs AOF

| RDB | AOF |
| -------------- | ----------------- |
| Snapshots | Command log |
| Faster backups | Better durability |
| Smaller | Larger |

______________________________________________________________________

# Coding Questions

## 1

Cache a user.

______________________________________________________________________

## 2

Store a profile using Hashes.

______________________________________________________________________

## 3

Build a leaderboard.

______________________________________________________________________

## 4

Create a task queue.

______________________________________________________________________

## 5

Publish a message.

______________________________________________________________________

## 6

Consume a Stream.

______________________________________________________________________

## 7

Use a pipeline.

______________________________________________________________________

## 8

Implement optimistic locking.

______________________________________________________________________

# Production Scenarios

## Scenario 1

Your Redis memory reaches 100%.

What do you investigate first?

Consider:

- Memory usage
- Eviction policy
- Key sizes
- TTL configuration

______________________________________________________________________

## Scenario 2

Cache hit ratio drops from 95% to 40%.

What could cause it?

Possible causes include:

- Short TTLs
- Incorrect cache keys
- Deployment changes
- Increased cache evictions

______________________________________________________________________

## Scenario 3

Redis suddenly becomes unavailable.

How should the application behave?

A well-designed application should fall back to the primary database where appropriate instead of failing every request.

______________________________________________________________________

## Scenario 4

Users report stale product information.

How would you investigate cache invalidation and TTL strategy?

______________________________________________________________________

## Scenario 5

A leaderboard query is slow.

Would you redesign the data structure or optimize the query?

Explain.

______________________________________________________________________

# Rapid Fire

1. Redis vs PostgreSQL
1. Redis vs Memcached
1. String vs Hash
1. List vs Stream
1. Set vs Sorted Set
1. RDB vs AOF
1. Pipeline vs Transaction
1. Pub/Sub vs Streams
1. Cache Hit vs Cache Miss
1. Cache Stampede vs Avalanche
1. LRU vs LFU
1. TTL vs PERSIST
1. SCAN vs KEYS
1. WATCH vs MULTI
1. Cache-Aside vs Write-Through

______________________________________________________________________

# Common Mistakes

- Using Strings for every use case.
- Forgetting TTL.
- Using `KEYS *` in production.
- Treating Redis as a relational database.
- Assuming Redis transactions behave like SQL transactions.
- Ignoring cache invalidation.
- Forgetting to acknowledge stream messages.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is Redis preferred over Memcached in modern applications?

Redis supports rich data structures, persistence, replication, transactions, Pub/Sub, Streams, Lua scripting, and many
other features that extend beyond simple caching. While Memcached remains useful for straightforward in-memory caching,
Redis's versatility allows it to solve a much wider range of backend problems with a single technology.

______________________________________________________________________

# Practice Questions

## Conceptual

1. Why is Redis fast?
1. Why is Redis single-threaded?
1. Is Redis really single-threaded?
1. Why use Hashes?
1. Why use Sorted Sets?
1. Explain Cache-Aside.
1. Explain TTL.
1. Explain RDB.
1. Explain AOF.
1. Explain Streams.

## Coding

1. Implement a cache.
1. Create a leaderboard.
1. Build a task queue.
1. Use pipelines.
1. Publish notifications.
1. Read from Streams.

______________________________________________________________________

# Summary

After this chapter you should be able to explain:

- Redis fundamentals
- Architecture
- Data structures
- Caching
- Transactions
- Pub/Sub
- Streams
- Persistence
- Common interview questions

______________________________________________________________________

## Next File

[Redis Interview Masterclass - Part 2](6-redis-interview-masterclass-part-2.md)
