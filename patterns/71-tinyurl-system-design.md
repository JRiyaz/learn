# System Design - Part 71

# TinyURL System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- How to approach a real System Design interview
- Requirement gathering
- Capacity estimation
- API design
- URL shortening algorithms
- Database schema
- Cache strategy
- High-Level Architecture
- Scaling
- Reliability
- Security
- Trade-offs

______________________________________________________________________

# Before We Start

Imagine

you're interviewing

at

Google,

Amazon,

Uber,

or

Microsoft.

The interviewer says:

> **Design TinyURL.**

Many candidates

immediately start

drawing

Redis,

Kafka,

and

Load Balancers.

That's a mistake.

Remember

Lesson 70.

Always follow

the methodology.

______________________________________________________________________

# Step 1

# Clarify Requirements

Never assume.

Ask questions.

Functional Requirements

- Shorten long URLs
- Redirect short URLs
- Support custom aliases (optional)
- Track click counts (optional)
- URL expiration (optional)

Non-Functional Requirements

- High availability
- Low latency
- Highly scalable
- High read throughput

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

the service

has

100 Million users.

Assume

100 Million

new URLs

are created

every day.

Reads

are much higher

than writes.

Assume

10 redirects

per shortened URL.

```text id="tiny7101"
Writes

100M/day
```

```text id="tiny7102"
Reads

1B/day
```

Average Requests/sec

Writes

≈ 1,200/sec

Reads

≈ 11,500/sec

Peak traffic

is usually

2–3×

the average.

______________________________________________________________________

# Storage Estimation

Suppose

each record

stores

approximately

500 bytes.

```text id="tiny7103"
100M URLs/day

×

500 Bytes

=

50 GB/day
```

Yearly storage

≈ 18 TB

Storage planning

becomes

important.

______________________________________________________________________

# Step 3

# API Design

Create Short URL

```http id="tiny7104"
POST /api/v1/urls
```

Request

```json id="tiny7105"
{
  "url": "https://example.com/very/long/url"
}
```

Response

```json id="tiny7106"
{
  "short_url": "https://tiny.ly/aZ91Q"
}
```

______________________________________________________________________

Redirect

```http id="tiny7107"
GET /aZ91Q
```

Response

```http id="tiny7108"
HTTP 302 Found

Location:
https://example.com/very/long/url
```

302

is commonly used

because

the destination

may change.

______________________________________________________________________

# Step 4

# High-Level Design

```text id="tiny7109"
Client

↓

Load Balancer

↓

URL Service

↓

Redis Cache

↓

Database
```

______________________________________________________________________

Request Flow

Create

```text id="tiny7110"
Client

↓

API

↓

Generate Short Code

↓

Store Database

↓

Return Short URL
```

______________________________________________________________________

Redirect Flow

```text id="tiny7111"
Client

↓

Redis

↓

Database (if cache miss)

↓

Redirect
```

Most requests

never reach

the database.

______________________________________________________________________

# Step 5

# Database Design

Example Table

```text id="tiny7112"
URL

------

id

short_code

long_url

created_at

expires_at

click_count
```

Indexes

should exist

on

```text id="tiny7113"
short_code
```

because

redirects

search

using

the short code.

______________________________________________________________________

# Step 6

# Generating Short URLs

Interview favorite.

Requirements

- Unique
- Short
- Fast
- Collision-free

Several approaches

exist.

______________________________________________________________________

## Option 1

Auto Increment ID

```text id="tiny7114"
123456
```

Convert

to

Base62.

______________________________________________________________________

# Base62 Encoding

Characters

contain

```text id="tiny7115"
a-z

A-Z

0-9
```

Total

62 characters.

Example

```text id="tiny7116"
125

↓

cb
```

Large IDs

become

very small strings.

______________________________________________________________________

Advantages

✅ Simple

✅ Fast

Disadvantages

❌ Sequential IDs

are predictable.

______________________________________________________________________

## Option 2

Random Strings

Generate

6–8

random characters.

Example

```text id="tiny7117"
Ab91xQ
```

Advantages

✅ Hard to guess

Disadvantages

❌ Collision handling

is required.

______________________________________________________________________

## Option 3

Hash Function

Hash

the URL.

Example

```text id="tiny7118"
SHA-256
```

Take

the first

few characters.

Problem

Different URLs

may produce

the same

short code.

Need

collision resolution.

______________________________________________________________________

# Collision Handling

Interview favorite.

Suppose

two URLs

generate

the same code.

Possible solutions:

- Retry
- Append random character
- Generate another code

Never overwrite

existing mappings.

______________________________________________________________________

# Step 7

# Cache

Redirects

are

read-heavy.

Store

popular URLs

inside Redis.

```text id="tiny7119"
Redis

↓

Long URL
```

Benefits

✅ Low latency

✅ Reduced DB load

______________________________________________________________________

# Cache Flow

```text id="tiny7120"
Request

↓

Redis

↓

Database

↓

Redis

↓

Redirect
```

Classic

Cache-Aside Pattern.

______________________________________________________________________

# Step 8

# Scaling

Scale

URL Service

horizontally.

```text id="tiny7121"
Load Balancer

↓

Service 1

Service 2

Service 3
```

Services

remain

stateless.

______________________________________________________________________

# Database Scaling

Initially

one database

may be enough.

Later

add:

- Read Replicas
- Sharding

if

billions

of URLs

exist.

______________________________________________________________________

# CDN

Interview favorite.

Should

TinyURL

use

a CDN?

Generally,

No.

TinyURL

returns

HTTP redirects,

not

large static files.

Redis

provides

greater benefit

than

a CDN.

______________________________________________________________________

# Analytics

Suppose

we track

click counts.

Should

redirects

wait

for

database updates?

No.

Publish

an event.

```text id="tiny7122"
Redirect

↓

Kafka

↓

Analytics Worker
```

The redirect

remains fast.

______________________________________________________________________

# URL Expiration

Some links

expire

after

a certain date.

Example

```text id="tiny7123"
Expires

30 Days
```

Expired URLs

return

```http id="tiny7124"
404 Not Found
```

or

```http id="tiny7125"
410 Gone
```

depending

on

business requirements.

______________________________________________________________________

# Security

Protect

against:

- Malicious URLs
- Phishing
- Spam
- Abuse

Use:

- Authentication (optional)
- Rate Limiting
- Safe Browsing checks

______________________________________________________________________

# Availability

Use:

- Multiple API instances
- Database Replication
- Redis Replication
- Health Checks

Avoid

single points

of failure.

______________________________________________________________________

# Observability

Monitor:

- Redirect latency
- Cache hit rate
- Error rate
- Database latency
- Top URLs
- Requests/sec

Structured logs

should include

the short code

and

request ID.

______________________________________________________________________

# Failure Scenario

Suppose

Redis

fails.

```text id="tiny7126"
Redis

↓

Unavailable
```

Fallback

to

the database.

The system

becomes slower,

but

continues working.

______________________________________________________________________

# Another Failure

Suppose

Database

fails.

Redirects

for cached URLs

may still work

until

their cache entries

expire.

Database replication

reduces

this risk.

______________________________________________________________________

# Trade-offs

Base62

vs

Random IDs

| Base62 | Random |
| ------------- | ------------------- |
| Sequential | Random |
| No collisions | Possible collisions |
| Predictable | Hard to guess |

______________________________________________________________________

Redis

vs

Database

| Redis | Database |
| ---------------- | --------------- |
| Very fast | Persistent |
| Expensive memory | Larger storage |
| Cache | Source of truth |

______________________________________________________________________

# End-to-End Architecture

```text id="tiny7127"
Users

↓

DNS

↓

Load Balancer

↓

URL Service

↓

Redis

↓

PostgreSQL

↓

Kafka

↓

Analytics Worker
```

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design TinyURL?

Start by clarifying functional and non-functional requirements, then estimate expected traffic and storage. Design APIs
for creating and redirecting shortened URLs. Store mappings between short codes and long URLs in a relational database
with an index on the short code. Generate unique short codes using techniques such as Base62 encoding or random strings
with collision detection. Use Redis to cache frequently accessed URLs and reduce database load. Scale the application
horizontally behind a load balancer, replicate the database for high availability, and publish click events
asynchronously to Kafka for analytics. Protect the service using rate limiting and URL validation while monitoring
latency, cache hit rates, and system health.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Capacity estimation
- API design
- URL shortening algorithms
- Base62 encoding
- Database schema
- Redis caching
- High-level architecture
- Scaling
- Security
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL

This is the first complete end-to-end system design where multiple concepts from the foundation course come together.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design one of the most frequently asked interview questions:

- Real-time messaging
- Online presence
- Message delivery
- Read receipts
- Media uploads
- Offline synchronization
- Push notifications

We'll design **WhatsApp** from scratch.

______________________________________________________________________

# What's Next

[WhatsApp System Design](72-whatsapp-system-design.md)
