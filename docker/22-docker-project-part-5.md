# Docker - Part 22

# Docker Project - Part 5

# Integrating Redis Caching

______________________________________________________________________

# Introduction

Our application now performs all CRUD operations using PostgreSQL.

That's correct,

but there's a problem.

Suppose

10,000 users

request the same book.

```text id="cache001"
GET /books/1

↓

PostgreSQL

↓

GET /books/1

↓

PostgreSQL

↓

GET /books/1

↓

PostgreSQL
```

The database executes the same query thousands of times.

This is inefficient.

Redis solves this problem.

______________________________________________________________________

# Caching Strategy

Our application will use the

**Cache-Aside Pattern**,

which is one of the most common caching strategies.

```text id="cache002"
Client

↓

Redis

│

├── Hit

│      ↓

│   Return Response

│

└── Miss

       ↓

 PostgreSQL

       ↓

 Save to Redis

       ↓

 Return Response
```

______________________________________________________________________

# Project Structure

We add one file.

```text id="cache003"
app/

├── cache.py

├── crud.py

├── routes.py

└── ...
```

______________________________________________________________________

# Install Redis Client

`requirements.txt`

```text id="cache004"
redis[hiredis]
```

We'll continue using the modern

**redis-py**

library.

______________________________________________________________________

# Redis Configuration

Create

```text id="cache005"
cache.py
```

______________________________________________________________________

# Reading Configuration

```python id="cache006"
import os

REDIS_URL = os.getenv(
    "REDIS_URL"
)
```

Configuration remains external.

______________________________________________________________________

# Creating the Client

```python id="cache007"
from redis import Redis

client = Redis.from_url(

    REDIS_URL,

    decode_responses=True

)
```

The client is created once

and reused.

______________________________________________________________________

# Why decode_responses?

Without it,

Redis returns

```text id="cache008"
bytes
```

Example

```python id="cache009"
b"Clean Code"
```

With

```python id="cache010"
decode_responses=True
```

you receive

```python id="cache011"
"Clean Code"
```

Much easier to work with.

______________________________________________________________________

# Cache Keys

We'll use

```text id="cache012"
book:1

book:2

book:3
```

Pattern

```text id="cache013"
resource:id
```

This keeps Redis organized.

______________________________________________________________________

# Cache Helper

```python id="cache014"
def book_key(
    book_id: int
) -> str:

    return f"book:{book_id}"
```

Now

every endpoint

uses the same key format.

______________________________________________________________________

# Caching Books

Redis stores strings,

so we'll serialize

our model.

```python id="cache015"
import json


def cache_book(book):

    client.set(

        book_key(book.id),

        json.dumps(

            book.model_dump()

        )

    )
```

______________________________________________________________________

# Reading Cache

```python id="cache016"
import json


def get_cached_book(
    book_id: int
):

    data = client.get(

        book_key(book_id)

    )

    if data is None:

        return None

    return json.loads(data)
```

______________________________________________________________________

# Cache Flow

```text id="cache017"
Request

↓

Redis

↓

Hit?

│

├── Yes

│      ↓

│   Return

│

└── No

       ↓

 Database

       ↓

 Cache Result

       ↓

 Return
```

______________________________________________________________________

# Updating GET Endpoint

Current flow

```text id="cache018"
GET

↓

Database
```

New flow

```text id="cache019"
GET

↓

Redis

↓

Database

↓

Redis
```

______________________________________________________________________

# Example

```python id="cache020"
cached = get_cached_book(
    book_id
)

if cached:

    return cached

book = get_book(
    session,
    book_id
)

if book:

    cache_book(book)

return book
```

The database

is queried

only on a cache miss.

______________________________________________________________________

# Cache Invalidation

Suppose

a book changes.

```text id="cache021"
Database

↓

Updated

↓

Old Cache
```

Now

Redis contains

stale data.

______________________________________________________________________

# Solution

Whenever

a book changes,

remove

its cache.

```python id="cache022"
def invalidate_book(
    book_id: int
):

    client.delete(

        book_key(book_id)

    )
```

______________________________________________________________________

# When Should We Invalidate?

Whenever

```text id="cache023"
Create

Update

Delete

Borrow

Return
```

changes data,

the cache must be refreshed or invalidated.

______________________________________________________________________

# Update Flow

```text id="cache024"
Update Book

↓

Database

↓

Delete Cache

↓

Next Request

↓

Reload Cache
```

This is still

the Cache-Aside pattern.

______________________________________________________________________

# Using Expiration

Instead of

keeping cache forever,

set

a TTL.

```python id="cache025"
client.set(

    book_key(book.id),

    json.dumps(

        book.model_dump()

    ),

    ex=300
)
```

Meaning

```text id="cache026"
300 Seconds

↓

Automatically Remove
```

______________________________________________________________________

# Why TTL?

Suppose

cache invalidation

fails.

Eventually,

expired entries

disappear automatically.

TTL also prevents stale data from living forever.

______________________________________________________________________

# Measuring Performance

Without Redis

```text id="cache027"
Request

↓

Database

↓

12 ms
```

With Redis

```text id="cache028"
Request

↓

Redis

↓

1 ms
```

Actual numbers vary,

but Redis is generally much faster than querying a relational database.

______________________________________________________________________

# Health Check

Add Redis verification.

```python id="cache029"
client.ping()
```

Expected

```text id="cache030"
True
```

Useful for readiness checks.

______________________________________________________________________

# Request Lifecycle

```text id="cache031"
Client

↓

FastAPI

↓

Redis

│

├── Hit

│

└── Miss

      ↓

 PostgreSQL

↓

Cache

↓

Response
```

______________________________________________________________________

# Current Architecture

```text id="cache032"
Browser

↓

FastAPI

│

├── Redis

│

└── PostgreSQL
```

Kafka

will be integrated

next.

______________________________________________________________________

# Common Mistakes

### Never Invalidating Cache

The application returns stale data.

______________________________________________________________________

### Using Random Cache Keys

Adopt a consistent naming convention.

______________________________________________________________________

### Forgetting TTL

Long-lived cache entries can become stale if invalidation fails.

______________________________________________________________________

### Caching Everything

Cache frequently accessed or expensive-to-compute data,

not every query.

______________________________________________________________________

# Best Practices

- Use the Cache-Aside pattern.
- Use consistent cache keys.
- Set reasonable TTL values.
- Invalidate cache after updates.
- Cache only useful data.
- Keep Redis configuration in environment variables.

______________________________________________________________________

# Hands-on Exercise

1. Create `cache.py`.
1. Configure the Redis client.
1. Implement cache key helpers.
1. Cache books after database reads.
1. Check Redis before querying PostgreSQL.
1. Invalidate cache after updates.
1. Add TTL.
1. Verify Redis is being used.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is the Cache-Aside pattern widely used with Redis?

The Cache-Aside pattern keeps Redis as an optimization layer rather than the system of record. The application first
checks Redis for data. On a cache miss, it loads the data from the database, stores it in Redis, and returns it. When
data changes, the application invalidates or updates the cache. This approach is simple, scalable, and keeps the
database as the authoritative source of truth.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Redis integration
- Cache-Aside pattern
- Redis client configuration
- Cache keys
- Serialization
- Cache invalidation
- TTL
- Health checks
- Performance improvements
- Redis best practices

Our application now uses PostgreSQL as the source of truth and Redis as a high-speed cache.

In the next chapter, we'll integrate **Kafka**, publishing events whenever books are created, updated, borrowed,
returned, or deleted.

______________________________________________________________________

## Next File

[Docker Project - Part 6](23-docker-project-part-6.md)
