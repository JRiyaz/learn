# Redis Production, Performance & Interview Masterclass

## Introduction

Knowing Redis commands is not enough.

Senior Backend Engineers are expected to understand:

- Production architecture
- Memory management
- Eviction policies
- Persistence
- High Availability
- Replication
- Redis Sentinel
- Redis Cluster
- Distributed Locks
- Rate Limiting
- Monitoring
- Performance tuning
- Interview questions

This chapter combines production concepts and interview preparation into one comprehensive guide.

______________________________________________________________________

# Redis in Production

A typical production architecture looks like this:

```text id="redisprod001"
                Clients
                    │
        ┌───────────┴───────────┐
        │                       │
      FastAPI              Worker Service
        │                       │
        └───────────┬───────────┘
                    │
                 Redis
                    │
             PostgreSQL
```

Redis sits between the application and the database for caching, messaging, and fast data access.

______________________________________________________________________

# Redis Memory Model

Redis stores most data in RAM.

```text id="redisprod002"
Application

↓

Redis

↓

RAM

↓

(Optional)

Disk Persistence
```

Memory is finite.

Eventually,

Redis must either:

- Reject writes
- Remove old data

______________________________________________________________________

# Measuring Memory

CLI

```bash id="redisprod003"
INFO memory
```

Python

```python id="redisprod004"
info = client.info("memory")

print(info)
```

Useful fields include:

- used_memory
- used_memory_human
- maxmemory

______________________________________________________________________

# Setting Maximum Memory

CLI

```bash id="redisprod005"
CONFIG SET maxmemory 1gb
```

Python

```python id="redisprod006"
client.config_set(
    "maxmemory",
    "1gb"
)
```

When the limit is reached,

Redis applies an eviction policy.

______________________________________________________________________

# Eviction Policies

Common policies:

| Policy | Description |
| --------------- | ------------------------------------------ |
| noeviction | Reject new writes |
| allkeys-lru | Remove least recently used keys |
| volatile-lru | Remove least recently used keys with TTL |
| allkeys-lfu | Remove least frequently used keys |
| volatile-lfu | Remove least frequently used keys with TTL |
| allkeys-random | Remove random keys |
| volatile-random | Remove random expiring keys |
| volatile-ttl | Remove keys closest to expiration |

______________________________________________________________________

# LRU

Least Recently Used

```text id="redisprod007"
Old Access

↓

Removed

↓

Recent Access

↓

Kept
```

Excellent for caches.

______________________________________________________________________

# LFU

Least Frequently Used

```text id="redisprod008"
Rarely Used

↓

Removed

↓

Frequently Used

↓

Kept
```

Better for long-lived caches where frequently accessed items should remain even if they haven't been accessed recently.

______________________________________________________________________

# Choosing an Eviction Policy

General guidance:

- Cache → `allkeys-lru` or `allkeys-lfu`
- Session store → often `volatile-lru` when sessions have TTLs
- Critical data → avoid relying on eviction

Always evaluate based on application requirements.

______________________________________________________________________

# Persistence

Redis supports two persistence mechanisms.

```text id="redisprod009"
Persistence

├── RDB

└── AOF
```

______________________________________________________________________

# RDB

Redis Database Snapshot

Flow

```text id="redisprod010"
RAM

↓

Snapshot

↓

dump.rdb
```

Advantages

- Compact
- Fast recovery
- Good backups

Disadvantages

- Some recent writes may be lost if Redis crashes before the next snapshot.

______________________________________________________________________

# AOF

Append Only File

Flow

```text id="redisprod011"
SET

↓

Append

↓

appendonly.aof
```

Advantages

- Better durability
- Replays commands during recovery

Disadvantages

- Larger files
- More write overhead

______________________________________________________________________

# RDB vs AOF

| RDB | AOF |
| ---------------------------- | -------------------------------------------------------- |
| Snapshots | Every write is logged (based on configured fsync policy) |
| Smaller | Larger |
| Faster startup in many cases | Better durability |
| Backup friendly | Better crash recovery |

Modern Redis deployments may use both.

______________________________________________________________________

# Replication

Replication improves availability and read scalability.

```text id="redisprod012"
Primary

↓

Replica 1

↓

Replica 2
```

Applications typically write to the primary.

Replicas can serve read traffic.

______________________________________________________________________

# Advantages

- High availability
- Read scaling
- Backup replicas
- Disaster recovery

______________________________________________________________________

# Redis Sentinel

Sentinel monitors Redis servers.

```text id="redisprod013"
Sentinel

↓

Primary Failure

↓

Elect New Primary
```

Responsibilities:

- Health monitoring
- Automatic failover
- Configuration discovery

______________________________________________________________________

# Redis Cluster

Redis Cluster partitions data across multiple nodes.

```text id="redisprod014"
Client

↓

Cluster

├── Node A

├── Node B

└── Node C
```

Redis uses **16,384 hash slots** to distribute keys across the cluster.

______________________________________________________________________

# Sentinel vs Cluster

| Sentinel | Cluster |
| ----------------- | -------------------------------------- |
| High availability | High availability + horizontal scaling |
| One primary | Multiple primaries |
| No sharding | Automatic sharding |

______________________________________________________________________

# Distributed Locks

Sometimes only one application instance should perform a task.

Example

```text id="redisprod015"
Job Scheduler

↓

Redis Lock

↓

Only One Worker
```

______________________________________________________________________

# SET NX

CLI

```bash id="redisprod016"
SET lock:job worker1 NX EX 30
```

Meaning

- NX → Only if key does not exist
- EX → Expire after 30 seconds

______________________________________________________________________

# Python

```python id="redisprod017"
success = client.set(
    "lock:job",
    "worker1",
    nx=True,
    ex=30
)
```

If `success` is true,

the lock was acquired.

______________________________________________________________________

# Releasing Locks Safely

A worker should release only **its own** lock.

A common production approach is:

1. Store a unique random token as the lock value.
1. Release the lock using a Lua script that verifies ownership before deleting.

This avoids accidentally deleting another worker's lock.

______________________________________________________________________

# Rate Limiting

Simple fixed-window implementation.

```python id="redisprod018"
key = "rate:user:123"

count = client.incr(key)

if count == 1:
    client.expire(key, 60)

if count > 100:
    raise Exception("Rate limit exceeded")
```

100 requests

↓

1 minute

Simple and effective for many APIs.

______________________________________________________________________

# Distributed Counters

Redis provides atomic counters.

```python id="redisprod019"
client.incr("page_views")
```

Useful for:

- Likes
- Downloads
- Analytics
- API usage

______________________________________________________________________

# Monitoring

Important commands

CLI

```bash id="redisprod020"
INFO

MONITOR

SLOWLOG GET
```

Python

```python id="redisprod021"
client.info()

client.slowlog_get()
```

Use `MONITOR` carefully because it has significant overhead and is generally intended for debugging.

______________________________________________________________________

# Performance Tips

- Use pipelines for bulk operations.
- Avoid `KEYS *`.
- Use `SCAN`.
- Set appropriate TTL values.
- Keep values reasonably small.
- Reuse Redis connections through connection pools.
- Monitor memory usage.
- Measure before optimizing.

______________________________________________________________________

# Connection Pooling (`redis-py`)

`redis-py` automatically supports connection pooling.

Example

```python id="redisprod022"
import redis

pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    decode_responses=True,
    max_connections=20
)

client = redis.Redis(
    connection_pool=pool
)
```

Benefits

- Reuses TCP connections
- Reduces connection overhead
- Improves throughput

______________________________________________________________________

# Common Mistakes

### Using Redis as Permanent Storage

Redis can persist data, but many deployments use it primarily for caching and fast access.

______________________________________________________________________

### Forgetting TTL

Old cache entries consume memory.

______________________________________________________________________

### Using KEYS in Production

Use SCAN instead.

______________________________________________________________________

### Ignoring Memory Limits

Eventually Redis will start evicting keys or rejecting writes, depending on configuration.

______________________________________________________________________

### Not Monitoring Redis

Production systems should monitor:

- Memory
- CPU
- Slow commands
- Hit ratio
- Evictions

______________________________________________________________________

# Best Practices

- Keep PostgreSQL (or another durable database) as the system of record.
- Use Redis for speed.
- Configure eviction policies deliberately.
- Enable appropriate persistence.
- Monitor memory continuously.
- Use Sentinel or Cluster for high availability.
- Use pipelines for bulk operations.
- Use distributed locks carefully.
- Benchmark changes before deployment.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design a production Redis deployment for a high-traffic application?

I would configure Redis with appropriate memory limits, choose an eviction policy that matches the workload, enable
persistence based on durability requirements, and monitor memory usage, latency, and slow commands. For high
availability, I would use Redis Sentinel or Redis Cluster depending on whether horizontal scaling is required. I would
use connection pooling in the application, pipelines for bulk operations, TTLs for cache entries, and distributed locks
where coordination between multiple application instances is necessary.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is an eviction policy?
1. Explain LRU and LFU.
1. What is RDB?
1. What is AOF?
1. RDB vs AOF.
1. What is replication?
1. What is Redis Sentinel?
1. What is Redis Cluster?
1. What is a distributed lock?
1. How does Redis implement rate limiting?
1. Why use connection pooling?
1. Why avoid `KEYS *`?

## Coding

1. Configure Redis memory limits.
1. Implement a distributed lock.
1. Build a rate limiter.
1. Configure a connection pool.
1. Retrieve Redis memory statistics.
1. Batch writes using pipelines.

______________________________________________________________________

# Hands-on Exercise

Build a Production Cache Layer.

Requirements:

1. Configure a Redis connection pool.
1. Cache API responses.
1. Add TTL values.
1. Implement a distributed lock.
1. Add a rate limiter.
1. Measure memory usage.
1. Retrieve slow queries.
1. Benchmark pipelined vs non-pipelined writes.

______________________________________________________________________

# Cheat Sheet

```text id="redisprod023"
Memory

↓

Eviction

↓

RDB

↓

AOF

↓

Replication

↓

Sentinel

↓

Cluster

↓

Distributed Lock

↓

Rate Limiting

↓

Connection Pool

↓

Monitoring
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Redis production architecture
- Memory management
- Eviction policies
- RDB persistence
- AOF persistence
- Replication
- Redis Sentinel
- Redis Cluster
- Distributed locks
- Rate limiting
- Connection pooling
- Monitoring
- Performance tuning
- Production best practices
- Interview patterns

You now understand how Redis is deployed and managed in production environments and how to answer senior-level Redis
interview questions confidently.

______________________________________________________________________

## Course Summary

After completing the Redis section, you should be comfortable with:

- Redis fundamentals
- Redis data structures
- Caching strategies
- TTL and expiration
- Pub/Sub
- Streams
- Consumer Groups
- Transactions
- Pipelines
- Lua scripts
- Persistence
- High availability
- Clustering
- Distributed locks
- Rate limiting
- Production deployment
- Performance optimization

______________________________________________________________________

## Next File

[6-redis-interview-masterclass.md](6-redis-interview-masterclass-part-1.md)
