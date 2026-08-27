# 38. System Design Fundamentals

**Previous:** [37. DSA Coding Practice](./37-dsa-practice.md)

**Next:** [39. Backend Architecture Building Blocks](./39-system-design-building-blocks.md)

______________________________________________________________________

## Objective

By the end of this topic, you should be able to:

- Approach a system-design interview systematically.
- Separate functional and non-functional requirements.
- Estimate basic traffic, storage and capacity requirements.
- Explain scalability, availability and reliability.
- Reason about latency and throughput.
- Explain why stateless services are useful.
- Understand load balancing.
- Choose where caching helps.
- Understand the role of databases, queues and workers.
- Explain rate limiting.
- Design basic monitoring and observability.
- Understand retry and timeout behavior.
- Explain circuit breakers.
- Design idempotent operations.
- Explain the basic CAP theorem trade-off.
- Communicate architecture decisions and trade-offs clearly.

> **Scope:** This is a practical system-design foundation for a 5+ year Python backend engineer. Advanced distributed-system theory and very large-scale architecture are intentionally kept out of scope.

______________________________________________________________________

# 1. What Is System Design?

System design is the process of deciding how software components should work together to satisfy requirements.

A backend system may contain:

```text
Clients
  ↓
Load Balancer
  ↓
Application Services
  ↓
Cache / Database / Queue
  ↓
Workers / External Services
```

The important part is not drawing many boxes.

The important part is explaining:

```text
Why is each component there?
What problem does it solve?
What trade-off does it introduce?
What happens when it fails?
```

______________________________________________________________________

# 2. System Design Interview Mindset

Do not immediately start drawing architecture.

A strong process is:

```text
Requirements
→ Constraints
→ Capacity estimation
→ High-level design
→ Data/storage
→ Scaling
→ Reliability
→ Failure handling
→ Observability
→ Trade-offs
```

This gives the discussion a logical structure.

______________________________________________________________________

# 3. Functional Requirements

Functional requirements describe what the system must do.

Example for a URL-shortening service:

```text
Create short URL
Redirect short URL
Track basic usage
```

Functional requirements should be specific enough to guide the design.

______________________________________________________________________

# 4. Non-Functional Requirements

Non-functional requirements describe system qualities and constraints.

Examples:

```text
Availability
Latency
Throughput
Reliability
Scalability
Security
Durability
Consistency
```

Example:

> The redirect API should respond within 100 ms for normal traffic.

That requirement influences caching, database selection and architecture.

______________________________________________________________________

# 5. Functional vs Non-Functional

| Functional | Non-Functional |
|---|---|
| Create user | 99.9% availability |
| Upload file | \<200 ms latency |
| Send message | 10,000 requests/sec |
| Generate report | Durable storage |
| Process payment | Strong consistency |

Interviewers expect you to clarify both.

______________________________________________________________________

# 6. Requirements Questions

At the beginning of an interview, clarify:

### Users

```text
How many users?
How many active users?
```

### Traffic

```text
Requests per second?
Read/write ratio?
Peak traffic?
```

### Data

```text
How much data?
How fast does it grow?
How long must it be retained?
```

### Reliability

```text
Availability target?
Can requests be lost?
```

### Latency

```text
What latency is acceptable?
Is this interactive or asynchronous?
```

______________________________________________________________________

# 7. Capacity Estimation

Capacity estimation gives approximate numbers for the architecture.

You do not need exact production numbers.

The goal is to identify scale.

Typical estimates include:

```text
Requests per second
Storage
Bandwidth
Memory/cache size
Database size
```

______________________________________________________________________

# 8. Traffic Estimation

Suppose:

```text
10 million requests/day
```

Average requests per second:

```text
10,000,000 / 86,400
≈ 116 requests/sec
```

If peak traffic is 5× average:

```text
≈ 580 requests/sec
```

The exact peak multiplier should be justified rather than blindly assumed.

______________________________________________________________________

# 9. Read/Write Ratio

Suppose:

```text
1000 requests/sec
```

with:

```text
90% reads
10% writes
```

Then approximately:

```text
900 reads/sec
100 writes/sec
```

This affects:

- Caching
- Database design
- Read replicas
- Queue usage

______________________________________________________________________

# 10. Storage Estimation

Suppose:

```text
1 million records/day
2 KB/record
```

Daily raw data:

```text
1,000,000 × 2 KB
≈ 2 GB/day
```

Yearly:

```text
≈ 730 GB/year
```

Then account for:

```text
Indexes
Replication
Backups
Metadata
Growth
```

______________________________________________________________________

# 11. Bandwidth Estimation

If:

```text
1000 requests/sec
10 KB average response
```

then outgoing data is approximately:

```text
1000 × 10 KB
= 10 MB/sec
```

This helps determine whether:

```text
CDN
Compression
Caching
Pagination
```

may be important.

______________________________________________________________________

# 12. Peak vs Average

Designing only for average traffic can be dangerous.

For example:

```text
Average: 1,000 RPS
Peak:    10,000 RPS
```

The system must tolerate the peak if the requirement says so.

Possible approaches:

```text
Horizontal scaling
Caching
Queues
Rate limiting
Autoscaling
Load shedding
```

______________________________________________________________________

# 13. Scalability

Scalability is the ability to handle increasing workload by increasing resources or improving architecture.

Two broad approaches:

```text
Vertical scaling
Horizontal scaling
```

______________________________________________________________________

# 14. Vertical Scaling

Increase resources on one machine:

```text
More CPU
More RAM
Faster storage
```

Advantages:

- Simple
- Minimal architectural complexity

Limitations:

- Hardware ceiling
- Single-machine constraints
- Potentially expensive

______________________________________________________________________

# 15. Horizontal Scaling

Add more instances:

```text
        Load Balancer
        /     |     \
      App1   App2   App3
```

Advantages:

- Better scale
- Fault isolation
- Easier capacity expansion

Requirements often include:

```text
Stateless application
Shared external state
Load balancing
```

______________________________________________________________________

# 16. Stateless Services

A stateless service does not depend on local process memory for durable user/session state.

For example, avoid relying on:

```python
sessions[user_id] = session
```

inside one application instance.

If traffic moves from:

```text
App1 → App2
```

the request should still work.

Externalize shared state into:

```text
Database
Redis
Object storage
```

as appropriate.

______________________________________________________________________

# 17. Why Statelessness Helps

Suppose:

```text
        Load Balancer
        /           \
      App1          App2
```

If user state exists only in App1, requests routed to App2 may fail.

With external state:

```text
App1 ─┐
      ├→ Redis/DB
App2 ─┘
```

any instance can serve the request.

This improves horizontal scalability.

______________________________________________________________________

# 18. Load Balancing

A load balancer distributes traffic across service instances.

Conceptually:

```text
Client
  ↓
Load Balancer
  ↓
App1 / App2 / App3
```

Common strategies include:

```text
Round robin
Least connections
Weighted routing
Hash-based routing
```

The right strategy depends on workload and requirements.

______________________________________________________________________

# 19. Health Checks

Load balancers need to know whether instances are usable.

A health endpoint might be:

```text
GET /health
```

But distinguish:

```text
Liveness
Readiness
```

### Liveness

Is the process alive?

### Readiness

Can the instance safely receive traffic?

An application can be alive but not ready to serve traffic.

______________________________________________________________________

# 20. Caching

Caching stores frequently accessed data closer to the application/user.

Typical cache:

```text
Client
 ↓
Application
 ↓
Cache
 ↓ miss
Database
```

Benefits:

- Lower latency
- Lower database load
- Higher throughput

Costs:

- Stale data
- Invalidation complexity
- Memory usage
- Cache failures

______________________________________________________________________

# 21. Cache Hit and Miss

### Cache hit

Requested data exists:

```text
Request
 ↓
Cache
 ↓
Response
```

### Cache miss

Data is absent:

```text
Request
 ↓
Cache miss
 ↓
Database
 ↓
Cache
 ↓
Response
```

The cache-aside strategy is commonly used in backend systems.

______________________________________________________________________

# 22. Cache Invalidation

One of the hardest caching problems is keeping cached data consistent with the source of truth.

Common approaches:

```text
TTL
Explicit invalidation
Versioned keys
Write-through
Cache-aside
```

There is usually a trade-off between:

```text
Freshness
+
Performance
+
Complexity
```

______________________________________________________________________

# 23. Database Role

Databases provide durable storage and querying.

In system design, ask:

```text
What data exists?
How is it accessed?
How much is read?
How much is written?
What consistency is required?
```

Do not select a database purely because it is popular.

______________________________________________________________________

# 24. Database Bottlenecks

A database can become a bottleneck because of:

```text
CPU
Disk I/O
Memory
Locks
Connections
Slow queries
Indexes
Storage capacity
```

Possible solutions:

```text
Query optimization
Indexes
Caching
Read replicas
Partitioning
Sharding
```

Use the simplest solution that satisfies the requirements.

______________________________________________________________________

# 25. Queues

Queues decouple producers from consumers.

Example:

```text
API
 ↓
Queue
 ↓
Worker
 ↓
Database / External service
```

This is useful when work is:

```text
Slow
Retryable
Burst-heavy
Asynchronous
```

______________________________________________________________________

# 26. Why Queues Help

Suppose an API receives:

```text
10,000 requests/sec
```

but a downstream system can process only:

```text
2,000 operations/sec
```

A queue can absorb bursts.

Instead of forcing every API request to wait for downstream processing:

```text
API → Queue → Worker
```

the API can often return quickly after safely accepting the work.

______________________________________________________________________

# 27. Queue Trade-Offs

Queues introduce their own concerns:

```text
Delivery semantics
Ordering
Retries
Duplicate processing
Dead letters
Backpressure
Consumer lag
Durability
```

This connects directly to the Kafka/RabbitMQ topics covered earlier.

______________________________________________________________________

# 28. Workers

Workers consume asynchronous jobs.

Example:

```text
FastAPI
 ↓
Queue
 ↓
Celery Worker
 ↓
Email provider
```

Workers are useful for:

- Email
- Report generation
- Image processing
- Notifications
- Long-running tasks
- External API workflows

______________________________________________________________________

# 29. Synchronous vs Asynchronous Work

Use synchronous processing when the client needs the result immediately.

Use asynchronous processing when:

```text
Work is slow
Work can happen later
Work can be retried
Work is independent of the immediate response
```

A common design:

```text
POST /reports
      ↓
Create job
      ↓
Return job ID

Worker processes job

GET /reports/{id}
      ↓
Return status/result
```

______________________________________________________________________

# 30. Rate Limiting

Rate limiting controls how much traffic a client can generate.

Example:

```text
100 requests/minute/user
```

Benefits:

- Protects services
- Prevents abuse
- Controls resource consumption
- Reduces accidental overload

______________________________________________________________________

# 31. Rate-Limiting Algorithms

Common approaches include:

```text
Fixed window
Sliding window
Token bucket
Leaky bucket
```

For interview fundamentals, understand the purpose and trade-offs rather than implementing every algorithm.

______________________________________________________________________

# 32. Distributed Rate Limiting

If there are multiple application instances:

```text
App1
App2
App3
```

a local counter on each instance may allow a client to exceed the intended global limit.

Shared state such as Redis can maintain the distributed counter.

______________________________________________________________________

# 33. Retry

Retries can recover from transient failures.

Examples:

```text
Temporary network failure
Transient database issue
Service temporarily unavailable
```

But retries can make outages worse.

______________________________________________________________________

# 34. Exponential Backoff

Instead of retrying immediately:

```text
Retry 1 → short delay
Retry 2 → longer delay
Retry 3 → longer delay
```

A common conceptual sequence is:

```text
1s
2s
4s
8s
```

with jitter added to avoid synchronized retry storms.

______________________________________________________________________

# 35. What Should Be Retried?

Retry only when the failure is plausibly transient.

Examples:

```text
Connection timeout
Temporary 503
Transient network failure
```

Be careful with:

```text
Validation errors
Authentication failures
Permanent business errors
```

______________________________________________________________________

# 36. Timeout

Every network dependency should have an appropriate timeout.

Without timeouts:

```text
App
 ↓
Dependency hangs
 ↓
Connection occupied
 ↓
Requests accumulate
 ↓
Resources exhausted
```

Timeouts prevent indefinite waiting.

______________________________________________________________________

# 37. Timeout Types

A request can have multiple timeout considerations:

```text
Connection timeout
Read timeout
Write timeout
Overall request deadline
```

The exact configuration depends on the client/library.

______________________________________________________________________

# 38. Retry + Timeout Interaction

Suppose:

```text
Request timeout = 5 sec
Retries = 3
```

If each retry can consume the full timeout, the total request may take much longer than expected.

Therefore design around an overall deadline.

Conceptually:

```text
Overall deadline
 ├─ attempt 1
 ├─ backoff
 ├─ attempt 2
 └─ attempt 3
```

______________________________________________________________________

# 39. Circuit Breaker

A circuit breaker prevents repeatedly calling a failing dependency.

Typical states:

```text
Closed
Open
Half-open
```

### Closed

Requests flow normally.

### Open

Requests fail fast without calling the dependency.

### Half-open

A limited test request checks whether the dependency recovered.

______________________________________________________________________

# 40. Why Circuit Breakers Help

Without a circuit breaker:

```text
Dependency failing
 ↓
Every request retries/calls it
 ↓
Threads/connections accumulate
 ↓
Caller becomes unhealthy
```

A circuit breaker limits the blast radius.

______________________________________________________________________

# 41. Idempotency

An operation is idempotent if repeating it produces the same intended final effect.

Examples:

```text
PUT /users/123
```

setting the same representation repeatedly is generally idempotent.

For APIs such as payments, use an idempotency key where appropriate:

```text
Idempotency-Key: abc123
```

The server can associate the key with the operation/result.

______________________________________________________________________

# 42. Why Idempotency Matters

Suppose:

```text
Client → Payment API
```

The payment succeeds, but the response is lost.

The client retries.

Without idempotency:

```text
Payment 1
Payment 2
```

With an idempotency mechanism:

```text
Payment 1
Retry → return original result
```

This is critical for distributed systems.

______________________________________________________________________

# 43. Idempotency vs Deduplication

These concepts are related but not identical.

### Idempotency

Repeating the same logical request has the same intended effect.

### Deduplication

Detecting and suppressing duplicate messages/operations.

Message consumers often need idempotent processing because at-least-once delivery can produce duplicates.

______________________________________________________________________

# 44. Reliability

Reliability means the system performs correctly over time despite expected failures.

Examples:

```text
Retries
Timeouts
Replication
Backups
Health checks
Graceful degradation
Queues
Circuit breakers
```

Reliability is broader than simply "the server is up."

______________________________________________________________________

# 45. Availability

Availability describes whether the system is accessible when requested.

A common representation:

```text
Availability =
uptime / total time
```

For example:

```text
99.9%
```

allows more downtime than:

```text
99.99%
```

The additional "9" has significant operational implications.

______________________________________________________________________

# 46. Reliability vs Availability

### Availability

> Can I access the service?

### Reliability

> Does the system consistently perform the intended operation correctly?

A system can be:

```text
Available but unreliable
```

For example, an API returns quickly but frequently returns incorrect results.

______________________________________________________________________

# 47. Latency

Latency is the time required to complete an operation.

Examples:

```text
API latency
Database query latency
Network latency
Queue processing latency
```

For user-facing systems, distinguish:

```text
Average
p50
p95
p99
```

______________________________________________________________________

# 48. Why p95/p99 Matter

Suppose:

```text
Average latency = 50 ms
p99 latency = 2 sec
```

Most requests are fast, but a meaningful tail is slow.

Average latency can hide these tail problems.

Backend engineers should understand:

```text
Tail latency
```

when designing systems.

______________________________________________________________________

# 49. Throughput

Throughput is the amount of work processed per unit time.

Examples:

```text
Requests/sec
Messages/sec
Transactions/sec
Files/sec
```

Latency and throughput are related but not identical.

A system can have:

```text
High throughput
+
High latency
```

if it processes many operations but each takes a long time.

______________________________________________________________________

# 50. Latency vs Throughput

Think:

```text
Latency
→ How long does one operation take?

Throughput
→ How many operations can we process per unit time?
```

Both should be considered during capacity planning.

______________________________________________________________________

# 51. Backpressure

Backpressure occurs when downstream processing cannot keep up with incoming work.

Example:

```text
Producer: 10,000 jobs/sec
Consumer: 2,000 jobs/sec
```

Backlog grows.

Possible controls:

```text
Queue
Rate limiting
Load shedding
Autoscaling
Batching
Bounded concurrency
```

______________________________________________________________________

# 52. Load Shedding

When a system is overloaded, it may be better to reject some work than allow the entire system to collapse.

Examples:

```text
429 Too Many Requests
503 Service Unavailable
```

This protects critical resources.

______________________________________________________________________

# 53. Graceful Degradation

Instead of failing completely, return a reduced experience.

Example:

```text
Primary recommendation service unavailable
→ Return cached recommendations
```

or:

```text
Analytics unavailable
→ Core transaction still succeeds
```

This improves resilience.

______________________________________________________________________

# 54. CAP Theorem

CAP describes a trade-off in distributed systems involving:

```text
Consistency
Availability
Partition tolerance
```

During a network partition, a distributed system cannot simultaneously guarantee both strong consistency and
availability for all operations.

______________________________________________________________________

# 55. Consistency in CAP

Consistency means clients observe data according to the system's consistency guarantee.

In the simplified CAP discussion:

```text
C = consistent responses
```

This is not identical to database ACID consistency.

Be careful not to conflate:

```text
CAP consistency
```

with:

```text
ACID consistency
```

______________________________________________________________________

# 56. Availability in CAP

Availability means that every request to a non-failing node receives a response.

During a network partition, choosing availability can mean accepting responses that may not reflect the latest state.

______________________________________________________________________

# 57. Partition Tolerance

A partition occurs when distributed nodes cannot reliably communicate.

Example:

```text
Node A  X  Node B
```

The network link fails.

In a distributed system, partitions are possible, so partition tolerance is generally a practical requirement.

The key CAP trade-off becomes:

```text
During partition:
Consistency
vs
Availability
```

______________________________________________________________________

# 58. CAP Interview Trap

Do not say:

> "You choose any two of CAP."

A better explanation is:

> "When a network partition occurs, a distributed system must trade off strong consistency against availability."

This is more precise.

______________________________________________________________________

# 59. Monitoring

A production system needs visibility into its behavior.

Important signals include:

```text
Traffic
Errors
Latency
Saturation
```

Also monitor:

```text
CPU
Memory
Disk
Connections
Queue depth
Consumer lag
Cache hit rate
Database latency
```

______________________________________________________________________

# 60. Metrics

Useful backend metrics:

### Request metrics

```text
RPS
Error rate
Latency percentiles
```

### Resource metrics

```text
CPU
Memory
Disk
Network
```

### Dependency metrics

```text
Database latency
Redis errors
External API failures
Queue lag
```

______________________________________________________________________

# 61. Logs

Logs answer:

```text
What happened?
When?
For which request?
Which user/resource?
What error occurred?
```

Use structured logs where practical.

Example fields:

```text
request_id
service
endpoint
status_code
duration_ms
error_type
```

Avoid putting sensitive secrets or credentials into logs.

______________________________________________________________________

# 62. Tracing

Distributed tracing follows a request across services.

Conceptually:

```text
API
 ↓
Service A
 ↓
Service B
 ↓
Database
```

A trace can show which component consumed the latency budget.

This becomes particularly useful in microservice architectures.

______________________________________________________________________

# 63. Correlation IDs

A request identifier can connect related logs across components.

Example:

```text
request_id = abc123
```

The same identifier can appear in:

```text
API log
Service log
Worker log
Dependency call
```

This greatly improves debugging.

______________________________________________________________________

# 64. Failure Points

Every architecture should ask:

```text
What can fail?
```

For:

```text
Client
 ↓
Load Balancer
 ↓
API
 ↓
Redis
 ↓
Database
 ↓
External API
```

potential failures include:

```text
Network timeout
Service crash
Connection exhaustion
Database failure
Cache outage
Dependency overload
```

A design is incomplete if it discusses only the happy path.

______________________________________________________________________

# 65. Dependency Failure

If Redis fails:

```text
What happens?
```

Possible answer:

```text
Fall back to database
```

But ask:

```text
Can the database handle the increased traffic?
```

This is a key system-design insight.

Every fallback can create another bottleneck.

______________________________________________________________________

# 66. Retry Storm

Suppose:

```text
1000 requests
```

all retry a failing dependency simultaneously.

The dependency receives:

```text
1000 original requests
+
1000 retries
+
more retries
```

This can worsen the outage.

Mitigations:

```text
Exponential backoff
Jitter
Retry limits
Circuit breaker
Timeouts
Load shedding
```

______________________________________________________________________

# 67. Connection Pool Exhaustion

Suppose an application has:

```text
DB pool = 20 connections
```

If requests hold connections too long:

```text
20 busy connections
→ new requests wait
→ latency increases
→ timeouts
```

This can look like an application slowdown even when CPU is low.

Monitoring connection-pool utilization is important.

______________________________________________________________________

# 68. System Design Building Blocks

A basic backend architecture may look like:

```text
Client
  ↓
Load Balancer
  ↓
Stateless API
  ├──→ Cache
  ├──→ Database
  └──→ Queue → Workers
```

Supporting concerns:

```text
Rate limiting
Timeouts
Retries
Circuit breakers
Monitoring
```

The next topic expands these components individually.

______________________________________________________________________

# 69. Example: Simple API Architecture

Requirement:

> Build an API serving user profiles.

Possible architecture:

```text
Client
 ↓
Load Balancer
 ↓
FastAPI instances
 ↓
Redis
 ↓
PostgreSQL
```

Reasoning:

```text
Load balancer
→ distribute traffic

Stateless FastAPI
→ horizontal scaling

Redis
→ reduce repeated database reads

PostgreSQL
→ durable source of truth
```

______________________________________________________________________

# 70. Example: Asynchronous Report Generation

Requirement:

> Generate large reports without blocking API requests.

Architecture:

```text
Client
 ↓
FastAPI
 ↓
Queue
 ↓
Worker
 ↓
Database/Object Storage
```

Request:

```text
POST /reports
```

returns:

```text
202 Accepted
{
    "job_id": "..."
}
```

Client later checks:

```text
GET /reports/{job_id}
```

This is a classic asynchronous backend design.

______________________________________________________________________

# 71. Example: Protecting an External API

Requirement:

> Our API depends on a slow external service.

Use:

```text
FastAPI
 ↓
Timeout
 ↓
Retry with backoff
 ↓
Circuit breaker
 ↓
External service
```

If the dependency is repeatedly failing:

```text
Circuit opens
→ fail fast
```

This protects application resources.

______________________________________________________________________

# 72. System Design Trade-Offs

There is rarely one perfect architecture.

Examples:

### Cache

```text
Performance ↑
Freshness complexity ↑
```

### Replication

```text
Read capacity ↑
Operational complexity ↑
```

### Queue

```text
Decoupling ↑
Asynchronous complexity ↑
```

### Strong consistency

```text
Consistency ↑
Availability/latency trade-offs ↑
```

Senior engineers should explain these trade-offs explicitly.

______________________________________________________________________

# 73. Common System Design Mistakes

## Mistake 1 — Starting with technology

Bad:

> "Let's use Redis, Kafka and Kubernetes."

Better:

> "The requirement is high read volume, so caching may reduce database load."

Then select technology.

______________________________________________________________________

## Mistake 2 — Ignoring requirements

Without requirements, architecture becomes guesswork.

______________________________________________________________________

## Mistake 3 — Overengineering

Do not introduce distributed systems complexity without a requirement.

______________________________________________________________________

## Mistake 4 — Ignoring failure

Always ask:

```text
What happens if this dependency fails?
```

______________________________________________________________________

## Mistake 5 — Ignoring bottlenecks

Scaling the API does not help if:

```text
Database
```

is already the bottleneck.

______________________________________________________________________

## Mistake 6 — Treating retries as free

Retries consume resources and can amplify outages.

______________________________________________________________________

## Mistake 7 — Ignoring idempotency

Retries and duplicate messages can cause duplicate side effects.

______________________________________________________________________

# 74. System Design Interview Framework

Use this framework in interviews:

## 1. Requirements

```text
Functional
Non-functional
```

## 2. Scale

```text
Users
RPS
Storage
Read/write ratio
Peak traffic
```

## 3. High-Level Architecture

```text
Client
→ LB
→ API
→ Cache/DB/Queue
```

## 4. Data

```text
Schema
Storage
Indexes
Consistency
```

## 5. Scaling

```text
Horizontal scaling
Caching
Replication
Partitioning
```

## 6. Reliability

```text
Retries
Timeouts
Circuit breakers
Idempotency
Backups
```

## 7. Observability

```text
Metrics
Logs
Tracing
Alerts
```

## 8. Trade-Offs

Explain why you selected each major component.

______________________________________________________________________

# 75. Interview Questions & Answers

## Q1. What is the difference between functional and non-functional requirements?

**Answer:**

Functional requirements describe what the system does. Non-functional requirements describe qualities and constraints
such as latency, availability, reliability, throughput and scalability.

______________________________________________________________________

## Q2. Why do you perform capacity estimation?

**Answer:**

To understand the approximate workload and identify architectural requirements such as number of instances, database
capacity, cache size, bandwidth and queue capacity.

______________________________________________________________________

## Q3. Average traffic or peak traffic?

**Answer:**

Both. Average traffic helps understand normal capacity, while peak traffic determines whether the system can handle
expected bursts.

______________________________________________________________________

## Q4. What is horizontal scaling?

**Answer:**

Adding more service instances to handle additional workload rather than making one machine larger.

______________________________________________________________________

## Q5. Why are stateless services easier to scale?

**Answer:**

Any healthy instance can handle any request because important shared state is stored externally. This allows load
balancers to distribute requests across instances without depending heavily on local process state.

______________________________________________________________________

## Q6. What does a load balancer do?

**Answer:**

It distributes incoming traffic across available service instances and can often perform health checks and routing
decisions.

______________________________________________________________________

## Q7. Why is caching useful?

**Answer:**

It reduces latency and lowers load on the underlying data source by serving frequently accessed data from a faster
layer.

______________________________________________________________________

## Q8. What is the biggest challenge with caching?

**Answer:**

Cache invalidation and stale data. You must decide how fresh the cached value needs to be and how updates invalidate or
expire it.

______________________________________________________________________

## Q9. Why use a queue?

**Answer:**

To decouple producers and consumers, absorb bursts, process work asynchronously and support retryable background
processing.

______________________________________________________________________

## Q10. What happens if a consumer is slower than the producer?

**Answer:**

The queue backlog grows. You can respond with more consumers, autoscaling, batching, rate limiting, backpressure or load
shedding depending on the requirements.

______________________________________________________________________

## Q11. What is rate limiting?

**Answer:**

Rate limiting restricts how frequently a client or identity can perform operations within a defined policy, protecting
the system from abuse and overload.

______________________________________________________________________

## Q12. Why are timeouts important?

**Answer:**

They prevent requests from waiting indefinitely on unhealthy dependencies and help bound resource consumption.

______________________________________________________________________

## Q13. Why can retries be dangerous?

**Answer:**

Retries consume additional resources and can amplify an outage into a retry storm. They should use appropriate limits,
backoff and jitter and should only retry suitable failures.

______________________________________________________________________

## Q14. What is a circuit breaker?

**Answer:**

A mechanism that stops repeatedly calling a failing dependency and allows the caller to fail fast until the dependency
appears healthy again.

______________________________________________________________________

## Q15. Explain circuit-breaker states.

**Answer:**

Closed allows normal requests. Open rejects/fails fast without calling the dependency. Half-open allows limited test
traffic to determine whether recovery has occurred.

______________________________________________________________________

## Q16. What is idempotency?

**Answer:**

An operation is idempotent when repeating the same logical request produces the same intended final effect.

______________________________________________________________________

## Q17. Why is idempotency important for payments?

**Answer:**

A client may retry after a timeout even though the original payment succeeded. An idempotency key allows the server to
recognize the repeated logical operation and avoid charging twice.

______________________________________________________________________

## Q18. What is the difference between latency and throughput?

**Answer:**

Latency is the time taken by an operation. Throughput is how much work the system processes per unit time.

______________________________________________________________________

## Q19. Why are p95 and p99 useful?

**Answer:**

They expose tail latency that averages can hide. A system can have a good average while a significant small percentage
of requests are extremely slow.

______________________________________________________________________

## Q20. What is reliability?

**Answer:**

Reliability is the ability of a system to perform its intended function correctly and consistently over time, including
under expected failures.

______________________________________________________________________

## Q21. What is availability?

**Answer:**

Availability measures how often the system is accessible and able to respond successfully over a period.

______________________________________________________________________

## Q22. Can a system be available but unreliable?

**Answer:**

Yes. It can return responses consistently while producing incorrect results or failing to perform the intended business
operation correctly.

______________________________________________________________________

## Q23. What is CAP theorem?

**Answer:**

CAP describes a distributed-system trade-off among consistency, availability and partition tolerance. When a network
partition occurs, a system cannot simultaneously guarantee strong consistency and availability for all operations.

______________________________________________________________________

## Q24. What is the most common CAP interview mistake?

**Answer:**

Saying simply "choose any two." The important point is that during a partition, the system must trade off consistency
against availability.

______________________________________________________________________

## Q25. What is backpressure?

**Answer:**

Backpressure is a mechanism for handling a situation where downstream processing cannot keep up with incoming work.
Queues, bounded concurrency and rate limiting are examples of ways to manage it.

______________________________________________________________________

## Q26. What is graceful degradation?

**Answer:**

Continuing to provide core functionality while reducing or disabling non-critical features when dependencies or parts of
the system fail.

______________________________________________________________________

## Q27. What is load shedding?

**Answer:**

Intentionally rejecting or dropping lower-priority work during overload to protect critical system functionality.

______________________________________________________________________

## Q28. What would you monitor in a production API?

**Answer:**

Traffic/RPS, error rate, p50/p95/p99 latency, CPU, memory, connection pools, database latency/errors, cache hit rate,
queue depth/lag and dependency failures.

______________________________________________________________________

## Q29. Why are logs alone insufficient?

**Answer:**

Logs provide detailed events but are not always efficient for identifying aggregate trends. Metrics show system-level
behavior, while traces show request paths across distributed components. The three complement each other.

______________________________________________________________________

## Q30. What is a correlation/request ID?

**Answer:**

An identifier propagated across related operations so logs and traces from multiple components can be associated with
the same request or workflow.

______________________________________________________________________

## Q31. What should happen when Redis fails?

**Answer:**

It depends on the role of Redis. If it is a cache, the system may fall back to the database if capacity allows. If Redis
contains critical state, a different recovery strategy may be required. The key is to define the failure mode rather
than assuming Redis is always available.

______________________________________________________________________

## Q32. Why can a fallback cause another outage?

**Answer:**

If a cache fails and all traffic falls through to the database, the database may suddenly receive many more requests
than it was designed to handle.

______________________________________________________________________

## Q33. What is a retry storm?

**Answer:**

A situation where many clients or services repeatedly retry a failing dependency, increasing traffic to an already
unhealthy system and potentially making the outage worse.

______________________________________________________________________

## Q34. Why use exponential backoff with jitter?

**Answer:**

Backoff reduces retry frequency while jitter prevents many clients from retrying at exactly the same time, reducing
synchronized retry spikes.

______________________________________________________________________

## Q35. How would you design a slow operation?

**Answer:**

If the client does not need the result synchronously, I would consider asynchronous processing: accept the request,
create a job, enqueue it, process it with workers and expose job status/result separately.

______________________________________________________________________

## Q36. What makes a good system-design answer?

**Answer:**

A good answer starts with requirements and scale, proposes a simple architecture, explains data flow and bottlenecks,
addresses failure/reliability and observability, and explicitly discusses trade-offs.

______________________________________________________________________

# 76. Scenario Practice

## Scenario 1 — API Traffic Suddenly Doubles

Current:

```text
1,000 RPS
```

Traffic becomes:

```text
2,000 RPS
```

### Questions

What do you inspect first?

### Answer

Check:

```text
CPU
Memory
Latency
Error rate
Database load
Cache hit rate
Connection pools
```

Do not automatically add application instances. First identify the bottleneck.

______________________________________________________________________

## Scenario 2 — API Is Slow but CPU Is Low

### Question

What could be happening?

### Answer

Potential causes include:

```text
Database latency
Connection-pool exhaustion
Slow external API
Lock contention
Network latency
Queueing
```

CPU being low does not mean the system is healthy.

______________________________________________________________________

## Scenario 3 — Redis Goes Down

### Question

What should happen?

### Answer

If Redis is only a cache, fall back to the database if it can safely absorb the load. Add protections such as timeouts
and circuit-breaking as appropriate. If Redis contains authoritative state, the architecture needs a different failure
strategy.

______________________________________________________________________

## Scenario 4 — External Payment Service Is Timing Out

### Question

What would you add?

### Answer

At minimum:

```text
Timeout
```

Potentially:

```text
Limited retry
Exponential backoff + jitter
Circuit breaker
Idempotency
```

For payment operations, idempotency is particularly important before retrying.

______________________________________________________________________

## Scenario 5 — Queue Backlog Is Growing

### Question

What do you investigate?

### Answer

Check:

```text
Producer rate
Consumer rate
Consumer errors
Consumer concurrency
Processing latency
Downstream dependency latency
Queue capacity
```

Then determine whether to scale consumers, reduce incoming work, optimize processing or address the downstream
bottleneck.

______________________________________________________________________

## Scenario 6 — Database Is the Bottleneck

### Question

Would you immediately shard it?

### Answer

No. Start with simpler measures:

```text
Slow-query analysis
Indexes
Query optimization
Connection-pool tuning
Caching
Read replicas
```

Consider partitioning/sharding only when requirements justify the additional complexity.

______________________________________________________________________

# 77. Practical Design Exercise

Design:

> A backend API that receives user requests and generates a large report.

Start with:

```text
Client
 ↓
Load Balancer
 ↓
FastAPI
 ↓
Queue
 ↓
Worker
 ↓
Database
 ↓
Object Storage
```

Now answer:

### Requirements

```text
Can the report be asynchronous?
How long can generation take?
How many reports per minute?
How long are reports retained?
```

### Reliability

```text
What if worker crashes?
What if report generation fails?
Can the job be retried?
Is processing idempotent?
```

### Scaling

```text
Can workers scale horizontally?
What is the queue backlog?
Is the database the bottleneck?
```

### Observability

```text
Job duration
Queue depth
Failure rate
Worker utilization
Database latency
```

This exercise combines most of the concepts in this file.

______________________________________________________________________

# 78. Final Interview Readiness Checklist

Before moving to File 39, make sure you can:

- [ ] Explain system design.
- [ ] Separate functional and non-functional requirements.
- [ ] Ask useful clarification questions.
- [ ] Estimate requests per second.
- [ ] Estimate storage.
- [ ] Estimate bandwidth.
- [ ] Reason about peak vs average traffic.
- [ ] Explain scalability.
- [ ] Compare vertical and horizontal scaling.
- [ ] Explain stateless services.
- [ ] Explain why statelessness helps horizontal scaling.
- [ ] Explain load balancing.
- [ ] Explain health checks.
- [ ] Distinguish liveness and readiness.
- [ ] Explain caching.
- [ ] Explain cache hits/misses.
- [ ] Explain cache invalidation.
- [ ] Identify database bottlenecks.
- [ ] Explain queues.
- [ ] Explain workers.
- [ ] Compare synchronous and asynchronous processing.
- [ ] Explain rate limiting.
- [ ] Understand distributed rate limiting.
- [ ] Explain retry.
- [ ] Explain exponential backoff.
- [ ] Explain jitter.
- [ ] Explain timeouts.
- [ ] Explain retry/timeout interaction.
- [ ] Explain circuit breakers.
- [ ] Explain idempotency.
- [ ] Explain idempotency keys.
- [ ] Distinguish idempotency and deduplication.
- [ ] Explain reliability.
- [ ] Explain availability.
- [ ] Distinguish reliability and availability.
- [ ] Explain latency.
- [ ] Explain p50/p95/p99.
- [ ] Explain throughput.
- [ ] Explain backpressure.
- [ ] Explain load shedding.
- [ ] Explain graceful degradation.
- [ ] Explain CAP accurately.
- [ ] Explain monitoring.
- [ ] Explain metrics.
- [ ] Explain structured logging.
- [ ] Explain tracing.
- [ ] Explain correlation IDs.
- [ ] Identify architecture failure points.
- [ ] Explain fallback risks.
- [ ] Explain retry storms.
- [ ] Build a basic high-level backend architecture.
- [ ] Explain architecture trade-offs.
- [ ] Walk through a failure scenario.
- [ ] Communicate system design decisions clearly.

______________________________________________________________________

# 79. Final Takeaways

A strong system-design answer is not about drawing the largest architecture.

It is about reasoning from requirements:

```text
Requirements
→ Scale
→ Components
→ Data flow
→ Bottlenecks
→ Failure modes
→ Reliability
→ Observability
→ Trade-offs
```

Remember the core building blocks:

| Requirement | Common Building Block |
|---|---|
| Distribute traffic | Load balancer |
| Scale application | Stateless instances |
| Reduce read load | Cache |
| Persist data | Database |
| Handle async work | Queue + workers |
| Protect service | Rate limiting |
| Bound dependency waits | Timeout |
| Recover transient failures | Retry + backoff |
| Stop cascading failures | Circuit breaker |
| Prevent duplicate effects | Idempotency |
| Understand behavior | Metrics/logs/traces |
| Handle overload | Backpressure/load shedding |
| Improve resilience | Graceful degradation |

The senior-level habit is:

> **Every component should exist for a reason, every dependency should have a failure strategy, and every scaling decision should be tied to an actual bottleneck or requirement.**

The next topic goes deeper into the individual **backend architecture building blocks** and how they fit together in
production systems.

______________________________________________________________________

**Previous:** [37. DSA Coding Practice](./37-dsa-practice.md)

**Next:** [39. Backend Architecture Building Blocks](./39-system-design-building-blocks.md)
