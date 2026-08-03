# Capacity Estimation for System Design Interviews

**File:** `01-capacity-estimation.md`

> This document is a master reference for capacity estimation in High-Level Design (HLD) interviews.
>
> The goal is **not** to get exact numbers. The goal is to demonstrate structured thinking, reasonable assumptions, and an understanding of how scale impacts architecture.

______________________________________________________________________

# Table of Contents

1. Introduction
1. Why Capacity Estimation Matters
1. Interview Strategy
1. Standard Assumptions
1. Estimation Framework
1. Traffic Estimation
1. Storage Estimation
1. Bandwidth Estimation
1. Memory & Cache Estimation
1. Database Estimation
1. Queue Estimation
1. Growth Planning
1. Common Interview Numbers
1. Worked Examples
1. Common Mistakes
1. Quick Cheat Sheet
1. Navigation

______________________________________________________________________

# 1. Introduction

Capacity estimation answers questions like:

- How many users?
- How much storage?
- How many requests?
- How many servers?
- How much bandwidth?
- How much cache?

Interviewers don't expect exact calculations.

They expect you to think logically.

______________________________________________________________________

# 2. Why Capacity Estimation Matters

Capacity estimation helps determine:

- Database size
- Cache size
- CDN usage
- Network bandwidth
- Number of servers
- Number of Kafka partitions
- Number of Redis nodes

Without estimating scale,

it's impossible to choose the right architecture.

______________________________________________________________________

# 3. Interview Strategy

Always follow this order:

```
Users

↓

Traffic

↓

Storage

↓

Bandwidth

↓

Memory

↓

Database

↓

Cache

↓

Queue

↓

Growth
```

Never start with database sharding.

Start with users.

______________________________________________________________________

# 4. Standard Assumptions

Unless the interviewer specifies numbers, make reasonable assumptions.

| Metric | Typical Assumption |
|---------|-------------------:|
| Daily Active Users (DAU) | 10% of registered users |
| Peak Traffic | 3–10× average |
| Read : Write Ratio | 80:20 (typical web app) |
| Cache Hit Ratio | 80–95% |
| Replication Factor | 3 |
| KB | 1024 Bytes |
| MB | 1024 KB |
| GB | 1024 MB |
| TB | 1024 GB |

Always state assumptions clearly.

Example:

> I'll assume 10 million registered users and 1 million daily active users.

______________________________________________________________________

# 5. Estimation Framework

```
Users

↓

Requests

↓

QPS

↓

Storage

↓

Bandwidth

↓

Cache

↓

Database

↓

Growth
```

Memorize this.

______________________________________________________________________

# 6. Traffic Estimation

## Step 1

Estimate users.

Example:

Registered Users

```
100 Million
```

DAU

```
10 Million
```

______________________________________________________________________

## Step 2

Requests per User

Suppose

each user performs

20 requests/day.

Total Requests

```
10M × 20

=

200M Requests/day
```

______________________________________________________________________

## Step 3

Average QPS

Formula

```
Average QPS

=

Daily Requests

/

86400
```

Example

```
200M

/

86400

≈

2315 QPS
```

______________________________________________________________________

## Step 4

Peak QPS

Traffic isn't uniform.

Assume

Peak Factor = 5

```
Peak QPS

=

2315 × 5

≈

11,500
```

Design using Peak QPS.

______________________________________________________________________

# 7. Storage Estimation

Formula

```
Storage

=

Number of Objects

×

Average Object Size
```

______________________________________________________________________

## Example 1

Messages

100M messages/day

Average size

1 KB

```
100 GB/day
```

One year

```
36.5 TB
```

______________________________________________________________________

## Example 2

Photos

20M photos/day

Average size

2 MB

```
40 TB/day
```

______________________________________________________________________

## Example 3

Videos

1M videos/day

Average size

200 MB

```
200 TB/day
```

Videos dominate storage.

______________________________________________________________________

# Metadata Storage

Always separate

metadata

from

binary data.

Example

Photo

```
Image → Object Storage

Metadata → Database
```

______________________________________________________________________

# 8. Bandwidth Estimation

Formula

```
Bandwidth

=

QPS

×

Average Response Size
```

Example

```
10,000 QPS

×

100 KB

=

1 GB/sec
```

Large media

should always

go through a CDN.

______________________________________________________________________

# 9. Memory & Cache Estimation

Cache only

hot data.

Formula

```
Cache Size

=

Hot Data

×

Average Object Size
```

Example

10M hot products

1 KB each

```
10 GB Cache
```

Never cache everything.

______________________________________________________________________

## Cache Hit Ratio

Example

90%

1000 requests

↓

900 served by Redis

↓

100 go to Database

______________________________________________________________________

# 10. Database Estimation

Estimate:

- Rows
- Growth
- Replicas
- Shards

Example

Orders/day

```
5 Million
```

Yearly

```
≈1.8 Billion
```

Database design

must account for

future growth.

______________________________________________________________________

## Replication

Typical

```
Primary

↓

Replica

↓

Replica
```

Read traffic

is distributed

across replicas.

______________________________________________________________________

## Sharding

Required when

one database

cannot handle

storage

or

traffic.

Shard by:

- User ID
- Order ID
- Region

______________________________________________________________________

# 11. Queue Estimation

Suppose

Notifications

```
20 Million/day
```

Peak

```
2000/sec
```

Consumers

```
500 msg/sec
```

Required Consumers

```
2000

/

500

=

4
```

Always estimate

consumer throughput.

______________________________________________________________________

# 12. Growth Planning

Never design

only

for today's scale.

Estimate

1 year

3 years

5 years

Example

Current

```
10 TB
```

Growth

100%

Next Year

```
20 TB
```

Mention this during interviews.

______________________________________________________________________

# 13. Common Interview Numbers

These aren't rules—

they're reasonable assumptions.

| Metric | Typical Value |
|---------|--------------:|
| DAU | 10% of registered users |
| Peak Factor | 3–10× |
| Cache Hit Ratio | 80–95% |
| Read Heavy Apps | 90:10 |
| Social Media | 95:5 |
| Banking | 50:50 |
| Replication Factor | 3 |

______________________________________________________________________

# 14. Worked Example

## URL Shortener

Assumptions

Registered Users

```
100 Million
```

DAU

```
10 Million
```

Requests/User

```
5
```

Daily Requests

```
50 Million
```

Average QPS

```
≈580
```

Peak QPS

```
≈3000
```

Short URL

100 Bytes

Daily Storage

```
5 GB/day
```

Yearly

```
≈1.8 TB
```

This estimation

is sufficient

to start designing.

______________________________________________________________________

# 15. Common Mistakes

## No Assumptions

Never say

"I don't know."

State reasonable assumptions.

______________________________________________________________________

## Using Average Instead of Peak

Always estimate

Peak QPS.

______________________________________________________________________

## Ignoring Growth

Today's architecture

must support

future traffic.

______________________________________________________________________

## Estimating Everything

Estimate only

what affects architecture.

Don't waste time

calculating

CPU cycles

unless necessary.

______________________________________________________________________

## Forgetting CDN

Large images

videos

documents

should not

go through

application servers.

______________________________________________________________________

# 16. 5-Minute Cheat Sheet

## Estimation Order

```
Users

↓

Requests

↓

Average QPS

↓

Peak QPS

↓

Storage

↓

Bandwidth

↓

Memory

↓

Cache

↓

Database

↓

Growth
```

______________________________________________________________________

## Important Formulae

### Average QPS

```
Daily Requests

/

86400
```

______________________________________________________________________

### Peak QPS

```
Average QPS

×

Peak Factor
```

______________________________________________________________________

### Storage

```
Objects

×

Object Size
```

______________________________________________________________________

### Cache Size

```
Hot Data

×

Object Size
```

______________________________________________________________________

### Bandwidth

```
QPS

×

Response Size
```

______________________________________________________________________

## Golden Rules

✅ State assumptions clearly.

✅ Use Peak QPS.

✅ Separate metadata from binary data.

✅ Cache only hot data.

✅ Mention replication.

✅ Mention growth planning.

✅ Keep calculations simple.

✅ Round numbers for easier mental math.

______________________________________________________________________

# Final Notes

Capacity estimation is not a mathematics exam.

Interviewers evaluate:

- Structured thinking
- Reasonable assumptions
- Understanding of scale
- Ability to justify design decisions

If your assumptions are reasonable and your calculations are consistent, small numerical differences rarely matter.

______________________________________________________________________

## Next

[Load Balancer](02-load-balancer.md)
