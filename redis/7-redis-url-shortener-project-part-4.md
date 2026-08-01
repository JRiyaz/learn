# Redis URL Shortener Project - Part 4 (Final)

## Introduction

Congratulations!

You have successfully built a complete **Redis-powered URL Shortener**.

Throughout this project, you learned how Redis is used in real backend systems—not just as a cache, but as a
high-performance in-memory data store supporting multiple data structures and common application patterns.

In this final chapter, we'll:

- Review the complete architecture
- Run the application
- Walk through the request flow
- Discuss production improvements
- Cover interview questions
- Summarize everything learned

______________________________________________________________________

# Final Architecture

```text id="redis401"
                     Client
                        │
                        ▼
                  FastAPI API
                        │
                        ▼
                     Redis
      ┌──────────┬──────────┬──────────┬──────────┐
      ▼          ▼          ▼          ▼
   Strings     Hashes      Sets    Sorted Sets
      │          │          │          │
      ▼          ▼          ▼          ▼
 Original    Metadata   Visitors   Rankings
    URLs
```

Each Redis data structure solves a different problem.

______________________________________________________________________

# Complete Redis Key Design

```text id="redis402"
url:abc123
------------------------
Original URL

url_meta:abc123
------------------------
Metadata

clicks:abc123
------------------------
Click Counter

visitors:abc123
------------------------
Unique Visitors

top_urls
------------------------
Sorted Set
```

A consistent key naming strategy makes applications easier to understand and maintain.

______________________________________________________________________

# Complete Request Flow

User creates URL

```text id="redis403"
POST /shorten

↓

Generate Code

↓

Store URL

↓

Store Metadata

↓

Return Code
```

______________________________________________________________________

User opens URL

```text id="redis404"
GET /abc123

↓

Lookup URL

↓

Pipeline

├── Increment Click Counter

├── Update Last Access

├── Track Visitor

└── Update Ranking

↓

Return Original URL
```

______________________________________________________________________

Analytics

```text id="redis405"
GET /analytics/abc123

↓

Read

String

+

Hash

+

Set

+

Counter

↓

Return Statistics
```

______________________________________________________________________

# Running the Project

Start Redis.

```bash id="redis406"
redis-server
```

Verify Redis is running.

```bash id="redis407"
redis-cli ping
```

Expected output

```text id="redis408"
PONG
```

Run FastAPI.

```bash id="redis409"
uvicorn app:app --reload
```

______________________________________________________________________

# Example Session

Create URL

```http id="redis410"
POST /shorten
```

```text id="redis411"
https://www.python.org
```

Response

```json id="redis412"
{
    "short_code": "aB31Xd"
}
```

Open

```http id="redis413"
GET /aB31Xd
```

Analytics

```http id="redis414"
GET /analytics/aB31Xd
```

Example Response

```json id="redis415"
{
    "url": "https://www.python.org",
    "clicks": 25,
    "unique_visitors": 12,
    "metadata": {
        "created_by": "Alice",
        "created_at": "2026-08-02",
        "last_access": "2026-08-03T12:30:41"
    }
}
```

______________________________________________________________________

# Redis Concepts Used

| Redis Feature | Used |
| --------------- | ---- |
| Strings | ✅ |
| Hashes | ✅ |
| Sets | ✅ |
| Sorted Sets | ✅ |
| TTL | ✅ |
| Counters | ✅ |
| Pipelines | ✅ |
| Transactions | ✅ |
| MGET | ✅ |
| MSET | ✅ |
| Connection Pool | ✅ |
| Rate Limiting | ✅ |

______________________________________________________________________

# Data Structure Review

## Strings

Used for:

```text id="redis416"
Original URL
```

______________________________________________________________________

## Hashes

Used for:

```text id="redis417"
Metadata
```

______________________________________________________________________

## Sets

Used for:

```text id="redis418"
Unique Visitors
```

______________________________________________________________________

## Sorted Sets

Used for:

```text id="redis419"
Top URLs
```

______________________________________________________________________

## Counters

Used for:

```text id="redis420"
Click Count
```

______________________________________________________________________

# Why Redis?

Compared with storing everything in a relational database:

Redis provides:

- Extremely fast lookups
- Atomic counters
- Built-in expiration
- Efficient data structures
- Low latency
- High throughput

These characteristics make it ideal for caching, session storage, counters, leaderboards, and other
performance-sensitive workloads.

______________________________________________________________________

# Production Improvements

If this application were deployed to production,

consider adding:

### PostgreSQL

Persist URLs permanently.

Redis becomes a cache instead of the system of record.

______________________________________________________________________

### Cache-Aside Pattern

```text id="redis421"
Request

↓

Redis

↓

Cache Miss?

↓

PostgreSQL

↓

Save to Redis

↓

Return
```

______________________________________________________________________

### Authentication

Restrict URL creation to authenticated users.

______________________________________________________________________

### Background Jobs

Move analytics aggregation to asynchronous workers.

______________________________________________________________________

### Logging

Use structured logs.

______________________________________________________________________

### Monitoring

Track:

- Cache hit ratio
- Cache miss ratio
- Memory usage
- Latency
- Evictions
- Command throughput

______________________________________________________________________

### Docker

Containerize Redis and the application.

______________________________________________________________________

### Tests

Add:

- Unit tests
- Integration tests

______________________________________________________________________

# Common Interview Questions

## Why Redis Instead of PostgreSQL?

Redis keeps data in memory, making lookups significantly faster.

______________________________________________________________________

## Why Use Hashes?

To group related fields under a single key.

______________________________________________________________________

## Why Use Sorted Sets?

To maintain rankings based on scores.

______________________________________________________________________

## Why Use TTL?

Automatically remove temporary data.

______________________________________________________________________

## Why Use Pipelines?

Reduce network round trips and improve throughput.

______________________________________________________________________

## Why Use Connection Pools?

Reuse TCP connections instead of creating a new connection for every request.

______________________________________________________________________

## Why Are Redis Counters Useful?

They provide atomic increment operations without requiring explicit locking.

______________________________________________________________________

# Mini Interview

## Question

How would you improve this project for production?

### Answer

I would:

- Store permanent URL data in PostgreSQL.
- Use Redis as a cache.
- Add authentication and authorization.
- Implement proper HTTP redirects.
- Add structured logging.
- Add Docker and Docker Compose.
- Monitor Redis metrics.
- Add unit and integration tests.
- Add asynchronous analytics processing.
- Implement backup and persistence strategies.

______________________________________________________________________

# Suggested Extensions

Try implementing these features yourself.

1. Custom short URLs.
1. Password-protected URLs.
1. URL expiration dates.
1. QR code generation.
1. Country-based analytics.
1. Browser analytics.
1. Device analytics.
1. Daily click reports.
1. User accounts.
1. Public analytics dashboard.

These extensions reinforce Redis usage while introducing practical backend features.

______________________________________________________________________

# Final Revision

You should now understand:

✓ Redis Architecture

✓ Strings

✓ Hashes

✓ Sets

✓ Sorted Sets

✓ Counters

✓ TTL

✓ Expiration

✓ Connection Pools

✓ Pipelines

✓ Transactions

✓ MGET

✓ MSET

✓ Rate Limiting

✓ Caching Patterns

✓ Key Design

✓ Analytics

______________________________________________________________________

# Course Review Questions

1. Why is Redis so fast?
1. When should you use Strings?
1. When should you use Hashes?
1. When should you use Sets?
1. Why use Sorted Sets?
1. What is TTL?
1. What are Redis Pipelines?
1. Why use Connection Pools?
1. How do Redis counters work?
1. How would you implement rate limiting?
1. What is the Cache-Aside Pattern?
1. Why use Redis for session storage?
1. How would you monitor Redis in production?
1. When should Redis be the primary data store versus a cache?
1. How would you scale this application?

______________________________________________________________________

# Final Project Summary

In this project, you built a realistic Redis-powered URL Shortener that demonstrated:

- Redis connection pooling
- URL storage
- Temporary URLs with TTL
- Click counters
- Metadata using Hashes
- Unique visitor tracking using Sets
- Popular URL rankings using Sorted Sets
- Analytics endpoints
- Pipelines for performance
- Batch operations
- Rate limiting
- Cache-oriented design

This project brings together the Redis concepts covered throughout the course and provides a practical foundation before
using Redis alongside PostgreSQL, Kafka, Docker, and microservices in larger distributed systems.

______________________________________________________________________

# Completed Technology Projects

At this point, you now have three hands-on projects:

1. **SQL Library Management System**

   - Relational database design
   - SQLAlchemy 2.x
   - SQLModel
   - Transactions
   - Reporting

1. **Redis URL Shortener**

   - Redis data structures
   - TTL
   - Pipelines
   - Rate limiting
   - Analytics

1. **Kafka Order Processing System**

   - Producers
   - Consumers
   - Event-driven architecture
   - DLQ
   - Retry
   - Idempotent consumers

These projects will serve as the foundation for the final production-grade microservices application, where all of these
technologies will work together.

______________________________________________________________________

## Next File

[Kafka Fundamentals](../kafka/1-kafka-fundamentals.md)
