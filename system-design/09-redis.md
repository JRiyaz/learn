# Redis Deep Dive

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Master Redis from both an interview and production perspective. Learn how Redis works internally, when to use it, and how to answer Redis-related System Design questions confidently.

______________________________________________________________________

# Introduction

You've already learned

what caching is.

Now let's study

the most popular

distributed cache

used today.

```
Redis
```

If you've worked with

Python,

FastAPI,

Django,

Flask,

or Node.js,

there is a high chance

you've already used Redis,

even if indirectly.

______________________________________________________________________

# What Is Redis?

Redis stands for

```
REmote

DIctionary

Server
```

Redis is an

```
In-Memory

Key-Value

Database
```

Although many people

call it

a cache,

Redis is actually

much more than that.

______________________________________________________________________

# Why Redis Is Fast

Traditional database

```
Application

↓

Disk

↓

Response
```

Redis

```
Application

↓

RAM

↓

Response
```

RAM is

thousands of times

faster

than disk.

Approximate latency

| Storage | Latency |
|----------|----------|
| CPU Cache | Nanoseconds |
| RAM (Redis) | Microseconds |
| SSD | Hundreds of Microseconds |
| HDD | Milliseconds |

______________________________________________________________________

# Redis Architecture

```
Application

↓

Redis

↓

(Optional)

Persistence

↓

Disk
```

Normally,

all reads

come directly

from memory.

______________________________________________________________________

# Redis Is Single Threaded

One of the most common

interview questions.

Redis processes

commands

using

a single main thread.

```
Request

↓

Queue

↓

Redis

↓

Response
```

Why isn't this slow?

Because

- Operations are in memory
- Commands are extremely fast
- No thread synchronization overhead

Modern Redis versions

also use background threads

for tasks like

persistence,

network I/O,

and lazy deletion,

but command execution

remains primarily

single-threaded.

______________________________________________________________________

# Redis Data Types

Unlike

Memcached,

Redis supports

many data structures.

______________________________________________________________________

# String

Most common.

```
Key

↓

Value
```

Example

```
user:101

↓

"Riyaz"
```

Useful for

- Cache
- Session
- Tokens

______________________________________________________________________

# Hash

Stores

objects.

Example

```
user:101

↓

name

↓

Riyaz

email

↓

riyaz@email.com
```

Useful for

- User profiles
- Configuration
- Metadata

______________________________________________________________________

# List

Ordered collection.

Useful for

- Queues
- Recent activity
- Notifications

Commands

```
LPUSH

RPUSH

LPOP

RPOP
```

______________________________________________________________________

# Set

Unique values.

Example

```
User Permissions

↓

READ

WRITE

ADMIN
```

No duplicates.

______________________________________________________________________

# Sorted Set (ZSET)

Stores

values

with

scores.

Example

Leaderboard

```
Alice

1000

Bob

900

Charlie

850
```

Very common

for ranking systems.

______________________________________________________________________

# Bitmap

Efficient

true/false storage.

Useful for

- Daily active users
- Feature flags
- User activity tracking

______________________________________________________________________

# HyperLogLog

Used for

approximate

unique counts.

Example

```
Unique Visitors
```

Very memory efficient.

______________________________________________________________________

# Geospatial

Stores

latitude

longitude.

Useful for

- Uber
- Swiggy
- Zomato
- Delivery applications

______________________________________________________________________

# Streams

Message streaming

introduced

in newer Redis versions.

Useful for

event processing.

Kafka

is generally preferred

for very large-scale

streaming,

but Redis Streams

work well

for many applications.

______________________________________________________________________

# Common Redis Use Cases

Redis isn't

only

for caching.

______________________________________________________________________

# 1. Caching

Most common.

```
Application

↓

Redis

↓

Database
```

______________________________________________________________________

# 2. Session Storage

Instead of

storing sessions

inside

application memory

store them

inside Redis.

Benefits

- Shared across servers
- Stateless applications
- Horizontal scaling

______________________________________________________________________

# 3. Rate Limiting

Example

```
100 Requests

↓

Per Minute
```

Redis

tracks

request counts

very efficiently.

______________________________________________________________________

# 4. Distributed Lock

Suppose

multiple servers

try updating

the same resource.

Redis

can coordinate

using locks.

We'll discuss

Redlock later.

______________________________________________________________________

# 5. Leaderboards

Sorted Sets

make

leaderboards

extremely easy.

Example

Gaming

Fitness apps

Coding contests

______________________________________________________________________

# 6. Pub/Sub

Redis supports

Publisher

↓

Subscriber

communication.

Useful for

- Notifications
- Live dashboards
- Chat

Not ideal

for guaranteed delivery.

______________________________________________________________________

# 7. Real-Time Analytics

Count

- Views
- Likes
- Active users
- Clicks

Very efficiently.

______________________________________________________________________

# Persistence

Many candidates think

Redis

never stores data.

Wrong.

Redis supports

persistence.

______________________________________________________________________

# RDB Snapshot

Redis periodically

creates

snapshots.

```
Memory

↓

Snapshot

↓

Disk
```

Fast recovery.

May lose

recent changes

between snapshots.

______________________________________________________________________

# AOF (Append Only File)

Every write

is appended

to a log.

```
SET

↓

APPEND

↓

Disk
```

Safer.

Slightly slower.

______________________________________________________________________

# RDB vs AOF

| Feature | RDB | AOF |
|----------|-----|-----|
| Performance | Faster | Slightly Slower |
| Recovery | Snapshot | Replay Commands |
| Data Loss | Possible | Minimal |
| File Size | Smaller | Larger |

Many production systems

use

both.

______________________________________________________________________

# Replication

Redis

supports

Master

↓

Replica

```
Master

↓

Replica A

↓

Replica B
```

Reads

can be distributed

across replicas.

Writes

go

to the primary.

______________________________________________________________________

# Redis Sentinel

What happens

if the primary fails?

Sentinel

monitors

Redis.

```
Master

↓

Crash

↓

Promote Replica

↓

New Master
```

Automatic failover.

______________________________________________________________________

# Redis Cluster

One Redis instance

cannot grow forever.

Solution

```
Redis Cluster
```

```
Application

↓

Redis Node A

Redis Node B

Redis Node C
```

Data

is distributed

using

hash slots.

Supports

horizontal scaling.

______________________________________________________________________

# TTL (Expiration)

Redis

can automatically

delete

keys.

Example

```
SET login_token

↓

TTL

15 Minutes
```

After

15 minutes

the key

disappears.

Useful for

- Sessions
- OTPs
- Verification codes

______________________________________________________________________

# Eviction Policies

Suppose

memory

becomes full.

Redis

must decide

what to remove.

Common policies

- noeviction
- allkeys-lru
- volatile-lru
- allkeys-lfu
- volatile-ttl
- random

For interviews,

know

```
LRU

and

LFU
```

______________________________________________________________________

# Redis Transactions

Redis supports

basic transactions.

Commands

```
MULTI

↓

Commands

↓

EXEC
```

Useful

for grouping operations.

Note

They differ

from full SQL transactions.

______________________________________________________________________

# Pipelines

Instead of

sending

100 requests

```
Network

↓

Redis

↓

Network

↓

Redis
```

Pipeline

sends

many commands

together.

Fewer

network round trips.

Better performance.

______________________________________________________________________

# Lua Scripting

Redis

supports

Lua scripts.

Useful for

atomic operations

that require

multiple commands.

______________________________________________________________________

# Redis Pub/Sub

Architecture

```
Publisher

↓

Redis

↓

Subscribers
```

Useful for

- Notifications
- Chat
- Live updates

Messages

are not persisted.

Subscribers

must be online.

______________________________________________________________________

# Redis vs Memcached

| Feature | Redis | Memcached |
|----------|--------|-----------|
| Data Structures | Many | String Only |
| Persistence | Yes | No |
| Replication | Yes | Limited |
| Transactions | Yes | No |
| Pub/Sub | Yes | No |
| Streams | Yes | No |

Redis

is more feature rich.

______________________________________________________________________

# Redis vs Database

Redis

```
Fast

↓

Memory

↓

Temporary
```

Database

```
Persistent

↓

Disk

↓

Source Of Truth
```

Redis

should not

replace

your primary database

for most applications.

______________________________________________________________________

# Common Interview Questions

## Why is Redis so fast?

Because it stores data in memory, uses efficient data structures, and processes commands with minimal overhead.

______________________________________________________________________

## Why is Redis single-threaded?

A single-threaded command execution model avoids locking and synchronization overhead while memory operations remain
extremely fast.

______________________________________________________________________

## Can Redis lose data?

Yes.

Depending on the persistence configuration.

RDB snapshots

may lose

recent writes.

AOF

reduces

this risk.

______________________________________________________________________

## Should Redis replace MySQL?

No.

Redis

is excellent

for caching,

sessions,

and fast data access,

while MySQL

remains

the system of record

for persistent relational data.

______________________________________________________________________

## What happens if Redis goes down?

The application

typically falls back

to the database.

Performance decreases,

but

the application

should continue functioning.

High availability

using

Sentinel

or

Cluster

reduces downtime.

______________________________________________________________________

# Common Mistakes

## Using Redis As Permanent Storage

Redis

is primarily

an in-memory datastore.

Persistent databases

remain

the source of truth.

______________________________________________________________________

## Forgetting Expiration

Temporary data

should usually

have

a TTL.

______________________________________________________________________

## Storing Huge Objects

Large objects

increase memory usage

and network latency.

Prefer

smaller values.

______________________________________________________________________

## No High Availability

Production Redis

should use

replication

and automatic failover.

______________________________________________________________________

# Best Practices

✅ Use Redis for frequently accessed data.

✅ Keep the database as the source of truth.

✅ Configure appropriate TTL values.

✅ Monitor memory usage and hit ratio.

✅ Use replication for read scaling.

✅ Use Sentinel or Cluster for high availability.

______________________________________________________________________

# Interview Deep Dive

## Question

When would you choose Redis over Memcached?

### Answer

Choose Redis when you need advanced data structures, persistence, replication, Pub/Sub, transactions, or features like
Sorted Sets and Streams. Memcached is suitable for simpler key-value caching scenarios.

______________________________________________________________________

## Question

Can Redis be used as a message queue?

### Answer

Yes. Redis supports Lists, Pub/Sub, and Streams. For lightweight messaging and notifications it works well, but for very
high-throughput, durable event streaming, systems like Kafka are generally more appropriate.

______________________________________________________________________

## Question

Why is Redis commonly paired with relational databases?

### Answer

The relational database remains the source of truth for durable storage, while Redis provides low-latency access to
frequently requested or temporary data, significantly reducing database load.

______________________________________________________________________

# Practice Exercise

For each application,

identify

1. Which Redis data structure would you use?
1. Would you configure a TTL?
1. Is persistence required?
1. Should replication be enabled?
1. Would Redis Cluster be necessary?

Applications

- Online Shopping Cart
- User Sessions
- OTP Verification
- Gaming Leaderboard
- Chat Application
- Rate Limiter
- Food Delivery Tracking
- URL Shortener

______________________________________________________________________

# Summary

Redis is much more than a cache.

It provides

- Extremely fast in-memory storage
- Rich data structures
- Replication and high availability
- Persistence options
- Distributed caching
- Session storage
- Rate limiting
- Messaging capabilities

Mastering Redis is essential because it appears in both **backend engineering interviews** and **System Design
interviews**, and it's widely used in modern distributed systems.

______________________________________________________________________

# Next

[Database Fundamentals (SQL vs NoSQL)](10-database-fundamentals.md)
