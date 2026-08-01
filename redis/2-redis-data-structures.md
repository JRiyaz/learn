# Redis Data Structures

## Introduction

Redis is much more than a simple key-value store.

Unlike traditional databases, Redis provides multiple **built-in data structures**, each optimized for different use
cases.

Choosing the correct data structure is one of the most common Redis interview topics.

In this chapter, you'll learn:

- Strings
- Hashes
- Lists
- Sets
- Sorted Sets
- Bitmaps
- HyperLogLog
- Geospatial Indexes
- Streams (Introduction)
- Real-world use cases
- Time complexities
- Python (`redis-py`) examples
- Production best practices

______________________________________________________________________

# Redis Data Structures Overview

```text id="redisds001"
Redis

├── Strings

├── Hashes

├── Lists

├── Sets

├── Sorted Sets

├── Bitmaps

├── HyperLogLog

├── Geospatial

└── Streams
```

Each structure is designed for a different problem.

______________________________________________________________________

# 1. Strings

Strings are the simplest and most commonly used Redis data structure.

A string can store:

- Text
- JSON
- Numbers
- Binary data

CLI

```bash id="redisds002"
SET username "riyaz"

GET username
```

Python

```python id="redisds003"
client.set(
    "username",
    "riyaz"
)

print(
    client.get("username")
)
```

Time Complexity

```text id="redisds004"
SET -> O(1)

GET -> O(1)
```

______________________________________________________________________

# Real Use Cases

Strings are commonly used for:

- Cache entries
- OTP codes
- JWT blacklist
- Session tokens
- Feature flags
- Configuration values

______________________________________________________________________

# Numeric Operations

CLI

```bash id="redisds005"
SET visitors 100

INCR visitors

DECR visitors
```

Python

```python id="redisds006"
client.set(
    "visitors",
    100
)

client.incr("visitors")

client.decr("visitors")
```

Useful for:

- API counters
- View counters
- Likes
- Downloads

______________________________________________________________________

# Atomic Operations

Redis operations are atomic.

Two users executing

```bash id="redisds007"
INCR counter
```

simultaneously

↓

Both updates succeed correctly.

No race condition occurs for the increment itself.

______________________________________________________________________

# 2. Hashes

Hashes store multiple fields inside one key.

Instead of

```text id="redisds008"
user:name

user:email

user:age
```

Store

```text id="redisds009"
user:1

↓

name

email

age
```

______________________________________________________________________

CLI

```bash id="redisds010"
HSET user:1 \
name Alice \
age 25 \
city Bangalore
```

Retrieve

```bash id="redisds011"
HGET user:1 name
```

Python

```python id="redisds012"
client.hset(
    "user:1",
    mapping={
        "name": "Alice",
        "age": 25,
        "city": "Bangalore"
    }
)

print(
    client.hget(
        "user:1",
        "name"
    )
)
```

______________________________________________________________________

# Retrieve Entire Hash

CLI

```bash id="redisds013"
HGETALL user:1
```

Python

```python id="redisds014"
client.hgetall("user:1")
```

______________________________________________________________________

# Time Complexity

| Command | Complexity |
| ------- | ---------: |
| HSET | O(1) |
| HGET | O(1) |
| HDEL | O(1) |

______________________________________________________________________

# Real Use Cases

Hashes are ideal for:

- User profiles
- Product information
- Shopping carts
- Configuration objects
- Account settings

______________________________________________________________________

# Strings vs Hashes

| Strings | Hashes |
| ------------ | --------------- |
| One value | Multiple fields |
| Simple cache | Structured data |
| GET | HGET |
| SET | HSET |

______________________________________________________________________

# 3. Lists

Lists maintain insertion order.

Think of a queue.

```text id="redisds015"
Task1

↓

Task2

↓

Task3
```

______________________________________________________________________

# Insert

Left

```bash id="redisds016"
LPUSH queue task1

LPUSH queue task2
```

Right

```bash id="redisds017"
RPUSH queue task3
```

Python

```python id="redisds018"
client.lpush(
    "queue",
    "task1"
)

client.rpush(
    "queue",
    "task2"
)
```

______________________________________________________________________

# Retrieve

CLI

```bash id="redisds019"
LRANGE queue 0 -1
```

Python

```python id="redisds020"
client.lrange(
    "queue",
    0,
    -1
)
```

______________________________________________________________________

# Remove

CLI

```bash id="redisds021"
LPOP queue

RPOP queue
```

Python

```python id="redisds022"
client.lpop("queue")

client.rpop("queue")
```

______________________________________________________________________

# Time Complexity

| Command | Complexity |
| ------- | ---------: |
| LPUSH | O(1) |
| RPUSH | O(1) |
| LPOP | O(1) |
| RPOP | O(1) |

______________________________________________________________________

# Real Use Cases

Lists are commonly used for:

- Task queues
- Background jobs
- Notification queues
- Message buffers

______________________________________________________________________

# 4. Sets

Sets contain **unique values**.

Duplicates are ignored.

CLI

```bash id="redisds023"
SADD roles admin

SADD roles admin

SADD roles user
```

Only

```text id="redisds024"
admin

user
```

exist.

______________________________________________________________________

Python

```python id="redisds025"
client.sadd(
    "roles",
    "admin"
)

client.sadd(
    "roles",
    "user"
)
```

______________________________________________________________________

# Membership

CLI

```bash id="redisds026"
SISMEMBER roles admin
```

Python

```python id="redisds027"
client.sismember(
    "roles",
    "admin"
)
```

______________________________________________________________________

# Retrieve

CLI

```bash id="redisds028"
SMEMBERS roles
```

Python

```python id="redisds029"
client.smembers("roles")
```

______________________________________________________________________

# Real Use Cases

- Permissions
- Tags
- Followers
- Unique visitors
- User interests

______________________________________________________________________

# Set Operations

Redis supports mathematical set operations.

Intersection

```bash id="redisds030"
SINTER group1 group2
```

Union

```bash id="redisds031"
SUNION group1 group2
```

Difference

```bash id="redisds032"
SDIFF group1 group2
```

Python

```python id="redisds033"
client.sinter(
    "group1",
    "group2"
)
```

______________________________________________________________________

# 5. Sorted Sets

A Sorted Set stores

```text id="redisds034"
Score

+

Value
```

Each value is unique.

Each value has a score.

______________________________________________________________________

CLI

```bash id="redisds035"
ZADD leaderboard \
100 Alice \
90 Bob \
150 Charlie
```

Python

```python id="redisds036"
client.zadd(
    "leaderboard",
    {
        "Alice": 100,
        "Bob": 90,
        "Charlie": 150
    }
)
```

______________________________________________________________________

# Ranking

CLI

```bash id="redisds037"
ZRANGE leaderboard 0 -1 WITHSCORES
```

Python

```python id="redisds038"
client.zrange(
    "leaderboard",
    0,
    -1,
    withscores=True
)
```

______________________________________________________________________

# Real Use Cases

Sorted Sets power:

- Leaderboards
- Rankings
- Trending posts
- Gaming scores
- Priority queues

Interview Tip

If an interviewer asks:

> "How would you build a leaderboard?"

Answer

```text id="redisds039"
Sorted Set
```

______________________________________________________________________

# Time Complexity

| Command | Complexity |
| ------- | -----------: |
| ZADD | O(log N) |
| ZRANGE | O(log N + M) |
| ZREM | O(log N) |

______________________________________________________________________

# 6. Bitmaps

Bitmaps store bits.

Example

```text id="redisds040"
1

0

1

1

0
```

Useful for boolean values.

CLI

```bash id="redisds041"
SETBIT login:today 10 1
```

Python

```python id="redisds042"
client.setbit(
    "login:today",
    10,
    1
)
```

______________________________________________________________________

# Real Use Cases

- Daily logins
- Attendance
- Online status
- Feature flags
- A/B testing

______________________________________________________________________

# 7. HyperLogLog

Counts approximately unique elements.

CLI

```bash id="redisds043"
PFADD visitors Alice Bob Charlie
```

Count

```bash id="redisds044"
PFCOUNT visitors
```

Python

```python id="redisds045"
client.pfadd(
    "visitors",
    "Alice",
    "Bob",
    "Charlie"
)

client.pfcount("visitors")
```

Uses very little memory even for millions of values.

______________________________________________________________________

# Real Use Cases

- Website visitors
- Unique IPs
- Analytics
- Daily active users

______________________________________________________________________

# 8. Geospatial

Redis can store coordinates.

CLI

```bash id="redisds046"
GEOADD stores \
77.5946 12.9716 Bangalore
```

Python

```python id="redisds047"
client.geoadd(
    "stores",
    (
        77.5946,
        12.9716,
        "Bangalore"
    )
)
```

Nearby search

CLI

```bash id="redisds048"
GEORADIUS stores \
77.59 \
12.97 \
10 km
```

______________________________________________________________________

# Real Use Cases

- Food delivery
- Ride sharing
- Nearby stores
- Logistics

______________________________________________________________________

# 9. Streams (Introduction)

Streams are Redis's persistent log data structure.

Example

```bash id="redisds049"
XADD orders * \
user Alice \
amount 100
```

Python

```python id="redisds050"
client.xadd(
    "orders",
    {
        "user": "Alice",
        "amount": 100
    }
)
```

We'll study Streams in depth later.

______________________________________________________________________

# Choosing the Right Data Structure

| Problem | Redis Structure |
| --------------- | --------------- |
| Cache | String |
| User Profile | Hash |
| Queue | List |
| Tags | Set |
| Leaderboard | Sorted Set |
| Login Tracking | Bitmap |
| Unique Visitors | HyperLogLog |
| Nearby Search | Geospatial |
| Event Streaming | Stream |

______________________________________________________________________

# Common Mistakes

### Using Strings for Everything

Redis provides specialized data structures.

Use them.

______________________________________________________________________

### Using Lists for Leaderboards

Use Sorted Sets.

______________________________________________________________________

### Using Sets When Order Matters

Sets are unordered.

______________________________________________________________________

### Ignoring Time Complexity

Understand operation costs before choosing a structure.

______________________________________________________________________

# Best Practices

- Choose the data structure that matches the problem.
- Use Hashes for structured objects.
- Use Sorted Sets for ranking.
- Use Lists for queues.
- Use Sets for uniqueness.
- Understand memory usage and operation complexity.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Which Redis data structure would you choose for a gaming leaderboard and why?

I would use a **Sorted Set** because each player can be stored as a unique member with their score as the associated
value. Redis maintains the members in score order, making it efficient to retrieve the top players, update scores, and
calculate rankings. Operations such as `ZADD`, `ZRANGE`, and `ZREVRANK` are designed specifically for this use case and
provide excellent performance.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What are Redis data structures?
1. Difference between String and Hash.
1. Difference between List and Set.
1. Why use Sorted Sets for leaderboards?
1. What is HyperLogLog?
1. What are Bitmaps?
1. What is Geospatial indexing?
1. What are Redis Streams?
1. Which structure is best for user profiles?
1. Which structure is best for queues?

## Coding

1. Store a cache entry using Strings.
1. Create a user profile using Hashes.
1. Build a task queue using Lists.
1. Store user roles using Sets.
1. Create a leaderboard using Sorted Sets.
1. Count unique visitors using HyperLogLog.
1. Track logins using Bitmaps.
1. Store store locations using Geospatial commands.

______________________________________________________________________

# Hands-on Exercise

Build a small social media backend using Redis.

Requirements:

1. Cache posts using Strings.
1. Store user profiles using Hashes.
1. Store notifications using Lists.
1. Store user interests using Sets.
1. Build a trending leaderboard using Sorted Sets.
1. Track daily active users using HyperLogLog.
1. Track login activity using Bitmaps.
1. Store nearby stores using Geospatial indexes.

______________________________________________________________________

# Cheat Sheet

```text id="redisds051"
Strings

↓

Hashes

↓

Lists

↓

Sets

↓

Sorted Sets

↓

Bitmaps

↓

HyperLogLog

↓

Geospatial

↓

Streams
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Redis data structures
- Strings
- Hashes
- Lists
- Sets
- Sorted Sets
- Bitmaps
- HyperLogLog
- Geospatial
- Streams (Introduction)
- Real-world use cases
- Time complexities
- Python (`redis-py`) examples
- Production best practices
- Interview patterns

You now understand how to choose the appropriate Redis data structure for different application requirements and how to
use each one through both the Redis CLI and Python.

______________________________________________________________________

## Next File

[Redis Caching Patterns & Expiration](3-redis-caching-patterns.md)
