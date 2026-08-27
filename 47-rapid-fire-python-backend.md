# 47. Rapid-Fire Python Backend Q&A

**Previous:** [46. AI-Assisted Software Engineering](./46-ai-assisted-development.md)

**Next:** [48. Technical Mock Interview & Final Revision](./48-technical-mock-interview-final-revision.md)

______________________________________________________________________

## Objective

This is the **last-minute revision bank** for the Python backend interview plan.

The purpose is not to provide deep explanations.

Use this file to quickly refresh:

- Python
- Collections
- OOP
- Concurrency
- AsyncIO
- FastAPI
- HTTP
- SQL
- Normalization
- SQLAlchemy
- Redis
- Kafka
- RabbitMQ
- Celery
- Docker
- Linux
- Security
- Git
- DSA
- System Design

For detailed preparation, return to the corresponding topic file.

The recommended revision pattern is:

```text
Question
   ↓
Answer in 20–60 seconds
   ↓
Explain one example
   ↓
Mention one trade-off / caveat
```

______________________________________________________________________

# Part 1 — Python

## Q1. What is the difference between a list and a tuple?

**Answer:**

A list is mutable, while a tuple is immutable.

```python
items = [1, 2, 3]
items.append(4)

values = (1, 2, 3)
```

Use a list when the collection needs modification and a tuple when immutability is useful.

______________________________________________________________________

## Q2. What is the difference between `is` and `==`?

**Answer:**

```text
== → value equality
is → object identity
```

Example:

```python
a == b
```

checks whether values are equal.

```python
a is b
```

checks whether both references point to the same object.

______________________________________________________________________

## Q3. What are mutable and immutable objects?

**Answer:**

Mutable objects can be changed after creation.

Examples:

```text
list
dict
set
```

Immutable objects cannot be modified in place.

Examples:

```text
int
float
str
tuple
frozenset
```

______________________________________________________________________

## Q4. What is shallow copy vs deep copy?

**Answer:**

A shallow copy creates a new outer object but keeps references to nested objects.

A deep copy recursively copies nested objects.

```python
import copy

shallow = copy.copy(obj)
deep = copy.deepcopy(obj)
```

______________________________________________________________________

## Q5. What are `*args` and `**kwargs`?

**Answer:**

```python
def func(*args, **kwargs):
    ...
```

`*args` collects positional arguments.

`**kwargs` collects keyword arguments.

______________________________________________________________________

## Q6. What is a Python decorator?

**Answer:**

A decorator wraps a function or class to extend or modify its behavior without changing the original implementation
directly.

```python
@decorator
def func():
    ...
```

______________________________________________________________________

## Q7. What is a context manager?

**Answer:**

A context manager manages setup and cleanup around a block of code.

```python
with open("file.txt") as f:
    data = f.read()
```

It is commonly used for:

```text
Files
Locks
Database connections
Transactions
Resources
```

______________________________________________________________________

## Q8. What is the difference between an iterator and an iterable?

**Answer:**

An iterable can produce an iterator.

An iterator implements the iteration protocol, primarily through:

```python
__iter__()
__next__()
```

______________________________________________________________________

## Q9. What is a generator?

**Answer:**

A generator produces values lazily, usually using `yield`.

```python
def numbers():
    yield 1
    yield 2
```

It avoids creating the entire result in memory at once.

______________________________________________________________________

## Q10. What is the GIL?

**Answer:**

The Global Interpreter Lock in CPython allows only one thread at a time to execute Python bytecode within a process.

It limits CPU-bound parallelism with traditional Python threads, while threads can still be useful for I/O-bound
workloads.

______________________________________________________________________

# Part 2 — Collections

## Q11. When would you use a list, set or dictionary?

**Answer:**

```text
list → ordered sequence / positional access
set → uniqueness / membership
dict → key-value lookup
```

Typical lookup complexity is approximately:

```text
list membership → O(n)
set membership  → O(1) average
dict lookup     → O(1) average
```

______________________________________________________________________

## Q12. Why are sets useful?

**Answer:**

Sets provide unique elements and efficient average-case membership testing.

```python
seen = set()

if value in seen:
    ...
```

______________________________________________________________________

## Q13. How does a dictionary work conceptually?

**Answer:**

A Python dictionary is hash-table based.

A key is hashed and the hash is used to locate the corresponding entry.

Keys must satisfy the required hashing/equality semantics.

______________________________________________________________________

## Q14. What makes a good dictionary key?

**Answer:**

The key must be hashable.

Common examples:

```text
str
int
tuple of hashable values
```

Mutable collections such as lists and dictionaries are not valid dictionary keys.

______________________________________________________________________

## Q15. What is `defaultdict`?

**Answer:**

`defaultdict` provides a default value when a missing key is accessed.

```python
from collections import defaultdict

groups = defaultdict(list)
groups["a"].append(1)
```

______________________________________________________________________

## Q16. What is `Counter`?

**Answer:**

`Counter` is useful for counting occurrences.

```python
from collections import Counter

counts = Counter(["a", "b", "a"])
```

Result conceptually:

```text
a → 2
b → 1
```

______________________________________________________________________

## Q17. What is a deque?

**Answer:**

`collections.deque` supports efficient insertion and removal from both ends.

It is useful for:

```text
Queues
Sliding windows
BFS
```

______________________________________________________________________

# Part 3 — OOP

## Q18. What are the four common OOP principles?

**Answer:**

```text
Encapsulation
Abstraction
Inheritance
Polymorphism
```

______________________________________________________________________

## Q19. Composition vs inheritance?

**Answer:**

Inheritance represents an "is-a" relationship.

Composition represents a "has-a" relationship.

Composition is often preferable when behavior should be assembled rather than inherited.

______________________________________________________________________

## Q20. What is MRO?

**Answer:**

MRO stands for Method Resolution Order.

It defines the order Python follows when searching for attributes and methods across an inheritance hierarchy.

```python
ClassName.__mro__
```

______________________________________________________________________

## Q21. What does `super()` do?

**Answer:**

`super()` provides access to the next class in the MRO.

It is especially important with multiple inheritance because it allows cooperative method resolution.

______________________________________________________________________

## Q22. What is an abstract base class?

**Answer:**

An abstract base class defines an interface or common contract that subclasses are expected to implement.

Python provides this through the `abc` module.

______________________________________________________________________

## Q23. What is a mixin?

**Answer:**

A mixin is a small reusable class intended to provide specific behavior to another class through inheritance.

A mixin generally represents a capability rather than a complete domain object.

______________________________________________________________________

## Q24. What is a descriptor?

**Answer:**

A descriptor is an object implementing methods such as:

```python
__get__
__set__
__delete__
```

Descriptors allow custom attribute access behavior.

Properties are a common example of descriptor-based behavior.

______________________________________________________________________

## Q25. What is `__slots__`?

**Answer:**

`__slots__` can restrict which instance attributes are stored and can reduce per-instance memory usage in appropriate
cases.

It also changes some normal instance behavior, so it should be used deliberately.

______________________________________________________________________

## Q26. What is `__new__` vs `__init__`?

**Answer:**

```text
__new__  → creates/returns the instance
__init__ → initializes the instance
```

`__new__` is especially relevant for immutable types and advanced object creation.

______________________________________________________________________

## Q27. What is a metaclass?

**Answer:**

A metaclass controls how classes themselves are created.

Conceptually:

```text
object → instance
class  → instance of a metaclass
```

Metaclasses are advanced functionality and should be used only when simpler mechanisms are insufficient.

______________________________________________________________________

## Q28. What is duck typing?

**Answer:**

Duck typing focuses on behavior rather than explicit type relationships.

Conceptually:

> If an object supports the required operations, it can be used.

______________________________________________________________________

## Q29. What is a Protocol?

**Answer:**

A `Protocol` provides structural typing.

A class can satisfy the protocol by providing the required attributes/methods without explicitly inheriting from it.

______________________________________________________________________

# Part 4 — Concurrency

## Q30. Thread vs process?

**Answer:**

Threads share process memory and are relatively lightweight.

Processes have separate memory spaces and provide true process-level parallelism.

Typical guideline:

```text
I/O-bound → threads or async
CPU-bound → processes / native parallelism
```

______________________________________________________________________

## Q31. CPU-bound vs I/O-bound?

**Answer:**

CPU-bound work spends most of its time computing.

I/O-bound work spends significant time waiting for:

```text
Network
Disk
Database
External services
```

Concurrency strategies depend on the workload.

______________________________________________________________________

## Q32. What is a race condition?

**Answer:**

A race condition occurs when the result depends on the timing/order of concurrent operations on shared state.

______________________________________________________________________

## Q33. What is a lock?

**Answer:**

A lock provides mutual exclusion so that only the intended execution path accesses a critical section at a time.

Example:

```python
with lock:
    shared_state += 1
```

______________________________________________________________________

## Q34. What is a deadlock?

**Answer:**

A deadlock occurs when concurrent operations wait indefinitely for resources held by one another.

A common prevention strategy is consistent lock ordering.

______________________________________________________________________

## Q35. What is `ThreadPoolExecutor`?

**Answer:**

It provides a pool of worker threads for executing callables concurrently.

It is useful for I/O-bound work and integrating blocking functions into otherwise structured applications.

______________________________________________________________________

## Q36. What is `ProcessPoolExecutor`?

**Answer:**

It uses separate processes to execute work concurrently.

It can be useful for CPU-bound tasks because separate processes are not constrained by the same interpreter-level GIL
behavior as threads.

______________________________________________________________________

# Part 5 — AsyncIO

## Q37. What is the event loop?

**Answer:**

The event loop coordinates asynchronous tasks and resumes them when awaited operations become ready.

______________________________________________________________________

## Q38. What is a coroutine?

**Answer:**

A coroutine is an asynchronous computation defined using `async def`.

```python
async def fetch():
    ...
```

Calling it produces a coroutine object that must be awaited or scheduled.

______________________________________________________________________

## Q39. What does `await` do?

**Answer:**

`await` suspends the current coroutine while an awaitable operation is pending, allowing the event loop to run other
work.

______________________________________________________________________

## Q40. What is an asyncio task?

**Answer:**

A task schedules a coroutine for execution by the event loop.

```python
task = asyncio.create_task(work())
```

______________________________________________________________________

## Q41. What does `asyncio.gather()` do?

**Answer:**

It allows multiple awaitables to be awaited together.

It is useful when independent asynchronous operations can progress concurrently.

______________________________________________________________________

## Q42. What happens if blocking code runs inside an async endpoint?

**Answer:**

It can block the event loop and prevent other asynchronous tasks from making progress.

Examples:

```text
Blocking file operations
Blocking network calls
CPU-heavy computation
Synchronous libraries
```

Use appropriate async APIs or move blocking work outside the event loop.

______________________________________________________________________

## Q43. Why are timeouts important?

**Answer:**

Without timeouts, a dependency can wait indefinitely and consume resources.

Timeouts provide bounded failure behavior.

______________________________________________________________________

## Q44. What is cancellation?

**Answer:**

Cancellation allows an asynchronous task to stop because its work is no longer needed or its deadline has expired.

Code should handle cancellation and clean up resources correctly.

______________________________________________________________________

# Part 6 — FastAPI

## Q45. What is FastAPI?

**Answer:**

FastAPI is a Python web framework designed for building APIs with type hints, validation and ASGI-based asynchronous
support.

______________________________________________________________________

## Q46. What is ASGI?

**Answer:**

ASGI is an interface specification for asynchronous Python web applications and servers.

It supports asynchronous request handling and protocols such as HTTP and WebSockets.

______________________________________________________________________

## Q47. What is dependency injection in FastAPI?

**Answer:**

FastAPI dependencies allow reusable components to be declared and injected into route handlers.

Common uses:

```text
Database sessions
Authentication
Authorization
Shared configuration
Reusable validation
```

______________________________________________________________________

## Q48. What is Pydantic used for?

**Answer:**

Pydantic is used for data modeling and validation.

FastAPI uses it heavily for:

```text
Request validation
Response models
Serialization
Schema generation
```

______________________________________________________________________

## Q49. Middleware vs dependency?

**Answer:**

Middleware operates around the request/response processing pipeline.

Dependencies are injected into specific routes or dependency trees.

Use middleware for cross-cutting behavior and dependencies for reusable request-level components.

______________________________________________________________________

## Q50. How should errors be handled in FastAPI?

**Answer:**

Use:

```text
HTTPException
Custom exceptions
Exception handlers
Validation error handling
```

Keep error responses consistent and avoid leaking sensitive internal details.

______________________________________________________________________

## Q51. What is OpenAPI?

**Answer:**

OpenAPI is a machine-readable specification for describing HTTP APIs.

FastAPI can generate OpenAPI documentation from route definitions, types and schemas.

______________________________________________________________________

## Q52. How do you version an API?

**Answer:**

A common approach is URL versioning:

```text
/api/v1/orders
/api/v2/orders
```

Other approaches exist, but consistency and compatibility strategy matter more than the exact mechanism.

______________________________________________________________________

# Part 7 — HTTP & Networking

## Q53. What happens when you enter a URL in a browser?

**Answer:**

A simplified flow is:

```text
DNS
 ↓
TCP connection
 ↓
TLS handshake for HTTPS
 ↓
HTTP request
 ↓
Server processing
 ↓
HTTP response
```

Real systems may also involve:

```text
CDN
WAF
Load balancer
Reverse proxy
```

______________________________________________________________________

## Q54. TCP vs UDP?

**Answer:**

TCP provides connection-oriented, reliable, ordered byte-stream delivery.

UDP is connectionless and provides datagrams without TCP's built-in reliability and ordering guarantees.

______________________________________________________________________

## Q55. What is the TCP three-way handshake?

**Answer:**

Conceptually:

```text
Client → SYN
Server → SYN-ACK
Client → ACK
```

This establishes the TCP connection.

______________________________________________________________________

## Q56. What does TLS provide?

**Answer:**

TLS provides:

```text
Encryption
Integrity
Server authentication
```

HTTPS is HTTP carried over TLS.

______________________________________________________________________

## Q57. Common HTTP methods?

**Answer:**

```text
GET
POST
PUT
PATCH
DELETE
HEAD
OPTIONS
```

______________________________________________________________________

## Q58. What does idempotent mean?

**Answer:**

An operation is idempotent when repeating it produces the same intended final effect as performing it once.

For APIs, idempotency is important when clients or infrastructure retry requests.

______________________________________________________________________

## Q59. Common HTTP status codes?

**Answer:**

```text
200 → OK
201 → Created
204 → No Content
400 → Bad Request
401 → Unauthenticated / credentials required
403 → Forbidden
404 → Not Found
409 → Conflict
422 → Unprocessable/validation-related request
429 → Too Many Requests
500 → Internal Server Error
502 → Bad Gateway
503 → Service Unavailable
504 → Gateway Timeout
```

______________________________________________________________________

## Q60. What is keep-alive?

**Answer:**

HTTP connection reuse allows multiple requests to use an existing connection instead of creating a new connection for
every request.

This reduces connection establishment overhead.

______________________________________________________________________

# Part 8 — SQL

## Q61. What is a primary key?

**Answer:**

A primary key uniquely identifies a row in a table.

It must satisfy the database's uniqueness and non-null requirements for primary keys.

______________________________________________________________________

## Q62. What is a foreign key?

**Answer:**

A foreign key represents a relationship to another table's key and can enforce referential integrity.

______________________________________________________________________

## Q63. What is a JOIN?

**Answer:**

A JOIN combines rows from tables based on a relationship or condition.

Common joins:

```text
INNER JOIN
LEFT JOIN
RIGHT JOIN
FULL OUTER JOIN
```

______________________________________________________________________

## Q64. `WHERE` vs `HAVING`?

**Answer:**

```text
WHERE  → filters rows before grouping
HAVING → filters groups after aggregation
```

______________________________________________________________________

## Q65. `GROUP BY`?

**Answer:**

`GROUP BY` groups rows so aggregate functions can be applied per group.

Example:

```sql
SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id;
```

______________________________________________________________________

## Q66. What is a subquery?

**Answer:**

A query nested inside another query.

It can be used in:

```text
SELECT
FROM
WHERE
HAVING
```

depending on the query.

______________________________________________________________________

## Q67. What is a correlated subquery?

**Answer:**

A correlated subquery refers to values from the outer query and may be evaluated in relation to each outer row.

______________________________________________________________________

## Q68. `EXISTS` vs `IN`?

**Answer:**

Both can test membership/existence, but their behavior and performance depend on the database, query shape and data.

`EXISTS` is often useful when you only care whether a related row exists.

Do not choose based only on a universal performance rule; inspect the actual query plan.

______________________________________________________________________

## Q69. What is a CTE?

**Answer:**

A Common Table Expression defines a named temporary query result using:

```sql
WITH ...
```

It can improve readability and help structure complex queries.

______________________________________________________________________

## Q70. What are window functions?

**Answer:**

Window functions calculate values across related rows without collapsing those rows into one row per group.

Examples:

```text
ROW_NUMBER
RANK
DENSE_RANK
LAG
LEAD
```

______________________________________________________________________

## Q71. `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`?

**Answer:**

For tied values:

```text
ROW_NUMBER → unique sequential numbers
RANK       → ties share rank and gaps can appear
DENSE_RANK → ties share rank and no gaps
```

______________________________________________________________________

# Part 9 — Database Normalization

## Q72. Why normalize a database?

**Answer:**

Normalization reduces unnecessary redundancy and helps prevent:

```text
Insert anomalies
Update anomalies
Delete anomalies
```

______________________________________________________________________

## Q73. What is 1NF?

**Answer:**

First Normal Form generally requires atomic values and removal of repeating groups so each field represents an
appropriate single value.

______________________________________________________________________

## Q74. What is 2NF?

**Answer:**

A relation is in 2NF when it is in 1NF and non-key attributes fully depend on the entire candidate key rather than only
part of a composite key.

______________________________________________________________________

## Q75. What is 3NF?

**Answer:**

A relation is in 3NF when it is in 2NF and non-key attributes do not have inappropriate transitive dependencies on a
key.

______________________________________________________________________

## Q76. What is BCNF?

**Answer:**

BCNF is a stronger normal form than 3NF.

Informally, every determinant should be a candidate key.

______________________________________________________________________

## Q77. What is denormalization?

**Answer:**

Denormalization intentionally introduces redundancy to improve read performance or simplify certain access patterns.

The trade-off is increased complexity around:

```text
Updates
Consistency
Storage
```

______________________________________________________________________

# Part 10 — SQL Indexes & Performance

## Q78. Why use indexes?

**Answer:**

Indexes can reduce the amount of data the database must scan for suitable queries.

The trade-offs include:

```text
Storage
Write overhead
Maintenance
```

______________________________________________________________________

## Q79. What is a B-tree index?

**Answer:**

A B-tree is a balanced tree structure commonly used for efficient ordered lookups, range queries and equality searches.

______________________________________________________________________

## Q80. What is a composite index?

**Answer:**

An index containing multiple columns.

Example:

```sql
CREATE INDEX idx_orders_customer_status
ON orders(customer_id, status);
```

Column order matters.

______________________________________________________________________

## Q81. What is selectivity?

**Answer:**

Selectivity describes how effectively a predicate distinguishes a small subset of rows from the total dataset.

High-selectivity predicates often provide more useful filtering for indexes, although actual usefulness depends on query
shape and data distribution.

______________________________________________________________________

## Q82. What is `EXPLAIN`?

**Answer:**

`EXPLAIN` shows the database's planned execution strategy for a query.

It can help identify:

```text
Sequential scans
Index scans
Join strategies
Estimated row counts
Potential bottlenecks
```

Use execution-analysis variants when actual runtime behavior is required.

______________________________________________________________________

## Q83. What is a covering index?

**Answer:**

An index that contains enough information for a query to be answered from the index without needing to fetch the
underlying table rows, depending on the database and query.

______________________________________________________________________

# Part 11 — Transactions & Concurrency

## Q84. What does ACID mean?

**Answer:**

```text
A → Atomicity
C → Consistency
I → Isolation
D → Durability
```

______________________________________________________________________

## Q85. What is atomicity?

**Answer:**

A transaction's operations succeed as a unit or are rolled back as a unit.

______________________________________________________________________

## Q86. What is isolation?

**Answer:**

Isolation controls how concurrent transactions interact and what intermediate/concurrent changes they can observe.

______________________________________________________________________

## Q87. Dirty read?

**Answer:**

Reading data written by another transaction before that transaction has committed.

______________________________________________________________________

## Q88. Non-repeatable read?

**Answer:**

A transaction reads the same row twice and gets different committed values because another transaction changed it
between the reads.

______________________________________________________________________

## Q89. Phantom read?

**Answer:**

A repeated range query observes a different set of rows because another transaction inserted or removed rows matching
the range.

______________________________________________________________________

## Q90. What is MVCC?

**Answer:**

Multi-Version Concurrency Control allows databases to manage concurrent reads and writes using multiple versions of
data.

The exact behavior depends on the database implementation and isolation level.

______________________________________________________________________

## Q91. Optimistic vs pessimistic locking?

**Answer:**

```text
Optimistic → assume conflicts are uncommon; detect conflicts when updating
Pessimistic → lock resources to prevent conflicting concurrent operations
```

______________________________________________________________________

# Part 12 — SQLAlchemy

## Q92. What is an SQLAlchemy Engine?

**Answer:**

The Engine is the central interface for database connectivity and manages access to the underlying DBAPI connections,
including pooling.

______________________________________________________________________

## Q93. What is a Session?

**Answer:**

A Session provides an ORM unit-of-work context for interacting with mapped objects and coordinating database operations.

______________________________________________________________________

## Q94. What is `flush()`?

**Answer:**

`flush()` synchronizes pending ORM changes with the database within the current transaction.

It does not by itself commit the transaction.

______________________________________________________________________

## Q95. `commit()` vs `flush()`?

**Answer:**

```text
flush  → send pending changes to database within transaction
commit → finalize transaction
```

A commit generally involves flushing pending changes first.

______________________________________________________________________

## Q96. What does rollback do?

**Answer:**

Rollback ends the current transaction and discards its uncommitted database changes.

ORM session state may also need appropriate handling after rollback.

______________________________________________________________________

## Q97. What is the identity map?

**Answer:**

The ORM identity map ensures that, within a Session, a database row represented by a particular identity is generally
associated with the corresponding in-memory object instance.

______________________________________________________________________

## Q98. What is the Unit of Work pattern?

**Answer:**

It tracks changes to objects and coordinates persistence of those changes as a unit, typically around a transaction.

______________________________________________________________________

## Q99. Lazy vs eager loading?

**Answer:**

```text
Lazy loading  → load related data when accessed
Eager loading → load related data as part of the planned query
```

Eager loading can help avoid excessive database round trips.

______________________________________________________________________

## Q100. What is the N+1 problem?

**Answer:**

A query loads N parent rows and then performs an additional query for each parent to load related data.

Instead of:

```text
1 + N queries
```

use an appropriate eager-loading strategy such as:

```text
joinedload
selectinload
```

when appropriate.

______________________________________________________________________

# Part 13 — Redis

## Q101. What is Redis?

**Answer:**

Redis is an in-memory data store commonly used for:

```text
Caching
Counters
Distributed coordination
Queues
Sessions
Rate limiting
```

depending on the workload and design.

______________________________________________________________________

## Q102. Redis data structures?

**Answer:**

Common structures include:

```text
Strings
Hashes
Lists
Sets
Sorted sets
Streams
```

______________________________________________________________________

## Q103. What is TTL?

**Answer:**

TTL means Time To Live.

It specifies how long a key should remain available before expiration.

______________________________________________________________________

## Q104. What is cache-aside?

**Answer:**

Typical flow:

```text
Application
 ↓
Check cache
 ↓
Hit → return
Miss
 ↓
Read database
 ↓
Populate cache
 ↓
Return
```

______________________________________________________________________

## Q105. What is cache invalidation?

**Answer:**

Removing or updating cached data when the underlying source of truth changes.

It is difficult because stale data and race conditions must be considered.

______________________________________________________________________

## Q106. What is a cache stampede?

**Answer:**

A large number of requests simultaneously miss or invalidate the same cache entry and overload the underlying system.

Possible mitigations include:

```text
Locking
Request coalescing
Jittered expiration
Prewarming
```

______________________________________________________________________

## Q107. What does `SET NX` do conceptually?

**Answer:**

It sets a key only if the key does not already exist.

It can be used as a building block for coordination or lock mechanisms, but robust distributed-lock design requires
careful handling of expiration, ownership and failure.

______________________________________________________________________

## Q108. RDB vs AOF?

**Answer:**

```text
RDB → periodic snapshots
AOF → append/log-style persistence of write operations
```

They provide different durability and recovery trade-offs.

______________________________________________________________________

## Q109. LRU vs LFU?

**Answer:**

```text
LRU → evict based on recent usage
LFU → evict based on frequency of usage
```

The appropriate strategy depends on workload characteristics.

______________________________________________________________________

# Part 14 — Kafka

## Q110. What is a Kafka broker?

**Answer:**

A broker is a Kafka server responsible for storing and serving partitions and participating in the Kafka cluster.

______________________________________________________________________

## Q111. What is a Kafka topic?

**Answer:**

A topic is a logical stream/category of records.

Topics are divided into partitions for scalability and parallelism.

______________________________________________________________________

## Q112. What is a partition?

**Answer:**

A partition is an ordered append-only log within a topic.

Kafka provides ordering within a partition, not automatically across all partitions of a topic.

______________________________________________________________________

## Q113. What is a consumer group?

**Answer:**

A consumer group allows multiple consumers to coordinate consumption of partitions.

Within a group, a partition is generally assigned to one consumer at a time.

______________________________________________________________________

## Q114. What is an offset?

**Answer:**

An offset identifies a record's position within a partition.

Consumers track offsets to manage their progress.

______________________________________________________________________

## Q115. What is consumer lag?

**Answer:**

Consumer lag represents how far a consumer/group is behind the latest available records.

It is an important operational signal.

______________________________________________________________________

## Q116. At-most-once vs at-least-once?

**Answer:**

```text
At-most-once  → message may be lost, but is not intentionally retried
At-least-once → message should not be lost but may be delivered more than once
```

Exactly-once behavior is more complex and depends on the entire processing design.

______________________________________________________________________

## Q117. How do you handle duplicate Kafka messages?

**Answer:**

Design consumers to be idempotent.

Possible mechanisms:

```text
Idempotency key
Unique database constraint
Processed-event record
Transactional state update
```

______________________________________________________________________

# Part 15 — RabbitMQ

## Q118. What is a RabbitMQ exchange?

**Answer:**

An exchange receives messages from producers and routes them to queues according to its type, bindings and routing
information.

______________________________________________________________________

## Q119. What is a queue?

**Answer:**

A queue stores messages until consumers process them.

______________________________________________________________________

## Q120. What is a binding?

**Answer:**

A binding connects an exchange to a queue and defines routing relationships.

______________________________________________________________________

## Q121. What is a routing key?

**Answer:**

A routing key is message metadata used by exchanges to determine how a message should be routed.

______________________________________________________________________

## Q122. What is ACK?

**Answer:**

An acknowledgment tells RabbitMQ that a consumer has successfully processed a message.

Without appropriate acknowledgment handling, failure can result in redelivery.

______________________________________________________________________

## Q123. What is prefetch?

**Answer:**

Prefetch limits how many unacknowledged messages can be delivered to a consumer, helping control concurrency and
resource usage.

______________________________________________________________________

## Q124. What is a dead-letter exchange?

**Answer:**

A dead-letter exchange can route messages that meet configured dead-letter conditions to another routing path for
inspection or later handling.

______________________________________________________________________

# Part 16 — Celery

## Q125. What is Celery?

**Answer:**

Celery is a distributed task queue framework commonly used to execute background tasks using workers and a broker.

______________________________________________________________________

## Q126. What is a Celery worker?

**Answer:**

A worker process executes Celery tasks received through the broker.

______________________________________________________________________

## Q127. What is Celery Beat?

**Answer:**

Celery Beat is a scheduler that triggers periodic tasks.

______________________________________________________________________

## Q128. What should you consider when retrying Celery tasks?

**Answer:**

Consider:

```text
Retryable vs permanent errors
Maximum retries
Backoff
Jitter
Timeouts
Idempotency
Dead-letter/failure handling
```

Blind retries can amplify an outage.

______________________________________________________________________

## Q129. Why does idempotency matter in Celery?

**Answer:**

Tasks may be retried or executed more than once depending on failure and acknowledgment behavior.

Idempotent tasks prevent duplicate side effects.

______________________________________________________________________

# Part 17 — Kafka vs RabbitMQ vs Celery

## Q130. Kafka vs RabbitMQ?

**Answer:**

A simplified distinction:

```text
Kafka
→ durable event streaming
→ partitions
→ high throughput
→ consumer groups
→ event retention

RabbitMQ
→ message broker
→ flexible routing
→ queues/exchanges
→ work distribution
```

Choose based on requirements rather than popularity.

______________________________________________________________________

## Q131. Kafka vs Celery?

**Answer:**

Kafka is primarily an event streaming platform.

Celery is a task execution framework.

They solve different problems, although both can participate in asynchronous architectures.

______________________________________________________________________

## Q132. RabbitMQ vs Celery?

**Answer:**

RabbitMQ is a broker.

Celery provides the distributed task execution abstraction and worker system, and RabbitMQ can be used as its broker.

______________________________________________________________________

# Part 18 — Docker

## Q133. Image vs container?

**Answer:**

An image is a packaged filesystem and metadata used as a template.

A container is a running instance created from an image.

______________________________________________________________________

## Q134. What are Docker layers?

**Answer:**

Docker images are built from layers.

Layer reuse can improve build performance and storage efficiency.

______________________________________________________________________

## Q135. Why use multi-stage builds?

**Answer:**

Multi-stage builds allow build-time dependencies and tooling to remain out of the final runtime image.

This can reduce image size and attack surface.

______________________________________________________________________

## Q136. Volume vs container filesystem?

**Answer:**

Container writable storage is tied to the container lifecycle.

Volumes provide persistent storage managed separately from the container lifecycle.

______________________________________________________________________

## Q137. What is Docker Compose?

**Answer:**

Docker Compose defines and runs multi-container applications.

For example:

```text
FastAPI
PostgreSQL
Redis
```

can be described as services in a Compose configuration.

______________________________________________________________________

## Q138. Why use health checks?

**Answer:**

Health checks help determine whether a service is functioning as expected rather than merely whether its process exists.

______________________________________________________________________

# Part 19 — Linux

## Q139. What is a process?

**Answer:**

A process is an executing program with its own process context and resources.

______________________________________________________________________

## Q140. Process vs thread?

**Answer:**

A process provides an isolated address space.

Threads within a process share the process's memory and resources.

______________________________________________________________________

## Q141. What is a signal?

**Answer:**

Signals provide a mechanism for sending asynchronous notifications to processes.

Examples:

```text
SIGTERM
SIGKILL
SIGHUP
SIGINT
```

______________________________________________________________________

## Q142. SIGTERM vs SIGKILL?

**Answer:**

```text
SIGTERM → asks the process to terminate and allows cleanup
SIGKILL → forcefully terminates the process
```

Applications should generally be given the opportunity to handle graceful shutdown first.

______________________________________________________________________

## Q143. What are pipes?

**Answer:**

Pipes connect the output of one command to the input of another.

```bash
command1 | command2
```

______________________________________________________________________

## Q144. What is SSH?

**Answer:**

SSH provides secure remote access and secure communication channels over a network.

______________________________________________________________________

## Q145. How would you investigate high CPU usage?

**Answer:**

Start with:

```text
Identify process
→ inspect CPU usage
→ inspect threads if relevant
→ inspect application metrics
→ inspect logs
→ identify workload
→ profile if necessary
```

______________________________________________________________________

## Q146. How would you investigate memory growth?

**Answer:**

Check:

```text
Process memory
Container limits
Application metrics
Heap/object behavior
Logs
Recent deployments
```

Then profile or inspect allocations to identify the source.

______________________________________________________________________

# Part 20 — Security

## Q147. What is SQL injection?

**Answer:**

SQL injection occurs when untrusted input is incorporated into SQL in an unsafe way, allowing unintended query
manipulation.

Use parameterized queries and safe database APIs.

______________________________________________________________________

## Q148. What is XSS?

**Answer:**

Cross-site scripting occurs when attacker-controlled content is executed as script in a user's browser.

Defenses include appropriate output encoding, safe templating and security controls.

______________________________________________________________________

## Q149. What is CSRF?

**Answer:**

Cross-site request forgery tricks an authenticated browser into making an unwanted request to a site where the user is
already authenticated.

Appropriate defenses depend on the authentication mechanism and application architecture.

______________________________________________________________________

## Q150. Authentication vs authorization?

**Answer:**

```text
Authentication → Who are you?
Authorization  → What are you allowed to do?
```

______________________________________________________________________

## Q151. What is SSRF?

**Answer:**

Server-Side Request Forgery occurs when an attacker can influence a server into making unintended requests to internal
or other protected resources.

Controls include strict destination validation and network-level restrictions.

______________________________________________________________________

## Q152. What is path traversal?

**Answer:**

Path traversal attempts to access files outside the intended directory, often using path components such as:

```text
../
```

Applications should validate and safely resolve user-controlled paths.

______________________________________________________________________

## Q153. What is least privilege?

**Answer:**

Give users, services and processes only the permissions required to perform their responsibilities.

______________________________________________________________________

## Q154. Why is rate limiting important?

**Answer:**

Rate limiting controls request volume and can protect systems from:

```text
Abuse
Brute force
Resource exhaustion
Traffic spikes
```

______________________________________________________________________

# Part 21 — Git

## Q155. Merge vs rebase?

**Answer:**

```text
merge  → combines histories and preserves branch structure
rebase → rewrites commits onto another base
```

Rebase can create a cleaner linear history but should be used carefully on shared branches.

______________________________________________________________________

## Q156. Reset vs revert?

**Answer:**

```text
reset  → moves branch/HEAD and can rewrite local history
revert → creates a new commit that reverses an earlier change
```

Revert is generally safer for already-shared history.

______________________________________________________________________

## Q157. What is `git stash`?

**Answer:**

It temporarily stores uncommitted changes so you can switch context without committing incomplete work.

______________________________________________________________________

## Q158. What is cherry-pick?

**Answer:**

`git cherry-pick` applies the changes introduced by selected commits onto the current branch.

______________________________________________________________________

## Q159. What is reflog?

**Answer:**

Reflog records updates to references such as HEAD, helping recover commits or branch positions that may no longer be
reachable through normal branch history.

______________________________________________________________________

## Q160. What is `git bisect`?

**Answer:**

`git bisect` performs a binary search through commits to identify which commit introduced a bug.

______________________________________________________________________

## Q161. What makes a good pull request?

**Answer:**

A good PR should be:

```text
Focused
Understandable
Tested
Reviewable
Clearly described
```

Explain:

```text
What changed
Why
How it was tested
Any risks
```

______________________________________________________________________

# Part 22 — DSA

## Q162. What is Big-O?

**Answer:**

Big-O describes how resource usage grows as input size increases, typically focusing on an asymptotic upper bound.

______________________________________________________________________

## Q163. Common complexity examples?

**Answer:**

```text
O(1)      → constant
O(log n)  → logarithmic
O(n)      → linear
O(n log n)
O(n²)     → quadratic
```

______________________________________________________________________

## Q164. When would you use a hash map?

**Answer:**

Use a hash map when you need efficient average-case key-based lookup, insertion or membership.

______________________________________________________________________

## Q165. BFS vs DFS?

**Answer:**

```text
BFS → explores level by level, commonly uses a queue
DFS → explores deeply, commonly uses recursion or a stack
```

BFS is useful for shortest paths in unweighted graphs.

______________________________________________________________________

## Q166. What is the sliding-window pattern?

**Answer:**

It maintains a moving range over a sequence to avoid repeatedly processing overlapping portions.

Common uses:

```text
Longest substring
Maximum/minimum window
Fixed-size window
```

______________________________________________________________________

## Q167. What is two pointers?

**Answer:**

Two pointers maintain two positions while scanning a sequence.

Common uses:

```text
Sorted arrays
Pair problems
Palindrome checks
Partitioning
Sliding-window variants
```

______________________________________________________________________

## Q168. What is Top-K?

**Answer:**

Top-K problems require finding the largest/smallest K elements efficiently.

Common tools include:

```text
Heap
Sorting
Counting
Quickselect
```

depending on the problem.

______________________________________________________________________

## Q169. What is prefix/suffix technique?

**Answer:**

Precompute information from the left or right side of an array/string so repeated range calculations become efficient.

______________________________________________________________________

## Q170. What is basic dynamic programming?

**Answer:**

Dynamic programming solves problems by breaking them into overlapping subproblems and storing results to avoid repeated
computation.

______________________________________________________________________

# Part 23 — System Design

## Q171. What should you do first in a system-design interview?

**Answer:**

Clarify requirements.

Separate:

```text
Functional requirements
Non-functional requirements
```

Then estimate scale and identify important constraints.

______________________________________________________________________

## Q172. What are non-functional requirements?

**Answer:**

Examples:

```text
Availability
Reliability
Latency
Throughput
Scalability
Security
Durability
```

______________________________________________________________________

## Q173. What is capacity estimation?

**Answer:**

Estimate:

```text
Users
Requests/sec
Storage
Bandwidth
Read/write ratio
Peak traffic
```

It helps determine architectural requirements.

______________________________________________________________________

## Q174. Why keep services stateless?

**Answer:**

Stateless services can be more easily scaled horizontally because requests can be routed to any healthy instance.

State can be stored in shared systems such as:

```text
Database
Cache
Object storage
```

______________________________________________________________________

## Q175. What does a load balancer do?

**Answer:**

It distributes traffic across backend instances and can perform health checks and routing depending on the
implementation.

______________________________________________________________________

## Q176. What is a reverse proxy?

**Answer:**

A reverse proxy sits in front of backend servers and can provide:

```text
Routing
TLS termination
Load balancing
Caching
Compression
Security controls
```

______________________________________________________________________

## Q177. What is a CDN?

**Answer:**

A Content Delivery Network distributes cached content closer to users to reduce latency and origin load.

______________________________________________________________________

## Q178. What is an API gateway?

**Answer:**

An API gateway can provide a centralized entry point for APIs and perform functions such as:

```text
Routing
Authentication
Rate limiting
Request transformation
Observability
```

______________________________________________________________________

## Q179. What is a circuit breaker?

**Answer:**

A circuit breaker prevents repeated calls to an unhealthy dependency after failures cross a threshold.

Conceptually:

```text
Closed
 ↓ failures
Open
 ↓ recovery period
Half-open
 ↓ test
Closed / Open
```

______________________________________________________________________

## Q180. What is idempotency in distributed systems?

**Answer:**

Idempotency allows repeated requests or messages to produce the same intended business outcome as a single successful
operation.

It is particularly important when retries are possible.

______________________________________________________________________

## Q181. What is CAP?

**Answer:**

CAP describes a trade-off in distributed systems involving:

```text
Consistency
Availability
Partition tolerance
```

When a network partition occurs, a distributed system must make a trade-off between consistency and availability.

______________________________________________________________________

## Q182. What is a read replica?

**Answer:**

A read replica maintains replicated database data and can serve suitable read workloads, reducing load on the primary.

Replication lag must be considered.

______________________________________________________________________

## Q183. What is sharding?

**Answer:**

Sharding distributes data across multiple database nodes according to a partitioning/sharding key.

It can improve scale but introduces significant operational and query complexity.

______________________________________________________________________

## Q184. What is a message queue useful for?

**Answer:**

Queues can provide:

```text
Asynchronous processing
Load smoothing
Decoupling
Retry handling
Independent worker scaling
```

______________________________________________________________________

## Q185. What is an outbox pattern?

**Answer:**

The outbox pattern stores a database change and the event representing that change in the same local transaction.

A separate process then publishes the stored event.

This helps avoid the dual-write problem.

______________________________________________________________________

# Part 24 — Rapid Scenario Questions

## Q186. API suddenly returns 500s. What do you check?

**Answer:**

```text
Error rate
Logs
Recent deployments
Dependency health
Database
Cache
Resource usage
Configuration
```

Start by determining the failure boundary and customer impact.

______________________________________________________________________

## Q187. API latency suddenly increases. What do you check?

**Answer:**

```text
p50/p95/p99
Database latency
External API latency
CPU
Memory
Connection pools
Cache hit rate
Recent changes
Traffic volume
```

______________________________________________________________________

## Q188. Database connection pool is exhausted. What could cause it?

**Answer:**

Possible causes:

```text
Long-running queries
Too many concurrent requests
Connection leaks
Transactions held too long
Pool configured too small
Database unavailable/slow
```

Investigate metrics and connection behavior before changing pool size blindly.

______________________________________________________________________

## Q189. Redis goes down. What happens?

**Answer:**

It depends on whether Redis is:

```text
Optional cache
```

or:

```text
Required application state
```

For a cache, the application may fall back to the database, but increased database load can become a secondary failure.

______________________________________________________________________

## Q190. Kafka consumer lag is increasing. What do you check?

**Answer:**

```text
Consumer processing time
Consumer errors
Consumer count
Partition count
CPU/memory
Downstream dependency latency
Rebalancing
Traffic increase
```

______________________________________________________________________

## Q191. Messages are duplicated. What do you do?

**Answer:**

First establish why duplicates occur.

Then make the consumer/business operation idempotent using mechanisms such as:

```text
Unique constraints
Idempotency keys
Processed-event tracking
Transactional updates
```

______________________________________________________________________

## Q192. Container keeps restarting. What do you check?

**Answer:**

```text
Container logs
Exit code
Health checks
Memory limits
CPU limits
Startup failures
Environment variables
Dependency connectivity
Recent image changes
```

______________________________________________________________________

## Q193. CPU is at 100%. What do you do?

**Answer:**

```text
Identify process
→ identify workload
→ inspect threads
→ inspect recent changes
→ profile if needed
→ mitigate
→ fix root cause
```

______________________________________________________________________

## Q194. Disk is full. What do you check?

**Answer:**

```text
df
du
Logs
Container layers
Temporary files
Core dumps
Database files
Application-generated files
```

Do not delete files blindly.

______________________________________________________________________

## Q195. An external API is timing out. What should you consider?

**Answer:**

```text
Timeout
Retry policy
Backoff
Circuit breaker
Fallback
Idempotency
Connection limits
Observability
```

Retries should be bounded and used only when appropriate.

______________________________________________________________________

# Part 25 — Last-Minute Rapid Review

Before an interview, make sure you can answer these without notes:

```text
1. What is the GIL?
2. List vs tuple?
3. Shallow vs deep copy?
4. Iterator vs generator?
5. Decorator?
6. Context manager?
7. MRO?
8. super()?
9. Composition vs inheritance?
10. Descriptor?
11. __slots__?
12. Thread vs process?
13. CPU-bound vs I/O-bound?
14. Race condition?
15. Deadlock?
16. Event loop?
17. Coroutine?
18. await?
19. gather?
20. Blocking code in async?
21. FastAPI dependency injection?
22. Middleware?
23. Pydantic?
24. ASGI?
25. HTTP lifecycle?
26. TCP handshake?
27. TLS?
28. HTTP idempotency?
29. JOIN?
30. WHERE vs HAVING?
31. CTE?
32. Window function?
33. EXISTS vs IN?
34. Normalization?
35. 1NF / 2NF / 3NF?
36. Denormalization?
37. Index?
38. Composite index?
39. EXPLAIN?
40. ACID?
41. Isolation levels?
42. MVCC?
43. Optimistic vs pessimistic locking?
44. SQLAlchemy Session?
45. flush vs commit?
46. Identity map?
47. N+1?
48. Redis TTL?
49. Cache-aside?
50. Cache stampede?
51. Kafka partition?
52. Consumer group?
53. Offset?
54. Consumer lag?
55. At-least-once?
56. RabbitMQ exchange?
57. ACK?
58. Prefetch?
59. Celery worker?
60. Celery Beat?
61. Docker image vs container?
62. Multi-stage build?
63. Linux process vs thread?
64. SIGTERM vs SIGKILL?
65. SQL injection?
66. Authentication vs authorization?
67. SSRF?
68. Least privilege?
69. Git merge vs rebase?
70. Reset vs revert?
71. Reflog?
72. Big-O?
73. BFS vs DFS?
74. Sliding window?
75. Two pointers?
76. Load balancer?
77. Reverse proxy?
78. CDN?
79. Circuit breaker?
80. CAP?
81. Read replica?
82. Sharding?
83. Outbox?
84. Idempotency?
85. How would you debug a production outage?
```

______________________________________________________________________

# 26. Final Rapid-Fire Strategy

Do not try to give a ten-minute answer to every question.

For short questions:

```text
Definition
→ One example
→ One important caveat
```

For architecture questions:

```text
Requirement
→ Decision
→ Trade-off
```

For debugging questions:

```text
Symptom
→ Evidence
→ Hypothesis
→ Verification
→ Fix
```

For production questions:

```text
Impact
→ Mitigation
→ Root cause
→ Prevention
```

For behavioral questions:

```text
Situation
→ Task
→ Action
→ Result
→ Learning
```

______________________________________________________________________

# 27. Final Takeaways

This file is a **revision bank**, not a replacement for the detailed topic files.

Use it in three passes.

### Pass 1 — Recognition

Read the questions and identify areas you cannot answer immediately.

### Pass 2 — Recall

Answer each question without looking at the answer.

### Pass 3 — Deep Dive

Return to the corresponding topic file for anything you cannot explain confidently.

A strong final revision loop is:

```text
Rapid-fire question
       ↓
Answer from memory
       ↓
Identify weak area
       ↓
Review detailed topic
       ↓
Answer again
```

For senior backend interviews, prioritize understanding over memorization.

You should be able to explain not only:

```text
"What is it?"
```

but also:

```text
"Why would I use it?"
"What problem does it solve?"
"What can go wrong?"
"What are the trade-offs?"
"How would I debug it?"
```

That is the level expected when discussing real backend systems.

> **Know the definition. Know the example. Know the trade-off. Know the failure mode.**

______________________________________________________________________

**Previous:** [46. AI-Assisted Software Engineering](./46-ai-assisted-development.md)

**Next:** [48. Technical Mock Interview & Final Revision](./48-technical-mock-interview-final-revision.md)
