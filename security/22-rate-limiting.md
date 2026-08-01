# Security - Part 22

# Rate Limiting

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Rate Limiting is
- Why it is important
- Common Rate Limiting algorithms
- Implementing Rate Limiting in FastAPI
- Redis-based Rate Limiting
- HTTP 429
- Best practices

______________________________________________________________________

# What is Rate Limiting?

Rate Limiting restricts **how many requests** a client can make within a specific period of time.

Instead of allowing unlimited requests,

the server enforces a limit.

Example

```text id="rl2201"
100 Requests

↓

1 Minute

↓

Allowed
```

If the client exceeds the limit,

the server rejects additional requests.

______________________________________________________________________

# Why Do We Need Rate Limiting?

Without Rate Limiting,

an attacker could:

- Brute-force passwords
- Spam APIs
- Overload servers
- Consume excessive resources
- Cause Denial of Service (DoS)

Rate Limiting helps protect your application and ensures fair usage for all users.

______________________________________________________________________

# Typical Flow

```text id="rl2202"
Client

↓

Request

↓

Rate Limiter

↓

Below Limit?

↓

Yes → Process Request

No → Reject (429)
```

______________________________________________________________________

# HTTP Status Code

When a limit is exceeded,

the server typically returns

```http id="rl2203"
429 Too Many Requests
```

Optionally,

include information such as:

```http id="rl2204"
Retry-After: 60
```

This tells the client

when it can try again.

______________________________________________________________________

# What Should Be Limited?

Common examples:

- Login attempts
- Password reset requests
- OTP verification
- Public APIs
- Search endpoints
- File uploads

Not every endpoint needs the same limit.

______________________________________________________________________

# Where Should We Rate Limit?

Rate limiting can be applied based on:

- IP Address
- User ID
- API Key
- Session
- Organization
- Combination of the above

Example

```text id="rl2205"
User ID

↓

100 Requests / Minute
```

______________________________________________________________________

# Common Algorithms

The most common algorithms are:

```text id="rl2206"
Fixed Window

↓

Sliding Window

↓

Token Bucket

↓

Leaky Bucket
```

Let's understand each.

______________________________________________________________________

# Fixed Window

Example

```text id="rl2207"
12:00 - 12:01

↓

100 Requests Allowed

↓

Reset Counter
```

Simple to implement,

but users can send many requests

at the boundary of two windows.

______________________________________________________________________

# Sliding Window

Instead of fixed windows,

the limit moves continuously.

```text id="rl2208"
Current Time

↓

Last 60 Seconds

↓

Count Requests
```

Advantages:

- Fairer
- Smoother request distribution

This is commonly used in production systems.

______________________________________________________________________

# Token Bucket

Imagine a bucket containing tokens.

```text id="rl2209"
Bucket

↓

100 Tokens
```

Each request

consumes one token.

Tokens are gradually refilled.

Advantages:

- Allows short bursts
- Prevents sustained abuse

Widely used by cloud providers and API gateways.

______________________________________________________________________

# Leaky Bucket

Imagine water leaking

from a bucket

at a constant rate.

```text id="rl2210"
Incoming Requests

↓

Bucket

↓

Constant Output
```

This smooths sudden traffic spikes.

______________________________________________________________________

# Which Algorithm Should You Use?

| Algorithm | When to Use |
| -------------- | -------------------- |
| Fixed Window | Simple applications |
| Sliding Window | Most REST APIs |
| Token Bucket | APIs allowing bursts |
| Leaky Bucket | Traffic smoothing |

For most backend APIs,

Sliding Window

or

Token Bucket

are excellent choices.

______________________________________________________________________

# Redis-Based Rate Limiting

Rate limiting needs shared state.

Suppose you have

three FastAPI servers.

```text id="rl2211"
FastAPI 1

↓

Redis

↑

FastAPI 2

↓

FastAPI 3
```

Redis stores

the request counters.

Every server

uses the same counters.

Without Redis,

each server would track requests independently,

leading to inconsistent limits.

______________________________________________________________________

# Simple FastAPI Workflow

```text id="rl2212"
Receive Request

↓

Identify User

↓

Increment Redis Counter

↓

Check Limit

↓

Allow or Reject
```

______________________________________________________________________

# Example Using `slowapi`

One popular library is

```text id="rl2213"
slowapi
```

Example

```python id="rl2214"
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address
)
```

Limit an endpoint

```python id="rl2215"
@limiter.limit("100/minute")
@app.get("/books")
async def get_books():
    return {"books": []}
```

This allows

100 requests

per minute

per client IP.

______________________________________________________________________

# Login Endpoint Example

Login endpoints

usually require stricter limits.

Example

```text id="rl2216"
5 Login Attempts

↓

5 Minutes
```

This significantly reduces

brute-force attacks.

______________________________________________________________________

# Rate Limiting + Authentication

Good workflow

```text id="rl2217"
Request

↓

Rate Limiter

↓

Authentication

↓

Authorization

↓

Business Logic
```

Rate limiting

should happen early,

before expensive processing.

______________________________________________________________________

# Monitoring

Log:

- Frequent rate-limit violations
- Suspicious IPs
- Brute-force attempts

This helps identify attacks.

______________________________________________________________________

# Defense in Depth

Combine:

```text id="rl2218"
HTTPS

↓

Rate Limiting

↓

Authentication

↓

Authorization

↓

Logging

↓

Monitoring
```

Rate limiting

doesn't replace authentication.

It complements it.

______________________________________________________________________

# Best Practices

✅ Rate limit authentication endpoints.

✅ Use Redis for distributed applications.

✅ Return HTTP 429.

✅ Log suspicious activity.

✅ Use Sliding Window or Token Bucket.

✅ Configure different limits for different endpoints.

______________________________________________________________________

# Common Mistakes

### One Limit for Everything

Login

and

public search

usually need different limits.

______________________________________________________________________

### Rate Limiting Only by IP

In authenticated systems,

consider using

User ID

or

API Key

instead of only IP addresses.

______________________________________________________________________

### Forgetting Distributed Systems

Multiple application servers

require shared counters,

typically stored in Redis.

______________________________________________________________________

### No Monitoring

Repeated rate-limit violations

may indicate

an ongoing attack.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| --------------------- | ------------------------- |
| Unlimited requests | Rate limiting |
| In-memory counters | Redis counters |
| No HTTP 429 | Return proper status code |
| Same limit everywhere | Endpoint-specific limits |
| Ignore violations | Log and monitor |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Rate Limiting, and how is it implemented in backend applications?

Rate Limiting restricts the number of requests a client can make within a specified time period to protect applications
from abuse, brute-force attacks, and denial-of-service attempts. Common algorithms include Fixed Window, Sliding Window,
Token Bucket, and Leaky Bucket. In distributed systems, Redis is commonly used to store request counters so that all
application instances enforce consistent limits.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Rate Limiting is
- Why it is important
- HTTP 429
- Rate Limiting algorithms
- Redis-based implementation
- FastAPI example
- Best practices

______________________________________________________________________

# What's Next

[Logging & Monitoring](23-logging-and-monitoring.md)
