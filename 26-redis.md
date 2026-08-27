# 26. Redis Fundamentals

**Previous:** [25. Database Scaling — Practical Overview](./25-database-scaling.md)

**Next:** [27. Redis Caching & Production](./27-redis-caching.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain what Redis is and where it fits in a backend architecture.
- Understand Redis's basic architecture and in-memory data model.
- Choose the appropriate Redis data type for a use case.
- Work conceptually with Strings, Hashes, Lists, Sets and Sorted Sets.
- Understand Streams at an overview level.
- Explain TTL and key expiration.
- Understand Redis atomic operations.
- Explain Redis transactions.
- Distinguish atomic commands from Redis transactions.
- Discuss common Redis use cases in Python backends.
- Answer common Redis interview questions confidently.

> **Scope note:** This file covers Redis fundamentals only. Caching patterns, cache invalidation, cache-aside, stampede protection, distributed locks, production configuration and Redis reliability are covered in File 27.

______________________________________________________________________

# 1. What Is Redis?

Redis is an in-memory data store commonly used as:

- Cache
- Key-value store
- Session store
- Counter store
- Rate-limit backend
- Queue-like structure
- Pub/sub infrastructure
- Stream/event-processing component

Redis is often used alongside a relational database rather than replacing it.

A common architecture is:

```text
Application
   ↓
Redis
   ↓ miss
Database
```

______________________________________________________________________

# 2. Why Redis Is Fast

Redis keeps its working dataset primarily in memory.

Compared with disk-oriented database access, memory access can be significantly faster.

Redis also uses efficient data structures and supports many operations as atomic commands.

However:

> Redis performance depends on workload, command complexity, data size, networking and deployment configuration.

______________________________________________________________________

# 3. Redis Is More Than a Simple Key-Value Store

A basic key-value model looks like:

```text
key → value
```

But Redis supports several native data structures:

```text
String
Hash
List
Set
Sorted Set
Stream
```

The data structure should be selected based on the operation you need.

______________________________________________________________________

# 4. Redis Architecture — Overview

A simplified architecture is:

```text
Python Application
       ↓
Redis Client
       ↓
Redis Server
       ↓
In-memory data structures
```

The client communicates with Redis over the network using the Redis protocol.

______________________________________________________________________

# 5. Redis Keys

Redis stores values under keys.

Example:

```text
user:1001
```

A useful naming convention can make keys easier to manage.

Examples:

```text
user:1001
session:abc123
cart:1001
rate_limit:user:1001
```

Use predictable namespaces.

______________________________________________________________________

# 6. Strings

Redis Strings are the simplest and most commonly used data type.

Example:

```text
SET user:1001:name "Alice"
GET user:1001:name
```

A String can represent:

- Text
- Integer-like counters
- Serialized JSON
- Binary data

______________________________________________________________________

# 7. String Operations

Common operations include:

```text
SET
GET
MSET
MGET
INCR
DECR
APPEND
```

Example:

```text
SET counter 10
INCR counter
```

The result becomes:

```text
11
```

______________________________________________________________________

# 8. Redis Counters

Strings are useful for counters.

Example:

```text
INCR page_views
```

This operation is atomic at the Redis command level.

Counters are commonly used for:

- Request counts
- Page views
- Rate limiting
- Usage tracking

______________________________________________________________________

# 9. Strings for JSON

An application can store serialized JSON as a String.

Conceptually:

```text
user:1001
    ↓
"{...json...}"
```

This is simple but means the application typically retrieves and deserializes the entire value.

If individual fields need independent access, a Hash may be more appropriate.

______________________________________________________________________

# 10. Hashes

A Redis Hash stores field-value pairs under one key.

Conceptually:

```text
user:1001
 ├── name → Alice
 ├── email → alice@example.com
 └── age → 30
```

Example:

```text
HSET user:1001 name "Alice" email "alice@example.com"
HGET user:1001 name
```

______________________________________________________________________

# 11. Hash Use Cases

Hashes are useful for:

- User profiles
- Object-like data
- Small sets of related fields
- Partial field updates

For example:

```text
HSET user:1001 last_login "2026-08-27"
```

updates one field without replacing the entire object.

______________________________________________________________________

# 12. Hash vs String

Suppose a user has:

```text
name
email
age
```

### String

Store the entire serialized object:

```text
user:1001 → JSON
```

### Hash

Store:

```text
user:1001
  name
  email
  age
```

A Hash can be convenient when individual fields need independent access.

______________________________________________________________________

# 13. Lists

Redis Lists are ordered collections of elements.

Common operations include:

```text
LPUSH
RPUSH
LPOP
RPOP
LRANGE
```

Example:

```text
LPUSH queue task1
RPUSH queue task2
```

______________________________________________________________________

# 14. List Use Cases

Lists can be used for:

- Simple queues
- Recent-item lists
- Task buffers
- Activity feeds

For more advanced event-processing requirements, Redis Streams may be more appropriate.

______________________________________________________________________

# 15. List as a Queue

Conceptually:

```text
Producer
   ↓
Redis List
   ↓
Consumer
```

A producer can add items.

A consumer can remove items.

For example:

```text
RPUSH jobs job1
LPOP jobs
```

______________________________________________________________________

# 16. Sets

A Redis Set is an unordered collection of unique elements.

Example:

```text
SADD online_users user1
SADD online_users user2
SADD online_users user1
```

`user1` still appears only once.

______________________________________________________________________

# 17. Set Operations

Important operations include:

```text
SADD
SREM
SISMEMBER
SMEMBERS
SCARD
```

Sets also support mathematical operations such as:

```text
SINTER
SUNION
SDIFF
```

______________________________________________________________________

# 18. Set Use Cases

Sets are useful for:

- Unique tags
- Membership checks
- Deduplication
- User permissions
- Unique visitors
- Group membership

Example:

```text
SISMEMBER admins user:1001
```

can efficiently answer whether a user belongs to a set.

______________________________________________________________________

# 19. Sorted Sets

A Sorted Set stores unique members with scores.

Conceptually:

```text
member → score
```

Example:

```text
leaderboard
 ├── Alice → 100
 ├── Bob   → 90
 └── Carol → 80
```

Members are unique, while scores determine ordering.

______________________________________________________________________

# 20. Sorted Set Operations

Common operations include:

```text
ZADD
ZRANGE
ZREVRANGE
ZRANK
ZSCORE
ZREM
```

For newer Redis command variants, range/query syntax can differ by command version.

______________________________________________________________________

# 21. Sorted Set Use Cases

Sorted Sets are useful for:

- Leaderboards
- Rankings
- Priority-like ordering
- Time-based indexes
- Scheduled items
- Score-based queries

Example:

```text
ZADD leaderboard 100 alice
ZADD leaderboard 90 bob
```

______________________________________________________________________

# 22. Sorted Set vs Set

### Set

```text
user1
user2
user3
```

Use when you care about:

```text
membership
uniqueness
```

### Sorted Set

```text
user1 → 100
user2 → 80
user3 → 95
```

Use when you need:

```text
uniqueness
+
ordering by score
```

______________________________________________________________________

# 23. Streams — Overview

Redis Streams provide an append-oriented data structure for event/message processing.

Conceptually:

```text
Event 1
Event 2
Event 3
Event 4
```

Each entry has an ID and fields.

Example:

```text
XADD orders * order_id 1001 status created
```

______________________________________________________________________

# 24. Why Streams?

Streams can support:

- Event processing
- Consumer groups
- Message history
- Asynchronous workflows
- Event pipelines

They are more structured than using a simple List as a queue.

______________________________________________________________________

# 25. Streams vs Lists

### List

Good for:

```text
simple queue
```

### Stream

Better suited for:

```text
event log
+
multiple consumers
+
consumer groups
+
message tracking
```

This file only covers Streams at an overview level.

______________________________________________________________________

# 26. TTL

TTL means:

> Time To Live.

Redis can associate an expiration time with a key.

Example:

```text
SET session:abc123 value EX 3600
```

The key is intended to expire after:

```text
3600 seconds
```

______________________________________________________________________

# 27. Why TTL Is Useful

TTL is useful for temporary data such as:

- Sessions
- Verification codes
- Temporary tokens
- Cache entries
- Rate-limit windows
- Temporary locks

Example:

```text
otp:user:1001
TTL → 300 seconds
```

______________________________________________________________________

# 28. `EXPIRE`

An expiration can also be applied after setting a key.

Conceptually:

```text
SET session:abc123 value
EXPIRE session:abc123 3600
```

The key will expire after the configured duration.

______________________________________________________________________

# 29. `TTL`

Redis provides:

```text
TTL key
```

to inspect the remaining lifetime.

Example:

```text
TTL session:abc123
```

The result indicates how much time remains according to Redis's TTL semantics.

______________________________________________________________________

# 30. Expiration

When a key expires, Redis removes it according to its expiration mechanism.

Applications should not depend on an expired key continuing to exist.

For temporary data:

```text
key
 ↓
TTL
 ↓
expiration
 ↓
key unavailable
```

______________________________________________________________________

# 31. TTL Design Considerations

TTL should be chosen based on the purpose of the data.

For example:

```text
OTP → short
Session → longer
Cache → workload dependent
Rate-limit window → fixed window
```

A TTL that is too short can cause unnecessary misses.

A TTL that is too long can keep stale/unneeded data in memory.

______________________________________________________________________

# 32. Atomic Redis Commands

Many individual Redis commands are atomic.

For example:

```text
INCR counter
```

is an atomic Redis operation.

Similarly:

```text
SADD users user1
```

is executed as one Redis command.

This is useful when multiple clients access the same key concurrently.

______________________________________________________________________

# 33. Why Atomic Operations Matter

Suppose two requests increment:

```text
counter = 10
```

A naive application-level sequence might be:

```text
GET → 10
GET → 10

A calculates 11
B calculates 11

SET → 11
SET → 11
```

The expected result:

```text
12
```

can become:

```text
11
```

Using:

```text
INCR counter
```

avoids that particular read-modify-write race.

______________________________________________________________________

# 34. Redis Transactions

Redis provides transactions using:

```text
MULTI
EXEC
```

Commands can be queued and then executed together.

Conceptually:

```text
MULTI
 ↓
COMMAND 1
COMMAND 2
COMMAND 3
 ↓
EXEC
```

______________________________________________________________________

# 35. Redis Transactions vs Database Transactions

Redis transactions should not automatically be equated with relational database transactions.

Redis transactions provide a different model.

A key interview point is:

> Redis transactions do not provide the same rollback semantics as a relational database transaction.

______________________________________________________________________

# 36. Redis Transaction Example

Conceptually:

```text
MULTI
INCR account:a
DECR account:b
EXEC
```

The queued commands are executed as a group without interleaving commands from other clients between the execution of
the transaction's commands.

______________________________________________________________________

# 37. No General Rollback

Redis does not generally roll back previously executed commands if a later command fails during `EXEC`.

For example:

```text
COMMAND 1 succeeds
COMMAND 2 fails
```

The effect of command 1 is not automatically undone like a traditional relational transaction rollback.

This distinction is important in interviews.

______________________________________________________________________

# 38. Redis Atomicity vs Transactions

Do not confuse:

```text
Atomic command
```

with:

```text
Redis transaction
```

An individual command can be atomic without `MULTI/EXEC`.

Use transactions when multiple Redis commands need grouped execution semantics.

______________________________________________________________________

# 39. WATCH

Redis also supports optimistic concurrency control using:

```text
WATCH
MULTI
EXEC
```

Conceptually:

```text
WATCH key
 ↓
Read key
 ↓
Calculate new value
 ↓
MULTI
 ↓
Write
 ↓
EXEC
```

If the watched key changes before `EXEC`, the transaction can be aborted/rejected according to Redis transaction
semantics.

______________________________________________________________________

# 40. Redis Atomicity Model

A useful interview-level summary:

```text
Single command
    ↓
Atomic execution

MULTI/EXEC
    ↓
Queued commands executed together

WATCH
    ↓
Optimistic concurrency control
```

______________________________________________________________________

# 41. Redis and Concurrency

Redis processes commands sequentially within the relevant execution model, so an individual command is not partially
interleaved with another command.

This is a major reason simple Redis operations can be safely used for counters and similar concurrency-sensitive
operations.

______________________________________________________________________

# 42. Command Complexity Matters

Redis operations have different computational complexity.

For example:

```text
GET
SET
INCR
```

are designed for efficient constant-time-style operations for normal use.

Other commands can involve scanning many elements.

For example:

```text
SMEMBERS
LRANGE
```

can return large amounts of data.

Therefore:

> "Redis is fast" does not mean every Redis command is cheap.

______________________________________________________________________

# 43. Large Values

Storing extremely large values can cause:

- High memory usage
- Network overhead
- Slow serialization/deserialization
- Latency spikes
- Expensive replication

Keep Redis values appropriately sized for their use case.

______________________________________________________________________

# 44. Redis as a Cache

A common pattern is:

```text
Application
    ↓
Redis GET
    ↓
Cache hit → return
    ↓ miss
Database
    ↓
Redis SET + TTL
```

Detailed caching patterns are covered in File 27.

______________________________________________________________________

# 45. Redis as a Session Store

A session can be stored as:

```text
session:<id>
```

with a TTL:

```text
SET session:abc123 ... EX 3600
```

This allows sessions to expire automatically.

______________________________________________________________________

# 46. Redis for Rate Limiting

Redis atomic counters are useful for rate limiting.

Conceptually:

```text
INCR requests:user:1001
EXPIRE requests:user:1001 60
```

The application can check whether the counter exceeds the allowed threshold.

Production-safe rate-limiting patterns are covered in File 27.

______________________________________________________________________

# 47. Redis for Leaderboards

Sorted Sets are a natural fit:

```text
ZADD leaderboard 100 user1
ZADD leaderboard 200 user2
```

Then the application can query users by ranking/score.

______________________________________________________________________

# 48. Redis for Membership

Sets are useful for:

```text
SADD admins user1
SISMEMBER admins user1
```

This can provide efficient membership checks.

______________________________________________________________________

# 49. Redis Data Type Selection

| Requirement | Data Type |
|---|---|
| Simple value/counter | String |
| Object-like fields | Hash |
| Ordered sequence/queue | List |
| Unique membership | Set |
| Unique + score/order | Sorted Set |
| Event/message stream | Stream |

Choosing the right data type is a common Redis interview topic.

______________________________________________________________________

# 50. Key Naming

Good:

```text
user:1001
session:abc123
cart:1001
leaderboard:global
```

Poor:

```text
u1001
x
data
temp1
```

A consistent namespace makes debugging and operational management easier.

______________________________________________________________________

# 51. Redis Memory

Redis is memory-oriented, so memory is a critical resource.

Monitor:

- Used memory
- Peak memory
- Key count
- Evictions where configured
- Fragmentation
- Large keys

Production memory management is covered in File 27.

______________________________________________________________________

# 52. Redis Persistence — Overview

Although Redis is commonly used as an in-memory store, it also supports persistence mechanisms.

Two important concepts are:

- RDB snapshots
- AOF (Append Only File)

For this course, know the names and purpose at a high level.

Persistence and production durability are covered further when discussing production Redis.

______________________________________________________________________

# 53. Redis vs Relational Database

Redis and relational databases solve different problems.

### Redis

Strong fit for:

- Fast key/value access
- Caching
- Counters
- Temporary data
- Certain queues/events
- Rate limiting

### Relational database

Strong fit for:

- Durable business data
- Complex relationships
- SQL queries
- Constraints
- Multi-row transactions
- Strong transactional consistency

Often they are used together.

______________________________________________________________________

# 54. Redis vs Database — Example

For an e-commerce system:

```text
PostgreSQL
  ↓
Orders
Users
Products
Payments
```

Redis:

```text
Cache
Sessions
Rate limits
Counters
Temporary state
```

Redis does not need to replace the relational database.

______________________________________________________________________

# 55. Redis and Durability

Redis can persist data, but the durability characteristics depend on configuration.

Therefore:

> Do not assume every Redis deployment is equivalent to a fully durable relational database.

For critical data, choose storage and persistence architecture according to business requirements.

______________________________________________________________________

# 56. Redis and Expiration

Expiration is particularly useful when the application knows that data has a finite lifetime.

Examples:

```text
verification_code:user:1001 → 5 min
session:user:1001 → 1 hour
cache:product:1001 → 10 min
```

TTL becomes part of the data model.

______________________________________________________________________

# 57. Atomic Check-and-Set Patterns

Many concurrency problems require:

```text
check condition
+
modify value
```

If the operation can be represented by a single atomic Redis command, prefer that.

For more complex workflows, consider:

- `WATCH`
- `MULTI/EXEC`
- Lua scripting where appropriate

This file only covers the fundamentals of those mechanisms.

______________________________________________________________________

# 58. Redis Transactions Are Not a Replacement for SQL Transactions

Suppose a business operation requires:

```text
Update order
Update inventory
Insert audit record
```

in a relational database.

Moving those operations to Redis does not automatically provide equivalent relational transaction guarantees.

Use the storage system appropriate to the consistency and durability requirements.

______________________________________________________________________

# 59. Common Redis Mistakes

## Mistake 1 — Treating Redis as a relational database

Redis is a different data model.

## Mistake 2 — Using the wrong data type

A Set may be better than a String containing a list of IDs.

## Mistake 3 — Ignoring TTL

Temporary data can remain indefinitely if expiration is not designed.

## Mistake 4 — Storing huge values

Large values can cause memory and latency problems.

## Mistake 5 — Confusing atomic commands with transactions

A single command can be atomic without `MULTI/EXEC`.

## Mistake 6 — Assuming Redis transactions roll back

Redis does not provide general relational-style rollback semantics.

## Mistake 7 — Using expensive commands on huge collections

Command complexity and result size matter.

## Mistake 8 — Sharing Redis and database responsibilities blindly

Choose the storage system according to the data's requirements.

______________________________________________________________________

# 60. Interview Questions & Answers

## Q1. What is Redis?

**Answer:**

Redis is an in-memory data store supporting multiple data structures and commonly used for caching, counters, sessions,
rate limiting, queues and event-processing workloads.

______________________________________________________________________

## Q2. Why is Redis fast?

**Answer:**

It keeps its working data primarily in memory and provides efficient native data structures and commands. Actual
performance still depends on workload, command complexity, networking and configuration.

______________________________________________________________________

## Q3. Is Redis only a key-value store?

**Answer:**

No.

It provides data structures such as Strings, Hashes, Lists, Sets, Sorted Sets and Streams.

______________________________________________________________________

## Q4. What are Redis Strings?

**Answer:**

Strings are general-purpose values that can store text, serialized data and integer-like values used for counters.

______________________________________________________________________

## Q5. How do you implement a Redis counter?

**Answer:**

Use an atomic command such as:

```text
INCR counter
```

______________________________________________________________________

## Q6. Why is `INCR` useful for concurrency?

**Answer:**

The increment is performed atomically by Redis, avoiding the race that can occur with a separate GET followed by SET.

______________________________________________________________________

## Q7. What is a Redis Hash?

**Answer:**

A collection of field-value pairs stored under one key, useful for object-like data and partial field updates.

______________________________________________________________________

## Q8. When would you use a Hash instead of a String?

**Answer:**

When the data consists of related fields and individual fields need to be accessed or updated independently.

______________________________________________________________________

## Q9. What is a Redis List?

**Answer:**

An ordered collection of elements that supports operations from both ends and can be used for simple queues or ordered
lists.

______________________________________________________________________

## Q10. What is a Redis Set?

**Answer:**

An unordered collection of unique members.

______________________________________________________________________

## Q11. What are Sets useful for?

**Answer:**

Membership checks, uniqueness, deduplication, tags and group membership.

______________________________________________________________________

## Q12. What is a Sorted Set?

**Answer:**

A collection of unique members associated with scores that determine ordering.

______________________________________________________________________

## Q13. What are Sorted Sets useful for?

**Answer:**

Leaderboards, rankings, score-based queries and other use cases requiring unique members with ordering.

______________________________________________________________________

## Q14. Set vs Sorted Set?

**Answer:**

A Set provides uniqueness and membership.

A Sorted Set provides uniqueness plus score-based ordering.

______________________________________________________________________

## Q15. What are Redis Streams?

**Answer:**

An append-oriented data structure for event/message processing with entries, IDs and consumer-group capabilities.

______________________________________________________________________

## Q16. Lists vs Streams?

**Answer:**

Lists are useful for simple queue-like behavior.

Streams provide richer event/message-processing semantics such as message IDs and consumer groups.

______________________________________________________________________

## Q17. What is TTL?

**Answer:**

Time To Live is the remaining lifetime associated with an expiring Redis key.

______________________________________________________________________

## Q18. Why use TTL?

**Answer:**

To automatically remove temporary data such as sessions, OTPs, cache entries and rate-limit state.

______________________________________________________________________

## Q19. What happens when a Redis key expires?

**Answer:**

The key becomes unavailable according to Redis's expiration mechanism and is removed from the dataset.

______________________________________________________________________

## Q20. What is `EXPIRE`?

**Answer:**

A Redis command that assigns an expiration time to an existing key.

______________________________________________________________________

## Q21. What is `TTL`?

**Answer:**

A command used to inspect the remaining expiration time of a key.

______________________________________________________________________

## Q22. Are Redis commands atomic?

**Answer:**

Many individual Redis commands execute atomically, although command complexity and multi-step application logic still
require careful design.

______________________________________________________________________

## Q23. What is a Redis transaction?

**Answer:**

A sequence of commands queued with `MULTI` and executed with `EXEC` as a grouped command sequence.

______________________________________________________________________

## Q24. Do Redis transactions support rollback like PostgreSQL?

**Answer:**

No.

Redis transactions do not provide general relational-style rollback semantics for already executed commands.

______________________________________________________________________

## Q25. Why use `MULTI/EXEC`?

**Answer:**

To group multiple Redis commands so they execute together without other client commands being interleaved between the
transaction's command execution.

______________________________________________________________________

## Q26. What is `WATCH`?

**Answer:**

`WATCH` provides optimistic concurrency control by monitoring keys and allowing the transaction attempt to be aborted if
watched keys change before execution.

______________________________________________________________________

## Q27. Atomic command vs Redis transaction?

**Answer:**

An atomic command is one Redis operation executed atomically.

A Redis transaction groups multiple commands for transactional execution semantics.

______________________________________________________________________

## Q28. Can a Redis transaction partially fail?

**Answer:**

Redis does not provide general rollback of earlier commands if a later command fails during execution. This differs from
traditional database transaction semantics.

______________________________________________________________________

## Q29. What is Redis commonly used for?

**Answer:**

Caching, sessions, counters, rate limiting, temporary state, queues, leaderboards, membership checks and event
processing.

______________________________________________________________________

## Q30. Should Redis replace PostgreSQL/MySQL?

**Answer:**

Not generally.

Redis and relational databases serve different purposes and are often used together.

______________________________________________________________________

## Q31. Why are large Redis values dangerous?

**Answer:**

They consume memory and can increase network transfer, serialization cost and latency.

______________________________________________________________________

## Q32. Why does command complexity matter?

**Answer:**

Some Redis commands process many elements. Large collections can make seemingly simple commands expensive.

______________________________________________________________________

## Q33. What is connection pooling in a Redis client?

**Answer:**

A mechanism for reusing network connections between the application and Redis rather than establishing a new connection
for every command. Client-library behavior varies.

______________________________________________________________________

## Q34. What is Redis persistence?

**Answer:**

Redis supports mechanisms such as RDB snapshots and AOF to persist data beyond process memory.

______________________________________________________________________

## Q35. Is Redis always durable?

**Answer:**

No.

Durability depends on persistence and deployment configuration. It should not automatically be treated as equivalent to
a fully durable relational database.

______________________________________________________________________

## Q36. What is a good Redis key naming strategy?

**Answer:**

Use predictable namespaces such as:

```text
user:1001
session:abc123
cart:1001
```

so keys are easy to understand and manage.

______________________________________________________________________

## Q37. How would you store a user profile in Redis?

**Answer:**

A Hash is often appropriate if individual fields need independent access:

```text
user:1001
  name
  email
  age
```

A serialized String can also be appropriate when the object is always read/written as a whole.

______________________________________________________________________

## Q38. How would you implement a leaderboard?

**Answer:**

Use a Sorted Set with the user's score as the sorted-set score.

______________________________________________________________________

## Q39. How would you implement unique membership?

**Answer:**

Use a Set and operations such as `SADD` and `SISMEMBER`.

______________________________________________________________________

## Q40. How would you implement a simple queue?

**Answer:**

A Redis List can be used with push/pop operations. For richer event-processing requirements, consider Streams.

______________________________________________________________________

## Q41. How would you implement temporary session data?

**Answer:**

Store it under a session key with an appropriate TTL.

______________________________________________________________________

## Q42. Why is TTL important for sessions?

**Answer:**

It prevents abandoned session data from remaining indefinitely and provides automatic expiration.

______________________________________________________________________

## Q43. How would you implement a simple counter safely?

**Answer:**

Use an atomic Redis command such as `INCR` instead of performing separate GET and SET operations.

______________________________________________________________________

## Q44. What is a read-modify-write race in Redis?

**Answer:**

Two clients independently read the same value, calculate updates and overwrite each other. Atomic commands or optimistic
concurrency mechanisms can prevent the specific race.

______________________________________________________________________

## Q45. When would you use `WATCH`?

**Answer:**

When a multi-step update needs optimistic concurrency control and should only proceed if watched keys have not changed.

______________________________________________________________________

## Q46. Why shouldn't you put relational business data entirely in Redis?

**Answer:**

Redis has a different data model and transaction/constraint model. Relational databases are often more appropriate for
durable business data, relationships and complex transactional operations.

______________________________________________________________________

## Q47. Does Redis guarantee that every command is O(1)?

**Answer:**

No.

Redis commands have different complexity characteristics. Operations over large collections can be expensive.

______________________________________________________________________

## Q48. Why can `SMEMBERS` become expensive?

**Answer:**

It returns all members of a Set, so a very large Set can produce a large response and require significant work.

______________________________________________________________________

## Q49. What is a Redis memory concern?

**Answer:**

Redis's in-memory dataset means memory capacity is a critical resource. Large values, too many keys and insufficient
memory management can cause serious performance/availability problems.

______________________________________________________________________

## Q50. Give a senior-level explanation of Redis.

**Answer:**

"Redis is an in-memory data store with native data structures and atomic commands. I would choose the data structure
based on access patterns—for example Strings for counters, Hashes for field-based objects, Sets for membership, Sorted
Sets for rankings and Streams for event processing. I would use TTL for temporary data and understand that `MULTI/EXEC`
provides grouped execution semantics rather than relational rollback. In production, I would also consider memory,
command complexity, connection management, persistence, failure behavior and caching consistency."

______________________________________________________________________

# 61. Scenario-Based Questions

## Scenario 1 — Counter Race

Two requests execute:

```text
GET counter
calculate +1
SET counter
```

and updates are lost.

**Answer:**

Use:

```text
INCR counter
```

because the increment is an atomic Redis command.

______________________________________________________________________

## Scenario 2 — User Membership

You need to answer:

> "Is user 1001 an administrator?"

**Answer:**

Use a Set:

```text
SADD admins user:1001
SISMEMBER admins user:1001
```

______________________________________________________________________

## Scenario 3 — Leaderboard

Users have scores and you need:

```text
Top 100 users
```

**Answer:**

Use a Sorted Set.

______________________________________________________________________

## Scenario 4 — Temporary OTP

An OTP should automatically become invalid after five minutes.

**Answer:**

Store it with a five-minute TTL.

______________________________________________________________________

## Scenario 5 — User Profile

You frequently update only:

```text
last_login
```

without replacing the entire profile.

**Answer:**

A Hash may be appropriate because individual fields can be updated independently.

______________________________________________________________________

## Scenario 6 — Simple Queue

A worker needs to consume simple jobs from a producer.

**Answer:**

A Redis List can provide basic queue-like behavior.

If the system needs richer event history, consumer groups and message-processing semantics, consider Streams.

______________________________________________________________________

## Scenario 7 — Event Processing

Multiple consumers need to process an event stream while tracking consumption.

**Answer:**

Redis Streams are more appropriate than a simple List.

______________________________________________________________________

## Scenario 8 — Redis Transaction Rollback

A developer says:

> "We'll use MULTI/EXEC, so if command 3 fails, commands 1 and 2 automatically roll back."

**Answer:**

That assumption is incorrect.

Redis transactions do not provide general relational-style rollback semantics.

______________________________________________________________________

## Scenario 9 — Concurrent Update

Two clients read the same Redis value and calculate different new values.

**Answer:**

Use an atomic command where possible. If the operation requires a conditional multi-step update, consider `WATCH` with
`MULTI/EXEC` or another suitable Redis mechanism.

______________________________________________________________________

## Scenario 10 — Huge Set

A Set contains tens of millions of members and an endpoint calls:

```text
SMEMBERS
```

for every request.

**Answer:**

This is potentially expensive because it retrieves the entire collection. Redesign the access pattern to retrieve only
what is required.

______________________________________________________________________

# 62. Practice Exercises

## Exercise 1 — Strings

Implement:

```text
SET
GET
MSET
MGET
INCR
DECR
```

using a Redis client from Python.

______________________________________________________________________

## Exercise 2 — Counter

Build a concurrent request counter.

Compare:

```text
GET + SET
```

against:

```text
INCR
```

and explain the race condition.

______________________________________________________________________

## Exercise 3 — Hash

Store a user profile using:

```text
name
email
age
```

Update only the email field.

______________________________________________________________________

## Exercise 4 — List Queue

Implement a simple producer/consumer queue using a Redis List.

Document:

```text
Producer
Consumer
Push
Pop
```

______________________________________________________________________

## Exercise 5 — Set

Build a unique tag system.

Implement:

- Add tag
- Remove tag
- Check membership
- List tags

______________________________________________________________________

## Exercise 6 — Sorted Set

Build a leaderboard.

Implement:

- Add score
- Update score
- Get top users
- Get user rank
- Remove user

______________________________________________________________________

## Exercise 7 — TTL

Implement:

```text
verification_code:<user_id>
```

with a five-minute TTL.

Verify the key expires.

______________________________________________________________________

## Exercise 8 — Redis Transaction

Implement a simple multi-command `MULTI/EXEC` operation.

Observe what happens when one command cannot execute as expected.

Document why Redis transactions differ from relational database rollback.

______________________________________________________________________

## Exercise 9 — WATCH

Implement an optimistic concurrency example using:

```text
WATCH
MULTI
EXEC
```

Create two concurrent clients attempting to update the same value.

______________________________________________________________________

## Exercise 10 — Data Type Selection

For each requirement, select the appropriate Redis type:

1. Page-view counter.
1. User profile.
1. Unique online users.
1. Leaderboard.
1. Simple job queue.
1. Event stream.
1. Temporary OTP.

Explain each decision.

______________________________________________________________________

## Exercise 11 — Key Design

Design key names for:

```text
Users
Sessions
Shopping carts
Rate limits
Product cache
Leaderboards
```

Use consistent namespaces.

______________________________________________________________________

## Exercise 12 — Redis vs Database

For an e-commerce application, decide which system should own:

```text
Users
Orders
Payments
Product cache
Sessions
Rate limits
Leaderboards
```

Explain the reasoning.

______________________________________________________________________

# 63. Quick Revision

| Concept | Key Point |
|---|---|
| Redis | In-memory data store with multiple data structures |
| String | Simple value/counter |
| Hash | Field-value object-like data |
| List | Ordered collection/queue-like structure |
| Set | Unique unordered members |
| Sorted Set | Unique members ordered by score |
| Stream | Append-oriented event/message structure |
| TTL | Time remaining before key expiration |
| `EXPIRE` | Assign expiration |
| `TTL` | Inspect expiration |
| Atomic command | Individual command executes atomically |
| `MULTI` | Begin Redis transaction queue |
| `EXEC` | Execute queued transaction commands |
| `WATCH` | Optimistic concurrency control |
| Redis transaction | Grouped command execution, not relational rollback |
| Counter | `INCR`/`DECR` |
| Membership | Set |
| Ranking | Sorted Set |
| Queue | List |
| Event processing | Stream |
| Temporary data | TTL |
| Cache | Common Redis use case |
| Session store | Common Redis use case |
| Rate limiting | Often uses atomic counters |
| Persistence | RDB/AOF overview |
| Memory | Critical Redis resource |
| Command complexity | Varies by command |
| Large values | Can increase memory/network/latency |

______________________________________________________________________

# 64. Completion Checklist

Before moving to File 27, make sure you can explain:

- [ ] What Redis is
- [ ] Why Redis is fast
- [ ] Redis architecture overview
- [ ] Redis keys
- [ ] Key naming
- [ ] Strings
- [ ] String operations
- [ ] Atomic counters
- [ ] Hashes
- [ ] Hash vs String
- [ ] Lists
- [ ] List queue use case
- [ ] Sets
- [ ] Set membership
- [ ] Set operations
- [ ] Sorted Sets
- [ ] Sorted Set rankings
- [ ] Set vs Sorted Set
- [ ] Streams overview
- [ ] List vs Stream
- [ ] TTL
- [ ] `EXPIRE`
- [ ] `TTL`
- [ ] Expiration
- [ ] TTL design
- [ ] Atomic Redis commands
- [ ] Redis transactions
- [ ] `MULTI`
- [ ] `EXEC`
- [ ] `WATCH`
- [ ] Redis transaction vs relational transaction
- [ ] Redis rollback limitation
- [ ] Command complexity
- [ ] Large values
- [ ] Redis memory considerations
- [ ] Redis persistence overview
- [ ] Redis vs relational database
- [ ] Redis use cases
- [ ] Basic Redis concurrency patterns
- [ ] Data-type selection

______________________________________________________________________

# 65. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is Redis?
1. Why is Redis fast?
1. Is Redis only a key-value store?
1. What data structures does Redis provide?
1. What are Redis Strings?
1. How do you implement a Redis counter?
1. Why is `INCR` useful for concurrency?
1. What is a Redis Hash?
1. When would you choose Hash over String?
1. What is a Redis List?
1. What are Lists commonly used for?
1. What is a Redis Set?
1. What are Sets useful for?
1. What is a Sorted Set?
1. What are Sorted Sets useful for?
1. Set vs Sorted Set?
1. What are Redis Streams?
1. List vs Stream?
1. What is TTL?
1. Why use TTL?
1. What does `EXPIRE` do?
1. What does `TTL` do?
1. What happens when a key expires?
1. Are Redis commands atomic?
1. Give examples of atomic Redis commands.
1. What is a Redis transaction?
1. What are `MULTI` and `EXEC`?
1. Does Redis provide rollback like PostgreSQL?
1. What happens if one command in a Redis transaction fails?
1. What is `WATCH`?
1. How does `WATCH` provide optimistic concurrency?
1. Atomic command vs Redis transaction?
1. Why does command complexity matter in Redis?
1. Why can large Redis values be dangerous?
1. What is Redis commonly used for?
1. How would you implement a leaderboard?
1. How would you implement membership checking?
1. How would you implement a simple queue?
1. How would you implement temporary session data?
1. How would you implement an OTP with expiration?
1. How would you implement a rate-limit counter?
1. Should Redis replace a relational database?
1. When should you use a Hash?
1. When should you use a Set?
1. When should you use a Sorted Set?
1. When should you use Streams?
1. What is Redis persistence?
1. What are RDB and AOF?
1. Why is memory a critical Redis resource?
1. Give a senior-level explanation of how you would choose Redis data structures for a production Python backend.

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [25. Database Scaling — Practical Overview](./25-database-scaling.md)

**Next:** [27. Redis Caching & Production](./27-redis-caching.md)
