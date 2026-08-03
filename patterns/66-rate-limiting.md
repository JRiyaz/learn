# System Design - Part 66

# Rate Limiting

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Rate Limiting is
- Why Rate Limiting exists
- Request Quotas
- Fixed Window Algorithm
- Sliding Window Algorithm
- Token Bucket Algorithm
- Leaky Bucket Algorithm
- Distributed Rate Limiting
- Redis-based Rate Limiting
- API Gateway Rate Limiting
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

provides

a public API.

Anyone

can search

for books.

One user

accidentally

(or intentionally)

sends

100,000 requests

per second.

Question.

Should

one user

be allowed

to consume

all server resources?

Of course not.

The system

must protect

itself.

______________________________________________________________________

# The Problem

Suppose

10,000 users

normally send

```text id="rl6601"
10 Requests/sec
```

One attacker

sends

```text id="rl6602"
100,000 Requests/sec
```

Without protection,

the attacker

can:

- Overload servers
- Exhaust databases
- Increase cloud costs
- Cause denial of service

______________________________________________________________________

# The Idea

Allow

only

a limited number

of requests

during

a specific

time period.

Reject

requests

that exceed

the limit.

______________________________________________________________________

# What is Rate Limiting?

**Rate Limiting**

is the process

of restricting

how many requests

a client

can make

within

a given

time interval.

It protects

applications

from abuse,

accidental overload,

and unfair resource usage.

______________________________________________________________________

# Example

Suppose

the limit is

```text id="rl6603"
100 Requests

Per Minute
```

The first

100 requests

are accepted.

The 101st

request

is rejected.

______________________________________________________________________

# Typical Response

Most APIs

return

```text id="rl6604"
HTTP 429

Too Many Requests
```

This tells

the client

to slow down.

______________________________________________________________________

# What Can Be Limited?

Rate limits

can be applied

per:

- User ID
- API Key
- IP Address
- Device
- Tenant
- Organization

The identifier

depends

on

the application.

______________________________________________________________________

# Fixed Window Algorithm

Interview favorite.

Suppose

the limit is

100 requests

per minute.

Workflow

```text id="rl6605"
12:00

↓

Counter = 100

↓

Reject
```

At

12:01,

the counter

resets.

Advantages

✅ Simple

Disadvantages

❌ Burst traffic

at window boundaries.

______________________________________________________________________

# Fixed Window Problem

Suppose

a client

sends

100 requests

at

12:00:59

and

another

100 requests

at

12:01:01.

The client

effectively sends

200 requests

within

2 seconds,

while

still respecting

the limit.

This is

called

the

**Boundary Problem**.

______________________________________________________________________

# Sliding Window Algorithm

Instead of

fixed windows,

use

a moving window.

```text id="rl6606"
Last

60 Seconds
```

Every request

is evaluated

against

the previous

60 seconds.

Advantages

✅ More accurate

Disadvantages

❌ Slightly more expensive

______________________________________________________________________

# Token Bucket Algorithm

Interview favorite.

Imagine

a bucket

containing

tokens.

Each request

consumes

one token.

Tokens

are added

at

a fixed rate.

```text id="rl6607"
Bucket

↓

10 Tokens
```

If

no tokens

remain,

requests

are rejected.

Advantages

✅ Allows short bursts

✅ Widely used

______________________________________________________________________

# Example

Suppose

the bucket

holds

10 tokens.

Requests

arrive.

```text id="rl6608"
10 Tokens

↓

0 Tokens

↓

Reject
```

After

one second,

new tokens

are added.

______________________________________________________________________

# Leaky Bucket Algorithm

Imagine

a bucket

with

a small hole.

Requests

enter quickly,

but

leave

at

a constant rate.

```text id="rl6609"
Incoming Requests

↓

Bucket

↓

Constant Output
```

Advantages

✅ Smooth traffic

Disadvantages

❌ Burst requests

may wait

or be dropped.

______________________________________________________________________

# Algorithm Comparison

| Algorithm | Burst Support | Complexity |
| -------------- | ------------- | ---------- |
| Fixed Window | Poor | Low |
| Sliding Window | Good | Medium |
| Token Bucket | Excellent | Medium |
| Leaky Bucket | Smooth output | Medium |

______________________________________________________________________

# Distributed Problem

Suppose

your application

runs

on

10 servers.

```text id="rl6610"
Server 1

Server 2

...

Server 10
```

If

each server

maintains

its own counter,

clients

can bypass

the limit

by hitting

different servers.

______________________________________________________________________

# Redis-Based Rate Limiting

Interview favorite.

Instead,

store

the counters

inside

Redis.

```text id="rl6611"
Clients

↓

Load Balancer

↓

Application Servers

↓

Redis Counter
```

Every server

shares

the same counter.

______________________________________________________________________

# Why Redis?

Redis provides:

- Very fast operations
- Atomic increment commands
- Key expiration (TTL)
- High throughput

This makes it

ideal

for

distributed

rate limiting.

______________________________________________________________________

# API Gateway

Many companies

implement

Rate Limiting

at

the

API Gateway.

```text id="rl6612"
Client

↓

API Gateway

↓

Application
```

Requests

that exceed

the limit

never reach

the application.

This reduces

backend load.

______________________________________________________________________

# Retry-After Header

When

rejecting

requests,

the server

can include

```http id="rl6613"
Retry-After: 30
```

Meaning

the client

should wait

30 seconds

before

trying again.

______________________________________________________________________

# FastAPI Example

Suppose

an endpoint

allows

100 requests

per minute.

```python id="rl6614"
GET /books
```

The application

checks

Redis.

If

the limit

has been reached,

return

HTTP 429.

______________________________________________________________________

# AI/ML Example

Suppose

an LLM API

costs

money

for

every request.

Without

Rate Limiting,

one client

could generate

thousands

of expensive

inference requests.

Rate Limiting

protects

both

the infrastructure

and

the business.

______________________________________________________________________

# Public API Example

Suppose

a weather API.

Free users

may receive

```text id="rl6615"
100 Requests/Day
```

Premium users

may receive

```text id="rl6616"
10,000 Requests/Day
```

Different plans

can have

different limits.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

Protect:

- Login API
- OTP API
- Search API
- Checkout API

Rate Limiting

reduces:

- Credential stuffing
- Brute-force attacks
- Abuse
- Unexpected traffic spikes

______________________________________________________________________

# Rate Limiting vs Authentication

Interview favorite.

| Authentication | Rate Limiting |
| ---------------- | ------------------- |
| Identifies users | Limits requests |
| Security | Resource protection |

Both

should be

used together.

______________________________________________________________________

# Rate Limiting vs Circuit Breaker

| Rate Limiting | Circuit Breaker |
| ------------------------ | -------------------------------------------- |
| Protects your service | Protects against failing downstream services |
| Limits incoming requests | Stops repeated failed calls |

They solve

different problems.

______________________________________________________________________

# Benefits

Rate Limiting provides:

✅ Prevents abuse

✅ Protects infrastructure

✅ Fair resource usage

✅ Reduces attack impact

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Additional Redis calls

❌ Configuration complexity

❌ Risk of blocking legitimate users

______________________________________________________________________

# When NOT to Use Strict Rate Limits

Avoid

very strict limits

for:

- Internal services
- Health checks
- Critical system communication

Use

appropriate limits

based on

business requirements.

______________________________________________________________________

# Best Practices

✅ Use Redis

for distributed systems.

✅ Return HTTP 429.

✅ Include Retry-After headers.

✅ Configure different limits

for different user tiers.

______________________________________________________________________

# Common Mistakes

### Storing Counters Locally

Local counters

fail

when

multiple servers

handle requests.

Use

shared storage

like Redis.

______________________________________________________________________

### One Limit for Everyone

Different users

often require

different quotas.

Premium users

typically receive

higher limits.

______________________________________________________________________

### Forgetting API Gateway

Protecting

only

the application

still allows

unnecessary traffic

to reach

your infrastructure.

______________________________________________________________________

### No Monitoring

Track:

- Rejected requests
- Top clients
- Redis latency
- Limit violations

to ensure

your configuration

is effective.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Rate Limiting, and how would you implement it in a distributed system?

Rate Limiting restricts the number of requests a client can make within a specified time period to protect systems from
abuse, denial-of-service attacks, and excessive resource consumption. In a distributed system with multiple application
servers, request counters should be stored in a shared datastore such as Redis rather than in local memory. Redis
provides atomic increment operations and key expiration, making it ideal for implementing algorithms such as Fixed
Window, Sliding Window, or Token Bucket. Many production systems enforce rate limits at the API Gateway so that
excessive requests are rejected before reaching backend services.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Rate Limiting is
- Fixed Window
- Sliding Window
- Token Bucket
- Leaky Bucket
- Redis-based Rate Limiting
- API Gateway integration
- FastAPI example
- Best practices

______________________________________________________________________

# 🧠 Security Progress

You now understand:

- ✅ Authentication & Authorization
- ✅ Rate Limiting

These are two of the most fundamental security mechanisms used in modern backend systems.

______________________________________________________________________

# 🚀 What's Coming Next

The final topic in the **Security** module is:

- API Versioning

This is an essential concept for maintaining backward compatibility while continuously evolving APIs in production.

______________________________________________________________________

# What's Next

[API Versioning](67-api-versioning.md)
