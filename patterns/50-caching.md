# System Design - Part 50

# Caching

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Caching is
- Why Caching exists
- Cache Hit vs Cache Miss
- Types of Caches
- Cache-Aside Pattern
- Read-Through Cache
- Write-Through Cache
- Write-Back Cache
- Cache Eviction Policies
- Redis examples
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

has become

very popular.

Every user

opens

the homepage.

Each request

loads

the list

of

popular books.

Every request

queries

the database.

Initially,

everything works.

Until...

______________________________________________________________________

# The Problem

Suppose

100,000 users

request

the same data.

```text id="cache5001"
Users

↓

Application

↓

Database
```

The database

receives

100,000

identical queries.

CPU increases.

Latency increases.

Costs increase.

The same data

is fetched

again

and again.

______________________________________________________________________

# The Idea

Instead of

fetching

the same data

from

the database

every time,

store it

in

fast memory.

Future requests

reuse

that copy.

______________________________________________________________________

# What is a Cache?

A **Cache**

is

a high-speed

temporary storage

used

to store

frequently accessed data

so that

future requests

can be served

much faster.

______________________________________________________________________

# Architecture

Without Cache

```text id="cache5002"
Client

↓

Application

↓

Database
```

With Cache

```text id="cache5003"
Client

↓

Application

↓

Cache

↓

Database
```

Most requests

never reach

the database.

______________________________________________________________________

# Cache Hit

Suppose

the requested data

already exists

inside

the cache.

```text id="cache5004"
Application

↓

Cache

↓

Found
```

This is called

a

**Cache Hit**.

The response

is returned

immediately.

______________________________________________________________________

# Cache Miss

Suppose

the data

is not

in

the cache.

```text id="cache5005"
Application

↓

Cache

↓

Not Found

↓

Database
```

The application

loads

the data

from

the database,

stores it

in the cache,

and

returns it.

This is called

a

**Cache Miss**.

______________________________________________________________________

# Cache Hit Ratio

One of

the most important

cache metrics.

Formula

```text id="cache5006"
Cache Hits

──────────────

Total Requests
```

Example

900 Hits

100 Misses

↓

90% Hit Ratio

Higher

is usually better.

______________________________________________________________________

# Why Redis?

Redis

is

the most popular

cache

because it is:

- In-memory
- Extremely fast
- Supports TTL
- Supports data structures
- Easy to scale

Redis

can respond

in

microseconds,

whereas

a database query

may take

milliseconds.

______________________________________________________________________

# Cache-Aside Pattern

The most common

interview question.

Workflow

```text id="cache5007"
Application

↓

Cache

↓

Miss

↓

Database

↓

Store in Cache

↓

Return Response
```

The application

manages

the cache.

______________________________________________________________________

# FastAPI Example

```python id="cache5008"
book = redis.get(book_id)

if not book:

    book = database.get(book_id)

    redis.set(book_id, book)
```

Simple.

Effective.

Widely used.

______________________________________________________________________

# Read-Through Cache

Instead of

the application

loading data,

the cache

loads it

automatically.

Workflow

```text id="cache5009"
Application

↓

Cache

↓

Database
```

The application

never talks

to

the database

directly.

______________________________________________________________________

# Write-Through Cache

When

data changes,

write

to

both

the cache

and

the database

at

the same time.

Workflow

```text id="cache5010"
Application

↓

Cache

↓

Database
```

Benefits:

- Cache

always stays

up to date.

Drawback:

- Slower writes.

______________________________________________________________________

# Write-Back Cache

Also called

**Write-Behind Cache**.

Workflow

```text id="cache5011"
Application

↓

Cache

↓

Return Success

↓

Later

↓

Database
```

Writes

are very fast,

but

there is

a risk

of data loss

if

the cache fails

before

writing

to

the database.

______________________________________________________________________

# Cache Eviction

Caches

have

limited memory.

Eventually,

something

must be removed.

______________________________________________________________________

# Least Recently Used (LRU)

Remove

the item

that hasn't

been used

for

the longest time.

Most common

interview answer.

______________________________________________________________________

# Least Frequently Used (LFU)

Remove

the item

that is

used

least often.

Useful

when

popular data

should stay

in memory.

______________________________________________________________________

# FIFO

Remove

the oldest

cached item.

Simple,

but

less common

for

high-performance caches.

______________________________________________________________________

# Time-To-Live (TTL)

Sometimes,

data

expires

automatically.

Example

```text id="cache5012"
TTL = 5 Minutes
```

After

5 minutes,

the cache

removes

the item.

Next request

reloads

fresh data.

______________________________________________________________________

# Cache Invalidation

One of

the hardest

problems

in software engineering.

Suppose

a book

changes price.

The database

updates.

Should

the cache

still return

the old price?

No.

The cached value

must be

invalidated

or

updated.

______________________________________________________________________

# Example

Update Book

↓

Delete Cache

↓

Next Request

↓

Load Fresh Data

This is

the most common

cache invalidation strategy.

______________________________________________________________________

# Distributed Cache

Suppose

you have

10 application servers.

Each server

uses

its own

local cache.

Now,

Server 1

updates data.

Servers 2–10

still have

stale copies.

Instead,

share

one Redis cluster.

```text id="cache5013"
App 1

↓

Redis
```

```text id="cache5014"
App 2

↓

Redis
```

Everyone

uses

the same cache.

______________________________________________________________________

# CDN vs Cache

Interview favorite.

| Cache | CDN |
| ----------------------- | ------------------- |
| Stores application data | Stores static files |
| Redis | Cloudflare |
| Usually internal | Global edge network |

CDNs

cache

images,

videos,

CSS,

and

JavaScript.

Redis

caches

application data.

______________________________________________________________________

# Local Cache vs Distributed Cache

| Local Cache | Distributed Cache |
| ---------------------- | ------------------------------ |
| Inside one application | Shared by many applications |
| Fastest | Consistent across servers |
| Doesn't scale well | Better for distributed systems |

Examples

Local Cache

- Python dictionary
- LRU Cache

Distributed Cache

- Redis
- Memcached

______________________________________________________________________

# AI/ML Example

Suppose

users

ask

the same prompt

repeatedly.

```text id="cache5015"
"What is Python?"
```

Instead

of

calling

the LLM

every time,

cache

the response.

Benefits:

- Lower latency
- Lower API cost
- Reduced GPU usage

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce site.

Popular products

rarely change

every second.

Store

them

in Redis.

Most requests

avoid

the database,

reducing

load dramatically.

______________________________________________________________________

# Cache Stampede

Suppose

one cached item

expires.

Suddenly,

100,000 users

request it.

All requests

miss

the cache

simultaneously.

Every request

hits

the database.

This is called

a

**Cache Stampede**.

______________________________________________________________________

# Preventing Cache Stampede

Common techniques:

- Request Coalescing
- Distributed Locks
- Early Refresh
- Randomized TTL

We'll study

these

in advanced

system design.

______________________________________________________________________

# Benefits

Caching provides:

✅ Lower latency

✅ Reduced database load

✅ Lower infrastructure costs

✅ Higher throughput

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Stale data

❌ Cache invalidation

❌ Memory limits

❌ Additional infrastructure

______________________________________________________________________

# Real Company Example

Streaming platforms

cache

movie metadata,

user profiles,

and

recommendations

using

Redis,

allowing

millions

of requests

to be served

without

constantly querying

the database.

______________________________________________________________________

# When NOT to Use Caching

Avoid caching

when:

- Data changes constantly
- Strong consistency

is required

for every read

- The cost

of stale data

is unacceptable

Examples:

- Bank balances
- Payment confirmation

______________________________________________________________________

# Best Practices

✅ Cache frequently read data.

✅ Set appropriate TTLs.

✅ Monitor hit ratio.

✅ Invalidate stale entries.

______________________________________________________________________

# Common Mistakes

### Caching Everything

Not all data

benefits

from caching.

Cache

what is

expensive

to compute

or retrieve.

______________________________________________________________________

### Infinite TTL

Cached data

must eventually

expire

or

be invalidated.

______________________________________________________________________

### Ignoring Cache Misses

Always design

for

cache misses.

The database

remains

the source

of truth.

______________________________________________________________________

### Treating Cache as Permanent Storage

Caches

are temporary.

Never rely

on them

as

your only

copy of data.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is caching, and why is Redis commonly used?

Caching is the practice of storing frequently accessed data in fast memory so future requests can be served without
repeatedly querying slower storage systems such as databases. Redis is commonly used because it is an in-memory data
store that offers extremely low latency, supports TTLs, rich data structures, and horizontal scaling. Effective caching
reduces database load, improves response times, and increases system throughput, but requires careful cache invalidation
and consistency management.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Caching is
- Cache Hit vs Cache Miss
- Cache-Aside
- Read-Through
- Write-Through
- Write-Back
- Cache Eviction Policies
- Redis
- Cache Stampede
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand two of the most important building blocks:

- ✅ Load Balancers
- ✅ Caching

These two components alone are responsible for handling a massive percentage of web-scale traffic efficiently.

______________________________________________________________________

# What's Next

[Content Delivery Network (CDN)](51-content-delivery-network.md)
