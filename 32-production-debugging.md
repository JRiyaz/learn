# 32. Production Debugging & Incident Response

**Previous:** [31. Linux for Backend Engineers](./31-linux.md)

**Next:** [33. Backend Security](./33-security.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Debug production incidents systematically instead of guessing.
- Separate symptoms from root causes.
- Build a repeatable debugging workflow.
- Diagnose CPU saturation.
- Investigate memory growth and memory pressure.
- Diagnose full disks.
- Investigate slow APIs.
- Understand and debug HTTP 502/503 errors.
- Diagnose database connectivity failures.
- Investigate database connection-pool exhaustion.
- Diagnose Redis failures.
- Investigate Kafka consumer lag.
- Handle duplicate messages safely.
- Diagnose unexpected container restarts.
- Debug network problems layer by layer.
- Recognize and investigate deadlocks.
- Use logs, metrics, traces and system-level signals together.
- Communicate clearly during an incident.
- Apply safe mitigation before attempting deeper root-cause fixes.
- Perform a post-incident review.

______________________________________________________________________

# 1. Production Debugging Mindset

Production debugging is different from debugging locally.

In production:

- Users are affected.
- Data may be changing.
- Multiple services may be involved.
- Reproducing the issue may be difficult.
- Restarting a service may hide evidence.
- A seemingly harmless change can increase the impact.

The goal is therefore not:

> "Find something that looks suspicious."

The goal is:

> **Establish what is failing, determine where the failure occurs, reduce impact safely, and identify the root cause using evidence.**

______________________________________________________________________

# 2. Symptom vs Root Cause

Suppose users report:

```text
API is slow
```

That is a symptom.

Possible causes include:

```text
CPU saturation
Database slow query
Database connection pool exhaustion
Redis latency
External API latency
Network issue
Lock contention
Garbage collection pressure
Traffic spike
```

Do not treat the first visible symptom as the root cause.

______________________________________________________________________

# 3. Incident Debugging Loop

A useful repeatable loop is:

```text
Observe
  ↓
Scope impact
  ↓
Form hypothesis
  ↓
Collect evidence
  ↓
Test hypothesis
  ↓
Mitigate
  ↓
Verify
  ↓
Find root cause
  ↓
Prevent recurrence
```

Do not skip the verification step.

______________________________________________________________________

# 4. Step 1 — Confirm the Incident

Before making changes, establish:

- Is the alert real?
- Which service is affected?
- When did it start?
- Are all users affected?
- Which endpoints are affected?
- Is the issue still happening?
- Did a recent deployment occur?

Avoid immediately assuming the alert tells you the cause.

______________________________________________________________________

# 5. Step 2 — Determine Impact

Ask:

```text
How many requests are failing?
How many users are affected?
Which regions?
Which endpoints?
Read operations or writes?
One service or many?
```

A backend incident can be:

```text
Single endpoint
→ Single service
→ Dependency
→ Entire system
```

Understanding blast radius helps prioritize mitigation.

______________________________________________________________________

# 6. Step 3 — Establish a Timeline

Create a simple timeline:

```text
14:05 → deployment
14:08 → latency increases
14:10 → error rate increases
14:12 → alert fires
14:15 → rollback begins
```

Correlating the first symptom with recent changes is extremely valuable.

______________________________________________________________________

# 7. Step 4 — Check Recent Changes

Common changes include:

- Application deployment
- Configuration change
- Database migration
- Infrastructure change
- Dependency upgrade
- Traffic increase
- Feature flag
- External service change

A recent change is a hypothesis, not proof.

______________________________________________________________________

# 8. Step 5 — Check Golden Signals

A useful high-level framework is:

```text
Latency
Traffic
Errors
Saturation
```

### Latency

How long requests take.

### Traffic

How much work is arriving.

### Errors

How much work is failing.

### Saturation

How close resources are to their limits.

______________________________________________________________________

# 9. Observability

Production debugging usually combines:

```text
Logs
Metrics
Traces
```

### Logs

Detailed event information.

### Metrics

Numerical measurements over time.

### Traces

Request flow across services.

A strong engineer uses all three rather than relying only on logs.

______________________________________________________________________

# 10. Logs

Logs answer:

> What happened?

Useful fields include:

```text
timestamp
request ID
trace ID
user/request context where appropriate
endpoint
status code
latency
exception
dependency
```

Avoid logging sensitive data unnecessarily.

______________________________________________________________________

# 11. Metrics

Metrics answer:

> How much? How often? How long?

Useful backend metrics include:

```text
request rate
error rate
latency
CPU
memory
database connections
connection-pool utilization
Redis latency
Kafka consumer lag
queue depth
```

______________________________________________________________________

# 12. Traces

Distributed tracing helps answer:

> Where did this request spend its time?

For example:

```text
API
 ↓ 20ms
Auth
 ↓ 10ms
Service
 ↓ 800ms
Database
```

The database call becomes the strongest latency hypothesis.

______________________________________________________________________

# 13. Request Correlation

A request ID or trace ID allows related events to be connected.

Example:

```text
Request ID: abc123

API log
 ↓
Service log
 ↓
Database operation
 ↓
Error
```

Without correlation identifiers, debugging distributed systems becomes significantly harder.

______________________________________________________________________

# 14. CPU at 100%

Suppose:

```text
CPU = 100%
API latency = high
Error rate = increasing
```

Possible causes include:

- Infinite/expensive loops
- CPU-heavy serialization
- Large computations
- Excessive concurrency
- Traffic spike
- Memory pressure causing additional CPU work
- Inefficient algorithm
- Unexpected workload

Do not assume CPU is the root cause until you establish what is consuming it.

______________________________________________________________________

# 15. CPU Debugging Workflow

Start with:

```text
1. Identify affected hosts/containers.
2. Identify CPU-consuming processes.
3. Compare traffic with normal traffic.
4. Check recent deployments.
5. Check application metrics.
6. Investigate hot endpoints.
7. Determine whether work is CPU-bound.
8. Profile if necessary.
```

For Linux:

```bash
top
ps aux --sort=-%cpu | head
```

______________________________________________________________________

# 16. CPU Saturation in Python

For Python backends, investigate:

- Expensive loops
- Large JSON serialization
- Compression
- Data processing
- Regex-heavy operations
- Excessive object creation
- CPU-bound synchronous code inside request handlers

If work is genuinely CPU-bound, adding more threads may not solve the problem in CPython.

______________________________________________________________________

# 17. CPU Mitigation

Possible mitigations include:

- Roll back a bad deployment.
- Reduce expensive traffic.
- Disable a problematic feature.
- Scale appropriate workers.
- Move CPU-heavy work to background/process-based execution.
- Optimize the hot code path.

Choose mitigation based on evidence.

______________________________________________________________________

# 18. Memory Growth

Symptoms:

```text
Memory continuously increases
Requests become slower
Container restarts
OOM events
```

Possible causes:

- Memory leak
- Unbounded cache
- Large in-memory collections
- Large query results
- Excessive buffering
- Too many concurrent requests
- Objects retained unexpectedly
- Dependency-level memory issue

______________________________________________________________________

# 19. Memory Debugging Workflow

Check:

```bash
free -h
ps aux --sort=-%mem | head
```

For containers, also inspect:

```text
container memory usage
memory limit
restart history
OOM events
```

Then correlate memory growth with:

```text
traffic
request size
endpoint
deployment
background jobs
cache behavior
```

______________________________________________________________________

# 20. Python Memory Investigation

Ask:

```text
Is memory increasing continuously?
Does it return after traffic decreases?
Does it increase only for a specific endpoint?
Is a cache unbounded?
Are large objects retained?
```

Potential tools include:

```text
tracemalloc
memory profilers
application metrics
heap/object inspection
```

Use profiling carefully in production because instrumentation itself can have overhead.

______________________________________________________________________

# 21. OOM vs Memory Leak

These are not identical.

### OOM

The system/process exceeds available memory or its configured memory limit.

### Memory leak

Memory that should become reclaimable remains referenced or otherwise retained.

A memory leak can eventually cause OOM, but not every OOM is caused by a leak.

______________________________________________________________________

# 22. Disk Full

Symptoms:

```text
No space left on device
Database writes fail
Logs stop
Application errors
Containers fail
```

Possible causes:

- Logs
- Temporary files
- Database growth
- Core dumps
- Container storage
- Large uploads
- Backups
- Deleted-but-open files

______________________________________________________________________

# 23. Disk Debugging Workflow

Start with:

```bash
df -h
```

Then:

```bash
du -sh /var/*
```

Investigate:

```text
Logs
Temporary files
Container storage
Database data
Backups
Deleted-but-open files
```

Do not blindly delete production data.

______________________________________________________________________

# 24. Deleted-but-Open Files

A process may continue holding a deleted file open.

The directory entry disappears, but disk space can remain allocated until the process closes the file.

This can explain:

```text
df → filesystem nearly full
du → expected files don't explain usage
```

Investigate with:

```bash
lsof
```

______________________________________________________________________

# 25. Slow APIs

A slow API is a symptom, not a diagnosis.

Possible causes:

```text
Application CPU
Database query
Connection pool
Redis
External API
Network
Lock contention
Serialization
Large response
GC/memory pressure
```

______________________________________________________________________

# 26. Slow API Debugging

Start with:

```text
Request latency
    ↓
Endpoint
    ↓
Trace
    ↓
Application time
    ↓
Database time
    ↓
Cache time
    ↓
External dependency time
```

Find where the time is actually spent.

______________________________________________________________________

# 27. Latency Percentiles

Do not rely only on average latency.

Useful metrics include:

```text
p50
p95
p99
```

### p50

Median request latency.

### p95

95% of requests are at or below this latency.

### p99

99% are at or below this latency.

Tail latency is particularly important for backend systems.

______________________________________________________________________

# 28. Slow API Scenario

Suppose:

```text
Average latency → 100ms
p99 latency → 5s
```

The average can look healthy while a small percentage of users experience severe delays.

Investigate the slow request population rather than relying on the average.

______________________________________________________________________

# 29. Database Slow Query

If tracing shows:

```text
API
 ↓
Database
 ↓
2.5 seconds
```

investigate:

- Query plan
- Indexes
- Locking
- Connection acquisition
- Data volume
- Database CPU
- Database I/O

Use `EXPLAIN`/query-plan tooling as appropriate.

______________________________________________________________________

# 30. Connection Acquisition vs Query Execution

An important distinction:

```text
Get connection from pool
        ↓
Execute SQL
        ↓
Receive result
```

A request may be slow before the SQL even starts.

If the pool is exhausted, the application can spend significant time waiting for a connection.

______________________________________________________________________

# 31. 502 Bad Gateway

A `502` generally indicates that a gateway/proxy received an invalid or unsuccessful response from an upstream server.

Possible causes include:

- Upstream process crashed
- Upstream connection failure
- Invalid upstream response
- Protocol mismatch
- Proxy configuration issue

Do not treat every 502 as an application bug.

______________________________________________________________________

# 32. 503 Service Unavailable

A `503` generally indicates that the service is currently unavailable.

Possible causes include:

- No healthy upstreams
- Service overloaded
- Readiness failure
- Maintenance
- Dependency/service failure
- Load balancer cannot route traffic

The exact behavior depends on the proxy/load-balancer architecture.

______________________________________________________________________

# 33. 502 vs 503

A useful interview-level distinction:

| Status | Typical Meaning |
|---|---|
| 502 | Gateway/proxy got a bad/unusable upstream response |
| 503 | Service is unavailable or has no usable capacity/upstream |

Always inspect the actual architecture and proxy logs before concluding the cause.

______________________________________________________________________

# 34. Debugging 502/503

Follow the request path:

```text
Client
 ↓
CDN/WAF
 ↓
Load Balancer
 ↓
Reverse Proxy
 ↓
Application
```

Check each layer:

```text
Is upstream healthy?
Is it reachable?
Is the correct port configured?
Are health checks passing?
Are timeouts too aggressive?
Did the application crash?
Are all workers overloaded?
```

______________________________________________________________________

# 35. Database Unavailable

Symptoms:

```text
Connection refused
Timeout
Authentication failure
Too many connections
Requests fail
```

Possible causes:

- Database down
- Network issue
- DNS issue
- Firewall/security rule
- Connection exhaustion
- Credential/configuration problem
- Database overloaded

______________________________________________________________________

# 36. Database Availability Debugging

Separate the problem into layers:

```text
DNS
 ↓
Network
 ↓
TCP connection
 ↓
Database protocol
 ↓
Authentication
 ↓
Query
```

Do not jump directly to SQL debugging if TCP connectivity is already failing.

______________________________________________________________________

# 37. Connection Pool

A connection pool maintains reusable database connections.

Conceptually:

```text
Requests
   ↓
Connection Pool
   ↓
Database
```

Benefits:

- Avoid connection setup for every request.
- Limit database connection count.
- Reuse connections.

______________________________________________________________________

# 38. Connection Pool Exhaustion

Suppose:

```text
Pool size = 20
Concurrent DB work = 100
```

Only a limited number of requests can acquire connections at once.

Others wait.

Symptoms may include:

```text
High API latency
Connection timeout
Low/normal database CPU
High application wait time
```

This is a very important distinction.

______________________________________________________________________

# 39. Pool Exhaustion Debugging

Check:

```text
Pool size
Active connections
Idle connections
Wait time
Connection acquisition timeout
Long-running transactions
Slow queries
Request concurrency
```

Then ask:

> Why are connections not becoming available?

Possible causes:

- Slow queries
- Long transactions
- Connection leaks
- Pool too small
- Excessive application concurrency
- Database overload

______________________________________________________________________

# 40. Connection Leak

A connection leak occurs when application code acquires a resource and fails to return/release it correctly.

For database connections:

```text
Acquire
  ↓
Use
  ↓
Exception
  ↓
Connection never returned
```

Eventually:

```text
Pool exhausted
```

Use proper context management and framework/session lifecycle handling.

______________________________________________________________________

# 41. Redis Unavailable

Symptoms:

```text
Cache misses increase
Connection errors
Timeouts
API latency increases
Background jobs fail
```

First determine whether Redis is:

```text
Required for correctness
```

or:

```text
Only a performance optimization
```

This affects the appropriate failure behavior.

______________________________________________________________________

# 42. Redis Failure Modes

Possible causes:

- Redis process down
- Network failure
- DNS failure
- Connection exhaustion
- Memory pressure
- Slow commands
- Failover
- Configuration issue

______________________________________________________________________

# 43. Cache Failure Strategy

If Redis is only a cache, a resilient application may:

```text
Redis unavailable
      ↓
Cache miss/failure
      ↓
Fallback to database
```

But this can create a second problem:

```text
Redis fails
 ↓
All requests hit DB
 ↓
Database overload
```

This is a classic cascading failure scenario.

______________________________________________________________________

# 44. Redis Debugging

Investigate:

```text
Redis availability
Network connectivity
Latency
Command performance
Connection count
Memory
Eviction
Application timeout
Error rate
```

Avoid increasing timeouts blindly because it can increase request accumulation.

______________________________________________________________________

# 45. Kafka Consumer Lag

Consumer lag represents how far a consumer is behind the available Kafka data.

Conceptually:

```text
Producer
   ↓
Kafka partition
   ↓
Consumer
```

If producers continue writing faster than consumers process:

```text
Lag ↑
```

______________________________________________________________________

# 46. Causes of Kafka Consumer Lag

Possible causes:

- Consumer processing too slowly
- Consumer crashed
- Too few consumers
- Expensive database operations
- External API latency
- Large messages
- Rebalancing
- Partition constraints
- Consumer errors/retries

______________________________________________________________________

# 47. Kafka Lag Debugging

Check:

```text
Lag by partition
Consumer group membership
Consumer health
Processing latency
Error/retry rate
Partition count
Consumer count
Downstream dependency latency
```

Do not automatically add consumers without considering partition count and downstream capacity.

______________________________________________________________________

# 48. Partition Parallelism

Kafka consumer parallelism is constrained by partitions.

For a topic with:

```text
3 partitions
```

a consumer group cannot actively process more than approximately:

```text
3 partition assignments
```

at the same time.

Adding 20 consumers to a 3-partition topic does not provide 20-way partition parallelism.

______________________________________________________________________

# 49. Kafka Lag Caused by Database

A consumer might process:

```text
Kafka message
   ↓
Database operation
   ↓
500ms
```

If message arrival is faster than processing capacity, lag increases.

The root cause may therefore be the database rather than Kafka itself.

______________________________________________________________________

# 50. Duplicate Messages

Distributed systems commonly require duplicate-message handling.

A message may be delivered more than once because of:

```text
Consumer crash
Timeout
Retry
Offset handling
Network failure
```

Therefore consumers should often be designed to tolerate duplicates.

______________________________________________________________________

# 51. Idempotent Message Processing

Suppose:

```text
Payment ID = 123
```

A consumer receives the same event twice.

Instead of blindly creating two payments, use an idempotency mechanism such as:

```text
Unique business/event ID
```

and enforce the invariant in the database where appropriate.

______________________________________________________________________

# 52. Duplicate Message Debugging

Ask:

```text
Was the message actually produced twice?
Was it delivered twice?
Was it processed twice?
Did the first processing commit successfully?
When was the offset committed?
Did the consumer crash between processing and offset commit?
```

Do not assume duplicate production when the real issue is duplicate delivery/reprocessing.

______________________________________________________________________

# 53. At-Least-Once Processing

At-least-once delivery means a message may be processed more than once.

This makes idempotency important.

A typical flow:

```text
Receive message
   ↓
Process
   ↓
Commit business transaction
   ↓
Commit/advance offset
```

The exact design depends on the system and delivery semantics.

______________________________________________________________________

# 54. Container Restart

If a production container keeps restarting, determine:

```text
Why did it exit?
```

Possible causes:

- Application crash
- OOM
- Failed health check
- Configuration error
- Dependency startup issue
- Host/resource issue
- Deployment
- Orchestrator behavior

______________________________________________________________________

# 55. Container Restart Debugging

Check:

```text
Container state
Exit code
Logs
Restart count
Health status
Memory limit
CPU
Environment
Recent deployment
```

A restart is an event to investigate, not automatically a solution.

______________________________________________________________________

# 56. Exit Codes

An application process can exit with a status code.

A non-zero exit often indicates failure, but interpretation depends on the application.

Combine:

```text
exit code
+
logs
+
termination reason
```

to determine what happened.

______________________________________________________________________

# 57. Health Check Failures

A container can restart because a health check fails.

Determine:

```text
Is the process actually unhealthy?
Or is the health check itself incorrect?
```

A health endpoint that depends on an unstable external service can cause unnecessary restarts.

______________________________________________________________________

# 58. Network Problems

Network incidents can occur at multiple layers:

```text
DNS
 ↓
Routing
 ↓
TCP
 ↓
TLS
 ↓
HTTP
 ↓
Application protocol
```

Debug layer by layer.

______________________________________________________________________

# 59. DNS Problem

Test:

```bash
dig service.example.com
```

If DNS cannot resolve the hostname, continue investigating DNS before debugging the application.

______________________________________________________________________

# 60. TCP Problem

If DNS works, determine whether the TCP port is reachable.

Useful tools can include:

```bash
ss
curl
nc
```

depending on what is available and permitted in the environment.

______________________________________________________________________

# 61. TLS Problem

If TCP succeeds but HTTPS fails, investigate:

- Certificate validity
- Certificate chain
- Hostname mismatch
- TLS versions/ciphers
- Proxy configuration
- Trust store

Use appropriate TLS diagnostics and verbose HTTP clients.

______________________________________________________________________

# 62. HTTP Problem

If TCP/TLS work but requests fail:

```text
Check HTTP status
Check headers
Check response body
Check proxy logs
Check application logs
```

This separates transport problems from application-level problems.

______________________________________________________________________

# 63. Deadlocks

A deadlock occurs when multiple execution paths wait indefinitely for resources held by each other.

Conceptually:

```text
Thread A
  holds Lock 1
  waits for Lock 2

Thread B
  holds Lock 2
  waits for Lock 1
```

Neither can continue.

______________________________________________________________________

# 64. Deadlock Conditions

The classic conditions include:

- Mutual exclusion
- Hold and wait
- No preemption
- Circular wait

Breaking one of these conditions can prevent a deadlock.

______________________________________________________________________

# 65. Database Deadlocks

Databases can also experience deadlocks.

Example:

```text
Transaction A locks row 1
Transaction B locks row 2

A waits for row 2
B waits for row 1
```

Many databases detect deadlocks and abort one transaction.

Applications should handle the resulting transaction failure appropriately.

______________________________________________________________________

# 66. Application-Level Deadlock

Application code can deadlock when locks are acquired inconsistently.

Bad pattern:

```text
Function A:
  lock A
  lock B

Function B:
  lock B
  lock A
```

Prefer a consistent lock acquisition order.

______________________________________________________________________

# 67. Deadlock Debugging

Look for:

```text
Requests stuck
Threads waiting
Locks held
Database lock waits
Long transactions
Circular dependencies
```

Use database lock views, thread dumps, application diagnostics and traces where appropriate.

______________________________________________________________________

# 68. Cascading Failures

One service failure can create failures elsewhere.

Example:

```text
Redis fails
   ↓
Cache misses
   ↓
Database traffic increases
   ↓
DB becomes overloaded
   ↓
Connection pool exhausts
   ↓
API latency increases
   ↓
Requests time out
   ↓
Retries increase traffic
```

This is why production debugging must consider the entire dependency graph.

______________________________________________________________________

# 69. Retry Storms

Retries can amplify an incident.

Suppose:

```text
Dependency slow
 ↓
Requests timeout
 ↓
Clients retry
 ↓
Traffic doubles
 ↓
Dependency becomes slower
```

Use:

- Exponential backoff
- Jitter
- Maximum retry attempts
- Appropriate timeouts
- Circuit-breaking/failure isolation where applicable

Retries should not be infinite.

______________________________________________________________________

# 70. Timeout Design

Timeouts prevent requests from waiting forever.

Common layers include:

```text
Connect timeout
Read timeout
Request timeout
Database timeout
Redis timeout
External API timeout
```

A timeout should be aligned with the business operation and upstream/downstream timeout budgets.

______________________________________________________________________

# 71. Retry vs Timeout

A retry without a timeout can block indefinitely.

A timeout without appropriate retry behavior may fail transient operations unnecessarily.

A robust design considers:

```text
Timeout
+
Retry limit
+
Backoff
+
Jitter
+
Idempotency
```

______________________________________________________________________

# 72. Circuit Breaker Concept

A circuit breaker can stop repeatedly calling a failing dependency.

Conceptually:

```text
Healthy
  ↓
Failure threshold
  ↓
Open
  ↓
Stop calls
  ↓
Recovery test
  ↓
Closed
```

The exact implementation depends on the application architecture.

______________________________________________________________________

# 73. Graceful Degradation

When a dependency fails, the application may provide reduced functionality instead of total failure.

Examples:

```text
Recommendation service unavailable
→ Return response without recommendations

Analytics service unavailable
→ Queue/ignore analytics temporarily

Cache unavailable
→ Read from database
```

Only use fallback behavior when correctness and load characteristics permit it.

______________________________________________________________________

# 74. Fail-Fast vs Fail-Safe

### Fail-fast

Stop quickly when a required dependency cannot complete.

Useful when waiting longer cannot produce a useful response.

### Fail-safe/degraded

Continue with reduced functionality when possible.

The correct approach depends on whether the dependency is:

```text
critical for correctness
```

or:

```text
optional for functionality
```

______________________________________________________________________

# 75. Incident Mitigation

During an incident, mitigation can include:

- Rollback
- Disable feature flag
- Reduce traffic
- Scale service
- Fail over dependency
- Temporarily disable non-critical work
- Increase capacity
- Stop problematic consumers
- Reduce retry volume

Mitigation should reduce impact without creating a larger problem.

______________________________________________________________________

# 76. Rollback

If a deployment clearly correlates with the incident:

```text
Previous version
      ↑
Current version → incident
```

Rollback may be appropriate.

But preserve evidence where possible so the root cause can still be investigated.

______________________________________________________________________

# 77. Feature Flags

Feature flags allow risky functionality to be disabled without a full deployment.

For example:

```text
New recommendation engine
        ↓
Feature flag
        ↓
ON / OFF
```

This can significantly reduce incident impact.

______________________________________________________________________

# 78. Incident Communication

A good incident update should state:

```text
Impact
Current status
What is known
What is being investigated
Current mitigation
Next update
```

Avoid speculation presented as fact.

Example:

> "API p99 latency increased from 300ms to 4s beginning at 14:10. The issue currently affects the checkout endpoint. We are investigating database connection-pool utilization after a deployment at 14:05."

______________________________________________________________________

# 79. Incident Severity

Severity classification varies by organization, but generally consider:

- Number of users affected
- Revenue/business impact
- Data integrity
- Security impact
- Duration
- Availability
- Regulatory impact

Severity determines escalation and response urgency.

______________________________________________________________________

# 80. Preserve Evidence

During an incident, avoid destructive actions that erase evidence unnecessarily.

Examples:

```text
Do not immediately delete logs.
Do not immediately kill every process.
Do not repeatedly restart without collecting evidence.
Do not modify multiple variables simultaneously if avoidable.
```

Capture relevant:

```text
logs
metrics
timestamps
deployment versions
configuration changes
process/resource state
```

______________________________________________________________________

# 81. Change One Variable at a Time

When diagnosing a complex incident, changing many things simultaneously makes causality harder to establish.

Prefer:

```text
Hypothesis
 ↓
One controlled change
 ↓
Observe
 ↓
Verify
```

unless immediate mitigation requires multiple coordinated actions.

______________________________________________________________________

# 82. Production Debugging Decision Tree

Use this simplified mental model:

```text
Is the request failing?
        ↓
Which layer?
        ↓
Client / Network / Proxy / App / Dependency
        ↓
Is the process healthy?
        ↓
Are resources saturated?
        ↓
Are dependencies healthy?
        ↓
Is there a recent change?
        ↓
What evidence confirms the hypothesis?
```

______________________________________________________________________

# 83. CPU Incident Example

### Symptom

```text
CPU = 100%
p99 latency = 5s
```

### Investigation

```text
top
 ↓
API workers consume CPU
 ↓
One endpoint has traffic spike
 ↓
Endpoint performs expensive serialization
```

### Mitigation

Temporarily reduce traffic or disable the expensive feature if possible.

### Root cause

An application change caused unexpectedly expensive processing for large responses.

### Prevention

- Benchmark large payloads.
- Add latency/CPU metrics by endpoint.
- Add regression tests.
- Optimize serialization.
- Establish payload limits.

______________________________________________________________________

# 84. Memory Incident Example

### Symptom

```text
Memory steadily increases
container restarts
```

### Investigation

```text
Memory metric
 ↓
Specific worker grows continuously
 ↓
Traffic pattern correlates with upload endpoint
 ↓
Large objects retained after requests
```

### Mitigation

Reduce traffic to the endpoint or roll back the change.

### Root cause

Unexpected object retention.

### Prevention

Add memory regression testing, limits, monitoring and appropriate resource lifecycle management.

______________________________________________________________________

# 85. Slow API Incident Example

### Symptom

```text
p95 = 3s
```

### Trace

```text
API → 20ms
Redis → 10ms
DB → 2.8s
```

### Investigation

Database query plan reveals a missing/ineffective index.

### Mitigation

Depending on risk, reduce affected traffic or apply a safe database optimization.

### Prevention

Query performance testing and monitoring.

______________________________________________________________________

# 86. Connection Pool Incident Example

### Symptom

```text
API latency = high
DB CPU = normal
```

### Investigation

```text
Pool utilization = 100%
Connection wait time = high
```

Then discover long-running transactions.

### Root cause

Connections remain occupied longer than expected.

### Prevention

- Transaction scope review
- Query optimization
- Connection timeout
- Pool monitoring
- Proper session lifecycle

______________________________________________________________________

# 87. Redis Incident Example

### Symptom

```text
Redis unavailable
DB traffic spikes
```

### Investigation

Redis is only a cache.

### Risk

Fallback requests overload PostgreSQL.

### Mitigation

Protect the database using:

- Request throttling
- Cache fallback controls
- Rate limits
- Load shedding
- Temporary feature degradation

The correct mitigation depends on the system.

______________________________________________________________________

# 88. Kafka Incident Example

### Symptom

```text
Consumer lag increases rapidly
```

### Investigation

```text
Consumer healthy
 ↓
Processing latency increased
 ↓
Database calls now take 1s
```

### Root cause

Downstream database slowdown.

### Lesson

Kafka lag can be a downstream symptom rather than a Kafka infrastructure failure.

______________________________________________________________________

# 89. Duplicate Message Incident Example

### Symptom

A customer receives duplicate processing.

### Investigation

```text
Consumer processed event
 ↓
Database transaction committed
 ↓
Consumer crashed before offset commit
 ↓
Message delivered again
```

### Root cause

At-least-once processing without sufficient idempotency.

### Prevention

Use an idempotency key/business event ID and enforce uniqueness appropriately.

______________________________________________________________________

# 90. Container Restart Incident Example

### Symptom

```text
Container restart count increasing
```

### Investigation

```text
Container logs
 ↓
OOM termination
 ↓
Memory limit reached
```

### Root cause

Memory usage exceeded container capacity.

### Prevention

Investigate application memory behavior and configure appropriate capacity/limits.

Do not simply increase memory without understanding why usage grew.

______________________________________________________________________

# 91. Network Incident Example

### Symptom

```text
API cannot reach dependency
```

### Investigation

```text
DNS → works
TCP → fails
```

Therefore:

```text
Not primarily an application authentication problem.
```

Investigate:

- Routing
- Firewall
- Security rules
- Listening service
- Network policy

______________________________________________________________________

# 92. Deadlock Incident Example

### Symptom

```text
Requests hang
Database CPU normal
```

### Investigation

Database lock inspection shows:

```text
Transaction A → waits for B
Transaction B → waits for A
```

### Root cause

Circular lock dependency.

### Prevention

- Consistent lock ordering
- Shorter transactions
- Appropriate indexes
- Retry handling for aborted transactions
- Avoid unnecessary locking

______________________________________________________________________

# 93. Production Debugging Checklist

When an incident occurs, ask:

### Scope

- What is broken?
- Who is affected?
- When did it start?

### Application

- Are processes healthy?
- Are requests failing?
- Which endpoints?

### Resources

- CPU?
- Memory?
- Disk?
- File descriptors?

### Network

- DNS?
- TCP?
- TLS?
- HTTP?

### Dependencies

- Database?
- Redis?
- Kafka?
- External APIs?

### Changes

- Deployment?
- Configuration?
- Migration?
- Feature flag?

### Observability

- Logs?
- Metrics?
- Traces?

### Mitigation

- Rollback?
- Disable feature?
- Scale?
- Fail over?
- Degrade?

### Prevention

- Root cause?
- Monitoring gap?
- Test gap?
- Capacity problem?
- Design problem?

______________________________________________________________________

# 94. Common Debugging Mistakes

## Mistake 1 — Restart first

A restart can remove evidence and hide the real problem.

## Mistake 2 — Assume the alert identifies the cause

Alerts usually describe symptoms.

## Mistake 3 — Look only at application logs

The problem may be infrastructure, network or a dependency.

## Mistake 4 — Look only at infrastructure metrics

The CPU may be high because of an application regression.

## Mistake 5 — Increase every timeout

This can increase resource consumption and make cascading failures worse.

## Mistake 6 — Add retries everywhere

Retries can create retry storms.

## Mistake 7 — Scale without checking the bottleneck

Adding API instances can overload the database.

## Mistake 8 — Treat every duplicate message as duplicate production

The message may have been redelivered after successful processing.

## Mistake 9 — Delete evidence

Logs and state can be critical for root-cause analysis.

## Mistake 10 — Fix the symptom permanently without understanding it

A temporary mitigation is not necessarily a root-cause fix.

______________________________________________________________________

# 95. Interview Questions & Answers

## Q1. What is your general production debugging methodology?

**Answer:**

"I first confirm the incident and scope its impact. Then I establish a timeline and check recent changes. I inspect the
golden signals—latency, traffic, errors and saturation—and correlate logs, metrics and traces. I isolate the failing
layer, form hypotheses and collect evidence to validate them. I apply the safest mitigation that reduces user impact,
verify recovery and then perform root-cause analysis and prevention work."

______________________________________________________________________

## Q2. What do you check when CPU reaches 100%?

**Answer:**

I identify the affected process/containers, determine whether traffic changed, check recent deployments and identify
which endpoint or workload is consuming CPU. Then I determine whether the work is legitimately CPU-bound, an inefficient
code path, an infinite loop or another resource-pressure symptom.

______________________________________________________________________

## Q3. How do you debug memory growth?

**Answer:**

I determine whether the growth is system-wide or isolated to a process/container, correlate it with traffic and
endpoints, check limits/OOM events and investigate unbounded caches, large objects, buffering and object retention. For
Python, tools such as `tracemalloc` can help identify allocation patterns.

______________________________________________________________________

## Q4. How do you debug a full disk?

**Answer:**

Start with `df -h` to determine filesystem usage, then use `du` to locate large directories. Investigate logs, temporary
files, database/container storage and deleted-but-open files. I avoid blindly deleting production data.

______________________________________________________________________

## Q5. How do you debug a slow API?

**Answer:**

I start with latency percentiles and identify the affected endpoint. Then I use traces and dependency timings to
determine whether time is spent in application code, database access, Redis, external APIs, network calls or connection
acquisition.

______________________________________________________________________

## Q6. What is the difference between p50 and p99 latency?

**Answer:**

p50 is the median latency, while p99 represents the latency threshold below which approximately 99% of requests
complete. p99 exposes tail-latency problems that averages can hide.

______________________________________________________________________

## Q7. What does a 502 usually mean?

**Answer:**

It generally means a gateway or proxy received an invalid or unsuccessful response from an upstream service. Possible
causes include upstream failure, connection problems or proxy/protocol issues.

______________________________________________________________________

## Q8. What does a 503 usually mean?

**Answer:**

It generally means the service is unavailable or has no usable capacity/upstream. It can occur because of unhealthy
instances, overload or readiness/failover conditions.

______________________________________________________________________

## Q9. How would you debug a 502?

**Answer:**

I trace the request path from client through proxy/load balancer to the upstream. I check upstream health, connectivity,
ports, proxy logs, application logs, worker state and timeout/protocol configuration.

______________________________________________________________________

## Q10. How would you debug a 503?

**Answer:**

I check whether healthy upstream instances exist, whether readiness checks are failing, whether the service is
overloaded and whether a load balancer or reverse proxy is rejecting traffic.

______________________________________________________________________

## Q11. How do you debug a database outage?

**Answer:**

I separate DNS, network, TCP, authentication and query-level failures. I check database health, connection capacity,
application connection pools, credentials/configuration and database resource utilization.

______________________________________________________________________

## Q12. What is connection-pool exhaustion?

**Answer:**

It occurs when all available connections in the application's pool are occupied and new requests must wait or time out.
Causes can include slow queries, long transactions, connection leaks, excessive concurrency or an undersized pool.

______________________________________________________________________

## Q13. How can you distinguish database overload from pool exhaustion?

**Answer:**

With pool exhaustion, application connection-wait time can be high even when database CPU is relatively normal. Database
overload usually shows database-side resource pressure or slow query execution. Both can also occur together.

______________________________________________________________________

## Q14. What causes connection leaks?

**Answer:**

A connection can remain checked out because application code or resource lifecycle management does not release it,
particularly on exceptional paths. Proper session/context management and monitoring help prevent this.

______________________________________________________________________

## Q15. How would you debug Redis being unavailable?

**Answer:**

I verify Redis process/service availability, DNS and network connectivity, connection counts, latency and memory
behavior. I also determine whether Redis is required for correctness or is only a cache because that changes the
appropriate fallback strategy.

______________________________________________________________________

## Q16. What happens if Redis fails and it is only a cache?

**Answer:**

The application may fall back to the database, but that can cause a cache-miss storm and overload the database.
Therefore the fallback must be protected with appropriate load shedding, rate limiting or degradation strategies.

______________________________________________________________________

## Q17. What is Kafka consumer lag?

**Answer:**

It represents how far a consumer group is behind the available records. Increasing lag means processing is not keeping
up with production or consumption is otherwise delayed.

______________________________________________________________________

## Q18. What causes Kafka consumer lag?

**Answer:**

Slow processing, consumer failures, insufficient consumers relative to partitions, rebalances, downstream latency,
retries and other processing bottlenecks can all cause lag.

______________________________________________________________________

## Q19. Does adding more Kafka consumers always reduce lag?

**Answer:**

No. Parallelism is constrained by partition count, and additional consumers can also overload downstream systems such as
databases.

______________________________________________________________________

## Q20. Why do duplicate Kafka messages happen?

**Answer:**

At-least-once processing can result in redelivery when a consumer successfully processes a message but fails before its
offset is committed, among other retry/recovery scenarios.

______________________________________________________________________

## Q21. How do you handle duplicate messages?

**Answer:**

Make processing idempotent. Use a stable event/business identifier and enforce the required uniqueness or state
transition in a durable store where appropriate.

______________________________________________________________________

## Q22. What is a container restart telling you?

**Answer:**

It tells you that the container or its process exited or was considered unhealthy according to the runtime/orchestrator.
I would inspect logs, exit status, health checks, OOM events, resource limits and recent changes before deciding on
remediation.

______________________________________________________________________

## Q23. How do you debug network problems?

**Answer:**

I work layer by layer: DNS, routing/network reachability, TCP, TLS and HTTP/application protocol. This prevents treating
every network failure as an application problem.

______________________________________________________________________

## Q24. What is a deadlock?

**Answer:**

A deadlock occurs when execution paths wait indefinitely for resources held by each other, creating a circular
dependency.

______________________________________________________________________

## Q25. How can application deadlocks be prevented?

**Answer:**

Use consistent lock acquisition order, minimize lock scope, avoid unnecessary shared state and design lock ownership
carefully.

______________________________________________________________________

## Q26. How can database deadlocks be prevented?

**Answer:**

Keep transactions short, acquire locks in a consistent order, use appropriate indexes and avoid unnecessary locking.
Applications should also handle deadlock-related transaction failures with appropriate retry behavior when safe.

______________________________________________________________________

## Q27. Why can increasing retries make an incident worse?

**Answer:**

Retries increase load on an already failing dependency. Without bounded attempts, backoff and jitter, retries can create
a feedback loop or retry storm.

______________________________________________________________________

## Q28. What makes a good timeout strategy?

**Answer:**

Timeouts should exist at appropriate layers and be aligned with the operation's latency budget. They should be combined
with bounded retries, backoff, jitter and idempotency where retries are possible.

______________________________________________________________________

## Q29. What is graceful degradation?

**Answer:**

It means continuing to provide useful functionality when an optional dependency fails, rather than allowing the entire
request or service to fail.

______________________________________________________________________

## Q30. What is fail-fast behavior?

**Answer:**

Fail-fast behavior stops waiting or processing when a required operation cannot complete within an acceptable boundary.
It prevents resources from being held indefinitely.

______________________________________________________________________

## Q31. What should you do first during a major incident?

**Answer:**

Confirm the incident, understand the impact and establish the timeline. Then focus on safe mitigation while collecting
evidence for diagnosis.

______________________________________________________________________

## Q32. Should you restart a failing production service?

**Answer:**

A restart can be an appropriate mitigation in some situations, but I first consider whether it will remove useful
evidence, whether it will worsen the incident and whether it addresses the actual failure. I collect enough evidence
before taking destructive action when the situation allows.

______________________________________________________________________

## Q33. How do logs, metrics and traces differ?

**Answer:**

Logs provide detailed event information, metrics provide aggregated numerical measurements over time and traces show the
path/timing of individual requests across components.

______________________________________________________________________

## Q34. Why are correlation IDs useful?

**Answer:**

They allow logs and events associated with the same request or operation to be connected across services, making
distributed debugging much easier.

______________________________________________________________________

## Q35. What should an incident update contain?

**Answer:**

Impact, current status, confirmed facts, current investigation, mitigation and the next expected update. Speculation
should be clearly distinguished from confirmed information.

______________________________________________________________________

## Q36. What is a cascading failure?

**Answer:**

It occurs when one component's failure causes increased load or failures in dependent components, potentially spreading
the incident through the system.

______________________________________________________________________

## Q37. Give an example of a cascading failure.

**Answer:**

Redis fails, causing cache misses; database traffic increases; PostgreSQL becomes overloaded; connection pools exhaust;
API latency increases; requests time out; retries generate even more load.

______________________________________________________________________

## Q38. How do feature flags help incident response?

**Answer:**

They can allow a problematic feature to be disabled quickly without requiring a full deployment, reducing blast radius
and restoring service.

______________________________________________________________________

## Q39. What is the difference between mitigation and root-cause resolution?

**Answer:**

Mitigation reduces the current impact. Root-cause resolution fixes the underlying reason the incident occurred and
prevents recurrence.

______________________________________________________________________

## Q40. What is a post-incident review?

**Answer:**

A structured review of what happened, why it happened, how it was detected, how it was mitigated and what changes should
prevent or reduce recurrence.

______________________________________________________________________

## Q41. What should you preserve during an incident?

**Answer:**

Relevant logs, metrics, traces, timestamps, deployment versions, configuration changes, process/resource state and other
evidence needed to reconstruct the failure.

______________________________________________________________________

## Q42. Why should you avoid changing many things at once?

**Answer:**

Changing many variables makes it difficult to determine which change caused improvement or deterioration and can
introduce additional failures.

______________________________________________________________________

## Q43. What is load shedding?

**Answer:**

Deliberately rejecting or reducing lower-priority work when the system is overloaded so that critical functionality
remains available.

______________________________________________________________________

## Q44. Why is load shedding useful?

**Answer:**

It prevents an overloaded system from spending all available resources trying to serve work it cannot complete, helping
preserve critical capacity.

______________________________________________________________________

## Q45. Give a senior-level production debugging answer.

**Answer:**

"I treat production debugging as an evidence-driven process. I first establish impact and scope, create a timeline and
check recent changes. Then I use latency, traffic, errors and saturation along with logs, metrics and traces to isolate
the failing layer. I distinguish application problems from dependency, network and infrastructure problems, and I look
for cascading effects such as retries or connection-pool exhaustion. During the incident I prioritize safe mitigation
and verify recovery. After stabilization, I preserve evidence, identify the root cause and close monitoring, testing,
capacity or design gaps that allowed the incident to happen."

______________________________________________________________________

# 96. Scenario-Based Questions

## Scenario 1 — CPU 100% After Deployment

At 14:00 a new version is deployed.

At 14:05:

```text
CPU → 100%
p99 latency → 5s
```

### Investigation

1. Compare CPU with traffic.
1. Identify affected workers/processes.
1. Check deployment diff.
1. Identify hot endpoints.
1. Inspect traces/profiling data.
1. Determine whether new code introduced CPU-heavy work.

### Mitigation

If strongly correlated and safe:

```text
Rollback
```

or disable the problematic feature.

### Prevention

Add performance regression tests and endpoint-level resource metrics.

______________________________________________________________________

## Scenario 2 — Memory Growth and Container Restarts

Symptoms:

```text
Memory steadily grows
Container restarts every 30 minutes
```

### Investigation

Check:

```text
Memory graph
Container limit
OOM events
Restart count
Endpoint traffic
Recent deployments
```

Then identify whether a particular request pattern causes retained objects.

### Mitigation

Reduce affected traffic or roll back the responsible change.

### Prevention

Fix retention behavior and add memory monitoring/regression coverage.

______________________________________________________________________

## Scenario 3 — API p99 Increases

Metrics:

```text
p50 = 100ms
p99 = 5s
```

### Investigation

Trace slow requests.

You discover:

```text
DB = 4.5s
```

Investigate query plan, locks, connection acquisition and database resource usage.

Do not optimize FastAPI code before establishing that the database is responsible for the tail latency.

______________________________________________________________________

## Scenario 4 — 502 After Proxy Change

Users receive:

```text
502 Bad Gateway
```

### Investigation

Check:

```text
Proxy logs
Upstream health
Upstream port
Network connectivity
Application logs
Proxy timeout/protocol configuration
```

The 502 identifies the gateway/upstream interaction, not necessarily the root cause.

______________________________________________________________________

## Scenario 5 — 503 During Traffic Spike

Traffic increases 5x.

The load balancer reports no healthy upstreams.

### Investigation

Check:

```text
Application CPU
Memory
Worker count
Readiness checks
Connection pools
Database capacity
```

Potentially the application is alive but unable to become ready because the database is saturated.

______________________________________________________________________

## Scenario 6 — Database Connection Pool Exhausted

Metrics:

```text
Pool utilization = 100%
Database CPU = 40%
API latency = high
```

### Investigation

Check:

```text
Connection wait time
Long transactions
Slow queries
Connection leaks
Pool configuration
Request concurrency
```

The database itself may not be saturated.

______________________________________________________________________

## Scenario 7 — Redis Failure Causes Database Incident

Redis becomes unavailable.

Within minutes:

```text
Database QPS → 4x
Database CPU → 100%
API latency → 8s
```

### Root cause chain

```text
Redis failure
 ↓
Cache misses
 ↓
DB load spike
 ↓
DB saturation
 ↓
API slowdown
```

### Lesson

Fallback paths must also be capacity-tested.

______________________________________________________________________

## Scenario 8 — Kafka Lag Increasing

Kafka lag grows from:

```text
1,000 → 100,000
```

Consumers are healthy.

### Investigation

Tracing shows each message now performs a database operation taking 2 seconds.

### Root cause

Downstream database slowdown.

### Lesson

Consumer lag is an observable symptom; investigate the entire processing pipeline.

______________________________________________________________________

## Scenario 9 — Duplicate Payment

A payment event appears twice.

### Investigation

```text
Message processed
 ↓
DB transaction committed
 ↓
Consumer crashed
 ↓
Offset not committed
 ↓
Message redelivered
```

### Solution

Use idempotent processing based on a stable payment/event identifier.

The database should enforce the required uniqueness/state invariant where appropriate.

______________________________________________________________________

## Scenario 10 — Container Restart Loop

A container restarts every few seconds.

### Investigation

Check:

```text
docker ps -a
docker logs
container inspect/state
health status
exit code
memory limit
```

Suppose logs show a missing environment variable.

### Root cause

Configuration error.

### Fix

Correct runtime configuration and verify startup/health behavior.

______________________________________________________________________

## Scenario 11 — Network Failure

API cannot reach:

```text
payments.internal
```

Investigation:

```text
DNS → successful
TCP → connection timeout
```

### Conclusion

DNS is not the primary problem.

Investigate:

```text
Routing
Firewall
Security rules
Network policy
Listening service
```

______________________________________________________________________

## Scenario 12 — Deadlock

Two requests hang indefinitely.

Database monitoring shows:

```text
Transaction A waits for row held by B
Transaction B waits for row held by A
```

### Root cause

Circular locking dependency.

### Prevention

Use consistent lock ordering and keep transactions short.

______________________________________________________________________

# 97. Production Incident Runbook

When you receive an alert:

## Phase 1 — Confirm

```text
Is it real?
```

## Phase 2 — Scope

```text
Who/what is affected?
```

## Phase 3 — Timeline

```text
When did it start?
What changed?
```

## Phase 4 — Observe

```text
Latency
Traffic
Errors
Saturation
Logs
Metrics
Traces
```

## Phase 5 — Isolate

```text
Client
Network
Proxy
Application
Database
Cache
Messaging
External dependency
```

## Phase 6 — Hypothesize

Create explicit hypotheses.

Example:

> "Database connection pool exhaustion is causing request latency."

## Phase 7 — Test

Collect evidence that confirms or disproves the hypothesis.

## Phase 8 — Mitigate

Choose the safest action that reduces impact.

## Phase 9 — Verify

Confirm that:

```text
Error rate ↓
Latency ↓
Saturation ↓
User impact ↓
```

## Phase 10 — Prevent

Identify:

```text
Code fix
Monitoring improvement
Test improvement
Capacity improvement
Architecture improvement
Runbook improvement
```

______________________________________________________________________

# 98. Interview Preparation Checklist

Before moving to the next topic, make sure you can:

- [ ] Explain symptom vs root cause.
- [ ] Explain a repeatable debugging methodology.
- [ ] Scope production incidents.
- [ ] Build an incident timeline.
- [ ] Use recent changes as hypotheses.
- [ ] Explain latency, traffic, errors and saturation.
- [ ] Explain logs, metrics and traces.
- [ ] Explain correlation IDs.
- [ ] Debug CPU saturation.
- [ ] Debug Python CPU-bound workloads.
- [ ] Debug memory growth.
- [ ] Distinguish OOM from memory leak.
- [ ] Debug full disks.
- [ ] Explain deleted-but-open files.
- [ ] Debug slow APIs.
- [ ] Explain p50/p95/p99.
- [ ] Debug slow database queries.
- [ ] Distinguish connection acquisition from query execution.
- [ ] Explain 502.
- [ ] Explain 503.
- [ ] Debug proxy/upstream failures.
- [ ] Debug database unavailability.
- [ ] Explain connection pools.
- [ ] Diagnose pool exhaustion.
- [ ] Diagnose connection leaks.
- [ ] Debug Redis failures.
- [ ] Explain cache fallback risks.
- [ ] Explain Kafka consumer lag.
- [ ] Explain partition-constrained consumer parallelism.
- [ ] Diagnose Kafka lag.
- [ ] Explain duplicate delivery.
- [ ] Explain idempotent message processing.
- [ ] Debug container restarts.
- [ ] Interpret exit codes.
- [ ] Debug health-check failures.
- [ ] Debug DNS.
- [ ] Debug TCP.
- [ ] Debug TLS.
- [ ] Debug HTTP.
- [ ] Explain deadlocks.
- [ ] Explain database deadlocks.
- [ ] Explain cascading failures.
- [ ] Explain retry storms.
- [ ] Explain timeout strategy.
- [ ] Explain circuit breakers.
- [ ] Explain graceful degradation.
- [ ] Explain fail-fast behavior.
- [ ] Explain load shedding.
- [ ] Explain rollback.
- [ ] Explain feature flags.
- [ ] Communicate during incidents.
- [ ] Preserve production evidence.
- [ ] Distinguish mitigation from root-cause resolution.
- [ ] Conduct a post-incident review.

______________________________________________________________________

# 99. Final Senior Interview Scenario

You are the senior backend engineer on call.

The alert says:

```text
API error rate ↑
API p99 latency ↑
Database CPU ↑
Redis errors ↑
Kafka consumer lag ↑
```

A weak debugging approach is:

```text
Restart everything.
```

A strong approach is:

```text
1. Establish user impact.
2. Build the timeline.
3. Check recent changes.
4. Determine whether Redis failure preceded DB saturation.
5. Check whether cache fallback increased database traffic.
6. Check database connection-pool utilization.
7. Check API latency and traces.
8. Check Kafka processing latency.
9. Determine whether retries are amplifying load.
10. Apply controlled mitigation.
11. Verify recovery.
12. Identify the root cause.
13. Add preventive controls.
```

The important senior-level insight is:

> **Do not debug each alert independently. Build the causal chain across the system.**

For example:

```text
Redis failure
    ↓
Cache misses
    ↓
Database traffic spike
    ↓
Database saturation
    ↓
Connection pool exhaustion
    ↓
API latency
    ↓
Timeouts
    ↓
Retries
    ↓
More load
    ↓
Kafka consumers slow down
    ↓
Consumer lag
```

The incident may have one initiating failure and several secondary symptoms.

______________________________________________________________________

# 100. Final Takeaways

Production debugging is fundamentally an exercise in **observability, hypothesis testing and controlled mitigation**.

For a senior Python backend engineer, the expected skill is not knowing a magic command for every incident.

It is being able to reason:

```text
Symptom
 ↓
Scope
 ↓
Evidence
 ↓
Hypothesis
 ↓
Verification
 ↓
Mitigation
 ↓
Root cause
 ↓
Prevention
```

When debugging distributed systems, always consider the possibility that:

> **The component showing the symptom may not be the component causing the failure.**

A Kafka consumer can lag because PostgreSQL is slow.

An API can return 503 because its database connection pool is exhausted.

A database can become overloaded because Redis failed.

A service can restart because its health check is incorrectly designed.

A network error can actually be DNS, TCP, TLS or HTTP.

That ability to follow the causal chain is one of the most important differences between junior and senior production
debugging.

______________________________________________________________________

**Previous:** [31. Linux for Backend Engineers](./31-linux.md)

**Next:** [33. Backend Security](./33-security.md)
