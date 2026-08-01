# Redis URL Shortener Project - Part 3

## Introduction

In Part 2, we added analytics to our URL Shortener.

Current features:

- URL Shortening
- URL Lookup
- Click Counter
- Metadata
- Top URLs
- Unique Visitors

Now we'll make the application much closer to what you would see in a real backend service.

We'll implement:

- Caching
- Rate Limiting
- Pipelines
- Transactions
- Batch Operations
- Connection Pool Review
- Performance Optimizations

These are some of the most common Redis patterns used in production.

______________________________________________________________________

# Current Architecture

```text id="redis301"
                Client

                  │

                  ▼

              FastAPI

                  │

                  ▼

               Redis
```

Every request currently performs multiple Redis commands.

Let's optimize that.

______________________________________________________________________

# Why Caching?

Imagine the application frequently needs application settings.

Without cache

```text id="redis302"
Request

↓

Database

↓

Response
```

With Redis

```text id="redis303"
Request

↓

Redis

↓

Response
```

Much faster.

Although this project stores data directly in Redis, the same caching pattern is used in applications backed by
PostgreSQL or other databases.

______________________________________________________________________

# Cache Lookup Pattern

Typical flow

```text id="redis304"
Request

↓

Redis

↓

Cache Hit?

├── Yes

│     ↓

│   Return

│

└── No

      ↓

 Database

      ↓

 Save to Redis

      ↓

 Return
```

This is known as the **Cache-Aside Pattern**.

______________________________________________________________________

# Example Cache Function

```python id="redis305"
def get_url(

    code

):

    url = client.get(

        f"url:{code}"

    )

    if url is None:

        return None

    return url
```

Since URLs are already stored in Redis,

lookups are extremely fast.

______________________________________________________________________

# Why Pipelines?

Suppose

one redirect performs

```text id="redis306"
GET

INCR

HSET

ZINCRBY

SADD
```

Five network round trips.

______________________________________________________________________

# Redis Pipeline

Instead

```python id="redis307"
pipe = client.pipeline()

pipe.incr(

    f"clicks:{code}"

)

pipe.hset(

    f"url_meta:{code}",

    "last_access",

    current_time

)

pipe.zincrby(

    "top_urls",

    1,

    code

)

pipe.sadd(

    f"visitors:{code}",

    user_id

)

pipe.execute()
```

All commands are sent together,

reducing network overhead.

______________________________________________________________________

# Updated Redirect Flow

```text id="redis308"
GET URL

↓

Pipeline

↓

Update Analytics

↓

Return URL
```

Much more efficient than executing each command separately.

______________________________________________________________________

# Redis Transactions

Redis supports transactional execution using `MULTI` and `EXEC`.

With `redis-py`, this is commonly done using a transactional pipeline.

```python id="redis309"
pipe = client.pipeline(
    transaction=True
)

pipe.incr(
    "counter"
)

pipe.incr(
    "counter"
)

pipe.execute()
```

The queued commands execute together when `execute()` is called.

> **Note:** Redis transactions execute queued commands atomically, but they do not provide rollback semantics like SQL transactions. If a command fails due to an application-level issue (for example, a type error), previously executed commands are not automatically undone.

______________________________________________________________________

# Batch Delete

Suppose expired URLs need removal.

```python id="redis310"
pipe = client.pipeline()

for code in codes:

    pipe.delete(

        f"url:{code}"

    )

pipe.execute()
```

One network request.

Many deletes.

______________________________________________________________________

# Multiple Reads

Instead of

```python id="redis311"
client.get("url:1")

client.get("url:2")

client.get("url:3")
```

Use

```python id="redis312"
client.mget(

    [

        "url:1",

        "url:2",

        "url:3"

    ]

)
```

Efficient batch retrieval.

______________________________________________________________________

# Multiple Writes

Instead of

```python id="redis313"
client.set(

    "url:1",

    "..."

)

client.set(

    "url:2",

    "..."
)
```

Use

```python id="redis314"
client.mset(

    {

        "url:1":"...",

        "url:2":"..."

    }

)
```

______________________________________________________________________

# Rate Limiting

Suppose

one client sends

1000 requests per second.

We need protection.

______________________________________________________________________

# Simple Rate Limiter

```python id="redis315"
key = f"rate:{ip}"

count = client.incr(
    key
)

if count == 1:

    client.expire(
        key,
        60
    )

if count > 100:

    raise Exception(
        "Rate Limit Exceeded"
    )
```

Each IP gets

100 requests

per minute.

______________________________________________________________________

# Why Expire?

Without expiration

```text id="redis316"
rate:192.168.1.10
```

would remain forever.

With TTL

↓

Automatic cleanup.

______________________________________________________________________

# Connection Pool Review

Current implementation

```python id="redis317"
pool = redis.ConnectionPool(

    host="localhost",

    port=6379,

    db=0,

    decode_responses=True

)
```

Advantages

- Reuse connections
- Lower latency
- Better throughput
- Lower CPU usage

______________________________________________________________________

# Performance Improvements

Current redirect

```text id="redis318"
GET

↓

INCR

↓

HSET

↓

SADD

↓

ZINCRBY
```

Optimized

```text id="redis319"
GET

↓

Pipeline

↓

Everything Updated
```

Fewer network round trips.

______________________________________________________________________

# Complete Flow

```text id="redis320"
Request

↓

Lookup URL

↓

Pipeline

├── Increment Counter

├── Update Last Access

├── Add Visitor

└── Update Ranking

↓

Return URL
```

______________________________________________________________________

# Common Mistakes

### No Connection Pool

Creates unnecessary TCP connections.

______________________________________________________________________

### No Pipeline

Increases network latency.

______________________________________________________________________

### Forgetting TTL

Temporary keys accumulate forever.

______________________________________________________________________

### Storing Everything in Strings

Redis provides specialized data structures for different use cases.

______________________________________________________________________

### Ignoring Batch Operations

Use `MGET`, `MSET`, and pipelines where appropriate.

______________________________________________________________________

# Best Practices

- Reuse Redis connections.
- Use pipelines for related commands.
- Batch reads and writes when possible.
- Set TTL on temporary keys.
- Use atomic operations like `INCR`.
- Keep key names consistent.

______________________________________________________________________

# Hands-on Exercise

1. Add rate limiting to the `/shorten` endpoint.
1. Use a pipeline for every redirect.
1. Batch delete expired URLs.
1. Retrieve multiple URLs using `MGET`.
1. Store multiple URLs using `MSET`.
1. Display the remaining TTL for temporary URLs.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should Redis pipelines be used in high-performance applications?

Each Redis command normally requires a separate network round trip between the application and the Redis server.
Pipelines allow multiple commands to be sent together and processed in sequence before receiving the responses,
significantly reducing network latency and improving throughput. They are especially useful when several independent
Redis operations are performed as part of a single request.

______________________________________________________________________

# Summary

In this chapter, you implemented:

- Cache-aside pattern
- Redis pipelines
- Redis transactions
- Batch operations
- `MGET`
- `MSET`
- Rate limiting
- Connection pool review
- Performance optimizations

The URL Shortener now demonstrates several production-ready Redis usage patterns.

______________________________________________________________________

## Next File

[7-redis-url-shortener-project-part-4.md](7-redis-url-shortener-project-part-4.md)
