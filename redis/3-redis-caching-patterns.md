# Redis Caching Patterns & Expiration

## Introduction

Redis is used in production primarily as a **cache**.

Caching reduces:

- Database load
- API response time
- Network latency
- Infrastructure cost

A properly designed cache can reduce response times from **hundreds of milliseconds** to **a few milliseconds**.

However, caching introduces new challenges:

- Cache invalidation
- Stale data
- Cache stampede
- Cache penetration
- Cache avalanche

Understanding these patterns is one of the most important Redis interview topics.

In this chapter, you'll learn:

- What caching is
- Cache lifecycle
- Cache-Aside Pattern
- Write-Through Cache
- Write-Behind Cache
- Read-Through Cache
- TTL strategies
- Cache Invalidation
- Cache Stampede
- Cache Penetration
- Cache Avalanche
- Python (`redis-py`) examples
- FastAPI integration
- Production best practices

______________________________________________________________________

# What is Caching?

Without cache

```text id="cache001"
Client

↓

API

↓

PostgreSQL

↓

API

↓

Client
```

Every request reaches the database.

______________________________________________________________________

With Redis

```text id="cache002"
Client

↓

API

↓

Redis

↓

Cache Hit?

↓

Yes

↓

Return

↓

No

↓

PostgreSQL

↓

Redis

↓

Client
```

Much faster.

______________________________________________________________________

# Cache Hit

Requested data already exists.

```text id="cache003"
Redis

↓

Data Found

↓

Return
```

Fast.

______________________________________________________________________

# Cache Miss

Requested data does not exist.

```text id="cache004"
Redis

↓

No Data

↓

Database

↓

Redis

↓

Return
```

______________________________________________________________________

# Cache Lifecycle

```text id="cache005"
Request

↓

Redis

↓

Miss

↓

Database

↓

Redis

↓

Client

↓

TTL Expires

↓

Removed
```

______________________________________________________________________

# Cache-Aside Pattern (Lazy Loading)

The most popular caching strategy.

Flow

```text id="cache006"
Request

↓

Redis

↓

Miss?

↓

Database

↓

Store In Redis

↓

Return
```

______________________________________________________________________

## Redis CLI Example

Store product

```bash id="cache007"
SET product:1 \
'{"id":1,"name":"Laptop"}' \
EX 300
```

Retrieve

```bash id="cache008"
GET product:1
```

______________________________________________________________________

## Python Example

```python id="cache009"
import json
import redis

client = redis.Redis(
    decode_responses=True
)

def get_product(product_id: int):

    key = f"product:{product_id}"

    cached = client.get(key)

    if cached:
        return json.loads(cached)

    product = fetch_product_from_database(product_id)

    client.set(
        key,
        json.dumps(product),
        ex=300
    )

    return product
```

______________________________________________________________________

## Advantages

- Simple
- Database remains source of truth
- Most common production pattern

______________________________________________________________________

## Disadvantages

- First request is always slower.
- Cache misses still hit the database.

______________________________________________________________________

# Write-Through Cache

Flow

```text id="cache010"
Application

↓

Redis

↓

Database
```

Every write updates:

- Redis
- Database

Example

```python id="cache011"
def update_user(user):

    update_database(user)

    client.set(
        f"user:{user.id}",
        json.dumps(user),
        ex=600
    )
```

Advantages

- Cache always updated immediately after writes.

Disadvantages

- Every write performs additional cache work.
- Unused cached values may consume memory.

______________________________________________________________________

# Write-Behind (Write-Back)

Flow

```text id="cache012"
Application

↓

Redis

↓

Immediate Response

↓

Database Later
```

Redis acknowledges the write first.

The database is updated asynchronously.

Advantages

- Extremely fast writes.

Disadvantages

- Risk of data loss if the cache fails before data reaches the database.
- Increased implementation complexity.

______________________________________________________________________

# Read-Through Cache

Application

↓

Cache

↓

Database

Unlike Cache-Aside, the application interacts with the cache layer, which automatically loads missing data.

Common in managed caching solutions but less common with plain Redis.

______________________________________________________________________

# Time-To-Live (TTL)

Every cache entry should usually expire.

CLI

```bash id="cache013"
SET product:1 Laptop EX 300
```

Python

```python id="cache014"
client.set(
    "product:1",
    "Laptop",
    ex=300
)
```

______________________________________________________________________

# Choosing a TTL

Examples

| Data | TTL |
| --------------- | ---------------: |
| OTP | 5 minutes |
| Product Catalog | 5–30 minutes |
| User Profile | 10–60 minutes |
| Weather | 5–15 minutes |
| Feature Flags | Hours |
| Session | Session lifetime |

TTL depends on how frequently the data changes.

______________________________________________________________________

# Cache Invalidation

Interview favorite.

Cache invalidation means removing or updating stale cache entries when underlying data changes.

Example

```python id="cache015"
update_product(product)

client.delete(
    f"product:{product.id}"
)
```

The next read reloads fresh data from the database.

______________________________________________________________________

# Updating Cache Instead of Deleting

Sometimes updating the cache is preferable.

```python id="cache016"
client.set(
    f"user:{user.id}",
    json.dumps(user),
    ex=600
)
```

Useful when updated data is immediately needed.

______________________________________________________________________

# Cache Stampede

Problem

Suppose

```text id="cache017"
10,000

requests
```

Cache expires.

Every request simultaneously queries PostgreSQL.

Database overload.

______________________________________________________________________

# Solution 1

Random TTL

Instead of

```text id="cache018"
300 seconds
```

Use

```text id="cache019"
300–360 seconds
```

Example

```python id="cache020"
import random

client.set(
    key,
    value,
    ex=300 + random.randint(0, 60)
)
```

Different keys expire at slightly different times.

______________________________________________________________________

# Solution 2

Distributed Lock

Only one request rebuilds the cache.

Others wait or use stale data temporarily.

We'll cover distributed locks in a later lecture.

______________________________________________________________________

# Cache Penetration

Problem

Requests ask for

```text id="cache021"
product:999999999
```

which doesn't exist.

Every request hits the database.

______________________________________________________________________

# Solution

Cache negative results.

Example

```python id="cache022"
if product is None:

    client.set(
        key,
        "NOT_FOUND",
        ex=60
    )
```

Subsequent requests avoid unnecessary database queries.

______________________________________________________________________

# Cache Avalanche

Problem

Thousands of keys expire at exactly the same moment.

Database receives a huge burst of requests.

______________________________________________________________________

# Solutions

- Randomized TTL
- Staggered expiration
- Pre-warming caches
- Multi-level caching

______________________________________________________________________

# Cache Warm-Up

Instead of waiting for user requests,

populate the cache during deployment or startup.

Example

```python id="cache023"
products = fetch_all_products()

for product in products:

    client.set(
        f"product:{product.id}",
        json.dumps(product),
        ex=600
    )
```

Useful for frequently accessed reference data.

______________________________________________________________________

# FastAPI Example

```python id="cache024"
from fastapi import FastAPI
import json
import redis

app = FastAPI()

client = redis.Redis(
    decode_responses=True
)

@app.get("/products/{product_id}")
def get_product(product_id: int):

    key = f"product:{product_id}"

    cached = client.get(key)

    if cached:
        return json.loads(cached)

    product = fetch_product_from_database(product_id)

    client.set(
        key,
        json.dumps(product),
        ex=300
    )

    return product
```

This is a classic Cache-Aside implementation.

______________________________________________________________________

# Monitoring Cache Performance

Important metrics

- Cache Hit Ratio
- Cache Miss Ratio
- Average Response Time
- Redis Memory Usage
- Eviction Count
- Database Query Rate

A low cache hit ratio often indicates ineffective caching.

______________________________________________________________________

# Common Mistakes

### Never Expiring Cache

Stale data remains indefinitely.

______________________________________________________________________

### Using Very Long TTLs

Data may become outdated.

______________________________________________________________________

### Using Very Short TTLs

Frequent cache misses increase database load.

______________________________________________________________________

### Caching Everything

Not all data benefits from caching.

Focus on:

- Frequently accessed
- Expensive to compute
- Rarely changing

______________________________________________________________________

### Ignoring Cache Failures

Applications should continue working even if Redis is temporarily unavailable.

Redis is usually a performance optimization, not the system of record.

______________________________________________________________________

# Best Practices

- Use Cache-Aside for most applications.
- Set appropriate TTLs.
- Randomize expiration times.
- Monitor hit ratio.
- Handle cache failures gracefully.
- Invalidate stale cache entries after updates.
- Keep the database as the source of truth.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between Cache-Aside and Write-Through caching?

In the Cache-Aside pattern, the application first checks Redis. If the data is missing, it loads the data from the
database, stores it in Redis, and returns it. The cache is populated only when needed. In Write-Through caching, every
write updates both the database and Redis immediately, ensuring the cache stays synchronized after writes. Cache-Aside
is simpler and more commonly used, while Write-Through provides fresher cached data at the cost of additional write
overhead.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is caching?
1. What is a cache hit?
1. What is a cache miss?
1. Explain Cache-Aside.
1. Explain Write-Through.
1. Explain Write-Behind.
1. Explain Read-Through.
1. What is TTL?
1. What is cache invalidation?
1. What is cache stampede?
1. What is cache penetration?
1. What is cache avalanche?

## Coding

1. Implement Cache-Aside using `redis-py`.
1. Cache a user profile.
1. Delete cached data after an update.
1. Add randomized TTL values.
1. Cache negative lookups.
1. Pre-warm a product cache.

______________________________________________________________________

# Hands-on Exercise

Build a Product Cache Service.

Requirements:

1. Retrieve products from Redis.
1. Load from PostgreSQL on cache misses.
1. Cache results with a TTL.
1. Invalidate cache after product updates.
1. Randomize expiration times.
1. Cache "not found" results.
1. Measure cache hit ratio.
1. Test behavior when Redis is unavailable.

______________________________________________________________________

# Cheat Sheet

```text id="cache025"
Cache Hit

↓

Cache Miss

↓

Cache-Aside

↓

Write-Through

↓

Write-Behind

↓

Read-Through

↓

TTL

↓

Cache Invalidation

↓

Cache Stampede

↓

Cache Penetration

↓

Cache Avalanche
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Redis caching fundamentals
- Cache lifecycle
- Cache-Aside pattern
- Write-Through caching
- Write-Behind caching
- Read-Through caching
- TTL strategies
- Cache invalidation
- Cache stampede
- Cache penetration
- Cache avalanche
- FastAPI caching integration
- Monitoring cache performance
- Production best practices
- Interview patterns

You now understand how caching works in production systems, how to choose an appropriate caching strategy, and how to
avoid the most common caching pitfalls.

______________________________________________________________________

## Next File

[4-redis-pubsub-streams-transactions.md](4-redis-pubsub-streams-transactions.md)
