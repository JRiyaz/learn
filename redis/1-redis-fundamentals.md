# Redis Fundamentals

## Introduction

Modern applications rarely rely only on relational databases.

Imagine an e-commerce application.

Every request asks for:

- User Profile
- Product Details
- Shopping Cart
- Session Data
- Authentication Tokens

If every request hits PostgreSQL, the database quickly becomes the bottleneck.

Redis solves this problem.

Redis is one of the most widely used technologies in backend engineering interviews and production systems.

Companies like Netflix, Uber, Instagram, GitHub, Discord, and many others use Redis for high-speed data access.

In this chapter, you'll learn:

- What Redis is
- Why Redis is fast
- Redis Architecture
- Installation
- Redis CLI
- Python (`redis-py`)
- FastAPI Integration
- Memory Model
- Persistence
- Expiration
- Basic Commands
- Production Best Practices

______________________________________________________________________

# What is Redis?

Redis stands for

> **REmote DIctionary Server**

Redis is:

- An in-memory database
- A key-value store
- A cache
- A message broker
- A data structure server

Unlike PostgreSQL,

Redis stores data primarily in **RAM**, making access extremely fast.

______________________________________________________________________

# Why is Redis Fast?

Most databases

```text id="redis001"
Application

↓

Disk

↓

Database
```

Redis

```text id="redis002"
Application

↓

RAM

↓

Redis
```

Memory access is much faster than disk access.

Typical Redis operations complete in microseconds.

______________________________________________________________________

# Redis vs PostgreSQL

| Redis | PostgreSQL |
| ----------------------- | -------------------------------- |
| In-memory | Disk-based (with memory caching) |
| Key-Value | Relational |
| Extremely Fast | Rich SQL Features |
| No JOINs | JOIN Support |
| Cache | Primary Database |
| Temporary or Persistent | Persistent |

Interview Tip

Redis is **not** a replacement for PostgreSQL.

They solve different problems.

______________________________________________________________________

# Redis Architecture

```text id="redis003"
Application

↓

redis-py

↓

TCP Connection

↓

Redis Server

↓

RAM

↓

(Optional)

Persistence
```

Every Redis command travels over a TCP connection.

______________________________________________________________________

# Installing Redis

Ubuntu

```bash id="redis004"
sudo apt install redis-server
```

Mac

```bash id="redis005"
brew install redis
```

Docker

```bash id="redis006"
docker run -d \
--name redis \
-p 6379:6379 \
redis:latest
```

______________________________________________________________________

# Starting Redis

```bash id="redis007"
redis-server
```

Default port

```text id="redis008"
6379
```

______________________________________________________________________

# Redis CLI

Connect

```bash id="redis009"
redis-cli
```

Ping

```bash id="redis010"
PING
```

Output

```text id="redis011"
PONG
```

______________________________________________________________________

# Installing redis-py

```bash id="redis012"
pip install redis
```

The modern `redis` package supports both synchronous and asynchronous APIs.

______________________________________________________________________

# Connecting with Python

```python id="redis013"
import redis

client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
```

`decode_responses=True`

returns strings instead of bytes.

______________________________________________________________________

# Testing the Connection

CLI

```bash id="redis014"
PING
```

Python

```python id="redis015"
print(client.ping())
```

Output

```text id="redis016"
True
```

______________________________________________________________________

# Keys and Values

Everything in Redis is stored as

```text id="redis017"
Key

↓

Value
```

Example

```text id="redis018"
user:1

↓

Riyaz
```

______________________________________________________________________

# Setting Values

CLI

```bash id="redis019"
SET user:1 "Riyaz"
```

Python

```python id="redis020"
client.set(
    "user:1",
    "Riyaz"
)
```

Equivalent concept

```sql id="redis021"
INSERT ...
```

although Redis is not relational.

______________________________________________________________________

# Getting Values

CLI

```bash id="redis022"
GET user:1
```

Python

```python id="redis023"
name = client.get("user:1")
```

Output

```text id="redis024"
Riyaz
```

Time Complexity

```text id="redis025"
O(1)
```

______________________________________________________________________

# Updating Values

CLI

```bash id="redis026"
SET user:1 "Ahmed"
```

Python

```python id="redis027"
client.set(
    "user:1",
    "Ahmed"
)
```

Redis simply overwrites the existing value.

______________________________________________________________________

# Deleting Keys

CLI

```bash id="redis028"
DEL user:1
```

Python

```python id="redis029"
client.delete("user:1")
```

______________________________________________________________________

# Checking Existence

CLI

```bash id="redis030"
EXISTS user:1
```

Python

```python id="redis031"
client.exists("user:1")
```

Output

```text id="redis032"
1
```

means the key exists.

______________________________________________________________________

# Listing Keys

CLI

```bash id="redis033"
KEYS *
```

Python

```python id="redis034"
client.keys("*")
```

Interview Tip

Avoid

```text id="redis035"
KEYS *
```

in production.

It scans the entire keyspace and can block the server.

Use `SCAN` instead for large datasets.

______________________________________________________________________

# Key Naming

Good

```text id="redis036"
user:1

user:2

product:15

cart:100
```

Bad

```text id="redis037"
abc

xyz

hello
```

Use namespaces.

______________________________________________________________________

# Expiration (TTL)

Cache data should usually expire.

CLI

```bash id="redis038"
SET product:1 "Laptop"

EXPIRE product:1 300
```

Python

```python id="redis039"
client.set(
    "product:1",
    "Laptop",
    ex=300
)
```

300

↓

5 minutes.

______________________________________________________________________

# TTL

CLI

```bash id="redis040"
TTL product:1
```

Python

```python id="redis041"
client.ttl("product:1")
```

Output

```text id="redis042"
295
```

______________________________________________________________________

# Removing Expiration

CLI

```bash id="redis043"
PERSIST product:1
```

Python

```python id="redis044"
client.persist("product:1")
```

______________________________________________________________________

# Deleting All Keys

Current database

CLI

```bash id="redis045"
FLUSHDB
```

Python

```python id="redis046"
client.flushdb()
```

All databases

CLI

```bash id="redis047"
FLUSHALL
```

Python

```python id="redis048"
client.flushall()
```

Be extremely careful with these commands.

______________________________________________________________________

# Redis Persistence

Although Redis stores data in RAM, it can also persist data to disk.

Two main mechanisms:

- RDB Snapshots
- AOF (Append Only File)

We'll cover these in detail later.

______________________________________________________________________

# Real Production Example

Suppose every product page loads from PostgreSQL.

Instead,

check Redis first.

```text id="redis049"
Request

↓

Redis

↓

Cache Hit?

↓

Yes

↓

Return Data

↓

No

↓

PostgreSQL

↓

Redis

↓

Client
```

This is called the **Cache-Aside Pattern**.

______________________________________________________________________

# FastAPI Example

```python id="redis050"
from fastapi import FastAPI
import json
import redis

app = FastAPI()

client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

@app.get("/users/{user_id}")
def get_user(user_id: int):

    cache_key = f"user:{user_id}"

    cached = client.get(cache_key)

    if cached:
        return json.loads(cached)

    user = {
        "id": user_id,
        "name": "Alice"
    }

    client.set(
        cache_key,
        json.dumps(user),
        ex=300
    )

    return user
```

This avoids repeatedly querying the database for the same data.

______________________________________________________________________

# Time Complexity

| Command | Complexity |
| ------- | ---------: |
| GET | O(1) |
| SET | O(1) |
| DEL | O(1) |
| EXISTS | O(1) |
| EXPIRE | O(1) |
| TTL | O(1) |

One reason Redis is so fast.

______________________________________________________________________

# Common Mistakes

### Using Redis as the Only Database

Redis is often used **alongside** a relational database, not as its replacement.

______________________________________________________________________

### Forgetting TTL

Cache entries may become stale if they never expire.

______________________________________________________________________

### Using KEYS in Production

Prefer `SCAN` for large keyspaces.

______________________________________________________________________

### Storing Huge Objects

Large values increase memory usage and network transfer time.

______________________________________________________________________

### Poor Key Naming

Always use clear namespaces.

______________________________________________________________________

# Best Practices

- Use Redis primarily for caching and fast lookups.
- Choose meaningful key names.
- Set expiration times for cache entries.
- Avoid `KEYS *` in production.
- Keep cached values reasonably small.
- Understand cache invalidation strategies.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is Redis much faster than PostgreSQL?

Redis stores its working data in memory, so most operations avoid disk I/O and execute in constant time. PostgreSQL is a
full relational database that provides transactions, indexes, SQL, joins, and durable storage, which adds overhead.
Redis sacrifices many relational features in exchange for extremely low-latency access, making it ideal for caching,
sessions, counters, and other high-speed workloads.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is Redis?
1. Why is Redis so fast?
1. Redis vs PostgreSQL.
1. Why use Redis as a cache?
1. What is TTL?
1. What does `EXPIRE` do?
1. Difference between `DEL` and `FLUSHDB`.
1. Why is `KEYS *` dangerous?
1. What is the Cache-Aside pattern?
1. Why should cache entries expire?

## Coding

1. Connect to Redis using `redis-py`.
1. Store a user.
1. Retrieve a user.
1. Update a value.
1. Delete a value.
1. Set a TTL.
1. Retrieve the remaining TTL.
1. Build a simple cache for a FastAPI endpoint.

______________________________________________________________________

# Hands-on Exercise

Build a User Cache.

Requirements:

1. Start a Redis server.
1. Connect using `redis-py`.
1. Store user information.
1. Retrieve users.
1. Update users.
1. Delete users.
1. Apply a five-minute TTL.
1. Integrate Redis caching into a FastAPI endpoint.

______________________________________________________________________

# Cheat Sheet

```text id="redis051"
redis-server

↓

redis-cli

↓

PING

↓

SET

↓

GET

↓

DEL

↓

EXISTS

↓

EXPIRE

↓

TTL

↓

PERSIST

↓

FLUSHDB

↓

FLUSHALL
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Redis fundamentals
- Redis architecture
- Why Redis is fast
- Redis vs PostgreSQL
- Installing Redis
- Redis CLI
- `redis-py`
- Connecting from Python
- Basic key-value operations
- TTL and expiration
- Cache-Aside pattern
- FastAPI integration
- Time complexity
- Best practices
- Interview patterns

You now understand how Redis works at a fundamental level and how to use it both from the command line and from Python
applications.

______________________________________________________________________

## Next File

[Redis Data Structures](2-redis-data-structures.md)
