# 25. Database Scaling — Practical Overview

**Previous:** [24. SQLAlchemy Performance & Async](./24-sqlalchemy-performance.md)

**Next:** [26. Redis Fundamentals](./26-redis.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain why a database becomes a bottleneck as an application grows.
- Distinguish vertical and horizontal scaling.
- Explain database replication.
- Explain read replicas and their trade-offs.
- Understand partitioning and when it helps.
- Explain sharding at a practical overview level.
- Understand denormalization as a scaling technique.
- Identify common database bottlenecks.
- Choose an appropriate scaling strategy for a backend workload.
- Discuss database scaling decisions in a senior-level interview.

> **Scope note:** This is a practical overview rather than a deep database-internals topic. File 19 covers normalization/denormalization in detail, while File 21 covers indexes and query performance.

______________________________________________________________________

# 1. Why Database Scaling Matters

As an application grows, the database can become a bottleneck.

Growth can come from:

- More requests
- More concurrent users
- More data
- More writes
- More reads
- More complex queries
- Larger transactions

Eventually, simply adding application servers may not solve the problem.

```text
More application servers
        ↓
More database traffic
        ↓
Database becomes bottleneck
```

______________________________________________________________________

# 2. Database Bottleneck

A database bottleneck occurs when database capacity limits overall application performance.

Symptoms can include:

- High query latency
- High CPU usage
- High memory usage
- Disk I/O pressure
- Connection-pool exhaustion
- Lock contention
- Replication lag
- Slow writes
- Slow reads

The first step should be measurement rather than immediately introducing distributed database architecture.

______________________________________________________________________

# 3. Scaling Strategy

A practical progression is often:

```text
Optimize queries
      ↓
Indexes
      ↓
Scale database vertically
      ↓
Read replicas
      ↓
Partitioning
      ↓
Sharding
```

This is not a mandatory sequence.

The correct strategy depends on the actual bottleneck.

______________________________________________________________________

# 4. Vertical Scaling

Vertical scaling means increasing the resources of one database server.

For example:

```text
More CPU
More RAM
Faster storage
Higher I/O capacity
```

Instead of:

```text
Database A
```

you move to a more powerful:

```text
Database A+
```

______________________________________________________________________

# 5. Advantages of Vertical Scaling

Advantages include:

- Simple architecture
- Minimal application changes
- Easier transaction management
- No data-distribution logic
- Easier operational model

For many systems, vertical scaling can support substantial growth before more complex approaches are required.

______________________________________________________________________

# 6. Limitations of Vertical Scaling

There are practical limits.

You cannot increase:

```text
CPU
RAM
Storage performance
```

indefinitely.

Other concerns include:

- Cost
- Hardware limits
- Single-node capacity
- Maintenance windows
- Failure-domain limitations

______________________________________________________________________

# 7. Horizontal Scaling

Horizontal scaling means distributing workload across multiple database nodes.

Examples include:

- Read replicas
- Sharding
- Distributed databases

Conceptually:

```text
Application
    ↓
Multiple database nodes
```

Horizontal scaling can increase capacity but introduces architectural complexity.

______________________________________________________________________

# 8. Vertical vs Horizontal Scaling

| | Vertical | Horizontal |
|---|---|---|
| Approach | Bigger server | More nodes |
| Complexity | Lower | Higher |
| Application changes | Often minimal | Can be significant |
| Scaling limit | Hardware capacity | Distribution complexity/capacity |
| Transactions | Simpler | Potentially more complex |
| Operations | Simpler | More operational complexity |

______________________________________________________________________

# 9. Replication

Replication means maintaining copies of database data on multiple database nodes.

Conceptually:

```text
Primary
   ↓
Replica 1
Replica 2
Replica 3
```

The exact replication mechanism depends on the database.

______________________________________________________________________

# 10. Why Replication?

Replication can provide:

- Read scalability
- High availability
- Failover options
- Geographic distribution
- Disaster-recovery capabilities

Replication does not automatically solve every database bottleneck.

______________________________________________________________________

# 11. Primary and Replicas

A common architecture is:

```text
              ┌── Replica 1
              │
Application → Primary
              │
              ├── Replica 2
              │
              └── Replica 3
```

The primary handles writes.

Replicas can handle read workloads.

______________________________________________________________________

# 12. Read Replicas

A read replica is a database replica used primarily for read operations.

A backend may route:

```text
Writes → Primary
Reads  → Replica
```

This can reduce read load on the primary.

______________________________________________________________________

# 13. Read Replica Example

Suppose the workload is:

```text
90% reads
10% writes
```

A single database handles both.

With replicas:

```text
Writes
  ↓
Primary

Reads
  ↓
Replica 1
Replica 2
Replica 3
```

This can distribute read traffic.

______________________________________________________________________

# 14. Read Replica Trade-Off

Replicas can lag behind the primary.

Example:

```text
Primary:
user.name = "Alice"

Replica:
user.name = "Old Value"
```

A read immediately after a write may return stale data.

This is called:

> Replication lag.

______________________________________________________________________

# 15. Read-After-Write Consistency

Consider:

```text
POST /profile
    ↓
Write to primary

GET /profile
    ↓
Read from replica
```

If the replica has not caught up, the GET may return old data.

Possible strategies include:

- Read from primary after important writes.
- Session/request-level routing.
- Track replication position where supported.
- Design APIs to tolerate eventual consistency.

______________________________________________________________________

# 16. When Read Replicas Are Useful

They are useful when:

- Reads significantly exceed writes.
- Read queries are putting pressure on the primary.
- Some stale reads are acceptable.
- The application can route reads appropriately.

They are less useful when the bottleneck is primarily write-heavy.

______________________________________________________________________

# 17. Replication Does Not Automatically Scale Writes

A common interview mistake is:

> "Add read replicas to scale the database."

Read replicas primarily scale reads.

If the workload is:

```text
90% writes
10% reads
```

adding more read replicas does not directly increase primary write capacity.

______________________________________________________________________

# 18. Replication Lag

Replication lag is the delay between a change being committed on the primary and becoming visible on a replica.

Causes can include:

- High write volume
- Slow replica
- Network latency
- Replica resource pressure
- Long-running replica queries

Monitoring replication lag is important in production.

______________________________________________________________________

# 19. Partitioning

Partitioning divides a large logical table into smaller physical partitions managed by the database.

The application can still see the table as a logical dataset.

Conceptually:

```text
orders
 ├── partition 2024
 ├── partition 2025
 └── partition 2026
```

______________________________________________________________________

# 20. Why Partition?

Partitioning can help with:

- Very large tables
- Query pruning
- Maintenance
- Data lifecycle management
- Large historical datasets

It is not a replacement for indexes or query optimization.

______________________________________________________________________

# 21. Range Partitioning

A common strategy is range partitioning.

For example:

```text
orders_2025
orders_2026
orders_2027
```

based on:

```text
created_at
```

A query for 2026 data may only need to access the 2026 partition if the database can perform partition pruning.

______________________________________________________________________

# 22. List Partitioning

Data can also be partitioned by discrete values.

For example:

```text
region = IN
region = US
region = EU
```

The exact partitioning capabilities depend on the database.

______________________________________________________________________

# 23. Hash Partitioning

Hash partitioning distributes rows based on a hash of a partition key.

Conceptually:

```text
hash(user_id)
     ↓
Partition 1 / 2 / 3 / 4
```

This can distribute data more evenly when the key has a suitable distribution.

______________________________________________________________________

# 24. Partition Key

Choosing the partition key is critical.

A good partition key should align with:

- Common query patterns
- Data distribution
- Data lifecycle
- Expected growth

A poor partition key can produce:

- Uneven partitions
- Inefficient queries
- Hot partitions
- Difficult migrations

______________________________________________________________________

# 25. Partition Pruning

Partition pruning means the database avoids scanning partitions that cannot contain the requested rows.

For example:

```sql
SELECT *
FROM orders
WHERE created_at >= '2026-01-01'
  AND created_at < '2026-02-01';
```

If the table is partitioned by date, the database may access only the relevant partition(s).

______________________________________________________________________

# 26. Partitioning vs Sharding

These concepts are related but different.

### Partitioning

The database divides one logical table into partitions.

### Sharding

Data is distributed across separate database nodes/shards.

Conceptually:

```text
Partitioning:
One database
 ├── partition
 ├── partition
 └── partition

Sharding:
Database cluster
 ├── shard 1
 ├── shard 2
 └── shard 3
```

Exact implementations can vary.

______________________________________________________________________

# 27. Sharding

Sharding distributes data across multiple independent database nodes.

For example:

```text
user_id 1-1M       → Shard 1
user_id 1M-2M      → Shard 2
user_id 2M-3M      → Shard 3
```

Each shard owns a subset of the data.

______________________________________________________________________

# 28. Why Shard?

Sharding may be considered when:

- One database node cannot handle the workload.
- Dataset size exceeds practical single-node capacity.
- Write capacity needs to scale beyond one node.
- Workload can be partitioned effectively.

Sharding should generally not be the first optimization.

______________________________________________________________________

# 29. Sharding Complexity

Sharding introduces significant complexity around:

- Routing
- Data distribution
- Cross-shard queries
- Cross-shard transactions
- Rebalancing
- Backups
- Monitoring
- Schema changes

This is why sharding should be introduced only when justified.

______________________________________________________________________

# 30. Shard Key

The shard key determines where a row is stored.

For example:

```text
tenant_id
user_id
region
```

The key should support common access patterns.

______________________________________________________________________

# 31. Bad Shard Key

Suppose almost every query is:

```text
WHERE user_id = ?
```

but the data is sharded by:

```text
country
```

The application may have difficulty routing queries efficiently.

A good shard key aligns with the application's most common access patterns.

______________________________________________________________________

# 32. Hot Shard

A hot shard receives disproportionately high traffic.

Example:

```text
Shard 1 → 90% traffic
Shard 2 → 5%
Shard 3 → 5%
```

Although the data is technically distributed, capacity is not balanced.

Good shard-key selection attempts to avoid such hotspots.

______________________________________________________________________

# 33. Cross-Shard Query

Suppose data is distributed across:

```text
Shard 1
Shard 2
Shard 3
```

A query such as:

```sql
SELECT *
FROM orders
WHERE status = 'pending';
```

may require checking every shard if `status` is not part of the routing strategy.

This can be expensive.

______________________________________________________________________

# 34. Cross-Shard Transactions

Transactions become more complicated when a business operation affects multiple shards.

Example:

```text
Shard 1 → update account A
Shard 2 → update account B
```

Maintaining atomicity across independent databases is significantly more complex than a single-node transaction.

This is an important reason to avoid unnecessary sharding.

______________________________________________________________________

# 35. Denormalization

Denormalization intentionally duplicates or precomputes data to improve read performance.

For example, instead of repeatedly joining:

```text
orders
+
customers
```

a system might store selected customer information with an order.

______________________________________________________________________

# 36. Why Denormalize?

Denormalization can reduce:

- Expensive joins
- Repeated computation
- Read latency
- Query complexity

It can be useful in read-heavy workloads.

______________________________________________________________________

# 37. Denormalization Trade-Off

The major cost is consistency complexity.

Suppose:

```text
customers.name
orders.customer_name
```

If the customer's name changes, both representations may need updating.

This can introduce:

- Duplicate data
- Update complexity
- Stale values
- More storage
- More complicated writes

______________________________________________________________________

# 38. Normalization vs Denormalization

| | Normalization | Denormalization |
|---|---|---|
| Duplication | Reduced | Intentional |
| Write complexity | Often lower | Can increase |
| Read complexity | May require joins | Can simplify reads |
| Consistency | Easier to maintain | More application responsibility |
| Storage | Lower | Higher |
| Typical goal | Data integrity | Read performance |

File 19 covers normalization and denormalization in detail.

______________________________________________________________________

# 39. When to Denormalize

Consider denormalization when:

- A query is extremely frequent.
- Joins are a measured bottleneck.
- Read latency is important.
- Data changes relatively infrequently.
- The consistency strategy is well understood.

Do not denormalize simply because a table has joins.

______________________________________________________________________

# 40. Database Bottlenecks

Common bottleneck categories include:

### CPU

Complex queries, sorting, aggregation or high concurrency.

### Memory

Large working sets, caches or excessive concurrent operations.

### Disk I/O

Large scans, writes or insufficient storage performance.

### Network

Large result sets or high query round-trip counts.

### Connections

Too many concurrent application connections.

### Locks

Contention between transactions.

### Query plans

Poor execution strategies.

### Data volume

Tables/indexes becoming very large.

______________________________________________________________________

# 41. Diagnose Before Scaling

A slow database does not automatically mean:

> "We need replicas."

First ask:

```text
Is the query indexed?
Is there an N+1?
Is the query scanning too much data?
Is the result too large?
Is there lock contention?
Is the pool exhausted?
Is the database CPU-bound?
Is replication lag relevant?
```

Often a query/index improvement is much cheaper than architectural scaling.

______________________________________________________________________

# 42. Scaling Decision Framework

Use this general framework:

### Problem: Slow individual queries

Consider:

- Query optimization
- Indexes
- Better query plans
- Smaller result sets

### Problem: Too many reads

Consider:

- Caching
- Read replicas
- Query optimization

### Problem: Very large tables

Consider:

- Partitioning
- Archival
- Index optimization

### Problem: One database cannot handle total workload

Consider:

- Vertical scaling
- Read replicas
- Partitioning
- Sharding when necessary

______________________________________________________________________

# 43. Scaling Reads

A common progression:

```text
Optimize query
      ↓
Indexes
      ↓
Caching
      ↓
Read replicas
```

The correct solution depends on the workload.

______________________________________________________________________

# 44. Scaling Writes

Write scaling is more difficult.

Possible approaches include:

- Better queries
- Batch writes
- Vertical scaling
- Partitioning
- Data-model changes
- Queue-based asynchronous processing where appropriate
- Sharding

Read replicas generally do not increase write capacity on the primary.

______________________________________________________________________

# 45. Database Caching

Although Redis is covered in File 26, caching is an important database-scaling concept.

Instead of:

```text
Application → Database
```

frequently requested data can sometimes follow:

```text
Application
    ↓
Cache
    ↓ miss
Database
```

Caching can reduce database reads.

But caching introduces:

- Invalidation
- Staleness
- Memory limits
- Cache stampedes
- Operational complexity

______________________________________________________________________

# 46. Database and Cache

A common architecture:

```text
Client
  ↓
API
  ↓
Cache
  ↓ miss
Database
```

The cache should not automatically become the source of truth unless the architecture explicitly requires that design.

______________________________________________________________________

# 47. Read Scaling Example

Suppose:

```text
10,000 requests/sec
90% reads
10% writes
```

A possible architecture is:

```text
                  ┌── Read Replica
                  ├── Read Replica
Application ──────┤
                  └── Read Replica
                       ↑
                     Reads

Application ───────── Primary
                       ↑
                     Writes
```

This is useful only if the database workload and consistency requirements support it.

______________________________________________________________________

# 48. Write-Heavy Example

Suppose:

```text
10,000 writes/sec
```

Adding read replicas may not solve the primary bottleneck.

Potential approaches could include:

- Query/write optimization
- Batching
- Partitioning
- Vertical scaling
- Sharding
- Architectural redesign

The correct answer depends on where the write workload is concentrated.

______________________________________________________________________

# 49. Multi-Tenant Database Scaling

For a multi-tenant system, possible strategies include:

### Shared database/schema

```text
All tenants
    ↓
One database
```

### Database per tenant

```text
Tenant A → DB A
Tenant B → DB B
Tenant C → DB C
```

### Tenant sharding

```text
Tenants
   ↓
Shard 1 / 2 / 3
```

The choice depends on:

- Tenant size
- Isolation requirements
- Cost
- Operational complexity
- Growth

______________________________________________________________________

# 50. Database Scaling and Availability

Scaling and availability are related but different.

Replication can improve availability, but:

> More database nodes do not automatically mean stronger consistency or availability.

Consider:

- Failure detection
- Failover
- Recovery
- Data loss guarantees
- Replication mode
- Operational procedures

______________________________________________________________________

# 51. Scaling Is a Trade-Off

Every scaling strategy introduces trade-offs.

Examples:

```text
Vertical scaling
→ simpler, but limited

Read replicas
→ scale reads, but introduce lag

Partitioning
→ manage large tables, but adds design constraints

Sharding
→ scale across nodes, but adds major complexity

Denormalization
→ faster reads, but harder consistency
```

______________________________________________________________________

# 52. A Practical Scaling Checklist

Before changing architecture, identify:

### Workload

- Reads/sec
- Writes/sec
- Peak traffic
- Query distribution

### Data

- Total size
- Growth rate
- Largest tables
- Largest indexes

### Performance

- Query latency
- CPU
- Memory
- Disk I/O
- Connection utilization

### Concurrency

- Lock contention
- Transaction duration
- Pool utilization

### Consistency

- Is stale data acceptable?
- Are read-after-write guarantees required?
- Are cross-record transactions required?

______________________________________________________________________

# 53. Senior-Level Scaling Answer

When asked:

> "How would you scale a database?"

A strong answer is not:

> "Add read replicas and shard it."

Instead:

> "First I would measure the workload and identify whether the bottleneck is query execution, CPU, memory, I/O, connections, locks, data size or read/write volume. I would optimize queries and indexes first, then consider vertical scaling. If reads dominate, read replicas or caching may help. For very large tables, partitioning can help. If a single node still cannot support the workload, I would evaluate sharding based on access patterns and shard-key suitability, while explicitly considering consistency, cross-shard queries, transactions and operational complexity."

______________________________________________________________________

# 54. Interview Questions & Answers

## Q1. What is database scaling?

**Answer:**

Increasing database capacity so it can handle growing workload, data volume and concurrency while maintaining acceptable
performance and reliability.

______________________________________________________________________

## Q2. What is vertical scaling?

**Answer:**

Increasing the resources of a database server, such as CPU, memory or storage performance.

______________________________________________________________________

## Q3. What is horizontal scaling?

**Answer:**

Distributing database workload or data across multiple nodes.

______________________________________________________________________

## Q4. Vertical vs horizontal scaling?

**Answer:**

Vertical scaling makes one server more powerful.

Horizontal scaling adds/distributes work across multiple servers.

Vertical scaling is usually simpler; horizontal scaling can provide greater distributed capacity but adds complexity.

______________________________________________________________________

## Q5. What is replication?

**Answer:**

Maintaining copies of database data on multiple nodes.

______________________________________________________________________

## Q6. What is a read replica?

**Answer:**

A replica primarily used to serve read traffic, allowing read workload to be distributed away from the primary.

______________________________________________________________________

## Q7. Do read replicas scale writes?

**Answer:**

Not directly.

They primarily scale read capacity.

______________________________________________________________________

## Q8. What is replication lag?

**Answer:**

The delay between a change being committed on the primary and becoming visible on a replica.

______________________________________________________________________

## Q9. Why is replication lag a problem?

**Answer:**

A read routed to a replica immediately after a write may return stale data.

______________________________________________________________________

## Q10. What is read-after-write consistency?

**Answer:**

The guarantee that after a successful write, a subsequent read observes that write.

Replica lag can violate this if the read goes to a replica that has not caught up.

______________________________________________________________________

## Q11. What is partitioning?

**Answer:**

Dividing a large logical table into smaller physical partitions managed by the database.

______________________________________________________________________

## Q12. Why use partitioning?

**Answer:**

It can improve management and performance for very large tables through techniques such as partition pruning and easier
data lifecycle operations.

______________________________________________________________________

## Q13. What is partition pruning?

**Answer:**

The database eliminates partitions that cannot contain rows matching a query, reducing the amount of data scanned.

______________________________________________________________________

## Q14. What are common partitioning strategies?

**Answer:**

Range, list and hash partitioning are common approaches.

______________________________________________________________________

## Q15. What is a partition key?

**Answer:**

The column or expression used to determine which partition stores a row.

______________________________________________________________________

## Q16. What makes a good partition key?

**Answer:**

It should align with common queries, distribute data appropriately and support the system's data lifecycle.

______________________________________________________________________

## Q17. What is sharding?

**Answer:**

Distributing data across multiple independent database nodes or shards.

______________________________________________________________________

## Q18. Why is sharding complex?

**Answer:**

It introduces routing, data-distribution, rebalancing, cross-shard query, transaction, backup and operational
challenges.

______________________________________________________________________

## Q19. What is a shard key?

**Answer:**

The key used to determine which shard stores a record.

______________________________________________________________________

## Q20. What is a hot shard?

**Answer:**

A shard that receives disproportionately high traffic or data load compared with other shards.

______________________________________________________________________

## Q21. What is a cross-shard query?

**Answer:**

A query that requires accessing multiple shards because the requested data is not located on a single shard.

______________________________________________________________________

## Q22. Why are cross-shard transactions difficult?

**Answer:**

Maintaining atomicity across independent database nodes is substantially more complex than a single-node transaction.

______________________________________________________________________

## Q23. What is denormalization?

**Answer:**

Intentionally duplicating or precomputing data to reduce read complexity or improve read performance.

______________________________________________________________________

## Q24. What is the main trade-off of denormalization?

**Answer:**

It can improve reads but increases duplication and the complexity of keeping duplicated data consistent.

______________________________________________________________________

## Q25. When would you denormalize?

**Answer:**

When measured read performance or query complexity justifies it and the consistency strategy is well understood.

______________________________________________________________________

## Q26. What are common database bottlenecks?

**Answer:**

CPU, memory, disk I/O, network, connections, lock contention, inefficient queries, poor indexes and very large datasets.

______________________________________________________________________

## Q27. Should you scale the database before optimizing queries?

**Answer:**

Usually investigate and optimize obvious query/index problems first. Scaling infrastructure may be necessary, but it
should address a measured bottleneck.

______________________________________________________________________

## Q28. How would you scale a read-heavy database?

**Answer:**

First optimize queries and indexes, then consider caching and read replicas if consistency requirements allow it.

______________________________________________________________________

## Q29. How would you scale a write-heavy database?

**Answer:**

Investigate query and transaction efficiency, batching, partitioning, vertical scaling and potentially sharding or
architectural changes. Read replicas do not directly solve primary write capacity.

______________________________________________________________________

## Q30. Does adding more replicas always improve performance?

**Answer:**

No.

Replica capacity, routing, network overhead, replication lag and the actual workload determine whether additional
replicas help.

______________________________________________________________________

## Q31. What is database connection pressure?

**Answer:**

A condition where many application operations compete for a limited number of database connections, causing waiting and
potentially timeouts.

______________________________________________________________________

## Q32. How does connection pooling affect scaling?

**Answer:**

Every application instance can maintain its own pool, so total potential database connections grow with the number of
instances.

______________________________________________________________________

## Q33. Why can too many connections hurt a database?

**Answer:**

Connections consume database resources and excessive concurrency can cause memory/CPU pressure, context switching and
contention.

______________________________________________________________________

## Q34. What is a hot partition?

**Answer:**

A partition receiving disproportionately high traffic or writes, creating an uneven workload.

______________________________________________________________________

## Q35. Partitioning vs sharding?

**Answer:**

Partitioning divides a logical table into database-managed partitions.

Sharding distributes data across independent database nodes.

______________________________________________________________________

## Q36. Does partitioning automatically make every query faster?

**Answer:**

No.

It helps when query patterns allow effective partition pruning or when partitioning improves data management. Poor
partition design may provide little benefit.

______________________________________________________________________

## Q37. Does sharding automatically improve performance?

**Answer:**

No.

A poor shard key, cross-shard queries or hotspots can make a sharded system difficult or even slower.

______________________________________________________________________

## Q38. What is a good database scaling process?

**Answer:**

Measure workload and bottlenecks, optimize queries/indexes, scale vertically when appropriate, then introduce replicas,
partitioning or sharding only when the workload justifies their complexity.

______________________________________________________________________

## Q39. How would you handle replication lag?

**Answer:**

Measure and monitor lag, route consistency-sensitive reads to the primary when needed, and design workflows to tolerate
eventual consistency where appropriate.

______________________________________________________________________

## Q40. What is the difference between scaling reads and scaling writes?

**Answer:**

Read scaling distributes or reduces read workload through techniques such as caching and replicas.

Write scaling requires increasing the capacity of the write path, potentially through optimization, partitioning,
batching or sharding.

______________________________________________________________________

## Q41. Why can denormalization improve performance?

**Answer:**

It can eliminate expensive joins or repeated computations by storing data closer to the form required by frequent reads.

______________________________________________________________________

## Q42. Why can denormalization hurt writes?

**Answer:**

A logical change may require updating multiple duplicated representations.

______________________________________________________________________

## Q43. What should you consider before sharding?

**Answer:**

Workload distribution, shard key, access patterns, cross-shard queries, transaction requirements, rebalancing,
operational maturity and expected growth.

______________________________________________________________________

## Q44. How do you identify a database bottleneck?

**Answer:**

Measure query latency, CPU, memory, I/O, connection usage, locks, transaction duration, replication lag and workload
distribution.

______________________________________________________________________

## Q45. Give a senior-level database scaling answer.

**Answer:**

Start with measurement and bottleneck identification. Optimize queries and indexes first, then choose vertical scaling,
caching, read replicas, partitioning or sharding according to the workload and consistency requirements. Every step
should be justified by measured capacity needs and weighed against operational and application complexity.

______________________________________________________________________

# 55. Scenario-Based Questions

## Scenario 1 — Read-Heavy System

A product catalog receives:

```text
95% reads
5% writes
```

The primary database is overloaded with reads.

**Answer:**

Optimize queries first. If reads remain the bottleneck, caching and read replicas are strong candidates, provided the
consistency requirements allow replica reads.

______________________________________________________________________

## Scenario 2 — Write-Heavy System

A telemetry system receives millions of writes per minute.

**Answer:**

Read replicas will not directly solve the write bottleneck. Investigate batching, partitioning, storage design, vertical
scaling and potentially sharding or specialized ingestion architecture.

______________________________________________________________________

## Scenario 3 — Replica Returns Old Data

A user updates their profile and immediately requests it again, but the API returns the old value.

**Answer:**

The read likely went to a lagging replica. Route consistency-sensitive reads to the primary or use an appropriate
consistency strategy.

______________________________________________________________________

## Scenario 4 — Huge Orders Table

The `orders` table contains billions of historical rows and most queries filter by `created_at`.

**Answer:**

Partitioning by an appropriate time range may be useful, along with suitable indexes and data-retention/archival
strategies.

______________________________________________________________________

## Scenario 5 — Shard Hotspot

A sharded system stores data by `region`, but one region generates 80% of traffic.

**Answer:**

The shard key creates an uneven workload. Evaluate a more balanced key or a strategy that can distribute high-volume
tenants/regions more evenly.

______________________________________________________________________

## Scenario 6 — Cross-Shard Reporting

A report needs to aggregate data across all shards.

**Answer:**

This can be expensive. Consider whether reporting should use a separate analytical/reporting pipeline, precomputed data
or another architecture rather than frequently performing cross-shard production queries.

______________________________________________________________________

## Scenario 7 — Denormalization

A dashboard repeatedly joins five large tables and has strict latency requirements.

**Answer:**

After measuring the bottleneck, consider precomputed/denormalized data or a read model if the consistency requirements
permit it.

______________________________________________________________________

## Scenario 8 — Database CPU at 100%

The database CPU is constantly saturated.

**Answer:**

Identify expensive queries, missing/ineffective indexes, large scans, sorts and aggregations first. Then consider
vertical scaling or workload distribution if the optimized workload still exceeds capacity.

______________________________________________________________________

## Scenario 9 — Pool Exhaustion

The application has 30 instances and each maintains a pool of 20 database connections.

**Answer:**

The potential pooled connection count is roughly 600 before accounting for overflow and other connections. Verify
whether the database can safely support that concurrency.

______________________________________________________________________

## Scenario 10 — "Let's Shard"

A team proposes sharding because the database is slow.

**Answer:**

Do not immediately shard. Identify the actual bottleneck first. Query optimization, indexing, vertical scaling, caching,
replicas or partitioning may solve the problem with substantially less complexity.

______________________________________________________________________

# 56. Practice Exercises

## Exercise 1 — Bottleneck Analysis

Take a slow endpoint and record:

- Query count
- Query latency
- Database CPU
- Connection-pool utilization
- Transaction duration
- Result size

Identify the actual bottleneck.

______________________________________________________________________

## Exercise 2 — Vertical Scaling

Research your database's resource requirements.

Document how increasing:

```text
CPU
RAM
Storage performance
```

would affect your workload.

______________________________________________________________________

## Exercise 3 — Read Replica Design

Design an architecture for:

```text
90% reads
10% writes
```

Define:

- Write routing
- Read routing
- Consistency-sensitive reads
- Replica failure behavior
- Replication-lag monitoring

______________________________________________________________________

## Exercise 4 — Partitioning

Take an example:

```text
orders(created_at)
```

and design a range-partitioning strategy.

Explain:

- Partition key
- Partition boundaries
- Query patterns
- Partition pruning
- Data retention

______________________________________________________________________

## Exercise 5 — Shard Key

Design a shard key for:

```text
Multi-tenant SaaS
```

Compare:

```text
tenant_id
user_id
region
```

Discuss distribution, routing and hotspot risks.

______________________________________________________________________

## Exercise 6 — Cross-Shard Query

Design a query that requires data from multiple shards.

Explain why it is expensive and propose an alternative architecture.

______________________________________________________________________

## Exercise 7 — Denormalization

Take a frequently executed multi-table query.

Design a denormalized/read-model version.

Document:

- Duplicated data
- Update path
- Consistency model
- Read performance
- Write complexity

______________________________________________________________________

## Exercise 8 — Connection Capacity

Assume:

```text
15 application instances
pool size = 15
```

Calculate the potential pooled connection count.

Then determine whether your database can safely support it.

______________________________________________________________________

## Exercise 9 — Scaling Decision

Given:

```text
Read-heavy
High query latency
Large table
Low write volume
```

Choose among:

- Query optimization
- Vertical scaling
- Read replicas
- Partitioning
- Sharding
- Denormalization

Explain the order in which you would evaluate them.

______________________________________________________________________

## Exercise 10 — Senior Interview Exercise

Design a scaling strategy for:

```text
100,000 requests/sec
95% reads
5% writes
10 TB database
```

Discuss:

- Query optimization
- Caching
- Replication
- Partitioning
- Sharding
- Consistency
- Failure handling
- Operational complexity

Do not jump directly to sharding.

______________________________________________________________________

# 57. Quick Revision

| Concept | Key Point |
|---|---|
| Database scaling | Increase capacity for growing workload |
| Vertical scaling | Bigger database server |
| Horizontal scaling | Multiple database nodes |
| Replication | Multiple copies of database data |
| Read replica | Replica primarily serving reads |
| Replication lag | Replica behind primary |
| Read-after-write | Subsequent read sees prior write |
| Partitioning | Divide logical table into physical partitions |
| Partition pruning | Skip irrelevant partitions |
| Range partitioning | Partition by ranges |
| List partitioning | Partition by discrete values |
| Hash partitioning | Partition using a hash |
| Partition key | Determines partition placement |
| Sharding | Distribute data across independent nodes |
| Shard key | Determines shard placement |
| Hot shard | Unevenly overloaded shard |
| Cross-shard query | Query requiring multiple shards |
| Cross-shard transaction | Transaction spanning shards |
| Denormalization | Intentional data duplication/precomputation |
| Database bottleneck | Database limits application capacity |
| Read scaling | Increase/reduce read workload capacity |
| Write scaling | Increase write-path capacity |
| Pool pressure | High competition for DB connections |
| Vertical-first | Prefer simpler scaling when sufficient |
| Measurement | Identify bottleneck before scaling |

______________________________________________________________________

# 58. Completion Checklist

Before moving to File 26, make sure you can explain:

- [ ] Why databases become bottlenecks
- [ ] Database workload characteristics
- [ ] Vertical scaling
- [ ] Horizontal scaling
- [ ] Vertical vs horizontal trade-offs
- [ ] Replication
- [ ] Primary/replica architecture
- [ ] Read replicas
- [ ] Replica lag
- [ ] Read-after-write consistency
- [ ] When read replicas help
- [ ] Why replicas don't directly scale writes
- [ ] Partitioning
- [ ] Range partitioning
- [ ] List partitioning
- [ ] Hash partitioning
- [ ] Partition key
- [ ] Partition pruning
- [ ] Partitioning vs sharding
- [ ] Sharding
- [ ] Shard key
- [ ] Hot shards
- [ ] Cross-shard queries
- [ ] Cross-shard transactions
- [ ] Sharding trade-offs
- [ ] Denormalization
- [ ] Normalization vs denormalization
- [ ] Denormalization trade-offs
- [ ] Common database bottlenecks
- [ ] Query optimization before scaling
- [ ] Read scaling
- [ ] Write scaling
- [ ] Connection-pool pressure
- [ ] Multi-instance connection capacity
- [ ] Scaling decision framework
- [ ] Consistency considerations
- [ ] Availability considerations
- [ ] Senior-level scaling strategy

______________________________________________________________________

# 59. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is database scaling?
1. What is vertical scaling?
1. What is horizontal scaling?
1. Compare vertical and horizontal scaling.
1. What is replication?
1. What is a read replica?
1. Why do read replicas help?
1. Do read replicas scale writes?
1. What is replication lag?
1. Why can replica lag cause stale reads?
1. What is read-after-write consistency?
1. How would you handle read-after-write requirements with replicas?
1. What is partitioning?
1. Why partition a large table?
1. What is partition pruning?
1. What is range partitioning?
1. What is list partitioning?
1. What is hash partitioning?
1. How do you choose a partition key?
1. What is the difference between partitioning and sharding?
1. What is sharding?
1. Why is sharding complex?
1. What is a shard key?
1. What makes a good shard key?
1. What is a hot shard?
1. What is a cross-shard query?
1. Why are cross-shard transactions difficult?
1. What is denormalization?
1. Why can denormalization improve read performance?
1. What is the downside of denormalization?
1. When would you denormalize?
1. What are common database bottlenecks?
1. How would you diagnose a database bottleneck?
1. Why should you optimize queries before introducing sharding?
1. How would you scale a read-heavy application?
1. How would you scale a write-heavy application?
1. How does connection pooling affect database scaling?
1. Why can increasing connection-pool size hurt the database?
1. How does the number of application instances affect database connections?
1. How can caching reduce database load?
1. Does caching replace the database as the source of truth?
1. How would you handle replication lag?
1. How would you choose between partitioning and sharding?
1. What should you consider before sharding?
1. How would you design a shard key for a multi-tenant SaaS application?
1. How would you identify a hot shard?
1. How would you handle a very large time-series/orders table?
1. How would you scale a 95%-read workload?
1. How would you scale a 90%-write workload?
1. Give a senior-level answer to: "How would you scale a database?"

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [24. SQLAlchemy Performance & Async](./24-sqlalchemy-performance.md)

**Next:** [26. Redis Fundamentals](./26-redis.md)
