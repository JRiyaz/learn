# System Design - Part 86

# Redis System Design (How Redis Works Internally)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Redis exists
- Redis Architecture
- In-Memory Storage
- Redis Data Structures
- Persistence (RDB & AOF)
- Replication
- Sentinel
- Redis Cluster
- Pub/Sub
- Eviction Policies
- Distributed Caching
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Redis.**

Previously,

we used Redis

as:

- Cache
- Session Store
- Rate Limiter
- Pub/Sub
- Distributed Lock

Now,

we'll understand

how Redis

itself

is built.

______________________________________________________________________

# Why Redis?

Suppose

your application

queries

the database

for

every request.

```text id="rd8601"
Application

↓

Database
```

The database

becomes

the bottleneck.

Redis

stores

frequently accessed data

in memory,

making reads

thousands of times faster.

______________________________________________________________________

# High-Level Architecture

```text id="rd8602"
Application

↓

Redis

↓

Database
```

Redis

acts as

an in-memory layer

between

applications

and

persistent storage.

______________________________________________________________________

# In-Memory Storage

Interview favorite.

Redis stores

everything

in RAM.

Benefits:

- Extremely fast reads
- Extremely fast writes

Trade-off:

Memory

is expensive

and

volatile.

______________________________________________________________________

# Single-Threaded Event Loop

Interview favorite.

Unlike many databases,

Redis

primarily processes

commands

using

a single-threaded

event loop.

```text id="rd8603"
Clients

↓

Event Loop

↓

Memory
```

Why?

- No locking
- No thread contention
- Simpler implementation
- Very low latency

Modern Redis

uses background threads

for

I/O

and

certain maintenance tasks,

but

command execution

remains

largely single-threaded.

______________________________________________________________________

# Redis Data Structures

Interview favorite.

Redis

is

not

just

a key-value store.

Supported structures:

- Strings
- Hashes
- Lists
- Sets
- Sorted Sets (ZSET)
- Bitmaps
- HyperLogLog
- Streams
- Geospatial Indexes

______________________________________________________________________

# Strings

Most common type.

```text id="rd8604"
user:1

↓

John
```

Useful for:

- Cache
- Sessions
- Counters

______________________________________________________________________

# Hashes

Store

multiple fields.

```text id="rd8605"
User

↓

Name

Email

Age
```

Useful

for

user profiles.

______________________________________________________________________

# Lists

Ordered collection.

Useful

for:

- Queues
- Recent activity
- Job processing

______________________________________________________________________

# Sets

Unique elements.

Useful

for:

- Tags
- Followers
- Permissions

______________________________________________________________________

# Sorted Sets (ZSET)

Interview favorite.

Each element

has

a score.

```text id="rd8606"
Player A

100

Player B

95
```

Useful

for:

- Leaderboards
- Rankings
- Scheduling

______________________________________________________________________

# Persistence

Interview favorite.

Redis

stores data

in memory,

but

memory

is volatile.

Redis

supports

two persistence methods.

______________________________________________________________________

# RDB Snapshots

Periodically

save

memory

to disk.

```text id="rd8607"
Memory

↓

Snapshot

↓

Disk
```

Advantages:

- Small files
- Fast recovery

Disadvantages:

Recent changes

may be lost.

______________________________________________________________________

# AOF (Append Only File)

Every write

is appended

to a log.

```text id="rd8608"
SET A

↓

SET B

↓

SET C
```

On restart,

Redis

replays

the log.

Advantages:

- Better durability

Disadvantages:

- Larger files
- Slower recovery

______________________________________________________________________

# Hybrid Persistence

Modern Redis

can combine

RDB

and

AOF,

providing

fast startup

with

better durability.

______________________________________________________________________

# Replication

Interview favorite.

Redis

uses

Primary-Replica

replication.

```text id="rd8609"
Primary

↓

Replica 1

↓

Replica 2
```

Applications

typically:

- Write to Primary
- Read from Replicas

______________________________________________________________________

# Sentinel

Interview favorite.

Suppose

the Primary

fails.

Redis Sentinel

detects

the failure.

```text id="rd8610"
Primary

↓

Crash

↓

Replica promoted
```

Clients

switch

to

the new Primary.

______________________________________________________________________

# Redis Cluster

Interview favorite.

One server

cannot store

unlimited data.

Redis Cluster

partitions data

across nodes.

```text id="rd8611"
Slot 0–5000

↓

Node A

Slot 5001–10000

↓

Node B

Slot 10001–16383

↓

Node C
```

Redis

uses

16384 hash slots.

Keys

are mapped

to slots

using

hashing.

______________________________________________________________________

# Pub/Sub

Interview favorite.

Applications

can publish

messages.

```text id="rd8612"
Publisher

↓

Channel

↓

Subscribers
```

Unlike Kafka,

messages

are not stored.

If

a subscriber

is offline,

the message

is lost.

______________________________________________________________________

# Eviction Policies

Interview favorite.

Suppose

memory

becomes full.

Redis

must

evict data.

Common policies:

- LRU (Least Recently Used)
- LFU (Least Frequently Used)
- TTL-based
- Random

Choose

based on

your workload.

______________________________________________________________________

# Distributed Cache Pattern

```text id="rd8613"
Application

↓

Redis

↓

Database
```

Workflow:

1. Check Redis.
1. Cache miss → Query database.
1. Store result in Redis.
1. Return response.

This is

the

Cache-Aside Pattern.

______________________________________________________________________

# Scaling Redis

Scale by:

- Replication
- Redis Cluster
- Sharding

Large deployments

combine

all three.

______________________________________________________________________

# Failure Scenario

Suppose

the Primary

fails.

Sentinel

promotes

a Replica

to

Primary.

Clients

reconnect

automatically.

______________________________________________________________________

# Another Failure

Suppose

one Cluster node

fails.

Only

its assigned

hash slots

are affected.

Replica nodes

take ownership,

maintaining

availability.

______________________________________________________________________

# End-to-End Architecture

```text id="rd8614"
Application

↓

Redis Cluster

↓

Primary

↓

Replicas

↓

Sentinel

↓

Disk (RDB/AOF)
```

______________________________________________________________________

# Trade-offs

RDB

vs

AOF

| RDB | AOF |
| ------------------ | ----------------- |
| Faster recovery | Better durability |
| Smaller files | Larger files |
| Possible data loss | Minimal data loss |

______________________________________________________________________

Redis

vs

Database

| Redis | Database |
| ------------------- | --------------- |
| In-memory | Persistent |
| Millisecond latency | Higher latency |
| Cache | Source of truth |

______________________________________________________________________

Pub/Sub

vs

Kafka

| Redis Pub/Sub | Kafka |
| ---------------- | --------------- |
| Fire-and-forget | Durable log |
| No persistence | Persistent |
| Very low latency | High throughput |

______________________________________________________________________

# Best Practices

✅ Use Redis as a cache, not the primary database (unless intentionally designing for it).

✅ Choose the correct data structure for the problem.

✅ Configure appropriate eviction policies.

✅ Monitor memory usage and hit ratio.

✅ Use replication and Sentinel or Cluster for high availability.

______________________________________________________________________

# Common Mistakes

### Storing Everything in Redis

Memory

is expensive.

Store

only

hot data.

______________________________________________________________________

### Assuming Redis is Durable

Without

persistence,

a restart

can lose

all data.

______________________________________________________________________

### Using Redis Pub/Sub for Durable Messaging

Pub/Sub

does not

retain messages.

Offline subscribers

miss events.

Use Kafka

when durability

is required.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Redis?

Design Redis as an in-memory data store with a single-threaded event loop for command execution, providing extremely
low-latency operations. Support multiple data structures such as strings, hashes, lists, sets, and sorted sets. Add
persistence using RDB snapshots and AOF logs, replicate data from a primary node to replicas for fault tolerance, and
use Sentinel for automatic failover. For horizontal scaling, partition data across a Redis Cluster using hash slots.
Support Pub/Sub for real-time messaging, configurable eviction policies for memory management, and use Redis primarily
as a high-speed cache rather than the long-term source of truth.

______________________________________________________________________

# Summary

In this lesson, you learned:

- In-memory architecture
- Data structures
- RDB
- AOF
- Replication
- Sentinel
- Redis Cluster
- Pub/Sub
- Eviction policies
- Scaling
- Trade-offs

______________________________________________________________________

# What's Next

[Nginx System Design](87-nginx-system-design.md)
