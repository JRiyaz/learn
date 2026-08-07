# Caching Fundamentals

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand why caching is one of the most important techniques in distributed systems, how it works, different caching strategies, and how to discuss caching confidently in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

your application

receives

100,000 requests

every second.

Every request

queries

the database.

```
Users

↓

Application

↓

Database
```

Initially,

everything works.

As traffic grows,

the database becomes

the bottleneck.

```
High CPU

↓

Slow Queries

↓

High Latency

↓

Timeouts

↓

Poor User Experience
```

How do companies like

Netflix,

Instagram,

Amazon,

and Google

solve this?

The answer is

```
Caching
```

______________________________________________________________________

# What Is Caching?

Caching means

storing

frequently accessed data

in a

much faster storage layer.

Instead of

```
Application

↓

Database
```

we get

```
Application

↓

Cache

↓

Database
```

If data exists

inside the cache,

the database

is never queried.

______________________________________________________________________

# Why Do We Need Caching?

Databases are

relatively slow.

Memory

(RAM)

is

extremely fast.

Approximate access times

| Storage | Latency |
|----------|---------|
| CPU Cache | Nanoseconds |
| RAM (Redis) | Microseconds |
| SSD | Hundreds of Microseconds |
| Database Query | Milliseconds |
| Network Call | Milliseconds to Seconds |

A cache

reduces

response time

dramatically.

______________________________________________________________________

# Basic Architecture

```
Users

↓

Load Balancer

↓

Application

↓

Redis

↓

Database
```

Flow

```
Request

↓

Cache?

↓

Yes

↓

Return Data
```

Otherwise

```
Request

↓

Cache Miss

↓

Database

↓

Save To Cache

↓

Return Data
```

______________________________________________________________________

# Cache Hit

Suppose

User 123

is already

inside Redis.

```
Application

↓

Redis

↓

Found

↓

Return
```

Fast.

Database

is skipped.

______________________________________________________________________

# Cache Miss

Suppose

User 999

is not

inside Redis.

```
Application

↓

Redis

↓

Not Found

↓

Database

↓

Store In Redis

↓

Return
```

Future requests

become

Cache Hits.

______________________________________________________________________

# Cache Hit Ratio

One important metric

is

```
Cache Hit Ratio
```

Formula

```
Cache Hits

÷

Total Requests
```

Example

```
950 Hits

↓

1000 Requests

↓

95%
```

Excellent.

Only

5%

reach

the database.

______________________________________________________________________

# Why High Cache Hit Ratio Matters

Without Cache

```
100,000 Requests

↓

Database
```

With

95% Cache Hit

```
100,000 Requests

↓

5,000 Database Queries
```

Massive reduction.

______________________________________________________________________

# What Should Be Cached?

Good candidates

- User profiles
- Product details
- Configuration
- Frequently accessed data
- API responses
- Search results
- Popular posts

______________________________________________________________________

# What Should NOT Be Cached?

Generally avoid

- Bank balances
- Payment transactions
- Highly dynamic data
- Sensitive user-specific information
- Frequently changing counters (unless carefully managed)

Always consider

freshness.

______________________________________________________________________

# Types Of Cache

Caching exists

at many levels.

```
Browser Cache

↓

CDN

↓

Load Balancer

↓

Application Cache

↓

Redis

↓

Database Cache
```

Most systems

use

multiple layers.

______________________________________________________________________

# Browser Cache

Stores

CSS,

JavaScript,

images,

fonts,

and static assets.

Very fast.

No network request.

______________________________________________________________________

# CDN Cache

Stores

static content

near users.

Example

```
Image

↓

Nearest Edge Server
```

______________________________________________________________________

# Application Cache

Sometimes

applications

store

frequently used objects

in memory.

Example

Python dictionary

Java ConcurrentHashMap

Useful

for small deployments.

Not shared

between servers.

______________________________________________________________________

# Distributed Cache

Most production systems

use

Redis

or

Memcached.

```
Application A

↓

Redis

↑

Application B
```

All servers

share

the same cache.

______________________________________________________________________

# Cache Expiration (TTL)

Caches

cannot

store data forever.

Example

```
TTL

=

10 Minutes
```

After

10 minutes,

the entry

expires.

The next request

retrieves

fresh data

from the database.

______________________________________________________________________

# Cache Invalidation

One of the hardest problems

in software engineering

is

keeping

cached data

consistent.

Example

```
User Name

↓

Database Updated
```

Cache

still contains

old value.

Problem.

Solutions

- Delete cache
- Update cache
- Short TTL

______________________________________________________________________

# Write-Through Cache

Flow

```
Application

↓

Cache

↓

Database
```

Data

is written

to

both

cache

and

database.

Advantages

- Cache always fresh

Disadvantages

- Slightly slower writes

______________________________________________________________________

# Write-Behind Cache (Write-Back)

Flow

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

Advantages

- Very fast writes

Disadvantages

- Risk of data loss if cache fails before persistence

Used carefully

in high-throughput systems.

______________________________________________________________________

# Cache-Aside (Lazy Loading)

Most common strategy.

Flow

```
Application

↓

Check Cache

↓

Miss

↓

Database

↓

Store In Cache

↓

Return
```

Advantages

- Simple
- Efficient

Disadvantages

- First request is slower

______________________________________________________________________

# Read-Through Cache

Application

never talks

directly

to the database.

```
Application

↓

Cache

↓

Database
```

The cache

retrieves

missing data

automatically.

Less common

than Cache-Aside.

______________________________________________________________________

# Comparison

| Strategy | Reads | Writes | Common? |
|----------|--------|---------|----------|
| Cache-Aside | App manages cache | Database | ✅ Most Common |
| Read-Through | Cache manages reads | Database | Moderate |
| Write-Through | Cache + DB together | Immediate | Common |
| Write-Behind | Cache first | Async DB write | Specialized |

For interviews,

Cache-Aside

is usually

the default answer.

______________________________________________________________________

# Redis

Redis

is

the most common

distributed cache.

Features

- In-memory
- Extremely fast
- TTL support
- Pub/Sub
- Data structures
- Replication
- Persistence options

We'll study

Redis

in a dedicated chapter.

______________________________________________________________________

# Memcached

Another

popular cache.

Simpler than Redis.

Supports

- Key-value storage
- In-memory caching

No advanced data structures.

______________________________________________________________________

# Eviction Policies

Suppose

memory

is full.

Which entry

should be removed?

Common policies

- LRU (Least Recently Used)
- LFU (Least Frequently Used)
- FIFO (First In First Out)
- Random

LRU

is the most commonly discussed

in interviews.

______________________________________________________________________

# Cache Stampede

Problem

A cache entry

expires.

Thousands

of requests

arrive

simultaneously.

Every request

hits

the database.

```
Cache Expired

↓

1000 Requests

↓

Database Overloaded
```

Solutions

- Mutex locking
- Request coalescing
- Staggered TTL
- Background refresh

______________________________________________________________________

# Cache Penetration

Problem

Users repeatedly request

non-existent data.

```
Invalid Key

↓

Cache Miss

↓

Database

↓

Repeat Forever
```

Solutions

- Cache null values
- Bloom Filters

______________________________________________________________________

# Cache Avalanche

Problem

Thousands

of cache entries

expire

at exactly

the same time.

Database

gets overwhelmed.

Solution

Randomize TTL values.

______________________________________________________________________

# Where Does Cache Fit?

Typical architecture

```
Users

↓

DNS

↓

CDN

↓

Load Balancer

↓

Application

↓

Redis

↓

Database

↓

Object Storage
```

______________________________________________________________________

# Common Interview Questions

## Why not cache everything?

Because

some data

changes frequently,

is user-specific,

or requires strong consistency.

______________________________________________________________________

## Why Redis instead of a database?

Redis stores data

in memory,

making reads

much faster

than disk-based databases.

______________________________________________________________________

## When should cache be invalidated?

Whenever

the underlying data

changes

or

after the TTL expires,

depending on the consistency requirements.

______________________________________________________________________

## What happens if Redis crashes?

The application

falls back

to the database.

Performance decreases,

but the system

continues working.

High-availability Redis

reduces this risk.

______________________________________________________________________

# Common Mistakes

## Caching Frequently Changing Data

Frequent updates

can make the cache

less effective

and harder to keep consistent.

______________________________________________________________________

## Ignoring TTL

Without expiration,

stale data

may be served indefinitely.

______________________________________________________________________

## Assuming Cache Is The Source Of Truth

The database

remains

the source of truth.

The cache

is an optimization layer.

______________________________________________________________________

## Forgetting Cache Invalidation

A fast system

serving incorrect data

is still

a bad system.

______________________________________________________________________

# Best Practices

✅ Cache frequently read data.

✅ Keep the database as the source of truth.

✅ Use appropriate TTL values.

✅ Monitor cache hit ratio.

✅ Handle cache failures gracefully.

✅ Use Cache-Aside as the default strategy unless another approach is clearly justified.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is Redis commonly used for caching?

### Answer

Redis stores data entirely in memory, providing extremely low-latency access. It supports TTL, replication, multiple
data structures, and high throughput, making it an excellent choice for distributed caching.

______________________________________________________________________

## Question

What is the most common caching strategy?

### Answer

Cache-Aside (Lazy Loading). The application checks the cache first. On a cache miss, it retrieves the data from the
database, stores it in the cache, and returns it to the client.

______________________________________________________________________

## Question

What is the biggest challenge with caching?

### Answer

Maintaining consistency between the cache and the underlying database. Cache invalidation, expiration policies, and
handling stale data are among the most common challenges.

______________________________________________________________________

# Practice Exercise

For each application,

answer the following.

1. What data should be cached?
1. Which caching strategy would you use?
1. Appropriate TTL values.
1. What happens on a cache miss?
1. How would you invalidate the cache?
1. What cache-related failure scenarios should be considered?

Applications

- Instagram
- YouTube
- WhatsApp
- Netflix
- Food Delivery
- Banking System
- URL Shortener

______________________________________________________________________

# Summary

Caching is one of the most effective techniques for improving system performance.

It

- Reduces database load
- Lowers latency
- Improves scalability
- Handles traffic spikes
- Enhances user experience

Understanding cache strategies, expiration policies, invalidation, and common failure scenarios is essential for
designing scalable systems and succeeding in System Design interviews.

______________________________________________________________________

# Next

[Redis Deep Dive](09-redis.md)
