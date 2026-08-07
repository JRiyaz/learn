# System Design – Rate Limiter

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand Rate Limiting, why it is essential for modern systems, different rate limiting algorithms, distributed implementation, and how to confidently answer Rate Limiter questions in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

your API

receives

```
1 Million Requests

Per Second
```

Most requests

are legitimate.

Some are

```
Bots

Spam

DDoS

Abuse
```

Without protection,

your servers

may become

overloaded.

How do companies

like

Amazon,

Google,

Netflix,

and Stripe

protect

their APIs?

The answer is

```
Rate Limiting
```

______________________________________________________________________

# What Is Rate Limiting?

Rate Limiting

restricts

how many requests

a client

can make

within

a given time period.

Example

```
100 Requests

Per Minute
```

If

the client

exceeds

the limit,

the request

is rejected.

______________________________________________________________________

# Example

Allowed

```
100 Requests

↓

Accepted
```

Request

```
101

↓

429 Too Many Requests
```

______________________________________________________________________

# Why Do We Need It?

Rate Limiting

helps prevent

- API abuse
- DDoS attacks
- Brute-force attacks
- Resource exhaustion
- Expensive operations
- Fair resource usage

______________________________________________________________________

# Real-World Example

Suppose

one user

calls

```
/login
```

```
10,000 Times
```

Without

Rate Limiting,

the authentication service

may become overloaded.

______________________________________________________________________

# Basic Architecture

```
Client

↓

API Gateway

↓

Rate Limiter

↓

Backend Services
```

Requests

are checked

before

reaching

the backend.

______________________________________________________________________

# Where Can Rate Limiting Be Applied?

Examples

- API Gateway
- Reverse Proxy
- Load Balancer
- Web Server
- Application Layer

Most systems

perform

rate limiting

at

the edge.

______________________________________________________________________

# Rate Limiting Key

Limits

can be based on

- User ID
- API Key
- IP Address
- OAuth Client
- Session
- Device ID

Choose

the key

based on

business requirements.

______________________________________________________________________

# Response

When

the limit

is exceeded

return

```
HTTP 429

Too Many Requests
```

Optionally include

```
Retry-After
```

header.

______________________________________________________________________

# Algorithms

Several algorithms

exist.

Each

has

advantages

and disadvantages.

______________________________________________________________________

# 1. Fixed Window Counter

Very common.

Example

```
100 Requests

Per Minute
```

Counter

resets

every minute.

______________________________________________________________________

# Example

```
12:00

↓

Counter = 0
```

User sends

```
100 Requests

↓

Allowed
```

```
12:01

↓

Counter Reset
```

Simple.

______________________________________________________________________

# Problem

Boundary issue.

Example

```
12:00:59

↓

100 Requests
```

Immediately after

```
12:01:00

↓

100 More Requests
```

User sends

```
200 Requests

In 2 Seconds
```

Not ideal.

______________________________________________________________________

# 2. Sliding Window Log

Store

timestamps

of requests.

```
10:01

10:02

10:03
```

Remove

old timestamps.

Count

remaining requests.

Very accurate.

______________________________________________________________________

# Advantages

- Precise
- Fair

______________________________________________________________________

# Disadvantages

Stores

many timestamps.

Higher

memory usage.

______________________________________________________________________

# 3. Sliding Window Counter

Hybrid approach.

Combines

previous window

and

current window

to estimate

usage.

More memory efficient

than

Sliding Window Log.

______________________________________________________________________

# 4. Token Bucket

Interview favorite.

Imagine

a bucket

containing

tokens.

Each request

needs

one token.

```
Bucket

↓

100 Tokens
```

______________________________________________________________________

# Request

```
Token Available

↓

Allow Request
```

```
No Token

↓

Reject
```

______________________________________________________________________

# Token Refill

Tokens

are added

continuously.

Example

```
10 Tokens

Per Second
```

Allows

short bursts

while

maintaining

an average rate.

______________________________________________________________________

# Advantages

- Supports bursts
- Smooth traffic
- Widely used

______________________________________________________________________

# 5. Leaky Bucket

Imagine

a bucket

with

a small hole.

Water

enters

quickly,

but

leaves

at

a fixed rate.

```
Incoming Requests

↓

Bucket

↓

Constant Output
```

______________________________________________________________________

# Advantages

- Smooth traffic
- Predictable processing

______________________________________________________________________

# Disadvantages

Sudden bursts

may be

discarded

when

the bucket

becomes full.

______________________________________________________________________

# Algorithm Comparison

| Algorithm | Burst Support | Memory | Accuracy |
|------------|---------------|---------|-----------|
| Fixed Window | Poor | Low | Medium |
| Sliding Log | Excellent | High | High |
| Sliding Counter | Good | Medium | High |
| Token Bucket | Excellent | Low | High |
| Leaky Bucket | Limited | Low | High |

______________________________________________________________________

# Which Algorithm Should You Choose?

| Scenario | Recommended |
|-----------|-------------|
| Public APIs | Token Bucket |
| Login Protection | Sliding Window |
| Traffic Smoothing | Leaky Bucket |
| Simple Internal APIs | Fixed Window |

______________________________________________________________________

# Distributed Rate Limiting

Interview favorite.

Suppose

you have

```
10 API Servers
```

Each server

maintains

its own counter.

Problem

```
User

↓

Server A

↓

50 Requests
```

```
User

↓

Server B

↓

50 Requests
```

Total

```
100 Requests
```

But

each server

thinks

the limit

hasn't been reached.

______________________________________________________________________

# Shared Storage

Use

a central store.

```
API Servers

↓

Redis

↓

Shared Counter
```

Now

every server

sees

the same counter.

______________________________________________________________________

# Why Redis?

Redis

provides

- Atomic operations
- High speed
- Expiration
- Distributed access

Perfect

for

Rate Limiting.

______________________________________________________________________

# Atomic Increment

Interview favorite.

Redis

supports

```
INCR
```

```
INCR user:101
```

Counter

is updated

atomically.

No race conditions.

______________________________________________________________________

# Expiration

Suppose

limit

is

```
100 Requests

Per Minute
```

Redis key

expires

after

```
60 Seconds
```

Counter

resets

automatically.

______________________________________________________________________

# Distributed Architecture

```
Users

↓

Load Balancer

↓

API Gateway

↓

Redis

↓

Backend
```

All API servers

share

the same

Rate Limiter state.

______________________________________________________________________

# Different Limits

Example

Free User

```
100 Requests

Per Minute
```

Premium User

```
1000 Requests

Per Minute
```

Rate limits

can vary

based on

user plans.

______________________________________________________________________

# Endpoint-Specific Limits

Example

```
Login

↓

5 Requests/minute
```

```
Search

↓

200 Requests/minute
```

```
Payments

↓

20 Requests/minute
```

Different APIs

may require

different limits.

______________________________________________________________________

# Failure Scenario

Suppose

Redis

fails.

Possible approaches

- Fail Open

Allow requests

temporarily.

or

- Fail Closed

Reject requests.

Choice

depends on

business requirements.

______________________________________________________________________

# Monitoring

Monitor

- Rejected requests
- Allowed requests
- Redis latency
- Rate limit violations
- Top abusive users

______________________________________________________________________

# Typical Architecture

```
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Redis

↓

Microservices
```

______________________________________________________________________

# Common Interview Questions

## Why use Redis for Rate Limiting?

Redis supports fast in-memory operations, atomic counters, key expiration, and distributed access, making it ideal for
centralized rate limiting.

______________________________________________________________________

## Why not keep counters in memory?

With multiple application servers, each server would maintain a different counter. A shared data store ensures
consistent limits across the entire system.

______________________________________________________________________

## Why is Token Bucket popular?

It allows short bursts of traffic while enforcing a long-term average rate, making it suitable for APIs where occasional
bursts are acceptable.

______________________________________________________________________

## Why return HTTP 429?

HTTP 429 ("Too Many Requests") is the standard response indicating that the client has exceeded the allowed request
rate.

______________________________________________________________________

# Common Mistakes

## Using Local Memory

Local counters

do not work

well

in distributed systems.

______________________________________________________________________

## Ignoring Atomic Operations

Counters

must be

updated atomically

to avoid

race conditions.

______________________________________________________________________

## One Limit For Everything

Different APIs

often require

different limits.

______________________________________________________________________

## No Monitoring

Without metrics,

abuse

may go unnoticed.

______________________________________________________________________

# Best Practices

✅ Use Redis for distributed counters.

✅ Use atomic increment operations.

✅ Apply limits close to the edge.

✅ Return HTTP 429 with appropriate headers.

✅ Monitor rejected and accepted traffic.

✅ Choose algorithms based on traffic patterns.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between Token Bucket and Leaky Bucket?

### Answer

Token Bucket allows traffic bursts as long as tokens are available, while Leaky Bucket processes requests at a constant
rate, smoothing traffic but limiting bursts.

______________________________________________________________________

## Question

How would you implement a distributed Rate Limiter?

### Answer

Store request counters in a centralized system such as Redis using atomic increment operations and key expiration. All
application instances share the same counters, ensuring consistent enforcement.

______________________________________________________________________

## Question

Why isn't an in-memory counter sufficient?

### Answer

In-memory counters only track requests handled by a single server. In a distributed environment with multiple servers,
users could bypass limits by sending requests to different instances.

______________________________________________________________________

# Practice Exercise

Design

a Rate Limiter

for

100 Million Users.

Explain

1. Algorithm selection
1. Rate limit key
1. Redis design
1. Atomic operations
1. Distributed architecture
1. Failure handling
1. Monitoring
1. Trade-offs

Then answer

how your design

would change

for

- Login API
- Payment API
- Search API
- Public REST API

______________________________________________________________________

# Summary

Rate Limiting is one of the most common System Design interview topics because it protects services from abuse while
ensuring fair resource usage.

A strong solution should demonstrate

- Appropriate algorithm selection
- Distributed implementation
- Redis-based counters
- Atomic operations
- Monitoring
- Failure handling
- Trade-off analysis

Understanding Rate Limiting prepares you for designing scalable APIs, API Gateways, authentication systems, and
cloud-native applications.

______________________________________________________________________

# Next

[System Design – Notification System](29-design-notification-system.md)
