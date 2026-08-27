# 27. Redis Caching & Production

**Previous:** [26. Redis Fundamentals](./26-redis.md)

**Next:** [28. Kafka](./28-kafka.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain the major Redis caching patterns.
- Understand cache-aside, write-through and write-back caching.
- Explain cache invalidation and why it is difficult.
- Diagnose cache stampede, cache penetration and cache avalanche.
- Explain distributed locks and the `SET NX` pattern.
- Understand Redis persistence at a production overview level.
- Compare RDB and AOF.
- Explain Redis eviction policies.
- Understand LRU and LFU.
- Explain Redis replication.
- Understand Sentinel and Redis Cluster at an interview-ready level.
- Discuss Redis production trade-offs and failure scenarios.

> **Scope note:** File 26 covers Redis data structures, TTL, atomic commands and basic transactions. This file focuses on caching architecture and production concerns.

______________________________________________________________________

# 1. Redis in Production

Redis is commonly placed between an application and a primary database.

A typical architecture is:

```text
Client
  ↓
Backend
  ↓
Redis
  ↓ cache miss
Database
```

The goal is usually to reduce database load and improve response latency.

______________________________________________________________________

# 2. What Should Be Cached?

Good candidates often have:

- High read frequency
- Relatively expensive computation/query cost
- Data that can tolerate some staleness
- Frequently repeated access
- Predictable keys

Examples:

```text
Product details
User profile summaries
Configuration
Permissions
Frequently accessed reference data
```

Avoid caching data blindly.

______________________________________________________________________

# 3. Cache Key Design

A cache key should identify the exact logical data being cached.

Examples:

```text
product:1001
user:1001:summary
permissions:user:1001
```

For parameterized queries:

```text
products:list:category:10:page:2
```

Be consistent with naming and invalidation strategy.

______________________________________________________________________

# 4. Cache-Aside

Cache-aside is one of the most common caching patterns.

The application controls both cache reads and database reads.

Flow:

```text
Application
    ↓
Redis GET
    ↓
Hit → return
    ↓ miss
Database
    ↓
Redis SET
    ↓
Return
```

______________________________________________________________________

# 5. Cache-Aside Read Flow

Example:

```python
value = redis.get(key)

if value is not None:
    return deserialize(value)

value = load_from_database()

redis.set(key, serialize(value), ex=300)

return value
```

The application explicitly manages the cache.

______________________________________________________________________

# 6. Cache-Aside Write Flow

A common approach is:

```text
Write database
      ↓
Invalidate cache
```

Example:

```python
update_database(user)

redis.delete(f"user:{user_id}")
```

The next read repopulates the cache.

______________________________________________________________________

# 7. Advantages of Cache-Aside

Advantages:

- Simple
- Application-controlled
- Database remains source of truth
- Only requested data is cached
- Easy to introduce incrementally

It is a common default choice for backend systems.

______________________________________________________________________

# 8. Disadvantages of Cache-Aside

Potential problems:

- Cache misses
- Cache invalidation
- Stale data
- Cache stampede
- Application complexity

The cache and database can temporarily disagree.

______________________________________________________________________

# 9. Write-Through Cache

With write-through caching, writes go through the cache and are propagated to the backing data store.

Conceptually:

```text
Application
    ↓
Cache
    ↓
Database
```

A successful write updates both layers as part of the cache architecture.

______________________________________________________________________

# 10. Write-Through Example

Conceptually:

```text
Update product
      ↓
Update cache
      ↓
Update database
```

The exact ordering and consistency guarantees depend on the implementation.

______________________________________________________________________

# 11. Advantages of Write-Through

Potential advantages:

- Cache stays relatively fresh
- Frequently accessed data is already cached
- Read path can have fewer cache misses

______________________________________________________________________

# 12. Disadvantages of Write-Through

Potential disadvantages:

- Every write has cache-related work
- More complex write path
- Data-store/cache consistency still requires careful design
- Data that is never read may still be cached

______________________________________________________________________

# 13. Write-Back Cache

Write-back caching writes to the cache first and persists changes to the backing database later.

Conceptually:

```text
Application
    ↓
Redis
    ↓
Database later
```

This can reduce immediate database writes.

______________________________________________________________________

# 14. Write-Back Advantages

Potential benefits:

- Lower write latency
- Batching/coalescing of writes
- Reduced database write pressure

______________________________________________________________________

# 15. Write-Back Risks

The main concern is durability and consistency.

If the cache fails before data is persisted:

```text
Application
   ↓
Redis
   X
Database
```

data can potentially be lost depending on the architecture.

Write-back therefore requires careful durability and recovery design.

______________________________________________________________________

# 16. Cache Pattern Comparison

| Pattern | Read | Write | Main Benefit | Main Risk |
|---|---|---|---|---|
| Cache-aside | Cache first, DB on miss | DB + invalidate | Simple | Invalidation |
| Write-through | Cache participates in write | Cache + DB | Fresh cache | More write work |
| Write-back | Cache first | Cache, DB later | Fast writes | Data loss/consistency |

______________________________________________________________________

# 17. Cache Invalidation

Cache invalidation means removing or updating cached data when the underlying source changes.

Example:

```text
Database:
user.name = Alice

Redis:
user:1001 → Alice

Database updated:
user.name = Bob

Redis still:
user:1001 → Alice
```

The cache must eventually be invalidated or updated.

______________________________________________________________________

# 18. Why Cache Invalidation Is Difficult

Because there are two copies of information:

```text
Database
+
Cache
```

Every write creates a consistency decision.

Possible approaches include:

- Delete cache after DB write
- Update cache after DB write
- Short TTL
- Versioned keys
- Event-driven invalidation
- Explicit cache refresh

______________________________________________________________________

# 19. Delete vs Update Cache

Suppose:

```text
DB update
```

occurs.

### Delete

```text
DB update
   ↓
DEL cache
```

Next read loads fresh data.

### Update

```text
DB update
   ↓
SET cache with new value
```

The cache is immediately populated with the new value.

Both approaches have trade-offs.

______________________________________________________________________

# 20. Why Delete-After-Write Is Common

Deleting the cache is often simpler than reconstructing the exact cached representation.

For example, an API may cache:

```text
user:1001:profile
```

but the database update may affect multiple representations.

Deleting the relevant keys allows the next read to rebuild them.

______________________________________________________________________

# 21. Cache Invalidation Race

Consider:

```text
Request A:
Read DB → old value

Request B:
Update DB → new value
Delete cache

Request A:
Write old value into cache
```

Now Redis can contain stale data again.

This is why cache invalidation requires careful ordering and concurrency reasoning.

______________________________________________________________________

# 22. Cache Stampede

A cache stampede occurs when a popular cache entry expires and many requests simultaneously try to rebuild it.

Example:

```text
Popular key expires
       ↓
1,000 requests miss
       ↓
1,000 DB queries
       ↓
Database overloaded
```

______________________________________________________________________

# 23. Preventing Cache Stampede

Common techniques include:

- Request coalescing
- Distributed locks
- Early refresh
- Randomized TTL/jitter
- Background refresh
- Stale-while-revalidate
- Prewarming

The appropriate strategy depends on workload.

______________________________________________________________________

# 24. TTL Jitter

Suppose many keys are cached with exactly:

```text
TTL = 300 seconds
```

They may expire at nearly the same time.

Instead use a small random variation:

```text
300 ± random jitter
```

This spreads expirations over time.

______________________________________________________________________

# 25. Request Coalescing

Instead of allowing 1,000 requests to rebuild the same key:

```text
1,000 requests
      ↓
one request rebuilds
      ↓
other requests wait/use result
```

This reduces duplicate database work.

______________________________________________________________________

# 26. Cache Penetration

Cache penetration occurs when requests repeatedly ask for data that does not exist.

Example:

```text
GET product:999999999
```

If the product does not exist:

```text
Redis miss
   ↓
Database query
   ↓
Not found
```

Repeated malicious or accidental requests can repeatedly hit the database.

______________________________________________________________________

# 27. Preventing Cache Penetration

Common approaches:

- Cache negative results
- Bloom filters
- Input validation
- ID existence checks
- Request throttling

For example, cache:

```text
product:999999999 → NOT_FOUND
```

with a short TTL.

______________________________________________________________________

# 28. Cache Avalanche

A cache avalanche occurs when many cached entries become unavailable around the same time, causing a large surge of
database traffic.

Example:

```text
Millions of keys expire
       ↓
Mass cache misses
       ↓
Database overload
```

______________________________________________________________________

# 29. Stampede vs Penetration vs Avalanche

| Problem | Meaning |
|---|---|
| Stampede | Many requests rebuild the same missing popular key |
| Penetration | Requests repeatedly query nonexistent data |
| Avalanche | Many cached entries fail/expire around the same time |

These terms are commonly tested in backend interviews.

______________________________________________________________________

# 30. Preventing Cache Avalanche

Possible techniques:

- TTL jitter
- Staggered expiration
- Cache warming
- Multiple cache layers
- Rate limiting
- Graceful degradation
- Stale data fallback

The goal is to prevent a sudden synchronized load spike.

______________________________________________________________________

# 31. Distributed Locks

A distributed lock coordinates access to a resource across multiple application instances.

Example:

```text
Server A ─┐
Server B ─┼──→ Redis lock
Server C ─┘
```

Only one server should acquire the lock for a particular resource at a time.

______________________________________________________________________

# 32. Why Use Distributed Locks?

Potential use cases:

- Prevent duplicate cache rebuilding
- Coordinate scheduled jobs
- Prevent concurrent processing
- Serialize a critical operation

Use locks only when the operation actually requires coordination.

______________________________________________________________________

# 33. `SET NX`

A common Redis primitive for acquiring a lock is:

```text
SET lock:key unique-token NX EX 30
```

Important concepts:

- `NX` → set only if the key does not already exist
- `EX 30` → expiration in seconds
- `unique-token` → identifies the lock owner

______________________________________________________________________

# 34. Why Lock Expiration Matters

Never create a distributed lock that can remain forever if the owner crashes.

Without expiration:

```text
Server acquires lock
       ↓
Server crashes
       ↓
Lock remains
       ↓
Other workers blocked
```

A TTL provides automatic recovery from abandoned locks.

______________________________________________________________________

# 35. Lock Ownership

Suppose:

```text
Server A
token = abc
```

acquires:

```text
lock:product:1001 → abc
```

When releasing the lock, the application should ensure it is releasing its own lock rather than deleting another owner's
lock.

This generally requires an atomic check-and-delete mechanism rather than blindly executing `DEL`.

______________________________________________________________________

# 36. Distributed Lock Risks

Distributed locks have subtle failure modes:

- Process crashes
- Network partitions
- Lock expiration while work continues
- Clock/timing assumptions
- Client pauses
- Duplicate work after lease expiry

A Redis lock should not automatically be treated as a perfect global mutual-exclusion guarantee under every failure
scenario.

______________________________________________________________________

# 37. Lock for Cache Stampede

A common pattern is:

```text
Cache miss
   ↓
Try lock
   ↓
Lock acquired → rebuild cache
   ↓
Others → wait/recheck cache
```

This allows one request to rebuild a popular cache entry.

______________________________________________________________________

# 38. Redis Persistence

Redis can persist data to storage.

Two important mechanisms are:

- RDB
- AOF

The choice affects:

- Recovery
- Durability
- Storage
- Performance
- Operational complexity

______________________________________________________________________

# 39. RDB

RDB creates point-in-time snapshots of the Redis dataset.

Conceptually:

```text
Redis memory
     ↓
Snapshot
     ↓
RDB file
```

______________________________________________________________________

# 40. RDB Advantages

Potential advantages:

- Compact snapshot
- Efficient backups
- Faster restart in some scenarios
- Convenient point-in-time representation

______________________________________________________________________

# 41. RDB Disadvantages

Potential disadvantage:

If the last snapshot is older than the latest writes, those writes may not be present in the snapshot after a failure.

Therefore RDB alone may not satisfy strict durability requirements.

______________________________________________________________________

# 42. AOF

AOF records write operations so Redis can reconstruct the dataset during recovery.

Conceptually:

```text
Write command
     ↓
AOF
```

On restart, Redis can replay the recorded operations according to its persistence configuration.

______________________________________________________________________

# 43. AOF Advantages

Potential advantages:

- More frequent persistence opportunities
- Better recovery-point characteristics than infrequent snapshots
- Append-oriented persistence model

______________________________________________________________________

# 44. AOF Disadvantages

Potential disadvantages:

- Larger storage footprint
- More I/O
- More operational considerations
- Rewrite/compaction overhead

______________________________________________________________________

# 45. RDB vs AOF

| | RDB | AOF |
|---|---|---|
| Model | Snapshot | Write log |
| Storage | Usually compact | Can be larger |
| Recovery point | Snapshot-dependent | Configuration-dependent |
| Backup use | Strong | Possible |
| Write overhead | Snapshot-related | Write/persistence-related |
| Main trade-off | Potentially more lost recent data | More storage/I/O |

______________________________________________________________________

# 46. Persistence Is Not the Same as Backup

Persistence helps Redis recover its dataset.

Backups are a separate operational concern.

A production system should consider:

- Backup retention
- Restore testing
- Disaster recovery
- Off-host copies
- Recovery objectives

______________________________________________________________________

# 47. Redis Eviction

Redis has finite memory.

When configured memory limits are reached, Redis may need to evict keys according to its configured eviction policy.

Eviction means:

```text
Memory pressure
     ↓
Eligible key removed
```

______________________________________________________________________

# 48. Why Eviction Matters

If Redis is used as a cache, eviction can be acceptable.

If Redis contains important state, unexpected eviction can be dangerous.

Therefore eviction policy must match the data's purpose.

______________________________________________________________________

# 49. LRU

LRU means:

> Least Recently Used.

The idea is to remove keys that have not been accessed recently.

Conceptually:

```text
Recently used
    ↓
Keep

Least recently used
    ↓
Evict
```

Redis uses an approximation rather than maintaining an exact global LRU ordering for every key.

______________________________________________________________________

# 50. LFU

LFU means:

> Least Frequently Used.

It considers how often keys are accessed.

Conceptually:

```text
Frequently accessed
    ↓
Keep

Rarely accessed
    ↓
Evict
```

This can be useful when frequency is a better signal than recency.

______________________________________________________________________

# 51. LRU vs LFU

| | LRU | LFU |
|---|---|---|
| Signal | Recent access | Access frequency |
| Good for | Recency-based workloads | Popularity-based workloads |
| Question | "What hasn't been used recently?" | "What is rarely used?" |

Choose based on access patterns.

______________________________________________________________________

# 52. Other Eviction Concepts

Redis provides multiple policies beyond simple LRU/LFU, including policies that:

- Evict arbitrary keys
- Evict only keys with expiration
- Evict based on all keys
- Prefer keys with lower frequency/recency

The important interview concept is:

> Eviction policy determines what Redis removes when memory pressure occurs.

______________________________________________________________________

# 53. Cache-Only vs Persistent State

A useful distinction:

### Cache

Eviction can usually be tolerated because the source of truth exists elsewhere.

### Important application state

Eviction may cause data loss from the application's perspective.

Therefore Redis configuration must reflect what the data represents.

______________________________________________________________________

# 54. Redis Replication

Redis can replicate data from a primary to replicas.

Conceptually:

```text
Primary
  ↓
Replica 1
Replica 2
```

Replicas can improve:

- Read scalability in supported architectures
- Availability options
- Recovery options

______________________________________________________________________

# 55. Redis Replication and Asynchrony

Replication can be asynchronous.

Therefore a write acknowledged by the primary may not immediately be present on every replica.

This creates potential replication lag.

______________________________________________________________________

# 56. Redis Failover

If the primary fails, the system may need to promote a replica.

Failover can be:

- Manual
- Automated

Sentinel is one Redis mechanism for monitoring and automated failover in appropriate deployments.

______________________________________________________________________

# 57. Redis Sentinel

Redis Sentinel provides monitoring and high-availability coordination for Redis deployments.

At a high level, Sentinel can:

- Monitor Redis instances
- Detect failures
- Coordinate failover
- Provide clients with information about the current primary

______________________________________________________________________

# 58. Sentinel Architecture

Conceptually:

```text
             Sentinel
            /        \
           /          \
      Primary       Replica
```

Multiple Sentinel processes are typically used to avoid relying on a single Sentinel.

______________________________________________________________________

# 59. When Sentinel Is Useful

Sentinel is appropriate for architectures where you want:

- Primary/replica monitoring
- Automated failover
- High availability
- A relatively straightforward replicated Redis deployment

It does not turn Redis into a horizontally sharded data store.

______________________________________________________________________

# 60. Redis Cluster

Redis Cluster distributes data across multiple Redis nodes using hash slots.

Conceptually:

```text
             Redis Cluster
          /       |       \
      Node 1    Node 2    Node 3
       slots     slots     slots
```

The dataset is distributed across the cluster.

______________________________________________________________________

# 61. Redis Cluster Hash Slots

Redis Cluster uses:

```text
16,384 hash slots
```

Keys are mapped to hash slots.

The cluster distributes slots across nodes.

This allows data to be distributed rather than keeping the entire dataset on one primary.

______________________________________________________________________

# 62. Why Redis Cluster?

Redis Cluster can provide:

- Horizontal data distribution
- Higher total memory capacity
- Distributed write/read workload
- Node-level scaling

It introduces more operational and application considerations.

______________________________________________________________________

# 63. Redis Cluster vs Sentinel

This distinction is extremely important.

### Sentinel

Primarily provides:

```text
Monitoring
+
Failover
+
High availability
```

for a primary/replica setup.

### Cluster

Provides:

```text
Data sharding
+
Horizontal distribution
+
High availability capabilities
```

They solve different primary problems.

______________________________________________________________________

# 64. Cluster Key Distribution

A key is mapped to a hash slot.

Conceptually:

```text
key
 ↓
hash
 ↓
slot
 ↓
Redis node
```

This lets the cluster determine which node owns the key.

______________________________________________________________________

# 65. Redis Cluster and Multi-Key Operations

Multi-key operations can become complicated if the involved keys belong to different hash slots.

For example:

```text
key A → slot 100
key B → slot 9000
```

An operation requiring both may not be directly supported as a normal single-slot operation.

This is why related keys may be intentionally colocated.

______________________________________________________________________

# 66. Hash Tags

Redis Cluster supports hash tags to force related keys into the same hash slot.

Example:

```text
user:{1001}:profile
user:{1001}:cart
```

The `{1001}` portion can cause the keys to map using the same hash-tagged portion.

This can make certain multi-key operations possible within one slot.

______________________________________________________________________

# 67. Cluster Trade-Offs

Redis Cluster introduces:

- Data distribution
- Resharding
- Cluster-aware clients
- Multi-key constraints
- More complex operations
- Failure handling

It is powerful but should not be introduced without a capacity/distribution requirement.

______________________________________________________________________

# 68. Sentinel vs Cluster

| | Sentinel | Cluster |
|---|---|---|
| Primary purpose | HA/failover | Sharding + HA |
| Data sharding | No | Yes |
| Multiple data nodes | Replicas | Shards |
| Horizontal data capacity | Limited | Yes |
| Failover | Yes | Yes |
| Multi-key complexity | Lower | Higher |
| Operational complexity | Moderate | Higher |

______________________________________________________________________

# 69. Cache Consistency

A cache introduces a second representation of data.

Possible consistency models include:

### Stronger consistency

Try to keep cache synchronized immediately.

### Eventual consistency

Allow cache to temporarily contain stale data.

The correct model depends on the application.

______________________________________________________________________

# 70. Stale Data

Suppose:

```text
Database → $100
Redis    → $90
```

If the API returns Redis data:

```text
Customer sees $90
```

This may be acceptable for some data but unacceptable for:

- Payment amount
- Account balance
- Critical authorization decisions

Caching strategy must account for business correctness.

______________________________________________________________________

# 71. Cache TTL Is Not a Consistency Guarantee

A common mistake is:

> "The cache has a 5-minute TTL, so consistency is solved."

TTL only limits how long a cached value can remain without refresh.

It does not guarantee that stale data will never be served during that period.

______________________________________________________________________

# 72. Cache Invalidation Strategies

Common strategies:

### Explicit deletion

```text
DB update → DEL cache
```

### Explicit update

```text
DB update → SET cache
```

### TTL-based expiration

```text
SET key value EX 300
```

### Event-driven invalidation

```text
DB change
  ↓
Event
  ↓
Cache invalidation
```

______________________________________________________________________

# 73. Cache Warming

Cache warming means proactively populating cache entries before traffic requires them.

Useful after:

- Deployment
- Cache restart
- Large invalidation
- Failover
- Predictable traffic spikes

______________________________________________________________________

# 74. Cache Prewarming Example

Suppose the top 1,000 products receive most traffic.

Before a major event:

```text
Load top products
      ↓
Populate Redis
      ↓
Traffic arrives
```

This can reduce initial cache misses.

______________________________________________________________________

# 75. Stale-While-Revalidate

A cache can sometimes serve stale data while a background process refreshes the value.

Conceptually:

```text
Request
  ↓
Stale cache
  ↓
Return stale value

Background
  ↓
Refresh cache
```

This can reduce latency and prevent many requests from simultaneously rebuilding the same key.

______________________________________________________________________

# 76. Distributed Lock for Refresh

For an expensive cache rebuild:

```text
Cache miss
   ↓
Acquire lock
   ↓
If acquired:
    Query DB
    Update cache
    Release lock

If not acquired:
    Wait/recheck cache
```

The lock should have an expiration and safe ownership/release semantics.

______________________________________________________________________

# 77. Cache Penetration With Negative Caching

Suppose:

```text
product:999999
```

does not exist.

Instead of querying the database on every request:

```text
Redis:
product:999999 → NOT_FOUND
TTL → short
```

This is called negative caching.

______________________________________________________________________

# 78. Bloom Filters

A Bloom filter can provide a probabilistic membership check.

Conceptually:

```text
Request ID
   ↓
Bloom filter
   ↓
Definitely absent → avoid DB
Maybe present → query cache/DB
```

A Bloom filter can have false positives but should not have false negatives under its standard operation assumptions.

______________________________________________________________________

# 79. Cache Stampede Protection Strategy

For a highly popular key, a robust approach can combine:

```text
TTL
+
Jitter
+
Request coalescing/lock
+
Stale-while-revalidate
```

The exact combination depends on latency and consistency requirements.

______________________________________________________________________

# 80. Production Redis Checklist

### Capacity

- [ ] Memory usage monitored
- [ ] Maximum memory configured appropriately
- [ ] Eviction policy understood
- [ ] Large keys identified

### Performance

- [ ] Expensive commands monitored
- [ ] Large values avoided
- [ ] Connection behavior monitored
- [ ] Latency monitored

### Reliability

- [ ] Persistence requirements defined
- [ ] RDB/AOF choice understood
- [ ] Backups configured
- [ ] Restore tested

### High availability

- [ ] Replication configured where required
- [ ] Failover strategy defined
- [ ] Sentinel or Cluster selected appropriately

### Caching

- [ ] TTLs defined
- [ ] Invalidation strategy defined
- [ ] Stampede protection considered
- [ ] Penetration protection considered
- [ ] Avalanche protection considered

______________________________________________________________________

# 81. Common Redis Production Mistakes

## Mistake 1 — Caching everything

Not every query benefits from caching.

## Mistake 2 — No invalidation strategy

A cache without a consistency plan eventually causes stale-data problems.

## Mistake 3 — Identical TTLs everywhere

Synchronized expiration can create spikes.

## Mistake 4 — No protection for hot keys

A popular key can create a stampede when it expires.

## Mistake 5 — Unsafe distributed locks

Locks without expiration or ownership checks can cause stuck or incorrect behavior.

## Mistake 6 — Treating Redis persistence as a backup strategy

Persistence and backup are different concerns.

## Mistake 7 — Choosing Sentinel when sharding is required

Sentinel does not provide Redis Cluster-style data sharding.

## Mistake 8 — Choosing Cluster without needing distribution

Cluster adds operational and application complexity.

## Mistake 9 — Ignoring memory

Redis is memory-oriented, so memory pressure is a first-class production concern.

______________________________________________________________________

# 82. Interview Questions & Answers

## Q1. What is cache-aside?

**Answer:**

The application checks the cache first. On a miss, it loads data from the database, stores it in the cache and returns
it.

______________________________________________________________________

## Q2. Why is cache-aside popular?

**Answer:**

It is simple, application-controlled and keeps the database as the source of truth.

______________________________________________________________________

## Q3. What is write-through caching?

**Answer:**

A write updates the cache and backing data store through the cache architecture so the cache is kept relatively current.

______________________________________________________________________

## Q4. What is write-back caching?

**Answer:**

Writes are accepted by the cache first and persisted to the backing store later.

______________________________________________________________________

## Q5. What is the main risk of write-back caching?

**Answer:**

Data can potentially be lost if the cache fails before changes are persisted, depending on the persistence and recovery
architecture.

______________________________________________________________________

## Q6. What is cache invalidation?

**Answer:**

Removing or updating cached data when the underlying source of truth changes.

______________________________________________________________________

## Q7. Why is cache invalidation difficult?

**Answer:**

Because the cache and database contain separate representations that can become inconsistent, especially under
concurrent requests and failures.

______________________________________________________________________

## Q8. What is a cache stampede?

**Answer:**

Many requests simultaneously attempt to rebuild the same cache entry after it becomes unavailable.

______________________________________________________________________

## Q9. How do you prevent a cache stampede?

**Answer:**

Use techniques such as request coalescing, distributed locks, TTL jitter, early refresh or stale-while-revalidate.

______________________________________________________________________

## Q10. What is cache penetration?

**Answer:**

Repeated requests for data that does not exist bypass the cache and repeatedly hit the database.

______________________________________________________________________

## Q11. How do you prevent cache penetration?

**Answer:**

Negative caching, Bloom filters, validation and rate limiting are common approaches.

______________________________________________________________________

## Q12. What is cache avalanche?

**Answer:**

A large number of cache entries become unavailable at roughly the same time, causing a sudden surge of backend/database
traffic.

______________________________________________________________________

## Q13. How do you prevent cache avalanche?

**Answer:**

Use TTL jitter, staggered expiration, cache warming, stale-data strategies, rate limiting and graceful degradation.

______________________________________________________________________

## Q14. What is a distributed lock?

**Answer:**

A coordination mechanism that allows multiple application instances to agree that only one instance should perform a
particular critical operation at a time.

______________________________________________________________________

## Q15. How can Redis implement a lock?

**Answer:**

A common primitive is:

```text
SET lock:key unique-token NX EX 30
```

where `NX` ensures the key is created only if it does not already exist and `EX` provides expiration.

______________________________________________________________________

## Q16. Why does a Redis lock need a TTL?

**Answer:**

To prevent a crashed lock holder from leaving a permanent lock that blocks future work.

______________________________________________________________________

## Q17. Why is a unique lock token important?

**Answer:**

It identifies the owner of the lock so a client does not accidentally release a lock acquired by another client.

______________________________________________________________________

## Q18. Why is blindly using `DEL lock:key` dangerous?

**Answer:**

The original owner may have lost the lock due to expiration and another process may have acquired it. The old owner
could then delete the new owner's lock.

______________________________________________________________________

## Q19. What is RDB?

**Answer:**

A Redis persistence mechanism that creates point-in-time snapshots of the dataset.

______________________________________________________________________

## Q20. What is AOF?

**Answer:**

A persistence mechanism that records write operations so Redis can reconstruct the dataset during recovery.

______________________________________________________________________

## Q21. RDB vs AOF?

**Answer:**

RDB uses snapshots and is generally compact and convenient for backups.

AOF records writes and can provide different recovery-point characteristics, but may require more storage/I/O.

______________________________________________________________________

## Q22. Is RDB alone always sufficient for durability?

**Answer:**

No.

Recent writes since the latest snapshot may not be represented after a failure.

______________________________________________________________________

## Q23. Is persistence the same as backup?

**Answer:**

No.

Persistence helps recovery, while backups require retention, independent copies and tested restoration procedures.

______________________________________________________________________

## Q24. What is Redis eviction?

**Answer:**

Removing keys according to a configured policy when Redis reaches its configured memory limit.

______________________________________________________________________

## Q25. What is LRU?

**Answer:**

Least Recently Used. It favors evicting keys that have not been accessed recently.

______________________________________________________________________

## Q26. What is LFU?

**Answer:**

Least Frequently Used. It favors evicting keys with lower access frequency.

______________________________________________________________________

## Q27. LRU vs LFU?

**Answer:**

LRU focuses on recency.

LFU focuses on frequency.

The better choice depends on the workload's access pattern.

______________________________________________________________________

## Q28. Does Redis implement exact LRU?

**Answer:**

Redis uses an approximation rather than maintaining a perfect global LRU ordering across every key.

______________________________________________________________________

## Q29. What is Redis replication?

**Answer:**

Maintaining replicas of Redis data from a primary instance.

______________________________________________________________________

## Q30. Is Redis replication necessarily synchronous?

**Answer:**

No.

Redis replication can be asynchronous, so replicas can temporarily lag behind the primary.

______________________________________________________________________

## Q31. What is Redis Sentinel?

**Answer:**

A Redis high-availability mechanism that monitors instances and can coordinate automated failover and primary discovery.

______________________________________________________________________

## Q32. Does Sentinel shard Redis data?

**Answer:**

No.

Sentinel primarily addresses monitoring and failover for primary/replica deployments.

______________________________________________________________________

## Q33. What is Redis Cluster?

**Answer:**

A distributed Redis architecture that partitions data across nodes using hash slots and provides cluster-level
availability/scaling capabilities.

______________________________________________________________________

## Q34. How many hash slots does Redis Cluster have?

**Answer:**

Redis Cluster uses 16,384 hash slots.

______________________________________________________________________

## Q35. Why are hash slots important?

**Answer:**

They determine which cluster node owns a key, allowing Redis to distribute the dataset across nodes.

______________________________________________________________________

## Q36. What problem can multi-key commands have in Redis Cluster?

**Answer:**

If keys belong to different hash slots, operations requiring them together may not be executable as a normal single-slot
operation.

______________________________________________________________________

## Q37. What are Redis hash tags?

**Answer:**

A key-naming mechanism using `{...}` to ensure related keys are hashed using the same tag and therefore placed in the
same hash slot.

______________________________________________________________________

## Q38. Sentinel vs Cluster?

**Answer:**

Sentinel focuses on monitoring and failover of primary/replica deployments.

Cluster provides data sharding and horizontal distribution along with cluster availability features.

______________________________________________________________________

## Q39. What is cache warming?

**Answer:**

Proactively populating cache entries before they are requested, often before predictable traffic spikes or after cache
loss.

______________________________________________________________________

## Q40. What is stale-while-revalidate?

**Answer:**

Serving an existing stale value while refreshing the cache in the background.

______________________________________________________________________

## Q41. What is negative caching?

**Answer:**

Caching a representation of a known-missing result for a short period to prevent repeated database queries for
nonexistent data.

______________________________________________________________________

## Q42. What is a Bloom filter used for in caching?

**Answer:**

It can quickly identify values that are definitely absent, reducing unnecessary cache/database lookups.

______________________________________________________________________

## Q43. Can a Bloom filter return false positives?

**Answer:**

Yes.

It can say "maybe present" when an item is absent, but under standard Bloom-filter assumptions it does not produce false
negatives.

______________________________________________________________________

## Q44. Why use TTL jitter?

**Answer:**

To spread expiration events over time and reduce synchronized cache misses.

______________________________________________________________________

## Q45. Why is Redis memory important?

**Answer:**

Redis keeps its working dataset primarily in memory, so memory capacity and memory pressure directly affect availability
and performance.

______________________________________________________________________

## Q46. What happens if a cache entry expires while thousands of requests arrive?

**Answer:**

Without protection, many requests may query the database simultaneously, creating a cache stampede.

______________________________________________________________________

## Q47. How would you protect a very hot cache key?

**Answer:**

Consider request coalescing, a distributed lock, background refresh, stale-while-revalidate and TTL jitter.

______________________________________________________________________

## Q48. When is eviction acceptable?

**Answer:**

Eviction is generally more acceptable for cache-only data where the source of truth exists elsewhere.

______________________________________________________________________

## Q49. Why can eviction be dangerous for application state?

**Answer:**

Eviction can remove data that the application considers important, potentially causing data loss or incorrect behavior.

______________________________________________________________________

## Q50. Give a senior-level Redis production answer.

**Answer:**

"I would first define whether Redis is a cache or a source of important state, because that determines persistence,
eviction and recovery requirements. For caching, I would choose an appropriate pattern such as cache-aside, define TTL
and invalidation, and protect hot keys from stampedes. I would monitor memory, latency, command behavior and connection
usage. For availability, I would evaluate replication and Sentinel; for horizontal data distribution, I would evaluate
Cluster. I would also explicitly consider stale reads, failure behavior, persistence, backups and operational
complexity."

______________________________________________________________________

# 83. Scenario-Based Questions

## Scenario 1 — Cache Miss Storm

A popular product key expires and 10,000 requests hit the endpoint simultaneously.

**Answer:**

This is a cache stampede.

Use request coalescing or a distributed lock so one request rebuilds the value while others wait/recheck. TTL jitter and
stale-while-revalidate can further reduce the risk.

______________________________________________________________________

## Scenario 2 — Nonexistent IDs

An attacker requests random product IDs that do not exist.

**Answer:**

This is cache penetration.

Consider negative caching, Bloom filters, validation and rate limiting.

______________________________________________________________________

## Scenario 3 — Millions of Keys Expire Together

A deployment populated millions of keys with the same five-minute TTL.

**Answer:**

This can cause a cache avalanche.

Use TTL jitter/staggered expiration, warming and graceful degradation.

______________________________________________________________________

## Scenario 4 — Lock Holder Crashes

A worker acquires:

```text
lock:product:1001
```

and crashes.

**Answer:**

The lock needs an expiration/lease so another worker can eventually proceed.

______________________________________________________________________

## Scenario 5 — Old Worker Deletes New Lock

Worker A's lock expires. Worker B acquires the same lock. Worker A then executes:

```text
DEL lock:product:1001
```

**Answer:**

This is unsafe because A can delete B's lock.

Use an ownership token and an atomic compare-and-delete release mechanism.

______________________________________________________________________

## Scenario 6 — Cache and Database Disagree

The database has:

```text
price = 100
```

while Redis has:

```text
price = 90
```

**Answer:**

The cache is stale.

Determine whether the data can tolerate eventual consistency. For correctness-sensitive data, use a stronger
invalidation/read strategy rather than blindly serving stale cache data.

______________________________________________________________________

## Scenario 7 — Redis Memory Full

Redis reaches its configured memory limit.

**Answer:**

If an eviction policy is configured, eligible keys may be evicted. Determine whether Redis is cache-only or storing
important state, then verify that the eviction policy matches the data's role.

______________________________________________________________________

## Scenario 8 — Need Automated Failover

A primary/replica Redis deployment needs automatic primary failover.

**Answer:**

Evaluate Redis Sentinel for monitoring and failover coordination.

______________________________________________________________________

## Scenario 9 — Dataset Exceeds One Node

The Redis dataset and workload exceed the practical capacity of one node.

**Answer:**

Evaluate Redis Cluster for horizontal data distribution and capacity scaling.

______________________________________________________________________

## Scenario 10 — Multi-Key Cluster Operation

Two related keys are frequently used in the same multi-key operation but are assigned to different Redis Cluster slots.

**Answer:**

Use an appropriate hash-tagging strategy to colocate related keys in the same slot when the operation requires same-slot
keys.

______________________________________________________________________

## Scenario 11 — Strictly Consistent Payment Data

A payment amount is stored in Redis and can be slightly stale.

**Answer:**

Do not assume cache-aside plus TTL is sufficient. Payment correctness generally requires an authoritative durable data
store and an explicit consistency strategy.

______________________________________________________________________

## Scenario 12 — Write-Back Failure

An application writes important data to Redis, expecting it to reach the database later. Redis fails before persistence.

**Answer:**

Write-back introduces a potential data-loss window. For important data, design durable queues/persistence/recovery
mechanisms or use a transactional source of truth appropriate to the requirement.

______________________________________________________________________

# 84. Practice Exercises

## Exercise 1 — Cache-Aside

Implement:

```text
GET user
  ↓
Redis
  ↓ miss
Database
  ↓
Redis SET + TTL
```

Measure cache-hit and cache-miss latency.

______________________________________________________________________

## Exercise 2 — Invalidation

Implement:

```text
Update database
      ↓
Invalidate cache
```

Test whether subsequent reads retrieve fresh data.

______________________________________________________________________

## Exercise 3 — Invalidation Race

Create concurrent requests where one reads old data while another updates the database.

Observe how an old value can potentially be written back into the cache.

Document a mitigation strategy.

______________________________________________________________________

## Exercise 4 — Stampede

Simulate:

```text
1,000 concurrent requests
+
expired popular key
```

Measure database load.

Then implement a lock/request-coalescing strategy and compare.

______________________________________________________________________

## Exercise 5 — TTL Jitter

Populate many keys with:

```text
TTL = 300
```

Compare expiration behavior against randomized TTLs.

______________________________________________________________________

## Exercise 6 — Negative Caching

Build a lookup for nonexistent products.

Compare database load with and without negative caching.

______________________________________________________________________

## Exercise 7 — Bloom Filter

Implement a simple Bloom-filter-backed lookup.

Measure how many unnecessary database queries are avoided.

______________________________________________________________________

## Exercise 8 — Distributed Lock

Implement a lock using:

```text
SET key token NX EX
```

Test:

- Successful acquisition
- Failed acquisition
- Expiration
- Safe release
- Owner mismatch

______________________________________________________________________

## Exercise 9 — RDB vs AOF

Create a Redis instance and experiment with persistence settings.

Document:

- Recovery behavior
- Storage size
- Write overhead
- Recovery-point characteristics

______________________________________________________________________

## Exercise 10 — Eviction

Configure a small maximum memory and an eviction policy.

Observe which keys are evicted under memory pressure.

______________________________________________________________________

## Exercise 11 — LRU vs LFU

Create two workloads:

```text
Recent-access heavy
Frequency-heavy
```

Compare LRU and LFU behavior.

______________________________________________________________________

## Exercise 12 — Replication

Set up:

```text
Primary
Replica
```

Observe replication and replica lag.

______________________________________________________________________

## Exercise 13 — Sentinel

Study or create a small Sentinel deployment.

Document:

- Monitoring
- Failure detection
- Failover
- Client discovery

______________________________________________________________________

## Exercise 14 — Cluster

Study Redis Cluster using multiple nodes.

Document:

- Hash slots
- Key routing
- Resharding
- Multi-key constraints
- Hash tags

______________________________________________________________________

## Exercise 15 — Production Design

Design Redis for:

```text
10 million users
High read traffic
Product cache
Session storage
Rate limiting
```

Explain:

- Data types
- TTLs
- Cache pattern
- Invalidation
- Eviction
- Persistence
- Replication
- Sentinel/Cluster
- Failure handling

______________________________________________________________________

# 85. Quick Revision

| Concept | Key Point |
|---|---|
| Cache-aside | Application reads cache, DB on miss |
| Write-through | Cache participates in write path |
| Write-back | Cache receives writes and persists later |
| Invalidation | Remove/update stale cached data |
| Stampede | Many requests rebuild same missing key |
| Penetration | Requests repeatedly query nonexistent data |
| Avalanche | Many keys become unavailable together |
| TTL jitter | Randomize expiration timing |
| Request coalescing | One rebuild, others share/recheck |
| Negative caching | Cache missing results |
| Bloom filter | Probabilistic existence filter |
| Distributed lock | Coordinate work across instances |
| `SET NX` | Acquire key only if absent |
| Lock TTL | Prevent abandoned permanent locks |
| Lock token | Identify lock owner |
| RDB | Point-in-time snapshot |
| AOF | Append-oriented write persistence |
| Persistence | Recovery mechanism |
| Backup | Separate disaster-recovery concern |
| Eviction | Remove keys under memory pressure |
| LRU | Least Recently Used |
| LFU | Least Frequently Used |
| Replication | Primary → replica data copies |
| Sentinel | Monitoring/failover |
| Cluster | Sharding + horizontal distribution |
| Hash slots | Cluster key-routing mechanism |
| Hash tags | Colocate related keys |
| Cache warming | Populate cache proactively |
| Stale-while-revalidate | Serve stale while refreshing |
| Cache consistency | Cache can diverge from source |
| Memory pressure | Critical production concern |

______________________________________________________________________

# 86. Completion Checklist

Before moving to File 28, make sure you can explain:

- [ ] Cache-aside
- [ ] Cache-aside read flow
- [ ] Cache-aside write flow
- [ ] Write-through
- [ ] Write-back
- [ ] Cache pattern trade-offs
- [ ] Cache invalidation
- [ ] Delete vs update invalidation
- [ ] Invalidation races
- [ ] Cache stampede
- [ ] Request coalescing
- [ ] Distributed locks
- [ ] TTL jitter
- [ ] Cache penetration
- [ ] Negative caching
- [ ] Bloom filters
- [ ] Cache avalanche
- [ ] Avalanche prevention
- [ ] `SET NX`
- [ ] Lock expiration
- [ ] Lock ownership
- [ ] Safe lock release
- [ ] Distributed lock failure modes
- [ ] Redis persistence
- [ ] RDB
- [ ] AOF
- [ ] RDB vs AOF
- [ ] Persistence vs backup
- [ ] Redis eviction
- [ ] LRU
- [ ] LFU
- [ ] LRU vs LFU
- [ ] Redis replication
- [ ] Replication lag
- [ ] Sentinel
- [ ] Sentinel vs Cluster
- [ ] Redis Cluster
- [ ] Hash slots
- [ ] Hash tags
- [ ] Multi-key Cluster constraints
- [ ] Cache warming
- [ ] Stale-while-revalidate
- [ ] Production memory concerns
- [ ] Cache consistency
- [ ] Production Redis checklist

______________________________________________________________________

# 87. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is cache-aside?
1. Why is cache-aside commonly used?
1. What is write-through caching?
1. What is write-back caching?
1. Compare cache-aside, write-through and write-back.
1. What is cache invalidation?
1. Why is cache invalidation difficult?
1. Delete cache vs update cache?
1. Describe a cache invalidation race.
1. What is a cache stampede?
1. How do you prevent a cache stampede?
1. What is request coalescing?
1. What is TTL jitter?
1. What is cache penetration?
1. How do you prevent cache penetration?
1. What is negative caching?
1. What is a Bloom filter?
1. Can a Bloom filter have false positives?
1. What is cache avalanche?
1. How do you prevent cache avalanche?
1. What is a distributed lock?
1. How would you implement one with Redis?
1. Explain `SET NX`.
1. Why should a distributed lock have a TTL?
1. Why should a lock contain an owner token?
1. Why is blind `DEL` unsafe when releasing a lock?
1. What happens if a lock expires while its owner is still working?
1. What is RDB?
1. What is AOF?
1. Compare RDB and AOF.
1. Is Redis persistence the same as backup?
1. What is Redis eviction?
1. What is LRU?
1. What is LFU?
1. Compare LRU and LFU.
1. When is eviction acceptable?
1. Why can eviction be dangerous?
1. What is Redis replication?
1. Can Redis replicas lag?
1. What is Redis Sentinel?
1. What problem does Sentinel solve?
1. Does Sentinel shard data?
1. What is Redis Cluster?
1. How many hash slots does Redis Cluster use?
1. How does Redis Cluster route keys?
1. What happens with multi-key operations across different slots?
1. What are hash tags?
1. Sentinel vs Cluster?
1. How would you protect a hot cache key?
1. How would you design Redis for production?

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

# 88. Final Senior Interview Scenario

You are designing a Python/FastAPI backend with:

```text
10,000 requests/sec
90% reads
10% writes
```

The database is under heavy read load.

Your Redis design should address:

1. Cache-aside.
1. Key design.
1. TTL.
1. Invalidation.
1. Hot-key protection.
1. Stampede protection.
1. Penetration protection.
1. Memory limits.
1. Eviction.
1. Persistence.
1. Replication.
1. Failover.
1. Scaling.

A strong answer should explain **why** each decision is appropriate rather than simply listing Redis features.

______________________________________________________________________

**Previous:** [26. Redis Fundamentals](./26-redis.md)

**Next:** [28. Kafka](./28-kafka.md)
