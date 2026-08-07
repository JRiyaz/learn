# System Design – Distributed Cache

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how distributed caching works, why it is essential for scalable systems, cache strategies, cache consistency, eviction policies, Redis architecture, and confidently answer Distributed Cache questions in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

your application

receives

```
1 Million

Requests

Per Second
```

Every request

reads

from

the database.

Eventually

the database

becomes

the bottleneck.

How do

companies like

Amazon,

Netflix,

Instagram,

and Uber

handle this?

They use

```
Distributed Cache
```

______________________________________________________________________

# What Is A Cache?

A cache

is

a fast,

temporary

storage layer

that stores

frequently accessed data.

Instead of

```
Application

↓

Database
```

we use

```
Application

↓

Cache

↓

Database
```

______________________________________________________________________

# Why Do We Need Caching?

Benefits

- Lower latency
- Fewer database queries
- Higher throughput
- Better scalability
- Reduced infrastructure cost

______________________________________________________________________

# Example

Without cache

```
Request

↓

Database

↓

20 ms
```

With cache

```
Request

↓

Redis

↓

1 ms
```

Huge improvement.

______________________________________________________________________

# What Is A Distributed Cache?

Instead of

one cache server

```
Application

↓

Redis
```

we use

multiple cache servers.

```
Application

↓

Cache Cluster

↓

Node A

Node B

Node C
```

Allows

horizontal scaling.

______________________________________________________________________

# Why Not Use Local Memory?

Suppose

three application servers

exist.

```
App 1

↓

Memory
```

```
App 2

↓

Memory
```

```
App 3

↓

Memory
```

Each server

contains

different data.

Results

become

inconsistent.

Distributed cache

provides

shared state.

______________________________________________________________________

# Typical Architecture

```
                Users
                   │
                   ▼
            Load Balancer
                   │
                   ▼
             API Servers
                   │
                   ▼
            Redis Cluster
                   │
                   ▼
              Database
```

______________________________________________________________________

# Cache Read Flow

```
Request

↓

Cache

↓

Hit?

↓

Yes

↓

Return Data
```

______________________________________________________________________

# Cache Miss

```
Request

↓

Cache

↓

Miss

↓

Database

↓

Store In Cache

↓

Return Result
```

This pattern

is called

```
Cache-Aside
```

______________________________________________________________________

# Cache Hit

Interview favorite.

Requested data

already exists

inside

the cache.

```
Request

↓

Redis

↓

Response
```

Database

is not touched.

______________________________________________________________________

# Cache Miss

Requested data

does not exist.

```
Request

↓

Redis

↓

Database

↓

Redis

↓

Response
```

______________________________________________________________________

# Cache-Aside Pattern

Most common

interview answer.

Flow

```
Read Cache

↓

Miss

↓

Read Database

↓

Update Cache

↓

Return Data
```

Advantages

- Simple
- Popular
- Easy to implement

______________________________________________________________________

# Read Through Cache

Instead of

application

managing cache,

a cache layer

handles

loading data.

```
Application

↓

Cache

↓

Database
```

Application

doesn't know

about

cache misses.

______________________________________________________________________

# Write Through Cache

When

data changes

```
Application

↓

Cache

↓

Database
```

Cache

and

database

are updated

together.

______________________________________________________________________

# Advantages

- Cache

always

contains

fresh data.

______________________________________________________________________

# Disadvantages

Unused data

may also

be cached.

______________________________________________________________________

# Write Behind Cache

Interview favorite.

```
Application

↓

Cache

↓

Immediate Response

↓

Background Write

↓

Database
```

Very fast writes.

______________________________________________________________________

# Advantages

- Low latency
- High throughput

______________________________________________________________________

# Disadvantages

Cache failure

before persistence

may cause

data loss.

Suitable only

when

that trade-off

is acceptable.

______________________________________________________________________

# Refresh Ahead

Suppose

popular data

is about

to expire.

Refresh it

before

expiration.

```
Cache

↓

Background Refresh

↓

Database
```

Users

continue

getting

cache hits.

______________________________________________________________________

# Time To Live (TTL)

Cached data

should not

live forever.

Example

```
TTL

=

10 Minutes
```

After expiration

data

is removed

or refreshed.

______________________________________________________________________

# Cache Eviction

Suppose

cache

is full.

Which item

should be removed?

Need

an

eviction policy.

______________________________________________________________________

# LRU

Least Recently Used

Interview favorite.

Remove

the item

that has

not been used

for

the longest time.

______________________________________________________________________

# LFU

Least Frequently Used.

Remove

the item

with

the lowest

access count.

______________________________________________________________________

# FIFO

First In

First Out.

Oldest item

is removed

first.

______________________________________________________________________

# Random

Remove

a random item.

Simple,

but

rarely optimal.

______________________________________________________________________

# Eviction Comparison

| Policy | Good For |
|----------|----------|
| LRU | General-purpose caching |
| LFU | Frequently reused data |
| FIFO | Simple workloads |
| Random | Rarely preferred |

______________________________________________________________________

# Cache Consistency

Interview favorite.

Suppose

database

changes.

Cache

still contains

old value.

```
Stale Data
```

Need

a strategy

to keep

cache

consistent.

______________________________________________________________________

# Cache Invalidation

When

database

changes

```
Update Database

↓

Delete Cache
```

Next request

reloads

fresh data.

Most common

approach.

______________________________________________________________________

# Update Cache

Instead of

deleting

```
Update Database

↓

Update Cache
```

Useful

when

fresh data

must be

immediately available.

______________________________________________________________________

# Cache Stampede

Interview favorite.

Suppose

popular cache

expires.

Thousands

of requests

arrive

simultaneously.

All

hit

the database.

```
Database Overloaded
```

______________________________________________________________________

# Solutions

- Request coalescing
- Mutex locking
- Refresh Ahead
- Staggered TTLs

______________________________________________________________________

# Cache Penetration

Requests

ask

for

non-existent data.

```
User 999999999

↓

Database

↓

Not Found
```

Repeated

requests

still

hit

the database.

______________________________________________________________________

# Solution

Cache

negative results

for

a short time.

Example

```
NULL

↓

TTL 1 Minute
```

______________________________________________________________________

# Cache Avalanche

Many keys

expire

at

the same time.

```
Thousands

of Cache Misses
```

Database

gets overloaded.

______________________________________________________________________

# Solution

Use

randomized TTLs.

Example

```
10 Minutes

± Random Offset
```

Keys

expire

at different times.

______________________________________________________________________

# Hot Keys

Interview favorite.

Suppose

one product

becomes

viral.

Millions

of users

request

the same key.

One cache node

becomes

overloaded.

______________________________________________________________________

# Solutions

- Replicate hot data
- Local caching
- Request batching
- Load balancing

______________________________________________________________________

# Cache Partitioning

Large cache

is split

across

multiple nodes.

```
Node A

↓

Users
```

```
Node B

↓

Orders
```

or

using

hashing.

______________________________________________________________________

# Consistent Hashing

Adding

a new cache node

should not

move

every key.

Use

Consistent Hashing

to minimize

data movement.

______________________________________________________________________

# Replication

```
Primary

↓

Replica

↓

Replica
```

If

primary fails,

replica

takes over.

______________________________________________________________________

# Redis Cluster

Interview favorite.

Redis Cluster

provides

- Sharding
- Replication
- Failover
- High Availability

Automatically.

______________________________________________________________________

# Monitoring

Monitor

- Cache hit ratio
- Cache miss ratio
- Memory usage
- Evictions
- Latency
- Replication lag

______________________________________________________________________

# Failure Scenarios

## Cache Node Failure

Requests

fall back

to

database.

Performance

decreases,

but

service

continues.

______________________________________________________________________

## Database Failure

If

required data

is already

cached,

some requests

can still

be served

until

the cache expires,

depending on

application requirements.

______________________________________________________________________

## Cache Full

Eviction policy

removes

older

or

less valuable

entries.

______________________________________________________________________

# Typical Architecture

```
                    Users
                       │
                       ▼
                Load Balancer
                       │
                       ▼
                 API Servers
                       │
                       ▼
                 Redis Cluster
             ┌────────┼────────┐
             ▼        ▼        ▼
          Node A   Node B   Node C
                       │
                       ▼
                   Database
```

______________________________________________________________________

# Common Interview Questions

## Why use Redis instead of MySQL as a cache?

Redis stores data in memory, providing much lower latency than disk-based databases. It also supports expiration,
replication, clustering, and atomic operations.

______________________________________________________________________

## What is Cache-Aside?

Cache-Aside is a pattern where the application checks the cache first. On a cache miss, it loads data from the database,
stores it in the cache, and returns the result.

______________________________________________________________________

## What is Cache Stampede?

A Cache Stampede occurs when many requests simultaneously miss the cache after a popular key expires, causing a sudden
surge of database traffic.

______________________________________________________________________

## What is the difference between LRU and LFU?

LRU removes the least recently accessed item, while LFU removes the least frequently accessed item over time.

______________________________________________________________________

# Common Mistakes

## No TTL

Cached data

may become

stale.

______________________________________________________________________

## Ignoring Cache Consistency

Always

define

a strategy

for

cache updates

or invalidation.

______________________________________________________________________

## One Cache Node

Creates

a single point

of failure.

______________________________________________________________________

## Ignoring Stampedes

Popular keys

can overload

the database.

______________________________________________________________________

## Caching Everything

Only

cache

data

that benefits

from caching.

______________________________________________________________________

# Best Practices

✅ Use Redis Cluster.

✅ Set appropriate TTL values.

✅ Use Cache-Aside for most applications.

✅ Prevent Cache Stampedes.

✅ Monitor hit ratio.

✅ Replicate cache nodes.

______________________________________________________________________

# Interview Deep Dive

## Question

What cache strategy is most commonly used?

### Answer

Cache-Aside is the most widely used strategy because it is simple, flexible, and allows applications to cache only
frequently accessed data while keeping the database as the source of truth.

______________________________________________________________________

## Question

How do you prevent Cache Stampedes?

### Answer

Use techniques such as request coalescing, mutex locking, refresh-ahead, or randomized TTLs to prevent many requests
from simultaneously hitting the database after cache expiration.

______________________________________________________________________

## Question

Why isn't local application memory sufficient?

### Answer

Each application instance would maintain its own cache, leading to inconsistent data and inefficient memory usage. A
distributed cache provides shared, centralized access across all application servers.

______________________________________________________________________

# Practice Exercise

Design

a Distributed Cache

for

500 Million Users.

Explain

1. Cache strategy
1. TTL
1. Eviction policy
1. Cache consistency
1. Cache partitioning
1. Replication
1. Stampede prevention
1. Monitoring
1. Failure recovery
1. Trade-offs

Then explain

how

your design

would differ

for

- E-commerce
- Social Media
- Banking
- Video Streaming

______________________________________________________________________

# Summary

Distributed Caching is one of the most important System Design topics because it dramatically improves scalability and
performance.

A strong solution should demonstrate

- Cache strategies
- Eviction policies
- Cache consistency
- Distributed architecture
- Replication
- Consistent hashing
- Stampede prevention
- Monitoring
- Failure handling
- Trade-off analysis

Understanding distributed caching is essential for designing high-performance backend systems and is a frequent topic in
senior backend and System Design interviews.

______________________________________________________________________

# Next

[System Design – Web Crawler](32-design-web-crawler.md)
