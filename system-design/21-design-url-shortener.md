# System Design Case Study – URL Shortener (TinyURL / Bitly)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to approach a complete System Design interview from start to finish by designing a URL Shortener. This chapter demonstrates the interview methodology, requirement gathering, architecture, scaling decisions, trade-offs, bottlenecks, and follow-up discussions.

______________________________________________________________________

# Why Start With URL Shortener?

The URL Shortener

is probably

the most common

System Design interview.

Why?

Because it covers

- APIs
- Database Design
- Caching
- Load Balancing
- Database Scaling
- Read vs Write Patterns
- CAP Trade-offs
- Replication
- Sharding
- Consistent Hashing
- CDN
- Rate Limiting

If you can design

TinyURL,

you already understand

a large portion

of System Design.

______________________________________________________________________

# Step 1

# Clarify Requirements

Never

draw architecture

immediately.

First,

ask questions.

Example

```
Can users

create short URLs?
```

```
Can users

choose custom aliases?
```

```
Should URLs expire?
```

```
Should analytics exist?
```

```
Should login

be required?
```

Interviewers

expect

clarification.

______________________________________________________________________

# Functional Requirements

Assume

we need

- Create short URL
- Redirect to original URL
- Optional expiration
- Click analytics
- Custom aliases (optional)

______________________________________________________________________

# Non-Functional Requirements

Need

- High Availability
- Low Latency
- Massive Read Traffic
- Horizontal Scalability
- Fault Tolerance
- Reliability

______________________________________________________________________

# Step 2

# Estimate Capacity

Assumptions

```
100 Million

Daily Users
```

Each user

creates

```
2 URLs/day
```

Daily writes

```
200 Million
```

______________________________________________________________________

# Read Traffic

Suppose

every short URL

is opened

```
100 Times
```

Daily reads

```
20 Billion
```

Read-heavy system.

______________________________________________________________________

# RPS Estimation

Daily Reads

```
20 Billion
```

Seconds/day

```
86400
```

Average

```
≈231,000 RPS
```

Peak

```
≈1 Million RPS
```

Immediately

we know

```
Caching

is mandatory.
```

______________________________________________________________________

# Step 3

# High-Level Architecture

```
                Users
                   │
                   ▼
              DNS
                   │
                   ▼
          Load Balancer
                   │
                   ▼
             API Servers
          ┌────────┴────────┐
          ▼                 ▼
      Redis Cache      URL Database
          │                 │
          └────────┬────────┘
                   ▼
              Analytics Queue
                   │
                   ▼
             Analytics Workers
```

______________________________________________________________________

# APIs

Create URL

```
POST /shorten
```

Request

```json
{
  "url":"https://example.com"
}
```

Response

```json
{
"short_url":"tiny.ly/aB12X"
}
```

______________________________________________________________________

Redirect

```
GET /aB12X
```

Response

```
301 Redirect

↓

Original URL
```

______________________________________________________________________

Analytics

```
GET /stats/{id}
```

______________________________________________________________________

# Step 4

# Database Design

Simple schema

| Column | Description |
|----------|------------|
| id | Internal ID |
| short_code | Short URL |
| original_url | Long URL |
| created_at | Timestamp |
| expires_at | Optional |
| click_count | Optional |

______________________________________________________________________

# Which Database?

Interview answer

Relational database

works well

because

relationships

are simple

and

lookups

are mostly

key-based.

NoSQL

also works

at very large scale.

The important part

is

explaining

the trade-offs.

______________________________________________________________________

# Step 5

# Short URL Generation

Interview favorite.

Several methods exist.

______________________________________________________________________

## Auto Increment

```
ID

↓

12345

↓

Base62

↓

dnh
```

Simple.

Problem

Single database

limits scaling.

______________________________________________________________________

## UUID

```
550e8400

↓

Very Long
```

Not suitable

for short URLs.

______________________________________________________________________

## Hash Function

Hash

the original URL.

Problem

Collisions.

______________________________________________________________________

## Base62 Encoding

Most common.

Characters

```
a-z

A-Z

0-9
```

Total

```
62 Characters
```

Example

```
125

↓

cb
```

Produces

short,

human-friendly URLs.

______________________________________________________________________

# Why Base62?

URL

becomes

small.

```
123456789

↓

8M0kX
```

Perfect

for

sharing.

______________________________________________________________________

# Collision Handling

Suppose

generated code

already exists.

Options

- Retry
- Increment ID
- Random suffix

Collisions

must be handled.

______________________________________________________________________

# Step 6

# Read Flow

```
Client

↓

Load Balancer

↓

Redis

↓

Cache Hit?

↓

Yes

↓

Redirect
```

______________________________________________________________________

Cache Miss

```
Redis

↓

Database

↓

Store In Redis

↓

Redirect
```

______________________________________________________________________

# Why Redis?

Read traffic

is

much higher

than

write traffic.

Caching

reduces

database load

dramatically.

______________________________________________________________________

# Step 7

# Analytics

Every redirect

generates

an event.

Instead of

updating

the database

immediately

```
Redirect

↓

RabbitMQ / Kafka

↓

Analytics Worker

↓

Database
```

Fast redirects.

Eventually

updated statistics.

______________________________________________________________________

# Step 8

# Database Replication

```
Primary

↓

Replica

↓

Replica
```

Reads

can use

replicas.

Writes

go

to

primary.

______________________________________________________________________

# Step 9

# Database Sharding

Eventually

billions

of URLs

exist.

Shard

using

```
Short Code

or

Hash
```

Each shard

stores

part

of the data.

______________________________________________________________________

# Step 10

# Consistent Hashing

Adding

new shards

shouldn't move

every URL.

Use

Consistent Hashing

to minimize

data movement.

______________________________________________________________________

# Step 11

# CDN

Normally

redirect responses

are tiny,

so CDN

isn't essential

for redirect logic.

However,

if the service also hosts

preview pages,

logos,

or other static assets,

those can be served

through a CDN.

Don't force

a CDN

where it provides

little benefit.

______________________________________________________________________

# Step 12

# Expired URLs

Suppose

link expires.

```
GET

↓

Expired

↓

410 Gone
```

Or

```
404 Not Found
```

depending

on

business requirements.

______________________________________________________________________

# Step 13

# Security

Prevent

abuse.

Use

- Rate Limiting
- CAPTCHA (optional)
- Authentication (optional)
- URL validation
- Malware detection (optional)

______________________________________________________________________

# Step 14

# High Availability

```
Load Balancer

↓

Multiple API Servers

↓

Redis Cluster

↓

Replicated Database
```

No

single point

of failure.

______________________________________________________________________

# Step 15

# Failure Scenarios

## Redis Down

Fallback

to

database.

Performance

drops.

System

continues working.

______________________________________________________________________

## Primary Database Down

Replica

becomes

new primary.

______________________________________________________________________

## API Server Down

Load Balancer

routes traffic

to

healthy instances.

______________________________________________________________________

# Scaling

```
More Users

↓

More API Servers
```

```
More Reads

↓

More Redis Nodes
```

```
More Data

↓

More Database Shards
```

Everything

scales

horizontally.

______________________________________________________________________

# Read vs Write Ratio

```
Reads

99%
```

```
Writes

1%
```

Heavy

read optimization.

______________________________________________________________________

# CAP Discussion

URL Shortener

generally favors

```
Availability
```

Small delays

in analytics

or replication

are acceptable.

The core redirect

should remain

available.

______________________________________________________________________

# Rate Limiting

Prevent

abuse.

Example

```
100 URLs

Per Hour
```

Per user.

______________________________________________________________________

# Monitoring

Monitor

- Redirect latency
- Cache hit ratio
- Error rate
- Database latency
- Queue length
- API latency

______________________________________________________________________

# Possible Improvements

- QR Code generation
- Custom aliases
- Link expiration
- Password-protected URLs
- Geo analytics
- Device analytics
- Click history
- Spam detection

______________________________________________________________________

# Complete Architecture

```
                    Users
                       │
                       ▼
                     DNS
                       │
                       ▼
                Load Balancer
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
     API Server                   API Server
        │                             │
        └──────────────┬──────────────┘
                       ▼
                 Redis Cluster
                       │
              Cache Miss?
                 │          │
               Yes         No
                 │          │
                 ▼          ▼
           Primary Database Redirect
                 │
           Read Replicas
                 │
                 ▼
         RabbitMQ / Kafka
                 │
                 ▼
         Analytics Workers
                 │
                 ▼
          Analytics Database
```

______________________________________________________________________

# Common Interview Follow-Up Questions

## Why not use UUID?

UUIDs

are long,

consume

more storage,

and produce

less user-friendly URLs.

Base62

creates

shorter identifiers.

______________________________________________________________________

## Why use Redis?

The system

is read-heavy.

Caching

dramatically reduces

database queries

and latency.

______________________________________________________________________

## How do you prevent duplicate short URLs?

Use

a unique constraint

on

the short code

and regenerate

if a collision occurs.

______________________________________________________________________

## What happens if Redis loses all data?

The application

falls back

to the database.

Cache

is rebuilt

gradually.

______________________________________________________________________

## How would you support custom aliases?

Allow users

to request

a specific code,

validate

its availability,

and enforce

uniqueness.

______________________________________________________________________

## How would you delete expired links?

Background workers

periodically

remove

expired records

or mark them inactive.

______________________________________________________________________

# Common Mistakes

## Starting With Architecture

Always gather

requirements first.

______________________________________________________________________

## Forgetting Read/Write Ratio

The system

is

heavily

read-oriented.

______________________________________________________________________

## Ignoring Cache

Caching

is critical

for redirect performance.

______________________________________________________________________

## Storing Analytics Synchronously

Analytics

should be

asynchronous

to keep

redirects fast.

______________________________________________________________________

## Overengineering

Don't introduce

Kafka,

CDN,

or sharding

without explaining

why

they're needed.

______________________________________________________________________

# Best Practices

✅ Clarify requirements first.

✅ Estimate traffic.

✅ Design the API.

✅ Choose an appropriate database.

✅ Cache redirects.

✅ Use asynchronous analytics.

✅ Discuss replication and sharding only when scale requires them.

______________________________________________________________________

# Interview Deep Dive

## Question

How would you generate unique short URLs?

### Answer

A common approach is to generate a unique numeric ID and encode it using Base62 to produce a compact, URL-friendly short
code. Other approaches are possible, but they should address uniqueness and collision handling.

______________________________________________________________________

## Question

Why is Redis important in a URL Shortener?

### Answer

Redirect requests are read-heavy and latency-sensitive. Redis stores frequently accessed mappings in memory, allowing
redirects to complete much faster while significantly reducing database load.

______________________________________________________________________

## Question

Would you use RabbitMQ or Kafka for analytics?

### Answer

Either can work. RabbitMQ is suitable for reliable background processing, while Kafka is preferable for large-scale
event streaming and long-term analytics pipelines. The choice depends on throughput and analytics requirements.

______________________________________________________________________

# Practice Exercise

Redesign the URL Shortener

for

1 Billion Users.

Explain

1. API design
1. Capacity estimation
1. Database choice
1. Short code generation
1. Cache strategy
1. Replication
1. Sharding
1. Monitoring
1. Failure recovery
1. Trade-offs

Try answering

without notes.

This closely resembles

real

System Design interviews.

______________________________________________________________________

# Summary

The URL Shortener is one of the best interview problems because it combines many fundamental System Design concepts into
a single application.

A strong solution should demonstrate

- Requirement gathering
- Capacity estimation
- API design
- Database modeling
- Caching
- Asynchronous processing
- Replication
- Sharding
- High availability
- Trade-off analysis

If you can confidently design a URL Shortener, you'll have a strong foundation for tackling many other System Design
interview problems.

______________________________________________________________________

# Next

[System Design Case Study – Instagram](22-design-instagram.md)
