# System Design Cheat Sheet

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: A last-minute revision guide covering the most important System Design concepts, interview patterns, technologies, trade-offs, formulas, and decision-making strategies.

______________________________________________________________________

# 1. System Design Interview Flow

Always follow

```
Requirements

↓

Capacity Estimation

↓

API Design

↓

Data Model

↓

High-Level Architecture

↓

Deep Dive

↓

Scaling

↓

Failure Handling

↓

Monitoring

↓

Trade-offs
```

Never

start

with

technologies.

______________________________________________________________________

# 2. Functional Requirements

Examples

- Authentication
- CRUD
- Search
- Upload
- Download
- Notifications
- Analytics
- Scheduling

______________________________________________________________________

# 3. Non-Functional Requirements

Always clarify

- Availability
- Scalability
- Latency
- Consistency
- Durability
- Security
- Fault Tolerance

______________________________________________________________________

# 4. Capacity Estimation

Estimate

- Users
- DAU
- RPS
- Storage
- Bandwidth
- Growth

Interviewers

care about

your assumptions,

not

perfect numbers.

______________________________________________________________________

# 5. Core Components

Almost every system

uses

```
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Application Servers

↓

Cache

↓

Database

↓

Queue

↓

Storage
```

______________________________________________________________________

# 6. Load Balancer

Purpose

- Distribute traffic
- High availability
- Health checks

Examples

- NGINX
- HAProxy
- AWS ALB

______________________________________________________________________

# 7. API Gateway

Responsibilities

- Authentication
- Routing
- Rate Limiting
- Logging
- Monitoring
- Request Validation

______________________________________________________________________

# 8. Cache

When to use

- Read-heavy systems
- Frequently accessed data
- Expensive queries

Common choice

```
Redis
```

______________________________________________________________________

# 9. Cache Strategies

Cache Aside

```
Cache

↓

Database
```

Most common.

______________________________________________________________________

Write Through

```
Application

↓

Cache

↓

Database
```

______________________________________________________________________

Write Behind

```
Application

↓

Cache

↓

Background Database Write
```

______________________________________________________________________

Refresh Ahead

```
Refresh

Before

Expiration
```

______________________________________________________________________

# 10. Cache Problems

Cache Stampede

↓

Many requests

after expiration.

Solution

- Mutex
- Refresh Ahead
- Random TTL

______________________________________________________________________

Cache Penetration

↓

Invalid keys.

Solution

Cache NULL.

______________________________________________________________________

Cache Avalanche

↓

Many keys expire together.

Solution

Random TTL.

______________________________________________________________________

# 11. Database Scaling

Vertical

```
Bigger Machine
```

Horizontal

```
More Machines
```

Prefer

horizontal scaling.

______________________________________________________________________

# 12. Replication

```
Primary

↓

Replica

↓

Replica
```

Benefits

- High Availability
- Read Scaling

Trade-off

Replication lag.

______________________________________________________________________

# 13. Sharding

Split data

across

multiple databases.

Example

```
Shard 1

↓

Users 1-1M
```

```
Shard 2

↓

Users 1M-2M
```

______________________________________________________________________

# 14. Partitioning

Horizontal

↓

Rows

Vertical

↓

Columns

______________________________________________________________________

# 15. Consistent Hashing

Purpose

Reduce

data movement

when

adding

or removing

servers.

Used in

- Cache
- Database
- Storage

______________________________________________________________________

# 16. CAP Theorem

Choose

between

```
Consistency

Availability

Partition Tolerance
```

Examples

Banking

↓

Consistency

Social Feed

↓

Availability

______________________________________________________________________

# 17. Database Choice

SQL

Use when

- Transactions
- ACID
- Relationships

Examples

Orders

Payments

______________________________________________________________________

NoSQL

Use when

- Flexible schema
- Massive scale
- High write throughput

Examples

Logs

Feeds

Sessions

______________________________________________________________________

# 18. Message Queue

Use for

- Notifications
- Analytics
- Background Jobs
- Emails
- Image Processing

Examples

- RabbitMQ
- Kafka
- AWS SQS

______________________________________________________________________

# 19. RabbitMQ vs Kafka

RabbitMQ

- Task Queue
- Low latency
- Reliable jobs

Kafka

- Event Streaming
- High throughput
- Analytics

______________________________________________________________________

# 20. Distributed Transactions

Single Database

↓

ACID

Multiple Services

↓

Saga Pattern

Reliable Events

↓

Outbox Pattern

______________________________________________________________________

# 21. Storage

Relational DB

↓

Structured data

Object Storage

↓

Images

Videos

Documents

______________________________________________________________________

# 22. CDN

Store

static content

near users.

Used for

- Images
- Videos
- CSS
- JavaScript

Benefits

- Lower latency
- Lower bandwidth

______________________________________________________________________

# 23. Search

Need

- Full-text search
- Ranking
- Filters

Typical choice

```
Elasticsearch
```

______________________________________________________________________

# 24. Rate Limiter

Algorithms

- Fixed Window
- Sliding Window
- Token Bucket
- Leaky Bucket

Most common

```
Token Bucket
```

______________________________________________________________________

# 25. Notification System

Use

- Queue
- Workers
- Retry
- DLQ
- Templates
- Preferences

______________________________________________________________________

# 26. Distributed Cache

Remember

- Cache Aside
- TTL
- LRU
- LFU
- Replication
- Consistent Hashing

______________________________________________________________________

# 27. Service Discovery

Purpose

Find services

dynamically.

Examples

- Consul
- Eureka
- Kubernetes Services

______________________________________________________________________

# 28. Monitoring

Monitor

- CPU
- Memory
- Latency
- Error Rate
- Queue Length
- Cache Hit Ratio
- Database Latency

______________________________________________________________________

# 29. Failure Recovery

Always discuss

- Retry
- Timeout
- Circuit Breaker
- Failover
- Replication
- Backup

______________________________________________________________________

# 30. Security

Mention

- Authentication
- Authorization
- HTTPS
- Encryption
- Rate Limiting
- Input Validation

______________________________________________________________________

# 31. High Availability

Avoid

Single Points

of Failure.

Use

- Multiple Servers
- Replication
- Load Balancer
- Health Checks

______________________________________________________________________

# 32. Event-Driven Architecture

Producer

↓

Queue

↓

Consumer

Benefits

- Loose coupling
- Scalability
- Reliability

______________________________________________________________________

# 33. Real-Time Systems

Use

- WebSockets
- SSE (when appropriate)

Examples

- WhatsApp
- Uber
- Trading Platforms

______________________________________________________________________

# 34. Object Storage

Use for

- Images
- Videos
- PDFs
- Backups

Don't store

large binary files

inside

relational databases.

______________________________________________________________________

# 35. Common System Choices

| Problem | Typical Solution |
|----------|------------------|
| Read-heavy | Redis |
| Search | Elasticsearch |
| Messaging | Kafka / RabbitMQ |
| Images | Object Storage |
| Global Delivery | CDN |
| Real-time | WebSockets |
| Scheduling | Cron / Scheduler |
| Service Discovery | Kubernetes / Consul |
| Notifications | Queue + Workers |
| Analytics | Kafka |

______________________________________________________________________

# 36. Common Interview Questions

Be prepared for

```
Why Redis?

Why Kafka?

Why SQL?

Why NoSQL?

Why CDN?

Why Queue?

Why Sharding?

Why Replication?

Why WebSockets?

Why Saga?
```

Always answer

```
Problem

↓

Solution

↓

Trade-off
```

______________________________________________________________________

# 37. Universal Architecture

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
              API Gateway
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
    API Server  API Server API Server
         │
         ▼
      Redis Cache
         │
         ▼
      Database
         │
         ▼
 RabbitMQ / Kafka
         │
         ▼
 Background Workers
         │
         ▼
 Object Storage
         │
         ▼
        CDN
```

______________________________________________________________________

# 38. Universal Scaling Strategy

Traffic grows

↓

Load Balancer

↓

More API Servers

↓

Redis Cluster

↓

Read Replicas

↓

Database Sharding

↓

Message Queue

↓

Background Workers

Scale

only

the bottleneck.

______________________________________________________________________

# 39. Universal Failure Strategy

Ask

"What if this fails?"

For every component.

Examples

Load Balancer

↓

Health checks

Redis

↓

Fallback to DB

Database

↓

Replica Promotion

Queue

↓

Retry

Workers

↓

Another Worker

Storage

↓

Replication

______________________________________________________________________

# 40. Final Interview Checklist

Before finishing,

confirm

you covered

```
✔ Requirements

✔ Capacity Estimation

✔ APIs

✔ Data Model

✔ Architecture

✔ Database

✔ Cache

✔ Queue

✔ Storage

✔ Scaling

✔ Monitoring

✔ Security

✔ Failure Recovery

✔ Trade-offs
```

______________________________________________________________________

# 41. Golden Rules

✅ Clarify before designing.

✅ Keep the first architecture simple.

✅ Scale only bottlenecks.

✅ Explain every technology choice.

✅ Mention trade-offs.

✅ Handle failures.

✅ Think aloud.

✅ Don't overengineer.

______________________________________________________________________

# One-Minute Revision

```
Requirements

↓

Estimate Scale

↓

API

↓

Database

↓

Architecture

↓

Cache

↓

Queue

↓

Storage

↓

Scaling

↓

Monitoring

↓

Failures

↓

Trade-offs
```

If you remember

this sequence,

you can confidently approach

almost any

System Design interview.

______________________________________________________________________

# Summary

This cheat sheet is designed as a final revision guide before interviews.

Instead of memorizing complete architectures, remember:

- **Follow a structured framework**
- **Choose technologies to solve specific problems**
- **Always explain trade-offs**
- **Discuss scaling, failures, and monitoring**
- **Communicate your reasoning clearly**

A candidate who follows this approach consistently is far more likely to succeed than one who simply memorizes
technology names.

______________________________________________________________________

# Next

[System Design Common Mistakes](35-system-design-common-mistakes.md)
