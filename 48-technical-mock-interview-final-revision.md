# 48. Technical Mock Interview & Final Revision

**Previous:** [47. Rapid-Fire Python Backend Q&A](./47-rapid-fire-python-backend.md)

**Next:** End of the interview preparation plan

______________________________________________________________________

## Objective

This is the **final interview simulation and revision file**.

Unlike the rapid-fire revision bank, this file is designed to make you practice the way a real senior backend interview
progresses:

```text
Question
   ↓
Your answer
   ↓
Follow-up
   ↓
Deeper technical discussion
   ↓
Trade-off
   ↓
Failure scenario
   ↓
Production / system-design connection
```

Do not read the answers first.

Use the questions as a mock interview.

For each section:

1. Answer aloud.
1. Keep the first answer concise.
1. Expand only when challenged.
1. Explain your reasoning.
1. Mention trade-offs.
1. Use real project examples where appropriate.

______________________________________________________________________

# Part 1 — Mock Interview Rules

## 1. Answer Structure

For a definition question:

```text
Definition
→ Example
→ Important caveat
```

For a design question:

```text
Requirements
→ Design
→ Components
→ Data flow
→ Scaling
→ Failure handling
→ Trade-offs
```

For a debugging question:

```text
Symptom
→ Evidence
→ Hypotheses
→ Investigation
→ Root cause
→ Mitigation
→ Prevention
```

For a project question:

```text
Problem
→ Architecture
→ Your contribution
→ Decision
→ Trade-off
→ Result
```

______________________________________________________________________

## 2. Do Not Over-Answer

A common interview mistake is giving a five-minute answer to a thirty-second question.

Start concise.

Example:

> "What is a Python generator?"

Start with:

```text
A generator produces values lazily, commonly using yield, so the
entire result does not need to be held in memory at once.
```

Then stop.

Let the interviewer decide whether to go deeper.

______________________________________________________________________

# Part 2 — Python Mock Interview

## Question 1 — Mutable Defaults

What happens here?

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

What problem can this create?

### Expected discussion

The default list is created once when the function is defined rather than once per call.

A safer pattern:

```python
def add_item(item, items=None):
    if items is None:
        items = []

    items.append(item)
    return items
```

### Follow-up

Why is the default object reused?

______________________________________________________________________

## Question 2 — `is` vs `==`

Explain:

```python
a == b
a is b
```

### Follow-up

Why should identity comparisons generally use:

```python
x is None
```

rather than:

```python
x == None
```

______________________________________________________________________

## Question 3 — Shallow vs Deep Copy

Explain the difference.

### Follow-up

What happens when the object contains nested mutable objects?

______________________________________________________________________

## Question 4 — Decorators

Explain decorators.

### Follow-up

Why is `functools.wraps` useful?

______________________________________________________________________

## Question 5 — Context Managers

Explain:

```python
with resource:
    ...
```

### Follow-up

What happens if an exception occurs inside the block?

______________________________________________________________________

## Question 6 — Iterator vs Iterable

Explain the difference.

### Follow-up

What happens when Python executes:

```python
for item in collection:
    ...
```

______________________________________________________________________

## Question 7 — Generator

Why would you use a generator?

### Follow-up

When might a generator not be the best choice?

______________________________________________________________________

## Question 8 — Dictionary

How does a dictionary provide efficient lookup?

### Follow-up

What requirements must dictionary keys satisfy?

______________________________________________________________________

## Question 9 — `__new__` vs `__init__`

Explain the difference.

### Follow-up

Why is `__new__` particularly relevant to immutable objects?

______________________________________________________________________

## Question 10 — `__slots__`

Why would you use `__slots__`?

### Follow-up

What behavior changes when using it?

______________________________________________________________________

# Part 3 — Advanced OOP Mock Interview

## Question 11 — Multiple Inheritance

When would you use multiple inheritance?

### Follow-up

What problems can it introduce?

______________________________________________________________________

## Question 12 — MRO

Explain Method Resolution Order.

### Follow-up

How does Python determine the method to call in a diamond inheritance structure?

______________________________________________________________________

## Question 13 — `super()`

What does `super()` actually mean in Python?

### Follow-up

Why is it important in cooperative multiple inheritance?

______________________________________________________________________

## Question 14 — Mixins

What is a mixin?

### Follow-up

What makes a good mixin?

______________________________________________________________________

## Question 15 — Descriptor

What is a descriptor?

### Follow-up

Where do you encounter descriptor behavior in Python?

______________________________________________________________________

## Question 16 — Abstract Base Class vs Protocol

Compare:

```text
ABC
Protocol
```

### Follow-up

When would structural typing be useful?

______________________________________________________________________

# Part 4 — Concurrency & AsyncIO Mock Interview

## Question 17 — Thread vs Process

When would you choose a thread over a process?

### Follow-up

How does the GIL affect the decision?

______________________________________________________________________

## Question 18 — CPU-Bound vs I/O-Bound

Give examples of each.

### Follow-up

Why is async usually more useful for I/O-bound workloads?

______________________________________________________________________

## Question 19 — Race Condition

What is a race condition?

### Follow-up

How would you reproduce and diagnose one?

______________________________________________________________________

## Question 20 — Deadlock

What causes a deadlock?

### Follow-up

How can lock ordering help prevent it?

______________________________________________________________________

## Question 21 — Async Event Loop

Explain the event loop to a backend engineer.

### Follow-up

What happens if an async endpoint executes blocking code?

______________________________________________________________________

## Question 22 — `await`

What happens when a coroutine reaches:

```python
await operation()
```

### Follow-up

Does `await` automatically create a new thread?

______________________________________________________________________

## Question 23 — `gather`

When would you use:

```python
await asyncio.gather(...)
```

### Follow-up

When should operations be executed sequentially instead?

______________________________________________________________________

## Question 24 — Cancellation

Why is cancellation important in an async service?

### Follow-up

What resources need cleanup when a task is cancelled?

______________________________________________________________________

## Question 25 — Timeouts

Why should external calls have timeouts?

### Follow-up

What happens to your service if an external dependency hangs indefinitely?

______________________________________________________________________

# Part 5 — FastAPI Mock Interview

## Question 26 — FastAPI Architecture

Describe the architecture of a typical FastAPI service.

A strong answer might cover:

```text
ASGI server
→ FastAPI
→ Router
→ Dependencies
→ Service layer
→ Repository / ORM
→ Database
```

### Follow-up

Where should business logic live?

______________________________________________________________________

## Question 27 — Dependency Injection

Why use FastAPI dependency injection?

### Follow-up

How would you override a dependency in tests?

______________________________________________________________________

## Question 28 — Middleware

What is middleware?

### Follow-up

When would you use middleware instead of a dependency?

______________________________________________________________________

## Question 29 — Validation

How does FastAPI validate request data?

### Follow-up

What role does Pydantic play?

______________________________________________________________________

## Question 30 — Async Endpoint

When should a FastAPI endpoint be `async def`?

### Follow-up

What happens if it calls a blocking library?

______________________________________________________________________

## Question 31 — Error Handling

How would you design consistent API error handling?

### Follow-up

How should internal exceptions differ from client-facing errors?

______________________________________________________________________

## Question 32 — Authentication

How would you implement authentication in FastAPI?

Discuss:

```text
Token extraction
→ Token validation
→ User identity
→ Authorization
```

### Follow-up

Authentication vs authorization?

______________________________________________________________________

# Part 6 — HTTP & Networking Mock Interview

## Question 33 — URL Request Lifecycle

What happens when a client calls:

```text
https://api.example.com/orders
```

### Expected discussion

```text
DNS
→ TCP
→ TLS
→ HTTP
→ CDN/WAF if present
→ Load balancer
→ Reverse proxy
→ Application
```

### Follow-up

Where can latency be introduced?

______________________________________________________________________

## Question 34 — TCP Handshake

Explain:

```text
SYN
SYN-ACK
ACK
```

### Follow-up

Why does TCP need connection establishment?

______________________________________________________________________

## Question 35 — TLS

What does TLS provide?

### Follow-up

Where is TLS usually terminated in a production architecture?

______________________________________________________________________

## Question 36 — HTTP Status Codes

When would you use:

```text
400
401
403
404
409
422
429
500
502
503
504
```

______________________________________________________________________

## Question 37 — Idempotency

What does idempotency mean for an API?

### Follow-up

How would you make a payment endpoint safe against client retries?

______________________________________________________________________

# Part 7 — SQL Mock Interview

## Question 38 — JOIN

Explain the difference between:

```text
INNER JOIN
LEFT JOIN
```

### Follow-up

What happens when the right-side row does not exist?

______________________________________________________________________

## Question 39 — `WHERE` vs `HAVING`

Explain the difference.

### Follow-up

Can you use aggregate functions in `WHERE`?

______________________________________________________________________

## Question 40 — CTE

What is a CTE?

### Follow-up

When would a CTE improve query readability?

______________________________________________________________________

## Question 41 — Window Functions

Explain:

```text
ROW_NUMBER
RANK
DENSE_RANK
LAG
LEAD
```

### Follow-up

How would you find the second-highest salary per department?

______________________________________________________________________

## Question 42 — `EXISTS` vs `IN`

When might you use `EXISTS`?

### Follow-up

Would you claim one is always faster?

Correct reasoning:

> No. Query shape, data distribution and the database optimizer matter. Inspect the execution plan.

______________________________________________________________________

# Part 8 — Database Design & Normalization Mock Interview

## Question 43 — Why Normalize?

What problems does normalization solve?

Discuss:

```text
Redundancy
Insert anomaly
Update anomaly
Delete anomaly
```

______________________________________________________________________

## Question 44 — 1NF / 2NF / 3NF

Explain each normal form at a practical level.

### Follow-up

Why is 3NF often a useful design target?

______________________________________________________________________

## Question 45 — Functional Dependency

What is a functional dependency?

Example:

```text
student_id → student_name
```

means the student ID determines the student's name.

### Follow-up

How does this relate to normalization?

______________________________________________________________________

## Question 46 — Candidate Key

What is a candidate key?

### Follow-up

How is it different from the selected primary key?

______________________________________________________________________

## Question 47 — Normalization vs Denormalization

When would you intentionally denormalize?

### Follow-up

What problems does denormalization introduce?

______________________________________________________________________

# Part 9 — SQL Index & Performance Mock Interview

## Question 48 — Why an Index?

A query is slow.

Why might adding an index help?

### Follow-up

Why can adding too many indexes hurt?

______________________________________________________________________

## Question 49 — Composite Index

Given:

```sql
WHERE customer_id = ?
AND status = ?
```

what would you consider?

### Follow-up

Why does column ordering matter?

______________________________________________________________________

## Question 50 — Query Plan

How would you investigate a slow SQL query?

### Expected flow

```text
Identify query
→ EXPLAIN / EXPLAIN ANALYZE where appropriate
→ inspect scan/join strategy
→ inspect row estimates
→ inspect indexes
→ optimize
→ benchmark
```

______________________________________________________________________

# Part 10 — Transactions & Concurrency Mock Interview

## Question 51 — ACID

Explain all four properties.

______________________________________________________________________

## Question 52 — Isolation Levels

Why do databases provide isolation levels?

### Follow-up

Explain:

```text
Dirty read
Non-repeatable read
Phantom read
```

______________________________________________________________________

## Question 53 — MVCC

What problem does MVCC solve?

### Follow-up

How can MVCC reduce read/write blocking?

______________________________________________________________________

## Question 54 — Optimistic vs Pessimistic Locking

When would you choose each?

______________________________________________________________________

## Question 55 — Deadlock

Two transactions deadlock.

What should the application do?

### Strong answer

```text
Detect failure
→ rollback
→ retry when appropriate
→ keep transactions short
→ use consistent lock ordering
```

Retries must be bounded and the operation should be safe to repeat.

______________________________________________________________________

# Part 11 — SQLAlchemy Mock Interview

## Question 56 — Session Lifecycle

Explain the SQLAlchemy Session lifecycle.

### Follow-up

Who owns the Session in a web request?

______________________________________________________________________

## Question 57 — Flush vs Commit

What is the difference?

### Follow-up

Can database-generated values become available after `flush()` but before `commit()`?

______________________________________________________________________

## Question 58 — Rollback

What does rollback do?

### Follow-up

What should happen to the Session after a failed transaction?

______________________________________________________________________

## Question 59 — Identity Map

What is SQLAlchemy's identity map?

### Follow-up

Why can repeated queries for the same identity produce the same ORM instance within a Session?

______________________________________________________________________

## Question 60 — N+1

Explain the N+1 problem.

### Follow-up

Compare:

```text
joinedload
selectinload
```

______________________________________________________________________

## Question 61 — Async SQLAlchemy

What changes when using async SQLAlchemy?

Discuss:

```text
AsyncEngine
AsyncSession
await
Async-compatible database driver
```

### Follow-up

Can blocking database operations run safely on the event loop?

______________________________________________________________________

# Part 12 — Redis Mock Interview

## Question 62 — Why Redis?

Give three backend use cases.

______________________________________________________________________

## Question 63 — Cache-Aside

Explain the cache-aside pattern.

### Follow-up

What happens during a cache miss?

______________________________________________________________________

## Question 64 — Cache Stampede

What causes a cache stampede?

### Follow-up

How can you mitigate it?

______________________________________________________________________

## Question 65 — Redis Failure

Redis is unavailable.

What happens to the application?

### Important discussion

It depends on whether Redis is:

```text
Optional cache
```

or:

```text
Required state
```

For a cache, fallback may be possible but can overload the database.

______________________________________________________________________

## Question 66 — Distributed Lock

How can Redis participate in distributed locking?

### Follow-up

Why is:

```text
SET key value NX EX ...
```

more appropriate than a simple:

```text
GET
SET
```

sequence?

______________________________________________________________________

## Question 67 — Persistence

Compare:

```text
RDB
AOF
```

### Follow-up

What durability/recovery trade-offs exist?

______________________________________________________________________

# Part 13 — Kafka Mock Interview

## Question 68 — Topic vs Partition

Explain the relationship.

______________________________________________________________________

## Question 69 — Ordering

Does Kafka guarantee global ordering?

### Correct direction

Ordering is guaranteed within a partition, not automatically across the entire topic.

______________________________________________________________________

## Question 70 — Consumer Groups

Why use consumer groups?

### Follow-up

What happens when there are more consumers than partitions?

______________________________________________________________________

## Question 71 — Consumer Lag

What causes consumer lag?

### Follow-up

How would you diagnose it?

______________________________________________________________________

## Question 72 — Delivery Semantics

Explain:

```text
At-most-once
At-least-once
Exactly-once
```

### Follow-up

Why is exactly-once difficult in an end-to-end business workflow?

______________________________________________________________________

## Question 73 — Duplicate Events

A consumer processes the same event twice.

How do you protect the business operation?

### Strong direction

```text
Idempotency
+
Database constraints / processed-event tracking
```

______________________________________________________________________

# Part 14 — RabbitMQ & Celery Mock Interview

## Question 74 — RabbitMQ Exchange

What does an exchange do?

### Follow-up

Explain:

```text
Exchange
→ Binding
→ Queue
→ Consumer
```

______________________________________________________________________

## Question 75 — ACK

Why are acknowledgments important?

### Follow-up

What can happen when a consumer crashes before acknowledging a message?

______________________________________________________________________

## Question 76 — Prefetch

What does prefetch control?

### Follow-up

Why can unlimited message delivery be dangerous?

______________________________________________________________________

## Question 77 — Celery

What are the major components of Celery?

```text
Producer
Broker
Worker
Task
Result backend
Beat
```

______________________________________________________________________

## Question 78 — Celery Retry

When should a task be retried?

### Follow-up

Why do retries require idempotency and backoff?

______________________________________________________________________

# Part 15 — Docker Mock Interview

## Question 79 — Image vs Container

Explain the difference.

______________________________________________________________________

## Question 80 — Multi-Stage Build

Why use it?

______________________________________________________________________

## Question 81 — Container Restart

A production container keeps restarting.

What do you inspect?

```text
Logs
→ exit code
→ health check
→ memory
→ CPU
→ configuration
→ startup dependencies
→ recent image changes
```

______________________________________________________________________

## Question 82 — Docker Compose

Design a local backend stack containing:

```text
FastAPI
PostgreSQL
Redis
```

What configuration would you need?

______________________________________________________________________

# Part 16 — Linux Mock Interview

## Question 83 — High CPU

A Linux server has 100% CPU usage.

What do you do?

______________________________________________________________________

## Question 84 — Memory Growth

A process keeps consuming memory.

How do you investigate?

______________________________________________________________________

## Question 85 — Disk Full

Production disk reaches 100%.

What do you inspect?

______________________________________________________________________

## Question 86 — SIGTERM

Why is SIGTERM preferable to immediately using SIGKILL for application shutdown?

______________________________________________________________________

## Question 87 — Logs

How would you investigate an application using Linux logs?

Think about:

```text
systemd
journalctl
application logs
process state
recent deployment
```

______________________________________________________________________

# Part 17 — Security Mock Interview

## Question 88 — SQL Injection

How do you prevent SQL injection?

______________________________________________________________________

## Question 89 — Authentication vs Authorization

Explain the difference.

______________________________________________________________________

## Question 90 — JWT

What problem does a JWT solve?

### Follow-up

What are important JWT considerations?

```text
Signing
Expiration
Validation
Key management
Revocation strategy
Payload sensitivity
```

______________________________________________________________________

## Question 91 — SSRF

Explain SSRF.

### Follow-up

Why is SSRF particularly dangerous in cloud/backend environments?

______________________________________________________________________

## Question 92 — File Upload Security

What should a backend consider before accepting uploaded files?

Discuss:

```text
File type validation
Size limits
Filename/path safety
Storage location
Content inspection where appropriate
Authorization
Malware/security controls
```

______________________________________________________________________

## Question 93 — Secrets

Where should production secrets live?

### Strong direction

Use an appropriate secret-management mechanism rather than hard-coding secrets into source code or container images.

______________________________________________________________________

# Part 18 — Git Mock Interview

## Question 94 — Merge vs Rebase

Explain the difference.

______________________________________________________________________

## Question 95 — Reset vs Revert

When would you use each?

______________________________________________________________________

## Question 96 — Reflog

You accidentally moved a branch and lost track of a commit.

What Git feature might help?

______________________________________________________________________

## Question 97 — Bisect

How can `git bisect` help find a regression?

______________________________________________________________________

## Question 98 — Code Review

What do you look for when reviewing a backend PR?

Discuss:

```text
Correctness
Security
Performance
Concurrency
Error handling
Tests
Maintainability
Observability
```

______________________________________________________________________

# Part 19 — DSA Coding Round

For each problem:

```text
1. Clarify
2. Explain brute force
3. Explain optimal approach
4. Write code
5. Test manually
6. Discuss complexity
7. Discuss edge cases
```

______________________________________________________________________

## Problem 1 — Two Sum

Given an array and target, return indices of two numbers that add to the target.

### Expected pattern

```text
Hash map
```

Typical complexity:

```text
Time: O(n)
Space: O(n)
```

______________________________________________________________________

## Problem 2 — Contains Duplicate

Determine whether an array contains duplicate values.

### Expected pattern

```text
Set
```

______________________________________________________________________

## Problem 3 — Group Anagrams

Group strings that are anagrams.

Possible approaches:

```text
Sorted-character key
Character-frequency key
```

______________________________________________________________________

## Problem 4 — Top K Frequent Elements

Find the K most frequent elements.

Possible tools:

```text
Counter
Heap
Bucket-based approach
```

______________________________________________________________________

## Problem 5 — Longest Consecutive Sequence

Expected key idea:

```text
Set
+
start-of-sequence detection
```

______________________________________________________________________

## Problem 6 — Valid Palindrome

Use:

```text
Two pointers
```

______________________________________________________________________

## Problem 7 — Container With Most Water

Expected pattern:

```text
Two pointers
```

______________________________________________________________________

## Problem 8 — Longest Substring Without Repeating Characters

Expected pattern:

```text
Sliding window
+
Set / map
```

______________________________________________________________________

## Problem 9 — Valid Parentheses

Expected pattern:

```text
Stack
```

______________________________________________________________________

## Problem 10 — Daily Temperatures

Expected pattern:

```text
Monotonic stack
```

______________________________________________________________________

## Problem 11 — Reverse Linked List

Expected pattern:

```text
prev
current
next
```

______________________________________________________________________

## Problem 12 — Linked List Cycle

Expected pattern:

```text
Fast and slow pointers
```

______________________________________________________________________

## Problem 13 — Merge Two Sorted Lists

Use two pointers and build the merged list.

______________________________________________________________________

## Problem 14 — Binary Search

Know:

```text
left
right
mid
```

and clearly define the search interval.

______________________________________________________________________

## Problem 15 — Number of Islands

Expected pattern:

```text
DFS / BFS
```

______________________________________________________________________

## Problem 16 — Climbing Stairs

Expected pattern:

```text
Dynamic programming
```

______________________________________________________________________

## Problem 17 — House Robber

Expected pattern:

```text
Dynamic programming
```

______________________________________________________________________

## Problem 18 — Jump Game

Think about whether the reachable range can be maintained greedily.

______________________________________________________________________

# Part 20 — System Design Round

## Design 1 — URL Shortener

### Requirements

Clarify:

```text
Create short URL
Redirect short URL
Expiration?
Custom aliases?
Analytics?
Scale?
```

### Discuss

```text
API
Database
ID generation
Cache
Read/write ratio
Collision handling
Scaling
Availability
```

### Follow-up

What happens if the same short code is requested concurrently?

______________________________________________________________________

# Design 2 — Notification Service

### Requirements

```text
Email?
SMS?
Push?
Scheduling?
Retries?
Templates?
User preferences?
```

### Architecture

Possible:

```text
API
 ↓
Database
 ↓
Message broker
 ↓
Workers
 ↓
Providers
```

### Follow-up

What happens when a provider is unavailable?

Discuss:

```text
Timeout
Retry
Backoff
Dead-letter handling
Idempotency
```

______________________________________________________________________

# Design 3 — File Upload Service

### Requirements

```text
Maximum file size?
File types?
Private/public?
Download?
Processing?
Virus scanning?
```

### Possible architecture

```text
Client
 ↓
API
 ↓
Object storage
 ↓
Event
 ↓
Processing worker
```

### Follow-up

Why not store large files directly in PostgreSQL?

______________________________________________________________________

# Design 4 — Rate Limiter

### Requirements

```text
Per user?
Per IP?
Per API key?
Global?
Distributed?
```

### Discuss

```text
Redis
Counters
TTL
Atomic operations
Sliding window
Token bucket
Concurrency
```

### Follow-up

What happens if Redis is unavailable?

______________________________________________________________________

# Design 5 — Chat Service

### Requirements

```text
One-to-one?
Groups?
Message history?
Online status?
Delivery status?
Read status?
```

### Possible components

```text
API
WebSocket layer
Message service
Database
Cache
Message broker
```

### Follow-up

How would you scale WebSocket connections?

______________________________________________________________________

# Part 21 — Production Debugging Round

## Scenario 1 — CPU at 100%

### Question

Production API CPU reaches 100%.

What do you do?

### Expected methodology

```text
Confirm impact
→ identify process/container
→ inspect CPU by process/thread
→ inspect request rate
→ inspect recent changes
→ inspect logs/metrics
→ profile if necessary
→ mitigate
→ identify root cause
→ prevent recurrence
```

______________________________________________________________________

## Scenario 2 — Memory Growth

### Question

Memory continuously increases after deployment.

Investigate:

```text
Process memory
→ container limit
→ recent changes
→ allocation behavior
→ object/reference retention
→ traffic pattern
→ profiling
```

______________________________________________________________________

## Scenario 3 — Slow API

### Question

p95 latency increases from 200 ms to 2 seconds.

Check:

```text
Application
Database
Redis
External APIs
Connection pools
CPU
Memory
Traffic
Recent deployment
```

Break the latency into components.

______________________________________________________________________

## Scenario 4 — 502

### Question

Users receive 502 responses.

Potential layers:

```text
Client
→ Load balancer
→ Reverse proxy
→ Application
```

Determine which layer is returning the error.

______________________________________________________________________

## Scenario 5 — 503

A service returns 503.

Consider:

```text
Application unavailable
Health check failure
Overload
Deployment
Dependency failure
Load balancer behavior
```

______________________________________________________________________

## Scenario 6 — Database Unavailable

Ask:

```text
Is the database actually unreachable?
Is the problem connectivity?
Authentication?
Connection pool?
Database capacity?
Failover?
```

Then consider application behavior.

______________________________________________________________________

## Scenario 7 — Connection Pool Exhaustion

Investigate:

```text
Pool size
Active connections
Connection duration
Long queries
Unclosed sessions
Long transactions
Traffic increase
Database availability
```

______________________________________________________________________

## Scenario 8 — Redis Unavailable

Determine:

```text
Cache-only dependency?
Critical state?
Fallback?
Database capacity?
```

Prevent a cache failure from becoming a database outage.

______________________________________________________________________

## Scenario 9 — Kafka Consumer Lag

Investigate:

```text
Incoming rate
Processing rate
Consumer health
Partition distribution
Consumer count
CPU
Memory
Downstream latency
Errors
Rebalances
```

______________________________________________________________________

## Scenario 10 — Duplicate Messages

Investigate:

```text
Producer retry
Consumer retry
Acknowledgment
Offset handling
Network failure
Processing failure
```

Then ensure business operations are idempotent.

______________________________________________________________________

## Scenario 11 — Container Restart

Check:

```text
Exit code
Logs
OOM
Health checks
Startup
Configuration
Dependencies
```

______________________________________________________________________

## Scenario 12 — Network Problem

Investigate from the outside inward:

```text
DNS
→ TCP connectivity
→ TLS
→ HTTP
→ Application
→ Dependency
```

______________________________________________________________________

# Part 22 — Behavioral Crossover Questions

These are technical questions that also evaluate senior-level behavior.

## Question 1

Tell me about a production incident you owned.

Cover:

```text
Situation
→ Impact
→ Your role
→ Investigation
→ Mitigation
→ Root cause
→ Prevention
```

______________________________________________________________________

## Question 2

Tell me about a technical decision where your team disagreed.

Discuss:

```text
Different options
→ Evidence
→ Trade-offs
→ Decision
→ Result
```

Avoid turning the answer into criticism of another person.

______________________________________________________________________

## Question 3

Tell me about a time you made a technical mistake.

Strong answer:

```text
Mistake
→ Impact
→ Ownership
→ Correction
→ Learning
→ Prevention
```

Do not claim you have never made mistakes.

______________________________________________________________________

## Question 4

Tell me about a time you improved system performance.

Cover:

```text
Baseline
→ Bottleneck
→ Investigation
→ Change
→ Measurement
→ Result
```

______________________________________________________________________

## Question 5

Tell me about a technical debt decision.

Explain:

```text
Why debt existed
→ Why it was accepted
→ Cost
→ Trigger for addressing it
→ Result
```

______________________________________________________________________

## Question 6

How do you handle pressure during an outage?

A strong answer focuses on:

```text
Prioritize impact
→ Communicate
→ Stabilize
→ Investigate
→ Fix
→ Document
→ Prevent recurrence
```

______________________________________________________________________

# Part 23 — Senior-Level Follow-Ups

After almost any technical answer, expect questions such as:

```text
Why?
Why not the alternative?
What happens if it fails?
What is the bottleneck?
How does it scale?
What happens at 10x traffic?
How would you test it?
How would you monitor it?
What are the security risks?
What are the consistency implications?
What is the trade-off?
What would you change today?
```

Practice answering these without becoming defensive.

______________________________________________________________________

# Part 24 — The "10x Traffic" Test

For any backend architecture, ask:

```text
What happens if traffic becomes 10x?
```

Evaluate:

```text
Application CPU
Application memory
Load balancer
Database
Connection pool
Cache
Message broker
Workers
External APIs
Network
Storage
```

Then identify:

```text
First bottleneck
Second bottleneck
Scaling strategy
```

______________________________________________________________________

# Part 25 — The "Everything Fails" Test

For any system, ask:

```text
What if the database fails?

What if Redis fails?

What if Kafka/RabbitMQ fails?

What if an external API times out?

What if a worker crashes?

What if messages are duplicated?

What if traffic spikes?

What if a deployment is bad?

What if the network is partitioned?
```

A senior engineer should be comfortable discussing degraded behavior.

______________________________________________________________________

# Part 26 — Final Revision Checklist

## Python

- [ ] Mutable vs immutable
- [ ] `is` vs `==`
- [ ] Copying
- [ ] Functions
- [ ] Decorators
- [ ] Context managers
- [ ] Iterators
- [ ] Generators
- [ ] Collections
- [ ] Exceptions
- [ ] Modules/packages
- [ ] OOP
- [ ] Advanced OOP
- [ ] Memory management

## Concurrency

- [ ] Threads
- [ ] Processes
- [ ] GIL
- [ ] Locks
- [ ] Race conditions
- [ ] Deadlocks
- [ ] Executors
- [ ] AsyncIO
- [ ] Event loop
- [ ] Coroutines
- [ ] Tasks
- [ ] Cancellation
- [ ] Timeouts
- [ ] Blocking code

## FastAPI

- [ ] ASGI
- [ ] Routing
- [ ] Pydantic
- [ ] Validation
- [ ] Response models
- [ ] Dependency injection
- [ ] Middleware
- [ ] Error handling
- [ ] Authentication
- [ ] Authorization
- [ ] Async endpoints
- [ ] Background tasks
- [ ] Pagination
- [ ] Rate limiting
- [ ] Health checks
- [ ] Graceful shutdown
- [ ] Observability

## Networking

- [ ] DNS
- [ ] TCP
- [ ] UDP
- [ ] TCP handshake
- [ ] TLS
- [ ] HTTPS
- [ ] HTTP methods
- [ ] Status codes
- [ ] Headers
- [ ] Cookies
- [ ] Sessions
- [ ] Keep-alive
- [ ] HTTP/2 overview
- [ ] REST
- [ ] Idempotency

## Database

- [ ] SQL
- [ ] JOINs
- [ ] Subqueries
- [ ] CTEs
- [ ] Window functions
- [ ] Indexes
- [ ] Query plans
- [ ] Normalization
- [ ] Functional dependencies
- [ ] Candidate keys
- [ ] 1NF
- [ ] 2NF
- [ ] 3NF
- [ ] BCNF overview
- [ ] Denormalization
- [ ] Transactions
- [ ] ACID
- [ ] Isolation
- [ ] MVCC
- [ ] Locks
- [ ] Deadlocks

## SQLAlchemy

- [ ] Engine
- [ ] Connection
- [ ] Session
- [ ] Flush
- [ ] Commit
- [ ] Rollback
- [ ] Identity map
- [ ] Unit of work
- [ ] Relationships
- [ ] Lazy loading
- [ ] Eager loading
- [ ] N+1
- [ ] Async sessions
- [ ] Connection pooling

## Redis

- [ ] Data structures
- [ ] TTL
- [ ] Expiration
- [ ] Atomic operations
- [ ] Cache-aside
- [ ] Cache invalidation
- [ ] Cache stampede
- [ ] Distributed locks
- [ ] Persistence
- [ ] Eviction
- [ ] Replication
- [ ] Sentinel
- [ ] Cluster

## Messaging

- [ ] Kafka
- [ ] Topics
- [ ] Partitions
- [ ] Consumer groups
- [ ] Offsets
- [ ] Ordering
- [ ] Consumer lag
- [ ] Delivery semantics
- [ ] Idempotency
- [ ] Retry
- [ ] Dead-letter handling
- [ ] RabbitMQ
- [ ] Exchanges
- [ ] Queues
- [ ] Bindings
- [ ] ACK
- [ ] Prefetch
- [ ] Celery
- [ ] Workers
- [ ] Beat

## Infrastructure

- [ ] Docker
- [ ] Images
- [ ] Containers
- [ ] Dockerfile
- [ ] Layers
- [ ] Multi-stage builds
- [ ] Volumes
- [ ] Networking
- [ ] Health checks
- [ ] Compose
- [ ] Linux processes
- [ ] Threads
- [ ] Signals
- [ ] SSH
- [ ] Disk
- [ ] Memory
- [ ] systemd
- [ ] Logs
- [ ] cron

## Security

- [ ] OWASP fundamentals
- [ ] SQL injection
- [ ] XSS
- [ ] CSRF
- [ ] Authentication
- [ ] Authorization
- [ ] JWT
- [ ] OAuth2
- [ ] HTTPS
- [ ] CORS
- [ ] SSRF
- [ ] Command injection
- [ ] Path traversal
- [ ] File upload security
- [ ] Secrets
- [ ] Rate limiting
- [ ] Security headers
- [ ] Dependency security
- [ ] Least privilege

## Git

- [ ] Branching
- [ ] Merge
- [ ] Rebase
- [ ] Conflict resolution
- [ ] Reset
- [ ] Revert
- [ ] Stash
- [ ] Cherry-pick
- [ ] Squashing
- [ ] Reflog
- [ ] Bisect
- [ ] Pull requests
- [ ] Code reviews

## DSA

- [ ] Big-O
- [ ] Arrays
- [ ] Strings
- [ ] Hash maps
- [ ] Sets
- [ ] Stacks
- [ ] Queues
- [ ] Linked lists
- [ ] Trees
- [ ] Recursion
- [ ] Two pointers
- [ ] Sliding window
- [ ] Binary search
- [ ] BFS
- [ ] DFS
- [ ] Top-K
- [ ] Prefix/suffix
- [ ] Basic dynamic programming

## System Design

- [ ] Requirements
- [ ] Capacity estimation
- [ ] Scalability
- [ ] Availability
- [ ] Reliability
- [ ] Latency
- [ ] Throughput
- [ ] Stateless services
- [ ] Load balancing
- [ ] Caching
- [ ] Databases
- [ ] Queues
- [ ] Monitoring
- [ ] Retry
- [ ] Timeout
- [ ] Circuit breaker
- [ ] Idempotency
- [ ] CAP
- [ ] Architecture building blocks
- [ ] Practical system designs

______________________________________________________________________

# Part 27 — Final Interview-Day Strategy

## Before the Interview

Review only:

```text
Project summaries
Rapid-fire questions
System-design patterns
Recent production incidents
DSA patterns
Your resume
```

Do not attempt to learn a large new topic immediately before the interview.

______________________________________________________________________

## During Technical Questions

Use:

```text
Listen
→ Clarify
→ Think
→ Answer
→ Stop
```

If you need time:

```text
"Let me think through that."
```

is completely reasonable.

______________________________________________________________________

## When You Don't Know

Do not bluff.

A strong response is:

```text
"I haven't worked with that directly, but here's how I understand
the concept..."
```

Then explain what you know.

For an unfamiliar production scenario:

```text
"I would start by checking..."
```

and give a systematic investigation approach.

______________________________________________________________________

# Part 28 — Final Senior-Level Checklist

Before the interview, make sure you can answer:

### About Python

```text
Why Python for backend systems?
How does the GIL affect concurrency?
How do async and threads differ?
How does Python manage memory?
```

### About Your Projects

```text
What did you build?
Why did you build it?
What did you personally own?
Why did you choose the architecture?
What failed?
How did you scale it?
What would you change?
```

### About Databases

```text
Why this database?
How did you design the schema?
Why these indexes?
How did you handle transactions?
How did you handle concurrency?
```

### About Distributed Systems

```text
What happens when dependencies fail?
How do retries work?
How do you prevent duplicate operations?
How do you handle eventual consistency?
```

### About Production

```text
How do you debug?
How do you monitor?
How do you detect failures?
How do you mitigate incidents?
How do you prevent recurrence?
```

### About System Design

```text
What are the requirements?
What is the scale?
Where is the bottleneck?
How does it scale?
What happens when components fail?
What trade-offs did you make?
```

______________________________________________________________________

# Part 29 — Final Mock Interview Scorecard

After completing a mock interview, score yourself from **1 to 5**.

| Area | Score |
|---|---:|
| Python fundamentals | /5 |
| Advanced Python | /5 |
| Concurrency & AsyncIO | /5 |
| FastAPI | /5 |
| HTTP & networking | /5 |
| SQL | /5 |
| Database design | /5 |
| Transactions & concurrency | /5 |
| SQLAlchemy | /5 |
| Redis | /5 |
| Kafka / messaging | /5 |
| Docker | /5 |
| Linux | /5 |
| Security | /5 |
| Git | /5 |
| DSA | /5 |
| System design | /5 |
| Project depth | /5 |
| Production debugging | /5 |
| Communication | /5 |

Use:

```text
1 → Cannot explain
2 → Basic recognition
3 → Can explain fundamentals
4 → Strong practical understanding
5 → Can explain deeply with trade-offs and production examples
```

Your goal is not necessarily to score 5 everywhere.

Identify the weak areas that are most likely to matter for the role and revisit the corresponding detailed files.

______________________________________________________________________

# Part 30 — The Final 30-Minute Revision

If you have only 30 minutes before the interview:

### 0–5 minutes

Review:

```text
Your resume
Your project architecture
Your contribution
Your biggest achievement
Your biggest production incident
```

### 5–10 minutes

Review:

```text
Python
Concurrency
FastAPI
```

### 10–15 minutes

Review:

```text
SQL
Normalization
Indexes
Transactions
SQLAlchemy
```

### 15–20 minutes

Review:

```text
Redis
Kafka
RabbitMQ
Celery
```

### 20–25 minutes

Review:

```text
Security
Docker
Linux
Git
```

### 25–30 minutes

Review:

```text
System design
Failure handling
Trade-offs
DSA patterns
```

Then stop studying.

Focus on communication and clarity.

______________________________________________________________________

# 31. Final Takeaways

The entire preparation plan ultimately comes down to five abilities:

## 1. Build

Can you design and implement a backend system?

```text
Python
FastAPI
SQLAlchemy
Database
Redis
Messaging
Docker
```

## 2. Understand

Can you explain why the system works?

```text
Architecture
Protocols
Concurrency
Transactions
Data modeling
```

## 3. Debug

Can you find problems when the system behaves unexpectedly?

```text
Metrics
Logs
Tracing
Database
Network
Dependencies
```

## 4. Scale

Can you reason about what happens when the system grows?

```text
10x traffic
More data
More users
More workers
More services
```

## 5. Own

Can you explain:

```text
Your decisions
Your mistakes
Your trade-offs
Your production incidents
Your results
```

That final ability is especially important for senior-level interviews.

______________________________________________________________________

# Final Interview Mindset

Do not try to appear as someone who knows everything.

Aim to demonstrate that you can:

```text
Understand the problem
        ↓
Break it down
        ↓
Make a reasonable decision
        ↓
Explain the trade-off
        ↓
Implement it
        ↓
Test it
        ↓
Monitor it
        ↓
Debug it when it fails
        ↓
Improve it
```

If you don't know something, reason from first principles.

If you made a mistake, explain what you learned.

If there are multiple valid approaches, explain the trade-offs.

If the interviewer challenges your design, treat it as a technical discussion rather than a confrontation.

> **The goal is not to prove that your first answer is perfect. The goal is to demonstrate strong engineering judgment.**

______________________________________________________________________

## Final Rule

For every important backend concept, remember:

```text
What is it?
Why use it?
How does it work?
What can go wrong?
How do you test it?
How do you monitor it?
How does it scale?
What are the trade-offs?
```

For every important project:

```text
What problem?
What architecture?
What did I own?
Why those decisions?
What failed?
What was the impact?
What would I change?
```

For every production problem:

```text
Detect
→ Investigate
→ Mitigate
→ Root cause
→ Fix
→ Prevent
```

For every system design:

```text
Requirements
→ Estimate
→ Design
→ Scale
→ Fail
→ Recover
→ Trade-off
```

This completes the Python Backend Engineer interview preparation plan.

**Previous:** [47. Rapid-Fire Python Backend Q&A](./47-rapid-fire-python-backend.md)

**Next:** End of the interview preparation plan
