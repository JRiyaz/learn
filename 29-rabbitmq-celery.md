# 29. RabbitMQ & Celery

**Previous:** [28. Kafka](./28-kafka.md)

**Next:** [30. Docker](./30-docker.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain RabbitMQ's core messaging model.
- Understand exchanges, queues, bindings and routing keys.
- Explain acknowledgments and prefetch.
- Understand TTL, dead-letter exchanges and durability.
- Explain Celery's architecture and execution model.
- Understand tasks, workers, brokers and result backends.
- Configure and reason about retries and timeouts.
- Understand Celery Beat and periodic tasks.
- Explain worker concurrency.
- Design idempotent background tasks.
- Integrate Celery with FastAPI.
- Compare Kafka, RabbitMQ and Celery and choose an appropriate tool.

______________________________________________________________________

# 1. RabbitMQ Overview

RabbitMQ is a message broker used to route messages between producers and consumers.

A simplified flow is:

```text
Producer
   ↓
Exchange
   ↓
Queue
   ↓
Consumer
```

The producer normally publishes to an exchange rather than directly deciding which consumer receives a message.

______________________________________________________________________

# 2. Why Use RabbitMQ?

RabbitMQ is useful for:

- Asynchronous jobs
- Background processing
- Work queues
- Service-to-service messaging
- Routing messages to different consumers
- Controlling consumer workload

A common backend example is:

```text
FastAPI
   ↓
RabbitMQ
   ↓
Worker
   ↓
Email/API/Database operation
```

The HTTP request does not need to wait for the entire background operation.

______________________________________________________________________

# 3. RabbitMQ Core Concepts

The important concepts are:

- Producer
- Exchange
- Queue
- Binding
- Routing key
- Consumer
- ACK
- Prefetch
- TTL
- Dead-letter exchange
- Durability

The relationship between exchange, binding and queue is especially important for interviews.

______________________________________________________________________

# 4. Producer

A producer publishes a message.

Example:

```text
Order Service
     ↓
RabbitMQ
```

The producer typically specifies an exchange and routing information.

______________________________________________________________________

# 5. Exchange

An exchange receives messages from producers and decides which queues should receive them.

Conceptually:

```text
Producer
   ↓
Exchange
 ┌─┴───────┐
 ↓         ↓
Queue A   Queue B
```

The exchange does not normally store messages as the final destination; queues do.

______________________________________________________________________

# 6. Queue

A queue stores messages until consumers process them.

Conceptually:

```text
Exchange
   ↓
Queue
   ↓
Consumer
```

Messages wait in the queue when consumers are unavailable or slower than producers.

______________________________________________________________________

# 7. Binding

A binding connects an exchange to a queue.

Conceptually:

```text
Exchange
    │
 Binding
    │
    ↓
 Queue
```

The binding can include routing information depending on the exchange type.

______________________________________________________________________

# 8. Routing Key

A routing key is information carried with a published message that an exchange can use to determine routing.

Example:

```text
routing_key = order.created
```

The exchange uses the routing key and its configured bindings to determine destinations.

______________________________________________________________________

# 9. Exchange Types

RabbitMQ supports several exchange types.

The most important for interviews are:

- Direct
- Topic
- Fanout
- Headers

______________________________________________________________________

# 10. Direct Exchange

A direct exchange routes messages based on an exact routing-key match.

Example:

```text
routing key:
order.created

binding:
order.created
```

The message is routed to the queue with the matching binding key.

______________________________________________________________________

# 11. Topic Exchange

A topic exchange supports pattern-based routing keys.

Example:

```text
order.created
order.updated
payment.created
```

A consumer can subscribe to patterns such as:

```text
order.*
```

This is useful when consumers need a category of related events.

______________________________________________________________________

# 12. Fanout Exchange

A fanout exchange broadcasts messages to all queues bound to it.

Conceptually:

```text
           Exchange
          /   |   \
         ↓    ↓    ↓
       Q1    Q2    Q3
```

The routing key is not the primary routing mechanism for fanout behavior.

______________________________________________________________________

# 13. Headers Exchange

A headers exchange routes messages based on message headers rather than routing-key patterns.

It is less common in many backend applications but is part of RabbitMQ's exchange model.

______________________________________________________________________

# 14. Exchange Comparison

| Exchange | Routing Model | Common Use |
|---|---|---|
| Direct | Exact routing key | Specific routing |
| Topic | Pattern-based routing key | Event categories |
| Fanout | Broadcast | Publish to many queues |
| Headers | Header matching | Header-driven routing |

______________________________________________________________________

# 15. Queue Consumers

A consumer receives messages from a queue.

Example:

```text
Queue
 ↓
Worker 1
```

Multiple consumers can process messages from the same queue.

______________________________________________________________________

# 16. Work Queue

A common RabbitMQ pattern is a work queue.

```text
             Queue
          /    |    \
         ↓     ↓     ↓
       Worker Worker Worker
```

Messages are distributed among consumers so work can be processed concurrently.

______________________________________________________________________

# 17. Acknowledgment — ACK

An acknowledgment tells RabbitMQ that a consumer has successfully handled a message.

Conceptually:

```text
RabbitMQ
   ↓
Consumer
   ↓
Process
   ↓
ACK
```

The exact acknowledgment mode affects what happens when a consumer fails.

______________________________________________________________________

# 18. Why ACK Matters

Suppose:

```text
Message received
       ↓
Worker crashes
```

If the message has not been acknowledged and the queue is configured appropriately, RabbitMQ can make the message
available for another consumer.

This helps avoid losing work simply because a worker crashed.

______________________________________________________________________

# 19. Manual ACK

With manual acknowledgments, the consumer explicitly acknowledges successful processing.

A typical conceptual flow is:

```text
Receive
  ↓
Process
  ↓
ACK
```

This is useful when processing success must determine whether the message is considered completed.

______________________________________________________________________

# 20. ACK Too Early

If the worker acknowledges before processing:

```text
Receive
 ↓
ACK
 ↓
Process
 ↓
Crash
```

The message may be considered handled even though the business operation failed.

This can result in lost work.

______________________________________________________________________

# 21. ACK After Processing

A safer work-processing model is:

```text
Receive
 ↓
Process successfully
 ↓
ACK
```

If the worker crashes before the ACK, the message can potentially be redelivered.

This creates duplicate-processing considerations.

______________________________________________________________________

# 22. Idempotency and RabbitMQ

Redelivery can cause a task to execute more than once.

Therefore consumers should make important operations idempotent where practical.

Example:

```text
message_id = abc123
```

The application can record processed IDs and avoid applying the same business effect twice.

______________________________________________________________________

# 23. Prefetch

Prefetch controls how many unacknowledged messages a consumer can have outstanding.

Conceptually:

```text
Prefetch = 1
```

means a consumer receives only a small number of unacknowledged messages at a time.

______________________________________________________________________

# 24. Why Prefetch Matters

Without appropriate prefetch settings, one worker may receive many messages while another worker is idle.

Example:

```text
Queue
 ↓↓↓↓↓↓↓
Worker A → many messages
Worker B → few/no messages
```

Prefetch can improve workload distribution.

______________________________________________________________________

# 25. Prefetch Trade-Off

A small prefetch can improve fairness.

A larger prefetch can improve throughput by reducing message-delivery overhead.

The correct value depends on:

- Task duration
- Worker count
- Workload distribution
- Memory
- Desired fairness

______________________________________________________________________

# 26. TTL

TTL means Time To Live.

RabbitMQ can apply TTL to messages or queues depending on configuration.

A TTL allows messages to expire after a specified period.

Example:

```text
Message
   ↓
TTL = 60 seconds
   ↓
Expires if not processed
```

______________________________________________________________________

# 27. Why Use TTL?

TTL can be useful for:

- Time-sensitive jobs
- Temporary messages
- Preventing indefinitely stale work
- Expiring old requests

For example, a notification request that is useless after several minutes may have a TTL.

______________________________________________________________________

# 28. Dead-Letter Exchange

A dead-letter exchange (DLX) is used to route messages that can no longer remain in their original queue.

Messages can become dead-lettered for reasons such as:

- Rejection
- Expiration
- Queue limits
- Other configured dead-letter conditions

Conceptually:

```text
Main Queue
    ↓
Failure/expiration
    ↓
Dead-Letter Exchange
    ↓
Dead-Letter Queue
```

______________________________________________________________________

# 29. Why Dead-Lettering Matters

Without dead-letter handling:

```text
Bad message
   ↓
Repeated failure
   ↓
Repeated retry
```

can consume worker capacity.

Dead-lettering provides a place for failed messages to be inspected and handled separately.

______________________________________________________________________

# 30. Durability

RabbitMQ durability determines whether queues and messages are configured to survive broker restarts under the relevant
persistence settings.

There are multiple related concepts:

- Durable queues
- Persistent messages
- Durable exchanges

These should not be treated as exactly the same thing.

______________________________________________________________________

# 31. Durable Queue

A durable queue is designed to survive a broker restart.

However, declaring a queue as durable does not by itself mean every message stored in it is persistent.

______________________________________________________________________

# 32. Persistent Message

A message can be published as persistent.

This works together with durable infrastructure to improve the likelihood that messages survive broker restart.

Durability is still subject to the broker's storage and failure model.

______________________________________________________________________

# 33. Durable Exchange

An exchange can also be declared durable so its configuration survives broker restart.

Therefore, production messaging designs should consider:

```text
Exchange durability
+
Queue durability
+
Message persistence
```

together.

______________________________________________________________________

# 34. RabbitMQ Delivery Flow

A simplified production flow is:

```text
Producer
   ↓
Exchange
   ↓
Binding
   ↓
Queue
   ↓
Consumer
   ↓
Process
   ↓
ACK
```

On failure:

```text
Consumer
   ↓
Failure
   ↓
Retry / Requeue / Dead-letter
```

______________________________________________________________________

# 35. RabbitMQ Failure Handling

A robust consumer should define what happens when processing fails.

Possible strategies include:

- Retry
- Requeue
- Delayed retry architecture
- Dead-lettering
- Manual investigation

Do not blindly requeue a permanently invalid message forever.

______________________________________________________________________

# 36. Retry Loop Problem

Consider:

```text
Message
 ↓
Consumer
 ↓
Failure
 ↓
Requeue
 ↓
Consumer
 ↓
Failure
 ↓
Requeue
```

This can become an infinite hot loop.

A retry policy should include:

- Maximum attempts
- Backoff
- Error classification
- Dead-letter handling

______________________________________________________________________

# 37. RabbitMQ vs Kafka — High-Level

RabbitMQ and Kafka are both messaging technologies, but their core models differ.

RabbitMQ emphasizes:

```text
Message routing
+
Queues
+
Acknowledgments
+
Work distribution
```

Kafka emphasizes:

```text
Partitioned event log
+
Retention
+
Offsets
+
Replay
```

Neither is universally "better."

______________________________________________________________________

# 38. Kafka Strengths

Kafka is particularly strong for:

- High-throughput event streams
- Long-lived event retention
- Replay
- Multiple independent consumer groups
- Partition-based scaling

______________________________________________________________________

# 39. RabbitMQ Strengths

RabbitMQ is particularly strong for:

- Flexible routing
- Work queues
- Task distribution
- Per-message acknowledgment
- Fine-grained queue-based messaging

______________________________________________________________________

# 40. Celery Overview

Celery is a distributed task queue for executing Python tasks asynchronously.

A common architecture is:

```text
FastAPI
   ↓
Celery
   ↓
Broker
   ↓
Celery Worker
```

Redis or RabbitMQ can be used as a Celery broker depending on the architecture.

______________________________________________________________________

# 41. Celery Task

A Celery task is a Python function that can be executed asynchronously by a worker.

Conceptually:

```python
@celery.task
def send_email(user_id):
    ...
```

The application can enqueue the task instead of executing it synchronously.

______________________________________________________________________

# 42. Celery Worker

A Celery worker consumes tasks from the broker and executes them.

Conceptually:

```text
Broker
  ↓
Celery Worker
  ↓
Task
```

Multiple workers can execute tasks concurrently.

______________________________________________________________________

# 43. Celery Broker

The broker transports task messages between the application and workers.

Common broker choices include:

- RabbitMQ
- Redis

Conceptually:

```text
Application
     ↓
Broker
     ↓
Worker
```

______________________________________________________________________

# 44. Result Backend

The result backend stores task results/status information when the application is configured to use one.

For example:

```text
Task
 ↓
Worker
 ↓
Result
 ↓
Result Backend
```

A result backend is different from the message broker.

______________________________________________________________________

# 45. Broker vs Result Backend

### Broker

Responsible for transporting tasks.

### Result backend

Responsible for storing task results/state when used.

They solve different problems.

______________________________________________________________________

# 46. Celery Task Lifecycle

A simplified lifecycle is:

```text
Task submitted
      ↓
Broker
      ↓
Worker receives
      ↓
Task executes
      ↓
Success / Failure
      ↓
Result state
```

The exact states and configuration depend on the Celery setup.

______________________________________________________________________

# 47. Celery Retry

Celery supports task retries.

Retries are useful for transient failures such as:

- Network errors
- Temporary database failures
- External service failures

A task should distinguish retryable errors from permanent business errors.

______________________________________________________________________

# 48. Retry With Backoff

A production retry strategy should avoid immediate repeated execution.

Conceptually:

```text
Attempt 1
   ↓
wait
   ↓
Attempt 2
   ↓
longer wait
   ↓
Attempt 3
```

Exponential backoff and jitter can help prevent retry storms.

______________________________________________________________________

# 49. Celery Retry Idempotency

A retry can execute a task more than once.

For example:

```text
send_payment()
```

must not accidentally charge a customer twice simply because a retry occurred.

Important tasks should use:

- Idempotency keys
- Unique constraints
- Transactional state changes
- Deduplication

where appropriate.

______________________________________________________________________

# 50. Celery Timeout

Long-running tasks should have appropriate timeouts.

Timeouts prevent a task from consuming worker capacity indefinitely.

For example:

```text
External API call
      ↓
Timeout
      ↓
Retry/fail
```

Timeout behavior should be designed together with retry behavior.

______________________________________________________________________

# 51. Task Timeout vs HTTP Timeout

These are different layers.

```text
HTTP request timeout
        ≠
Celery task timeout
```

A FastAPI request can return immediately after scheduling a task while the Celery task continues independently.

______________________________________________________________________

# 52. Celery Beat

Celery Beat is used for periodic task scheduling.

Example:

```text
Every 5 minutes
      ↓
Cleanup task
```

Beat schedules the task, while workers execute it.

______________________________________________________________________

# 53. Beat vs Worker

### Beat

Answers:

> When should the task be submitted?

### Worker

Answers:

> Who executes the task?

Conceptually:

```text
Beat
 ↓
Broker
 ↓
Worker
```

______________________________________________________________________

# 54. Celery Worker Concurrency

Workers can execute multiple tasks concurrently using supported execution pools/configurations.

The appropriate concurrency depends on workload.

For example:

```text
I/O-heavy tasks
→ more concurrency may be useful

CPU-heavy tasks
→ process-based parallelism may be more appropriate
```

Worker concurrency must also account for database and downstream capacity.

______________________________________________________________________

# 55. Worker Concurrency Is Not Unlimited

If a worker executes 100 tasks concurrently but the database can handle only 20 expensive queries safely, increasing
concurrency can make the system worse.

Always consider:

```text
Worker capacity
+
Database capacity
+
External service capacity
```

______________________________________________________________________

# 56. Celery Idempotency

A Celery task should ideally be safe to execute more than once when duplicate execution is possible.

For example:

```python
@celery.task
def generate_report(report_id):
    ...
```

The implementation can check whether the report has already been generated before performing an irreversible operation.

______________________________________________________________________

# 57. FastAPI + Celery

FastAPI should generally handle HTTP concerns.

Celery should handle long-running/background jobs.

Example:

```text
POST /reports
       ↓
FastAPI
       ↓
enqueue Celery task
       ↓
return task/report ID

Celery Worker
       ↓
generate report
```

______________________________________________________________________

# 58. Why Not Run Long Tasks Directly in FastAPI?

A long-running operation can:

- Increase request latency
- Consume application workers
- Cause request timeouts
- Reduce API throughput

For expensive asynchronous work, a dedicated task worker is often more appropriate.

______________________________________________________________________

# 59. FastAPI Task Submission

A conceptual API flow:

```text
POST /reports
    ↓
Validate request
    ↓
Create job record
    ↓
Enqueue Celery task
    ↓
Return 202 Accepted
```

The client can later query:

```text
GET /reports/{id}
```

for status.

______________________________________________________________________

# 60. Job Status

A production API may expose states such as:

```text
PENDING
RUNNING
SUCCESS
FAILED
```

The exact model can be application-specific.

Persisting business-level job state in the application's database can be preferable when the status is important to the
domain.

______________________________________________________________________

# 61. FastAPI and Result Backend

The result backend can be useful for:

- Task state
- Task results
- Operational status

But it should not automatically be treated as the application's durable business database.

For important business state, use the application's appropriate persistent store.

______________________________________________________________________

# 62. Celery Architecture

A typical architecture is:

```text
                    ┌───────────────┐
                    │    FastAPI    │
                    └───────┬───────┘
                            ↓
                         Broker
                            ↓
                  ┌─────────┴─────────┐
                  ↓                   ↓
              Worker 1            Worker 2
                  ↓                   ↓
                Tasks               Tasks
```

A result backend may exist separately:

```text
Workers
   ↓
Result Backend
```

______________________________________________________________________

# 63. Celery Failure Scenarios

### Worker crash

A task may need to be redelivered depending on acknowledgment/execution configuration.

### Broker failure

Task submission/consumption can be disrupted.

### Task exception

The task can fail and potentially be retried.

### External API failure

Use timeout, retry and backoff.

### Duplicate execution

Make important operations idempotent.

______________________________________________________________________

# 64. Retryable vs Non-Retryable Errors

### Usually retryable

- Temporary network failure
- Connection reset
- Service unavailable
- Temporary database outage

### Usually not retryable

- Invalid input
- Permanent validation failure
- Unsupported operation
- Business rule violation

The classification depends on the application.

______________________________________________________________________

# 65. Dead-Letter Strategy for Celery

Celery can be built around broker-level retry/dead-letter mechanisms, but the exact design depends on the broker and
Celery configuration.

For RabbitMQ-backed deployments, RabbitMQ dead-letter exchanges can be part of the failure-handling architecture.

The important principle is:

```text
Transient failure
 → retry

Permanent failure
 → isolate/investigate
```

______________________________________________________________________

# 66. RabbitMQ + Celery

RabbitMQ can act as Celery's broker.

Conceptually:

```text
FastAPI
   ↓
Celery
   ↓
RabbitMQ
   ↓
Celery Worker
```

RabbitMQ provides message transport/routing while Celery provides Python task execution semantics.

______________________________________________________________________

# 67. Redis + Celery

Redis can also be used as a Celery broker in supported configurations.

Conceptually:

```text
FastAPI
   ↓
Celery
   ↓
Redis
   ↓
Worker
```

The choice depends on the required messaging behavior and operational environment.

______________________________________________________________________

# 68. Kafka vs RabbitMQ vs Celery

These technologies overlap but are not identical.

| Technology | Primary Role | Key Model |
|---|---|---|
| Kafka | Event streaming | Topics + partitions + offsets |
| RabbitMQ | Message broker | Exchanges + queues + acknowledgments |
| Celery | Python task queue | Tasks + workers + broker |

Celery itself commonly uses another messaging system as its broker.

______________________________________________________________________

# 69. Kafka vs RabbitMQ

### Kafka

Choose Kafka when you need:

- High-throughput event streaming
- Durable retention
- Replay
- Multiple independent consumer groups
- Partition-based scalability

### RabbitMQ

Choose RabbitMQ when you need:

- Flexible message routing
- Work queues
- Task distribution
- Queue-centric processing
- Fine-grained acknowledgments

______________________________________________________________________

# 70. RabbitMQ vs Celery

RabbitMQ is a message broker.

Celery is a Python distributed task execution framework.

A common architecture is:

```text
Celery
  ↓
RabbitMQ
  ↓
Celery Workers
```

They are complementary rather than direct substitutes.

______________________________________________________________________

# 71. Kafka vs Celery

Kafka is an event streaming platform.

Celery is designed around executing Python tasks asynchronously.

Use Kafka when the event itself is an important stream that multiple consumers may independently process or replay.

Use Celery when the primary requirement is:

```text
"Run this Python job asynchronously."
```

______________________________________________________________________

# 72. Decision Guide

### Send an event to multiple independent services

Consider:

```text
Kafka
```

### Route messages flexibly to queues/workers

Consider:

```text
RabbitMQ
```

### Run Python background tasks

Consider:

```text
Celery
```

### Run Python tasks using RabbitMQ

Use:

```text
Celery + RabbitMQ
```

______________________________________________________________________

# 73. Example Architecture — Email

Requirement:

```text
User signs up
→ send welcome email asynchronously
```

Possible design:

```text
FastAPI
   ↓
Celery task
   ↓
RabbitMQ
   ↓
Email worker
   ↓
Email provider
```

The HTTP request can complete without waiting for email delivery.

______________________________________________________________________

# 74. Example Architecture — Order Events

Requirement:

```text
OrderCreated
→ Inventory
→ Analytics
→ Notifications
```

A Kafka-based design may be appropriate:

```text
Order Service
      ↓
Kafka
 ┌────┼────┐
 ↓    ↓    ↓
Inventory
Analytics
Notifications
```

Each service can consume independently.

______________________________________________________________________

# 75. Example Architecture — Background Report

Requirement:

```text
Generate large PDF report
```

A Celery design is natural:

```text
FastAPI
   ↓
Celery
   ↓
RabbitMQ/Redis
   ↓
Worker
   ↓
Generate report
```

The API can return a job ID immediately.

______________________________________________________________________

# 76. Production Checklist — RabbitMQ

- [ ] Exchange design defined
- [ ] Queue design defined
- [ ] Bindings understood
- [ ] Routing keys documented
- [ ] ACK behavior defined
- [ ] Prefetch tuned
- [ ] TTL requirements defined
- [ ] Dead-letter strategy defined
- [ ] Retry policy defined
- [ ] Durable queues where required
- [ ] Persistent messages where required
- [ ] Monitoring configured
- [ ] Consumer capacity understood

______________________________________________________________________

# 77. Production Checklist — Celery

- [ ] Task boundaries defined
- [ ] Broker configured
- [ ] Result backend requirement evaluated
- [ ] Retry policy defined
- [ ] Timeouts defined
- [ ] Idempotency considered
- [ ] Worker concurrency tuned
- [ ] Beat tasks reviewed
- [ ] Failed tasks observable
- [ ] Dead-letter/failure strategy defined
- [ ] Database capacity considered
- [ ] External API limits considered
- [ ] FastAPI job-status API designed where needed

______________________________________________________________________

# 78. Common RabbitMQ Mistakes

## Mistake 1 — ACKing before processing

A crash can cause lost work.

## Mistake 2 — Infinite requeue

A poison message can create an endless retry loop.

## Mistake 3 — Ignoring prefetch

Poor prefetch can cause unfair workload distribution.

## Mistake 4 — No dead-letter strategy

Failed messages can become operationally difficult to investigate.

## Mistake 5 — Confusing durable queue with persistent messages

They are related but separate configuration concerns.

## Mistake 6 — Treating RabbitMQ as Kafka

The systems have different storage, consumption and replay models.

______________________________________________________________________

# 79. Common Celery Mistakes

## Mistake 1 — Long work inside HTTP request

This increases latency and consumes API worker capacity.

## Mistake 2 — Non-idempotent tasks

Retries/duplicates can cause duplicate business effects.

## Mistake 3 — Unlimited concurrency

Workers can overwhelm databases and downstream services.

## Mistake 4 — Blind retries

Retries can amplify dependency failures.

## Mistake 5 — Using result backend as the business database

Important business state should have an appropriate durable source of truth.

## Mistake 6 — Confusing Beat with workers

Beat schedules tasks; workers execute them.

______________________________________________________________________

# 80. Interview Questions & Answers

## Q1. What is RabbitMQ?

**Answer:**

RabbitMQ is a message broker that receives messages, routes them through exchanges and delivers them to queues consumed
by applications or workers.

______________________________________________________________________

## Q2. What is an exchange?

**Answer:**

An exchange receives messages from producers and routes them to queues according to its exchange type, bindings and
routing information.

______________________________________________________________________

## Q3. What is a queue?

**Answer:**

A queue stores messages until consumers process them.

______________________________________________________________________

## Q4. What is a binding?

**Answer:**

A binding connects an exchange to a queue and defines routing relationships, including routing keys or patterns
depending on the exchange type.

______________________________________________________________________

## Q5. What is a routing key?

**Answer:**

A routing key is information associated with a message that an exchange can use to determine where the message should be
routed.

______________________________________________________________________

## Q6. Explain a direct exchange.

**Answer:**

A direct exchange routes messages using an exact routing-key match.

______________________________________________________________________

## Q7. Explain a topic exchange.

**Answer:**

A topic exchange supports pattern-based routing using routing keys, making it useful for event categories.

______________________________________________________________________

## Q8. Explain a fanout exchange.

**Answer:**

A fanout exchange broadcasts messages to queues bound to the exchange.

______________________________________________________________________

## Q9. What is ACK in RabbitMQ?

**Answer:**

An acknowledgment tells RabbitMQ that a consumer has successfully handled a message.

______________________________________________________________________

## Q10. Why is manual acknowledgment useful?

**Answer:**

It allows the consumer to acknowledge a message only after successful processing, reducing the risk of losing work when
a worker fails before processing completes.

______________________________________________________________________

## Q11. What happens if a consumer crashes before ACK?

**Answer:**

Depending on the acknowledgment and queue configuration, the unacknowledged message can become available for redelivery
to another consumer.

______________________________________________________________________

## Q12. What is prefetch?

**Answer:**

Prefetch limits how many unacknowledged messages can be delivered to a consumer at once.

______________________________________________________________________

## Q13. Why does prefetch matter?

**Answer:**

It controls workload distribution and can prevent one consumer from receiving too many outstanding messages while others
remain idle.

______________________________________________________________________

## Q14. What is TTL?

**Answer:**

Time To Live defines how long a message or queue is allowed to exist before expiration according to the configured
RabbitMQ behavior.

______________________________________________________________________

## Q15. What is a dead-letter exchange?

**Answer:**

A dead-letter exchange receives messages that have been dead-lettered from another queue because of conditions such as
rejection, expiration or queue limits.

______________________________________________________________________

## Q16. Why use dead-lettering?

**Answer:**

It isolates failed or expired messages so they can be inspected without endlessly interfering with normal processing.

______________________________________________________________________

## Q17. What is a durable queue?

**Answer:**

A durable queue is configured to survive broker restart.

______________________________________________________________________

## Q18. Does a durable queue guarantee message persistence?

**Answer:**

No.

Queue durability and message persistence are separate concerns. The exchange/queue/message configuration must all be
considered.

______________________________________________________________________

## Q19. What is Celery?

**Answer:**

Celery is a distributed Python task queue used to execute background tasks asynchronously using workers and a message
broker.

______________________________________________________________________

## Q20. What is a Celery task?

**Answer:**

A Python function registered with Celery so that it can be submitted and executed asynchronously by a worker.

______________________________________________________________________

## Q21. What is a Celery worker?

**Answer:**

A process that consumes Celery tasks from the broker and executes them.

______________________________________________________________________

## Q22. What is a Celery broker?

**Answer:**

The messaging system used to transport tasks between the application and workers. RabbitMQ and Redis are common choices.

______________________________________________________________________

## Q23. What is a Celery result backend?

**Answer:**

A storage system used by Celery to maintain task results and/or task state when configured.

______________________________________________________________________

## Q24. Broker vs result backend?

**Answer:**

The broker transports tasks. The result backend stores task results/state. They solve different problems.

______________________________________________________________________

## Q25. What is Celery Beat?

**Answer:**

Celery Beat is a scheduler that submits tasks periodically. Workers execute those tasks.

______________________________________________________________________

## Q26. Beat vs worker?

**Answer:**

Beat determines when a periodic task should be submitted. Workers determine where and when the task is executed.

______________________________________________________________________

## Q27. Why should Celery tasks be idempotent?

**Answer:**

Retries, worker failures and message redelivery can result in duplicate execution. Idempotency prevents duplicate
business effects.

______________________________________________________________________

## Q28. How would you make a payment task idempotent?

**Answer:**

Use a unique payment or idempotency key and enforce the business operation atomically so repeated task execution cannot
create a second charge.

______________________________________________________________________

## Q29. How should Celery retries work?

**Answer:**

Retry transient failures with bounded attempts, exponential backoff and potentially jitter. Do not retry permanent
validation or business-rule failures indefinitely.

______________________________________________________________________

## Q30. Why are timeouts important?

**Answer:**

They prevent a task or external operation from consuming worker capacity indefinitely.

______________________________________________________________________

## Q31. What is worker concurrency?

**Answer:**

The number of task executions a worker can perform concurrently according to its configured execution pool.

______________________________________________________________________

## Q32. Why can excessive worker concurrency be harmful?

**Answer:**

It can overwhelm databases, external APIs, CPU, memory or other downstream resources.

______________________________________________________________________

## Q33. How would you integrate Celery with FastAPI?

**Answer:**

The FastAPI endpoint validates the request, creates any necessary job state, enqueues a Celery task and returns a
job/task identifier. The worker performs the long-running operation asynchronously.

______________________________________________________________________

## Q34. Why return HTTP 202 for an asynchronous job?

**Answer:**

`202 Accepted` communicates that the request has been accepted for processing but the final work has not necessarily
completed.

______________________________________________________________________

## Q35. Why not use FastAPI's in-process background task for every job?

**Answer:**

In-process background tasks are tied to the application process and are not equivalent to a distributed durable task
queue. Celery provides separate workers, broker-based delivery and richer retry/execution capabilities.

______________________________________________________________________

## Q36. Kafka vs RabbitMQ?

**Answer:**

Kafka is primarily a partitioned event-streaming platform with retention, offsets and replay. RabbitMQ is primarily a
message broker centered around exchanges, queues, routing and acknowledgments.

______________________________________________________________________

## Q37. RabbitMQ vs Celery?

**Answer:**

RabbitMQ is a message broker. Celery is a Python task execution framework that can use RabbitMQ as its broker.

______________________________________________________________________

## Q38. Kafka vs Celery?

**Answer:**

Kafka is designed around event streams and replayable logs. Celery is designed around asynchronous execution of Python
tasks.

______________________________________________________________________

## Q39. When would you choose Kafka?

**Answer:**

For high-throughput event streams, replay, multiple independent consumers and partition-based scaling.

______________________________________________________________________

## Q40. When would you choose RabbitMQ?

**Answer:**

For flexible routing, work queues, task distribution and queue-centric message processing.

______________________________________________________________________

## Q41. When would you choose Celery?

**Answer:**

When the primary requirement is executing Python background tasks asynchronously with workers, retries, scheduling and
task execution semantics.

______________________________________________________________________

## Q42. What happens if a Celery worker fails during a task?

**Answer:**

The exact behavior depends on acknowledgment, task and broker configuration. The task may be redelivered or otherwise
handled according to the configured execution semantics.

______________________________________________________________________

## Q43. What is a retry storm?

**Answer:**

A situation where many failed tasks immediately retry and create even more load on an already failing dependency.

______________________________________________________________________

## Q44. How do you prevent retry storms?

**Answer:**

Use bounded retries, exponential backoff, jitter and error classification.

______________________________________________________________________

## Q45. What is a poison message?

**Answer:**

A message that repeatedly fails processing and cannot succeed without correction.

______________________________________________________________________

## Q46. How should poison messages be handled?

**Answer:**

Limit retries and isolate the message through a dead-letter or equivalent failure-handling mechanism.

______________________________________________________________________

## Q47. What is prefetch's relationship to fairness?

**Answer:**

Lower prefetch can improve fairness by preventing one consumer from holding too many unacknowledged messages.

______________________________________________________________________

## Q48. Why is durable infrastructure important?

**Answer:**

It can help messages and messaging topology survive broker restarts when combined with appropriate persistence settings.

______________________________________________________________________

## Q49. Should every task use a result backend?

**Answer:**

No.

If the application does not need task results/state from Celery, a result backend may not be necessary. Important
business state should generally be stored in the application's appropriate durable store.

______________________________________________________________________

## Q50. Give a senior-level answer for Kafka vs RabbitMQ vs Celery.

**Answer:**

"I would first identify whether I need event streaming, message routing or Python task execution. Kafka is a strong
choice for high-throughput event streams, durable retention, replay and independent consumer groups. RabbitMQ is a
strong choice for queue-centric work distribution and flexible routing with exchanges, queues and acknowledgments.
Celery is a Python task execution framework and can use RabbitMQ or Redis as its broker. For a FastAPI application doing
long-running Python jobs, I would typically consider Celery with a suitable broker. For domain events consumed
independently by multiple services, I would consider Kafka. The final choice depends on ordering, replay, routing,
delivery, latency, operational and failure-handling requirements."

______________________________________________________________________

# 81. Scenario-Based Questions

## Scenario 1 — Send Email After Signup

A user registration API should return immediately while email is sent asynchronously.

**Answer:**

Use a background task architecture such as:

```text
FastAPI
 ↓
Celery task
 ↓
RabbitMQ/Redis broker
 ↓
Email worker
```

Return a successful asynchronous response without waiting for the email provider.

______________________________________________________________________

## Scenario 2 — Worker Crashes

A RabbitMQ worker receives a message and crashes before processing finishes.

**Answer:**

With appropriate manual acknowledgment behavior, the unacknowledged message can be redelivered. The processing operation
should be idempotent to tolerate duplicate execution.

______________________________________________________________________

## Scenario 3 — Poison Message

A message always fails because its payload is invalid.

**Answer:**

Do not requeue indefinitely. Apply a bounded retry policy and dead-letter the message for investigation.

______________________________________________________________________

## Scenario 4 — Uneven Work Distribution

One RabbitMQ worker receives many long-running tasks while another is idle.

**Answer:**

Review prefetch and consumer configuration. Lowering prefetch can improve fairness for uneven task durations.

______________________________________________________________________

## Scenario 5 — Expiring Jobs

A job is useful only for five minutes.

**Answer:**

Consider TTL so stale messages do not remain indefinitely.

______________________________________________________________________

## Scenario 6 — Periodic Cleanup

A database cleanup task must run every night.

**Answer:**

Use Celery Beat to schedule the task and Celery workers to execute it.

______________________________________________________________________

## Scenario 7 — External API Failure

A Celery task calls an external API that is temporarily unavailable.

**Answer:**

Use an appropriate timeout and bounded retry policy with exponential backoff and jitter. Do not retry permanent errors
indefinitely.

______________________________________________________________________

## Scenario 8 — Duplicate Payment Task

A payment task executes twice due to redelivery.

**Answer:**

Use an idempotency key and an atomic business-state mechanism so the second execution does not create a second payment.

______________________________________________________________________

## Scenario 9 — Many Independent Consumers

An order event must be consumed independently by:

```text
Analytics
Inventory
Notifications
```

**Answer:**

Kafka is a strong candidate because independent consumer groups can consume the same retained event stream.

______________________________________________________________________

## Scenario 10 — Flexible Routing

A system needs:

```text
order.created
order.updated
payment.created
```

with different consumers subscribing to patterns.

**Answer:**

RabbitMQ topic exchanges can provide pattern-based routing using routing keys.

______________________________________________________________________

## Scenario 11 — Run Python Report Generation

A user requests a large report that takes two minutes to generate.

**Answer:**

Use Celery rather than keeping the HTTP request open for two minutes.

A suitable API flow is:

```text
POST /reports
   ↓
Create job
   ↓
Enqueue task
   ↓
202 + job ID
```

Then expose job status separately.

______________________________________________________________________

## Scenario 12 — Worker Concurrency Overloads Database

Increasing Celery workers improved throughput but caused database failures.

**Answer:**

Worker concurrency has exceeded downstream capacity. Reduce concurrency or introduce appropriate rate limiting/batching
and optimize the database workload.

______________________________________________________________________

# 82. Practice Exercises

## Exercise 1 — RabbitMQ Direct Exchange

Create:

```text
Exchange: orders
Queue: order-worker
Routing key: order.created
```

Publish and consume an event.

______________________________________________________________________

## Exercise 2 — Topic Routing

Create routing keys:

```text
order.created
order.updated
payment.created
```

Create bindings for:

```text
order.*
```

Verify routing behavior.

______________________________________________________________________

## Exercise 3 — Fanout

Create multiple queues bound to a fanout exchange.

Publish one message and verify that each queue receives it.

______________________________________________________________________

## Exercise 4 — Manual ACK

Create a consumer that:

```text
Receive
 ↓
Process
 ↓
ACK
```

Force a worker failure before ACK and observe redelivery.

______________________________________________________________________

## Exercise 5 — Prefetch

Compare:

```text
prefetch = 1
```

with a larger prefetch under uneven task durations.

Document the effect on fairness and throughput.

______________________________________________________________________

## Exercise 6 — TTL

Publish messages with a short TTL.

Observe what happens when consumers do not process them before expiration.

______________________________________________________________________

## Exercise 7 — Dead Letter

Configure a dead-letter exchange and queue.

Send a message that repeatedly fails and document its final destination.

______________________________________________________________________

## Exercise 8 — Celery Task

Create:

```python
generate_report(report_id)
```

and execute it asynchronously from a Python application.

______________________________________________________________________

## Exercise 9 — FastAPI + Celery

Create:

```text
POST /reports
GET /reports/{id}
```

The POST endpoint should enqueue a task and return a job identifier.

______________________________________________________________________

## Exercise 10 — Celery Retry

Create a task that fails temporarily.

Implement:

```text
retry
backoff
maximum attempts
```

and document the behavior.

______________________________________________________________________

## Exercise 11 — Idempotent Task

Create a task that processes:

```text
payment_id
```

Ensure repeated execution cannot create duplicate business effects.

______________________________________________________________________

## Exercise 12 — Celery Beat

Create a periodic task that runs every few minutes.

Document:

```text
Beat
 ↓
Broker
 ↓
Worker
```

______________________________________________________________________

## Exercise 13 — Worker Concurrency

Run tasks with different execution times.

Experiment with worker concurrency and measure:

- Throughput
- Task latency
- Database load

______________________________________________________________________

## Exercise 14 — Kafka vs RabbitMQ

For each scenario, choose one:

1. Event replay
1. Flexible routing
1. Python background task
1. Multiple independent event consumers
1. Work queue
1. Periodic Python job

Explain your reasoning.

______________________________________________________________________

## Exercise 15 — Production Design

Design:

```text
FastAPI
+
RabbitMQ
+
Celery
+
PostgreSQL
```

for:

```text
10,000 background jobs/minute
```

Explain:

- Queue design
- Exchange design
- Routing keys
- ACK
- Prefetch
- Retry
- Dead-letter handling
- Task idempotency
- Worker concurrency
- Timeouts
- Database capacity
- Monitoring
- Failure recovery

______________________________________________________________________

# 83. Quick Revision

| Concept | Key Point |
|---|---|
| RabbitMQ | Message broker |
| Producer | Publishes messages |
| Exchange | Routes messages |
| Queue | Stores messages for consumers |
| Binding | Connects exchange to queue |
| Routing key | Routing information |
| Direct exchange | Exact routing-key match |
| Topic exchange | Pattern-based routing |
| Fanout exchange | Broadcast |
| Headers exchange | Header-based routing |
| ACK | Confirms successful processing |
| Manual ACK | Application controls acknowledgment |
| Prefetch | Limits unacknowledged deliveries |
| TTL | Message/queue expiration mechanism |
| DLX | Dead-letter exchange |
| Durable queue | Queue survives broker restart when configured |
| Persistent message | Message configured for persistence |
| Celery | Python distributed task queue |
| Task | Asynchronous Python operation |
| Worker | Executes tasks |
| Broker | Transports tasks |
| Result backend | Stores task results/state |
| Retry | Reattempt failed task |
| Backoff | Delays retries |
| Timeout | Limits execution/waiting |
| Beat | Periodic task scheduler |
| Worker concurrency | Parallel task execution capacity |
| Idempotency | Duplicate execution has safe final effect |
| FastAPI + Celery | HTTP API submits asynchronous jobs |
| Kafka | Event streaming platform |
| RabbitMQ | Queue/message routing broker |
| Celery | Python task execution framework |

______________________________________________________________________

# 84. Completion Checklist

Before moving to File 30, make sure you can explain:

- [ ] RabbitMQ architecture
- [ ] Producer
- [ ] Exchange
- [ ] Queue
- [ ] Binding
- [ ] Routing key
- [ ] Direct exchange
- [ ] Topic exchange
- [ ] Fanout exchange
- [ ] Headers exchange
- [ ] Consumer
- [ ] ACK
- [ ] Manual acknowledgment
- [ ] Redelivery
- [ ] Prefetch
- [ ] Prefetch trade-offs
- [ ] TTL
- [ ] Dead-letter exchange
- [ ] Dead-letter queue
- [ ] Retry loops
- [ ] Durable queues
- [ ] Persistent messages
- [ ] Durable exchanges
- [ ] RabbitMQ failure handling
- [ ] Celery architecture
- [ ] Celery task
- [ ] Celery worker
- [ ] Celery broker
- [ ] Result backend
- [ ] Broker vs result backend
- [ ] Celery retry
- [ ] Backoff
- [ ] Retry storms
- [ ] Timeouts
- [ ] Celery Beat
- [ ] Worker concurrency
- [ ] Concurrency limits
- [ ] Task idempotency
- [ ] FastAPI integration
- [ ] Asynchronous job APIs
- [ ] HTTP 202
- [ ] Task status
- [ ] Celery failure scenarios
- [ ] Kafka vs RabbitMQ
- [ ] RabbitMQ vs Celery
- [ ] Kafka vs Celery
- [ ] Tool-selection trade-offs

______________________________________________________________________

# 85. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is RabbitMQ?
1. What is an exchange?
1. What is a queue?
1. What is a binding?
1. What is a routing key?
1. Explain direct exchange.
1. Explain topic exchange.
1. Explain fanout exchange.
1. What is a headers exchange?
1. What is an ACK?
1. Why use manual ACK?
1. What happens if a worker crashes before ACK?
1. What is prefetch?
1. Why does prefetch matter?
1. What is TTL?
1. What is a dead-letter exchange?
1. Why use dead-lettering?
1. What is a poison message?
1. How do you avoid infinite requeue loops?
1. What does durable queue mean?
1. Does durable queue guarantee persistent messages?
1. What is Celery?
1. What is a Celery task?
1. What is a Celery worker?
1. What is a Celery broker?
1. What is a result backend?
1. Broker vs result backend?
1. What is Celery Beat?
1. Beat vs worker?
1. How does Celery retry work?
1. Why use exponential backoff?
1. Why use jitter?
1. Why should tasks be idempotent?
1. How would you make a payment task idempotent?
1. Why are timeouts important?
1. What is worker concurrency?
1. Why can excessive concurrency hurt performance?
1. How would you integrate Celery with FastAPI?
1. Why return 202 for asynchronous work?
1. Why not execute every long-running task inside FastAPI?
1. How should a job-status API work?
1. What happens if a Celery worker crashes?
1. How would you handle a poison task?
1. How would you handle an external API outage?
1. Kafka vs RabbitMQ?
1. RabbitMQ vs Celery?
1. Kafka vs Celery?
1. When would you choose Kafka?
1. When would you choose RabbitMQ?
1. When would you choose Celery?
1. Design FastAPI + Celery + RabbitMQ for background jobs.
1. How would you prevent duplicate task execution?
1. How would you control worker/database pressure?
1. How would you design retries and dead-letter handling?
1. Give a senior-level Kafka vs RabbitMQ vs Celery recommendation.

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

# 86. Final Senior Interview Scenario

You are designing a Python backend with:

```text
FastAPI
PostgreSQL
RabbitMQ
Celery
```

The system receives:

```text
10,000 background jobs/minute
```

Jobs include:

```text
Email delivery
PDF generation
External API synchronization
Database cleanup
```

Design the architecture.

Your answer should cover:

1. RabbitMQ exchanges.
1. Queue structure.
1. Routing keys.
1. Consumer acknowledgment.
1. Prefetch.
1. TTL.
1. Retry strategy.
1. Dead-letter handling.
1. Celery workers.
1. Worker concurrency.
1. Task timeouts.
1. Idempotency.
1. Celery Beat.
1. FastAPI job submission.
1. Job status.
1. Database capacity.
1. External API limits.
1. Failure recovery.
1. Monitoring.
1. When Kafka would be a better choice.

A strong senior-level answer should make the distinction clear:

> **RabbitMQ moves and routes messages. Celery executes Python tasks. FastAPI exposes the application API. PostgreSQL remains the appropriate source of truth for durable business state.**

______________________________________________________________________

**Previous:** [28. Kafka](./28-kafka.md)

**Next:** [30. Docker](./30-docker.md)
