# 28. Kafka

**Previous:** [27. Redis Caching & Production](./27-redis-caching.md)

**Next:** [29. RabbitMQ & Celery](./29-rabbitmq-celery.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain Kafka's architecture and core terminology.
- Understand brokers, topics and partitions.
- Explain how producers publish messages.
- Understand consumers, offsets and consumer groups.
- Explain partition ordering.
- Understand replication and fault tolerance.
- Explain consumer lag and how to reason about it.
- Compare at-most-once, at-least-once and exactly-once delivery semantics.
- Understand why idempotency is important in event-driven systems.
- Design retry and dead-letter handling.
- Explain schema evolution.
- Discuss common Kafka production and interview trade-offs.

> **Scope note:** This file focuses on Kafka fundamentals and practical backend interview knowledge. It does not attempt to cover Kafka internals, advanced broker tuning, Kafka Streams in depth, or large-scale cluster operations.

______________________________________________________________________

# 1. What Is Kafka?

Apache Kafka is a distributed event streaming platform commonly used for:

- Event-driven architectures
- Asynchronous processing
- Service-to-service communication
- Event pipelines
- Log aggregation
- Data integration
- High-throughput message processing

A simplified architecture is:

```text
Producer
   ↓
Kafka
   ↓
Consumer
```

Kafka is designed to handle large volumes of ordered event data.

______________________________________________________________________

# 2. Why Use Kafka?

Kafka is useful when a system needs:

- High-throughput event ingestion
- Durable event storage
- Asynchronous processing
- Multiple independent consumers
- Replayable events
- Decoupling between services

For example:

```text
Order Service
     ↓
Kafka
     ↓
 ┌──────────────┬──────────────┐
 ↓              ↓              ↓
Email Service   Analytics      Inventory
```

The producer does not need to synchronously call every downstream service.

______________________________________________________________________

# 3. Kafka Core Concepts

The most important terms are:

```text
Broker
Topic
Partition
Producer
Consumer
Offset
Consumer Group
Replication
```

Understanding how these concepts relate to each other is more important than memorizing definitions independently.

______________________________________________________________________

# 4. Broker

A Kafka broker is a Kafka server that stores and serves event data.

A Kafka cluster contains multiple brokers.

Conceptually:

```text
Kafka Cluster
 ├── Broker 1
 ├── Broker 2
 └── Broker 3
```

Brokers work together to provide distributed storage and processing.

______________________________________________________________________

# 5. Kafka Cluster

A Kafka cluster is a group of Kafka brokers working together.

A cluster can provide:

- Data distribution
- Replication
- Fault tolerance
- Increased throughput
- Horizontal capacity

A production Kafka deployment normally uses multiple brokers.

______________________________________________________________________

# 6. Topic

A topic is a logical category or stream of events.

Examples:

```text
orders
payments
user-events
notifications
```

A producer publishes events to a topic.

Consumers read events from a topic.

______________________________________________________________________

# 7. Topic Is Not a Single Queue

A topic is divided into partitions.

For example:

```text
orders
 ├── Partition 0
 ├── Partition 1
 └── Partition 2
```

Partitions are fundamental to Kafka's scalability and ordering model.

______________________________________________________________________

# 8. Partition

A partition is an ordered, append-only sequence of records.

Conceptually:

```text
Partition 0

Offset
  0 → Event A
  1 → Event B
  2 → Event C
  3 → Event D
```

Each record has an offset within its partition.

______________________________________________________________________

# 9. Why Partitions?

Partitions allow a topic to be distributed across brokers.

For example:

```text
Broker 1 → Partition 0
Broker 2 → Partition 1
Broker 3 → Partition 2
```

Multiple consumers can process different partitions concurrently.

This is one of Kafka's primary scalability mechanisms.

______________________________________________________________________

# 10. Partition Ordering

Kafka guarantees ordering within a partition.

For example:

```text
Partition 0

0 → OrderCreated
1 → OrderPaid
2 → OrderShipped
```

A consumer reading this partition sees records in partition order.

Kafka does not provide a simple global ordering guarantee across all partitions of a topic.

______________________________________________________________________

# 11. Global Ordering

Suppose:

```text
Topic
 ├── P0
 ├── P1
 └── P2
```

There can be:

```text
P0: A → B → C
P1: D → E → F
P2: G → H → I
```

Kafka preserves ordering inside each partition, but there is no single ordering such as:

```text
A → D → G → B → E → H ...
```

across the entire topic.

______________________________________________________________________

# 12. Choosing the Partition Key

Producers can provide a key when publishing an event.

A common design is:

```text
key = order_id
```

Records with the same key can be routed to the same partition according to the producer's partitioning behavior.

This is useful when events for the same entity need ordering.

______________________________________________________________________

# 13. Example: Order Events

Suppose:

```text
order_id = 1001
```

generates:

```text
OrderCreated
OrderPaid
OrderShipped
```

Using:

```text
key = order_id
```

can keep those events associated with the same partition.

This allows their relative ordering to be preserved within that partition.

______________________________________________________________________

# 14. Producer

A producer is an application that publishes records to Kafka.

Example:

```text
Order Service
     ↓
Producer
     ↓
orders topic
```

A producer typically specifies:

- Topic
- Value
- Optional key
- Optional headers

______________________________________________________________________

# 15. Producer Flow

A simplified flow is:

```text
Application
    ↓
Kafka Producer
    ↓
Choose partition
    ↓
Send record to broker
    ↓
Broker stores record
```

The producer can receive an acknowledgment indicating how the send was handled.

______________________________________________________________________

# 16. Producer Keys

Keys are useful for controlling partition assignment.

Example:

```text
key = customer_id
```

This can ensure events for the same customer are consistently associated with the same partition under the producer's
partitioning scheme.

This is useful when ordering matters per customer.

______________________________________________________________________

# 17. Producer Batching

Kafka producers can batch records before sending them.

Batching can improve throughput by reducing network overhead.

Conceptually:

```text
Event A
Event B
Event C
   ↓
Batch
   ↓
Kafka
```

The trade-off is that waiting to form a batch can add some latency.

______________________________________________________________________

# 18. Producer Compression

Kafka producers can compress batches.

Compression can reduce:

- Network traffic
- Storage requirements

But it introduces CPU work for compression/decompression.

The appropriate configuration depends on workload and infrastructure.

______________________________________________________________________

# 19. Consumer

A consumer is an application that reads records from Kafka.

Example:

```text
Kafka
  ↓
Consumer
  ↓
Business logic
```

Consumers track their progress using offsets.

______________________________________________________________________

# 20. Offset

An offset identifies a record's position within a partition.

Example:

```text
Partition 0

Offset 0 → A
Offset 1 → B
Offset 2 → C
Offset 3 → D
```

A consumer can use the offset to know where it is in the partition.

______________________________________________________________________

# 21. Offset Is Partition-Scoped

An offset such as:

```text
100
```

does not identify a globally unique Kafka record by itself.

It is meaningful together with the partition.

Conceptually:

```text
topic + partition + offset
```

identifies a record position.

______________________________________________________________________

# 22. Consumer Group

A consumer group is a group of consumers cooperating to process a topic.

For example:

```text
orders topic
     ↓
Consumer Group A
 ├── Consumer 1
 ├── Consumer 2
 └── Consumer 3
```

Partitions are distributed among consumers in the group.

______________________________________________________________________

# 23. Consumer Group Parallelism

Suppose:

```text
Topic → 6 partitions
Consumer group → 3 consumers
```

The partitions can be distributed roughly as:

```text
Consumer 1 → P0, P1
Consumer 2 → P2, P3
Consumer 3 → P4, P5
```

This allows parallel processing.

______________________________________________________________________

# 24. More Consumers Than Partitions

Suppose:

```text
4 partitions
8 consumers
```

Within one consumer group, at most four consumers can actively own partitions at a time.

Some consumers will have no partition assigned.

Therefore:

> Partition count limits consumer-group parallelism.

______________________________________________________________________

# 25. Multiple Consumer Groups

Different consumer groups can independently consume the same topic.

Example:

```text
                 orders
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
   Group A              Group B
   Email                 Analytics
```

Each group maintains its own consumption progress.

______________________________________________________________________

# 26. Kafka as Pub/Sub

Multiple consumer groups allow Kafka to behave like a durable event distribution system.

For example:

```text
orders
  ↓
 ┌─────────────┬─────────────┬─────────────┐
 ↓             ↓             ↓
Email Group    Inventory     Analytics
               Group         Group
```

Each group can independently process the same events.

______________________________________________________________________

# 27. Consumer Rebalancing

When consumers join, leave or fail, Kafka can rebalance partition assignments within a consumer group.

For example:

```text
Before:
C1 → P0, P1
C2 → P2, P3

C3 joins

After:
C1 → P0
C2 → P2
C3 → P1, P3
```

Rebalancing enables the group to adapt to membership changes.

______________________________________________________________________

# 28. Rebalancing Trade-Off

Rebalancing is useful but can temporarily disrupt processing.

Poorly behaved consumers can cause repeated group changes.

Production systems therefore pay attention to:

- Consumer stability
- Processing time
- Poll behavior
- Timeouts
- Group configuration

______________________________________________________________________

# 29. Consumer Lag

Consumer lag measures how far a consumer group is behind the latest available records.

Conceptually:

```text
Latest offset = 1000
Consumer offset = 900

Lag ≈ 100 records
```

Lag is an important operational metric.

______________________________________________________________________

# 30. Why Consumer Lag Matters

Growing lag can indicate:

- Consumer processing is too slow
- Too few consumers
- Too much incoming traffic
- Slow downstream services
- Consumer failures
- Rebalancing problems

A temporary lag spike is not necessarily an outage.

The trend and processing capacity matter.

______________________________________________________________________

# 31. Reducing Consumer Lag

Possible approaches include:

- Increase consumer processing capacity
- Add consumers, if partitions allow it
- Increase partition count where appropriate
- Optimize processing
- Batch work
- Reduce downstream latency
- Scale dependent services

Adding consumers beyond partition count does not increase parallelism within that group.

______________________________________________________________________

# 32. Replication

Kafka replicates partitions across brokers for fault tolerance.

For example:

```text
Partition 0
 ├── Broker 1
 ├── Broker 2
 └── Broker 3
```

One replica is the leader for the partition, while other replicas can maintain copies.

______________________________________________________________________

# 33. Partition Leader

For a replicated partition, one broker acts as the leader.

Producers and consumers generally interact with the partition leader for normal data operations.

Followers replicate the partition data.

If the leader fails, another eligible replica can be selected according to Kafka's configured cluster behavior.

______________________________________________________________________

# 34. Why Replication?

Replication protects against broker failure.

Without replication:

```text
Broker fails
   ↓
Partition unavailable/data risk
```

With replication:

```text
Broker fails
   ↓
Another replica can take over
```

Replication also affects storage requirements because data is stored multiple times.

______________________________________________________________________

# 35. Replication Factor

Replication factor describes how many copies of a partition are maintained.

For example:

```text
replication factor = 3
```

means the partition has three replicas.

Higher replication can improve fault tolerance but consumes more storage and network resources.

______________________________________________________________________

# 36. Producer Acknowledgments

Producer acknowledgment settings determine when the producer considers a write acknowledged.

At a high level:

```text
acks=0
acks=1
acks=all
```

### `acks=0`

The producer does not wait for a broker acknowledgment.

### `acks=1`

The leader acknowledges the record.

### `acks=all`

The leader waits for the required in-sync replicas according to the configured replication settings.

______________________________________________________________________

# 37. Durability Trade-Off

Higher acknowledgment guarantees can improve durability but may increase latency.

For example:

```text
Lower acknowledgment
→ potentially lower latency
→ weaker delivery/durability guarantees

Higher acknowledgment
→ stronger durability
→ potentially higher latency
```

The correct choice depends on the event's importance.

______________________________________________________________________

# 38. Delivery Semantics

A consumer/producer system can be designed around different delivery guarantees.

The major concepts are:

- At-most-once
- At-least-once
- Exactly-once

These are about how processing and delivery behave under failures.

______________________________________________________________________

# 39. At-Most-Once

At-most-once means:

> A message is processed zero or one time.

A message may be lost, but it should not be processed more than once under the intended processing model.

Conceptually:

```text
Read
 ↓
Commit offset
 ↓
Process
```

If processing fails after the offset is committed, the message may not be processed again.

______________________________________________________________________

# 40. At-Least-Once

At-least-once means:

> A message should not be lost under the intended processing model, but it may be processed more than once.

A common pattern is:

```text
Read
 ↓
Process
 ↓
Commit offset
```

If the consumer crashes after processing but before committing the offset:

```text
Process
  ↓
Crash
  ↓
Offset not committed
  ↓
Message processed again
```

This creates duplicate-processing risk.

______________________________________________________________________

# 41. Exactly-Once Concept

Exactly-once means that the system provides semantics where the intended effect of processing occurs once, despite
retries/failures, within the supported transactional/processing model.

It is important to avoid saying:

> "Kafka magically guarantees exactly-once for any external side effect."

Exactly-once semantics become much more complicated when processing includes external systems such as arbitrary
databases or APIs.

______________________________________________________________________

# 42. Why Exactly-Once Is Difficult

Consider:

```text
Kafka
  ↓
Consumer
  ↓
External API
```

The consumer might successfully call the external API and then crash before recording its Kafka progress.

On restart:

```text
Kafka message
   ↓
External API called again
```

Kafka alone cannot automatically undo or deduplicate arbitrary external side effects.

______________________________________________________________________

# 43. Idempotency

Idempotency means performing the same operation multiple times produces the same intended final result.

For example:

```text
Set order status = PAID
```

is easier to make idempotent than:

```text
Increase account balance by ₹100
```

because repeating an increment can change the result.

______________________________________________________________________

# 44. Idempotency Key

A consumer can use an event ID as an idempotency key.

Conceptually:

```text
event_id = abc123

Process:
  if abc123 already processed:
      skip
  else:
      perform operation
      record abc123
```

The deduplication store must itself be designed carefully.

______________________________________________________________________

# 45. Kafka and Idempotent Consumers

At-least-once delivery often means consumers should be designed to tolerate duplicates.

A robust consumer might:

```text
Receive event
   ↓
Check event ID
   ↓
Already processed?
 ┌───────┴───────┐
Yes              No
 ↓                ↓
Skip           Process
                  ↓
            Record completion
```

______________________________________________________________________

# 46. Retry

Retries are common when message processing fails temporarily.

Examples:

- Temporary database failure
- Network timeout
- External API unavailable
- Rate limit response

A retry strategy should distinguish transient errors from permanent failures.

______________________________________________________________________

# 47. Retry Storm

Blind retries can make an outage worse.

Example:

```text
Dependency fails
    ↓
1,000 messages fail
    ↓
1,000 immediate retries
    ↓
Dependency receives more traffic
    ↓
Failure worsens
```

Use controlled retry behavior.

______________________________________________________________________

# 48. Exponential Backoff

A common retry strategy increases the delay between attempts.

Example:

```text
Attempt 1 → 1 second
Attempt 2 → 2 seconds
Attempt 3 → 4 seconds
Attempt 4 → 8 seconds
```

A maximum delay is usually applied.

______________________________________________________________________

# 49. Retry Jitter

If every consumer retries at exactly the same time, they can create synchronized load.

Jitter adds randomness:

```text
base delay + random component
```

This helps distribute retries over time.

______________________________________________________________________

# 50. Dead-Letter Handling

A message that repeatedly fails processing may need to be moved to a dead-letter destination.

Conceptually:

```text
Main topic
   ↓
Consumer
   ↓ failure
Retry
   ↓ failure
Retry
   ↓ failure
Dead-letter topic
```

The exact implementation can vary.

______________________________________________________________________

# 51. Why Dead-Letter Handling?

It prevents one permanently bad message from repeatedly blocking normal processing.

Examples of permanent failures:

- Invalid payload
- Unsupported schema
- Missing required data
- Business rule violation

The dead-letter event can then be inspected and remediated separately.

______________________________________________________________________

# 52. Retry vs Dead Letter

Use retries for:

```text
Temporary failure
```

Use dead-letter handling for:

```text
Persistent/unrecoverable failure
```

The consumer should classify errors appropriately.

______________________________________________________________________

# 53. Poison Messages

A poison message is an event that repeatedly causes processing failure.

Without dead-letter handling:

```text
Message
 ↓
Fail
 ↓
Retry
 ↓
Fail
 ↓
Retry forever
```

This can waste consumer capacity.

A retry limit and dead-letter strategy can isolate the message.

______________________________________________________________________

# 54. Schema

A Kafka record typically contains data whose structure consumers need to understand.

For example:

```json
{
  "order_id": 1001,
  "status": "PAID"
}
```

As systems evolve, schemas change.

______________________________________________________________________

# 55. Schema Evolution

Suppose version 1 is:

```json
{
  "order_id": 1001,
  "status": "PAID"
}
```

Version 2 adds:

```json
{
  "order_id": 1001,
  "status": "PAID",
  "currency": "INR"
}
```

Consumers must be able to handle the evolution safely.

______________________________________________________________________

# 56. Backward Compatibility

A new producer version should ideally remain compatible with existing consumers where required.

For example, adding an optional field is generally easier to evolve than removing or changing the meaning of an existing
field.

The exact compatibility rules depend on the schema technology and policy.

______________________________________________________________________

# 57. Schema Registry — Overview

Kafka ecosystems often use a schema registry to manage and validate message schemas.

At a high level:

```text
Producer
   ↓
Schema Registry
   ↓
Kafka
   ↓
Consumer
   ↓
Schema Registry
```

A schema registry can enforce compatibility rules and make schema evolution more manageable.

______________________________________________________________________

# 58. Why Schema Evolution Matters

Without schema discipline:

```text
Producer changes
     ↓
Consumer breaks
```

With compatibility rules:

```text
Producer v2
     ↓
Compatible schema
     ↓
Existing consumers continue working
```

This is especially important when producers and consumers are deployed independently.

______________________________________________________________________

# 59. Kafka Message Retention

Kafka stores records for a configured retention period or according to configured storage policies.

This is an important difference from traditional queue semantics.

A consumer does not necessarily remove a message from Kafka after processing it.

Instead, the record remains available according to retention.

______________________________________________________________________

# 60. Replay

Because records remain available according to retention, consumers can replay historical events by resetting/choosing
appropriate offsets.

Example:

```text
Events
0 1 2 3 4 5 6 7

Consumer processed:
0 1 2

Consumer can later start again from:
1
```

Replay is one of Kafka's major strengths.

______________________________________________________________________

# 61. Kafka vs Traditional Queue

A traditional queue often emphasizes:

```text
produce → consume → remove
```

Kafka emphasizes:

```text
append → retain → consume by offset
```

This makes Kafka useful for event streams and replayable processing.

______________________________________________________________________

# 62. Kafka Consumer Commit

Consumers need to record progress.

The committed offset represents the position the consumer group has recorded.

The relationship between:

```text
processing
+
offset commit
```

is central to delivery semantics.

______________________________________________________________________

# 63. Commit Too Early

If the consumer commits before processing:

```text
Read
 ↓
Commit
 ↓
Process
 ↓
Crash
```

The event may not be processed again.

This is consistent with an at-most-once-style approach but can result in loss.

______________________________________________________________________

# 64. Commit Too Late

If processing succeeds but the consumer crashes before committing:

```text
Read
 ↓
Process
 ↓
Crash
 ↓
No commit
```

The event can be processed again.

This is a common source of at-least-once duplicates.

______________________________________________________________________

# 65. Offset Commit and Idempotency

A common practical strategy is:

```text
Read
 ↓
Process idempotently
 ↓
Commit offset
```

If the consumer crashes before commit, the event may run again, but the idempotent operation prevents an incorrect
duplicate effect.

______________________________________________________________________

# 66. Kafka Consumer Processing Model

A simplified consumer loop:

```text
Poll records
   ↓
Process records
   ↓
Commit offsets
   ↓
Poll again
```

The exact client APIs and configuration vary.

______________________________________________________________________

# 67. Batch Processing

Consumers can process records in batches.

Benefits can include:

- Better throughput
- Fewer database round trips
- Better network efficiency

Trade-offs include:

- Increased processing latency
- Larger failure/retry units
- More complicated partial-failure handling

______________________________________________________________________

# 68. Kafka and Databases

A common architecture is:

```text
Kafka
  ↓
Consumer
  ↓
Database
```

The key challenge is coordinating:

```text
Kafka offset
+
database transaction
```

______________________________________________________________________

# 69. Database + Kafka Dual Write Problem

Suppose a service needs to:

```text
Update database
+
Publish Kafka event
```

If these are separate operations:

```text
DB commit succeeds
Kafka publish fails
```

the system becomes inconsistent.

Or:

```text
Kafka publish succeeds
DB commit fails
```

the event may describe a change that did not persist.

This is a classic distributed consistency problem.

______________________________________________________________________

# 70. Transactional Outbox — Overview

One common solution is the transactional outbox pattern.

Conceptually:

```text
Application
   ↓
Database transaction
 ├── Business data
 └── Outbox event
        ↓
   Outbox publisher
        ↓
      Kafka
```

The business update and outbox record are committed together.

A separate process publishes the outbox event to Kafka.

______________________________________________________________________

# 71. Why Outbox Helps

If the database transaction succeeds:

```text
Business data + outbox event
```

are both durable together.

If Kafka is temporarily unavailable, the publisher can retry the outbox event later.

This reduces the dual-write inconsistency problem.

______________________________________________________________________

# 72. Kafka Consumer and External APIs

Suppose:

```text
Kafka
 ↓
Consumer
 ↓
Payment API
```

The consumer can receive the same event more than once.

The external operation should ideally support idempotency.

For example:

```text
payment_id = 123
idempotency_key = event_id
```

The downstream system can reject duplicate requests or return the existing result.

______________________________________________________________________

# 73. Ordering vs Parallelism

Kafka's key trade-off:

```text
More partitions
→ more parallelism
→ more possible independent ordering streams
```

If all events must be globally ordered, putting everything into one partition may provide ordering but limits
parallelism.

A practical design often chooses:

```text
ordering per entity
```

rather than global ordering.

______________________________________________________________________

# 74. Partition Count Trade-Off

More partitions can provide more parallelism.

But partitions also introduce:

- More metadata
- More files/resources
- More replication traffic
- More consumer-management complexity

Partition count should be chosen based on expected throughput and parallelism requirements.

______________________________________________________________________

# 75. Consumer Lag and Scaling

Suppose:

```text
Incoming = 100,000 events/sec
Processing capacity = 80,000 events/sec
```

Lag will grow.

To reduce lag, increase effective processing capacity through:

- More consumers
- More partitions
- Faster processing
- Better batching
- Faster downstream dependencies

Adding consumers alone cannot exceed available partition parallelism.

______________________________________________________________________

# 76. Backpressure

If consumers cannot process events as quickly as producers publish them, backlog grows.

This is a form of backpressure.

The system needs to consider:

- Consumer capacity
- Retry behavior
- Downstream capacity
- Queue/topic retention
- Alerting thresholds

______________________________________________________________________

# 77. Consumer Lag Alerting

A production system should monitor:

- Current lag
- Lag growth rate
- Processing latency
- Consumer errors
- Rebalances
- Throughput

A large lag number alone does not always indicate failure.

For example:

```text
Lag = 1 million
```

could be acceptable if consumers process:

```text
200,000/sec
```

and the backlog is rapidly shrinking.

______________________________________________________________________

# 78. Kafka Failure Scenarios

Common failures include:

### Producer failure

Events may fail to reach Kafka.

### Broker failure

Replicas may need to take over.

### Consumer failure

Partitions are reassigned and uncommitted events may be processed again.

### Dependency failure

Consumer processing can fail and create lag.

### Poison message

Repeated failures can block useful processing unless isolated.

______________________________________________________________________

# 79. At-Least-Once Practical Architecture

A common practical backend design is:

```text
Kafka
  ↓
Consumer
  ↓
Idempotent processing
  ↓
Database
  ↓
Commit offset
```

If processing succeeds but the consumer crashes before committing:

```text
Same event
   ↓
processed again
   ↓
idempotency prevents duplicate effect
```

This is often simpler than attempting to make every external operation exactly once.

______________________________________________________________________

# 80. Exactly-Once Concept in Practice

Exactly-once semantics can be meaningful within supported Kafka transactional processing scenarios.

However:

```text
Kafka
 ↓
External DB/API
```

requires additional coordination.

Therefore in interviews, explain exactly-once carefully:

> Kafka can provide transactional/exactly-once processing semantics in supported scenarios, but arbitrary external side effects still require their own idempotency/transaction strategy.

______________________________________________________________________

# 81. Kafka Design Checklist

When designing Kafka, ask:

### Topic

- What event does the topic represent?
- How long should events be retained?

### Partitions

- What is the expected throughput?
- What ordering is required?
- What key should determine partitioning?

### Producers

- What acknowledgment guarantees are required?
- Is producer retry enabled?
- Is idempotent publishing needed?

### Consumers

- How many consumers are required?
- What processing latency is expected?
- How are offsets committed?

### Failures

- What happens after a consumer crash?
- What happens when a dependency is unavailable?
- How are poison messages handled?

### Reliability

- What replication factor is appropriate?
- What durability guarantees are required?

### Schema

- How will schemas evolve?
- What compatibility rules are required?

______________________________________________________________________

# 82. Common Kafka Mistakes

## Mistake 1 — Assuming Kafka guarantees global ordering

Ordering is primarily guaranteed within a partition.

## Mistake 2 — Adding unlimited consumers

Consumer-group parallelism is bounded by partition count.

## Mistake 3 — Ignoring consumer lag

Growing lag can indicate that processing capacity is below incoming throughput.

## Mistake 4 — Blind retries

Retries can amplify an outage.

## Mistake 5 — Assuming exactly-once solves external side effects

External APIs and databases need their own consistency/idempotency design.

## Mistake 6 — No idempotency

At-least-once processing can produce duplicate effects.

## Mistake 7 — No dead-letter strategy

Poison messages can consume consumer capacity indefinitely.

## Mistake 8 — Poor partition key

An unsuitable key can create ordering or hotspot problems.

## Mistake 9 — Uncontrolled schema changes

Independent producer/consumer deployments require compatibility planning.

______________________________________________________________________

# 83. Interview Questions & Answers

## Q1. What is Kafka?

**Answer:**

Kafka is a distributed event streaming platform used for high-throughput, durable and replayable event processing and
communication between services.

______________________________________________________________________

## Q2. What is a Kafka broker?

**Answer:**

A Kafka broker is a server that stores and serves Kafka records as part of a Kafka cluster.

______________________________________________________________________

## Q3. What is a topic?

**Answer:**

A topic is a logical stream/category of records published by producers and consumed by consumers.

______________________________________________________________________

## Q4. What is a partition?

**Answer:**

A partition is an ordered append-only sequence of records within a topic. Partitions provide scalability and
parallelism.

______________________________________________________________________

## Q5. Why does Kafka use partitions?

**Answer:**

Partitions allow a topic to be distributed across brokers and processed concurrently by multiple consumers.

______________________________________________________________________

## Q6. Does Kafka guarantee ordering?

**Answer:**

Kafka guarantees ordering within a partition, not a single global ordering across all partitions.

______________________________________________________________________

## Q7. How would you preserve order for a customer?

**Answer:**

Use a stable partition key such as `customer_id`, so events for that customer are routed consistently to the same
partition under the producer's partitioning strategy.

______________________________________________________________________

## Q8. What is a Kafka producer?

**Answer:**

An application that publishes records to Kafka topics.

______________________________________________________________________

## Q9. What is a Kafka consumer?

**Answer:**

An application that reads and processes records from Kafka topics.

______________________________________________________________________

## Q10. What is an offset?

**Answer:**

An offset identifies a record's position within a partition.

______________________________________________________________________

## Q11. Is an offset globally unique?

**Answer:**

No.

An offset is scoped to a partition. A record position is generally understood using topic, partition and offset.

______________________________________________________________________

## Q12. What is a consumer group?

**Answer:**

A group of consumers that cooperatively processes topic partitions. Each partition is assigned to at most one consumer
within a group at a time.

______________________________________________________________________

## Q13. Can two consumer groups read the same topic?

**Answer:**

Yes.

Each consumer group maintains independent consumption progress and can process the same records independently.

______________________________________________________________________

## Q14. What happens if there are more consumers than partitions?

**Answer:**

Some consumers will remain idle because a partition can be actively assigned to only one consumer within a consumer
group at a time.

______________________________________________________________________

## Q15. How does Kafka achieve consumer parallelism?

**Answer:**

By distributing partitions across consumers in a consumer group.

______________________________________________________________________

## Q16. What is consumer lag?

**Answer:**

The amount by which a consumer group's progress trails the latest available records.

______________________________________________________________________

## Q17. What causes consumer lag?

**Answer:**

Slow processing, insufficient consumers/partitions, increased incoming traffic, downstream dependency latency, consumer
failures or rebalancing issues.

______________________________________________________________________

## Q18. How would you reduce consumer lag?

**Answer:**

Optimize processing, increase consumer capacity, add partitions when appropriate, batch work and improve downstream
dependencies.

______________________________________________________________________

## Q19. Does adding consumers always reduce lag?

**Answer:**

No.

If there are fewer partitions than consumers, extra consumers cannot provide additional parallelism within that group.

______________________________________________________________________

## Q20. What is Kafka replication?

**Answer:**

Kafka maintains multiple copies of partitions across brokers to improve fault tolerance and availability.

______________________________________________________________________

## Q21. What is replication factor?

**Answer:**

The number of replicas maintained for each partition.

______________________________________________________________________

## Q22. What is a partition leader?

**Answer:**

The broker currently responsible for serving normal read/write operations for a replicated partition.

______________________________________________________________________

## Q23. Why use replication?

**Answer:**

To tolerate broker failures and maintain copies of partition data on other brokers.

______________________________________________________________________

## Q24. What are Kafka producer acknowledgments?

**Answer:**

They determine how much broker-side confirmation the producer waits for before considering a send acknowledged, commonly
discussed as `acks=0`, `acks=1` and `acks=all`.

______________________________________________________________________

## Q25. What is at-most-once delivery?

**Answer:**

A processing model where a record is processed zero or one time. The trade-off is that records can be lost under
failures.

______________________________________________________________________

## Q26. What is at-least-once delivery?

**Answer:**

A processing model where records are intended not to be lost, but the same record may be processed more than once.

______________________________________________________________________

## Q27. Why can at-least-once produce duplicates?

**Answer:**

If processing succeeds but the consumer crashes before committing the offset, Kafka can deliver the record again after
restart/reassignment.

______________________________________________________________________

## Q28. What is exactly-once?

**Answer:**

Exactly-once describes semantics where the intended processing effect occurs once within the supported
transactional/processing model despite failures and retries.

______________________________________________________________________

## Q29. Does Kafka guarantee exactly-once for arbitrary external APIs?

**Answer:**

No.

External side effects require their own idempotency or transaction strategy.

______________________________________________________________________

## Q30. What is idempotency?

**Answer:**

The property that repeating an operation produces the same intended final effect rather than applying the business
effect repeatedly.

______________________________________________________________________

## Q31. Why is idempotency important in Kafka consumers?

**Answer:**

Because at-least-once processing can cause duplicate delivery/processing.

______________________________________________________________________

## Q32. How would you make a consumer idempotent?

**Answer:**

Use a unique event or idempotency key and atomically record processing state with the business operation where possible.

______________________________________________________________________

## Q33. What is retry?

**Answer:**

Retry means attempting failed processing again, usually for transient failures.

______________________________________________________________________

## Q34. Why is exponential backoff useful?

**Answer:**

It increases the delay between retries, reducing pressure on a temporarily failing dependency.

______________________________________________________________________

## Q35. Why add jitter to retries?

**Answer:**

To avoid many clients retrying simultaneously and creating synchronized traffic spikes.

______________________________________________________________________

## Q36. What is a dead-letter topic?

**Answer:**

A destination where messages that cannot be successfully processed after the retry policy can be isolated for
investigation or later remediation.

______________________________________________________________________

## Q37. What is a poison message?

**Answer:**

A message that repeatedly causes processing failure.

______________________________________________________________________

## Q38. Why is dead-letter handling important?

**Answer:**

It prevents a permanently failing message from repeatedly consuming processing capacity.

______________________________________________________________________

## Q39. What is schema evolution?

**Answer:**

Changing an event's structure over time while maintaining compatibility between independently deployed producers and
consumers.

______________________________________________________________________

## Q40. Why is adding an optional field generally easier than removing an existing field?

**Answer:**

Existing consumers can often ignore an additional optional field, while removing or changing an existing field can break
consumers that depend on it.

______________________________________________________________________

## Q41. What is a schema registry?

**Answer:**

A service commonly used to manage event schemas and enforce compatibility rules between schema versions.

______________________________________________________________________

## Q42. Why is Kafka good for replay?

**Answer:**

Kafka retains records according to configured retention rather than deleting them immediately after a consumer processes
them, allowing consumers to read from earlier offsets.

______________________________________________________________________

## Q43. Kafka vs traditional queue?

**Answer:**

Traditional queues often focus on consuming and removing messages. Kafka stores an ordered log and tracks consumer
progress through offsets, enabling multiple independent consumers and replay.

______________________________________________________________________

## Q44. What happens when a consumer crashes?

**Answer:**

Its partitions can be reassigned to other consumers in the group. Records whose offsets were not committed can be
processed again.

______________________________________________________________________

## Q45. What is consumer rebalancing?

**Answer:**

The reassignment of partitions among consumers when group membership or relevant group state changes.

______________________________________________________________________

## Q46. What is the relationship between partition count and consumer parallelism?

**Answer:**

Within a consumer group, partition count is the upper bound on active consumer parallelism for that topic.

______________________________________________________________________

## Q47. What is the dual-write problem?

**Answer:**

It occurs when an application must update two systems, such as a database and Kafka, separately and one operation
succeeds while the other fails.

______________________________________________________________________

## Q48. What is the transactional outbox pattern?

**Answer:**

The application writes business data and an outbox event in the same database transaction. A separate publisher then
sends the outbox event to Kafka.

______________________________________________________________________

## Q49. Why use an outbox?

**Answer:**

It reduces the inconsistency risk of independently committing a database change and publishing a Kafka event.

______________________________________________________________________

## Q50. Give a senior-level Kafka answer.

**Answer:**

"I would model Kafka around topics, partitions and consumer groups. I would choose the partition key based on the
required ordering and distribution characteristics, usually preserving order per entity rather than requiring global
ordering. I would monitor consumer lag and design consumers for at-least-once processing with idempotent business
effects where practical. Transient failures would use bounded retries with exponential backoff and jitter, while poison
messages would move to a dead-letter flow. I would define replication and acknowledgment requirements based on
durability needs and use a schema compatibility strategy for independently deployed producers and consumers. For
database-plus-Kafka consistency, I would consider an outbox pattern rather than relying on an unsafe dual write."

______________________________________________________________________

# 84. Scenario-Based Questions

## Scenario 1 — Order Events Must Stay Ordered

An order produces:

```text
Created
Paid
Shipped
Delivered
```

and these events must remain in order.

**Answer:**

Use a stable key such as `order_id` so events for the same order are routed consistently to one partition.

______________________________________________________________________

## Scenario 2 — Global Ordering Required

Every event in the entire topic must be globally ordered.

**Answer:**

A single partition provides a straightforward total ordering for that topic, but it limits partition-level parallelism.
The design should challenge whether global ordering is actually required.

______________________________________________________________________

## Scenario 3 — Six Partitions, Ten Consumers

A consumer group has:

```text
6 partitions
10 consumers
```

**Answer:**

At most six consumers can actively process those partitions at one time. Four consumers will have no partition assigned.

______________________________________________________________________

## Scenario 4 — Consumer Lag Keeps Growing

Incoming traffic is:

```text
100,000 events/sec
```

but consumers process:

```text
70,000 events/sec
```

**Answer:**

The system has insufficient processing capacity. Increase effective parallelism if partitions allow it, optimize
processing, batch work and address slow downstream dependencies.

______________________________________________________________________

## Scenario 5 — Duplicate Payment

A consumer processes:

```text
PaymentRequested
```

successfully, then crashes before committing its Kafka offset.

The event is delivered again.

**Answer:**

The payment operation must be idempotent. Use an event/payment idempotency key and ensure duplicate processing does not
charge the customer twice.

______________________________________________________________________

## Scenario 6 — Dependency Is Down

A consumer receives 100,000 events, but the downstream API is temporarily unavailable.

**Answer:**

Do not immediately retry all events continuously. Use bounded retries, exponential backoff and jitter. If failures
persist, isolate problematic events through an appropriate retry/dead-letter design.

______________________________________________________________________

## Scenario 7 — Poison Message

One event always fails schema validation.

**Answer:**

Do not retry indefinitely. After the configured retry attempts, move it to a dead-letter destination and continue
processing other events.

______________________________________________________________________

## Scenario 8 — Database and Kafka Must Stay Consistent

An order service needs to:

```text
Update order
Publish OrderUpdated
```

**Answer:**

Avoid independent dual writes where possible. A transactional outbox can commit the order change and event record
together, followed by asynchronous publishing to Kafka.

______________________________________________________________________

## Scenario 9 — Schema Change

A producer wants to add:

```text
currency
```

to an existing event.

**Answer:**

Make the change compatible with existing consumers, typically by introducing the field in a backward-compatible manner
according to the system's schema policy.

______________________________________________________________________

## Scenario 10 — More Consumers Do Not Help

A team keeps adding consumers, but lag does not decrease.

**Answer:**

Check partition count. If there are fewer partitions than active consumers, additional consumers cannot increase
parallelism for that topic/group.

______________________________________________________________________

## Scenario 11 — Broker Failure

One Kafka broker fails and contains replicas for several partitions.

**Answer:**

If sufficient replicas exist and the cluster is correctly configured, another eligible replica can become leader for
affected partitions. Replication factor and replica health determine the system's resilience.

______________________________________________________________________

## Scenario 12 — External API Exactly Once

A Kafka consumer must call an external shipping API exactly once.

**Answer:**

Kafka alone cannot guarantee exactly-once external side effects. Use an idempotency key or a downstream API contract
that makes repeated requests safe.

______________________________________________________________________

# 85. Practice Exercises

## Exercise 1 — Basic Producer

Create a Python Kafka producer that publishes:

```json
{
  "order_id": 1001,
  "status": "CREATED"
}
```

to:

```text
orders
```

______________________________________________________________________

## Exercise 2 — Consumer

Create a consumer that:

- Reads from `orders`.
- Logs the event.
- Tracks processing.
- Commits offsets intentionally.

Document when the offset is committed.

______________________________________________________________________

## Exercise 3 — Consumer Group

Run multiple consumers using the same group.

Observe:

- Partition assignment
- Parallel processing
- Rebalancing

______________________________________________________________________

## Exercise 4 — Multiple Consumer Groups

Create:

```text
email-group
analytics-group
```

and publish events to the same topic.

Verify that both groups independently consume the events.

______________________________________________________________________

## Exercise 5 — Ordering

Publish:

```text
order 1001 → Created
order 1001 → Paid
order 1001 → Shipped
```

using:

```text
key = order_id
```

Verify ordering within the partition.

______________________________________________________________________

## Exercise 6 — Consumer Lag

Create a consumer that intentionally processes slowly.

Observe lag increasing.

Then increase processing capacity and observe whether lag decreases.

______________________________________________________________________

## Exercise 7 — At-Least-Once

Create a consumer that:

```text
processes event
crashes before offset commit
```

Restart it and observe duplicate processing.

______________________________________________________________________

## Exercise 8 — Idempotent Consumer

Implement:

```text
event_id
```

based deduplication.

Test the same event twice and verify that the business effect happens only once.

______________________________________________________________________

## Exercise 9 — Retry

Implement:

```text
attempt 1
attempt 2
attempt 3
```

with exponential backoff and jitter.

Classify errors into:

```text
retryable
non-retryable
```

______________________________________________________________________

## Exercise 10 — Dead Letter

Create a consumer that sends permanently failing events to:

```text
orders.DLT
```

after a configured number of retries.

______________________________________________________________________

## Exercise 11 — Schema Evolution

Create:

```text
OrderEvent v1
OrderEvent v2
```

where v2 adds an optional field.

Test whether a v1-style consumer can safely process v2 events.

______________________________________________________________________

## Exercise 12 — Replication

Run a small multi-broker Kafka environment and document:

- Replication factor
- Partition leader
- Replica
- Broker failure
- Leader reassignment

______________________________________________________________________

## Exercise 13 — Partition Design

For each workload, choose a partition key:

### A

Order events.

### B

Customer events.

### C

Global analytics events.

Explain:

- Ordering requirement
- Distribution
- Hotspot risk
- Parallelism

______________________________________________________________________

## Exercise 14 — Database + Kafka

Design:

```text
Order update
+
OrderUpdated event
```

first using dual writes.

Then redesign it using the transactional outbox pattern.

Document the failure scenarios.

______________________________________________________________________

## Exercise 15 — Production Design

Design Kafka for:

```text
100,000 events/sec
```

with:

```text
10 consumer applications
Multiple downstream services
At-least-once processing
```

Explain:

- Topic structure
- Partition count
- Partition key
- Replication
- Producer acknowledgments
- Consumer groups
- Lag monitoring
- Retry
- Dead-letter handling
- Idempotency
- Schema evolution

______________________________________________________________________

# 86. Quick Revision

| Concept | Key Point |
|---|---|
| Kafka | Distributed event streaming platform |
| Broker | Kafka server |
| Cluster | Group of Kafka brokers |
| Topic | Logical stream/category |
| Partition | Ordered append-only sequence |
| Producer | Publishes records |
| Consumer | Reads/processes records |
| Offset | Position within a partition |
| Consumer group | Consumers sharing partition work |
| Partition parallelism | Limits active consumers per group |
| Multiple groups | Independently consume same topic |
| Rebalancing | Redistributes partitions |
| Consumer lag | Consumer progress behind latest data |
| Replication | Multiple copies of partitions |
| Replication factor | Number of partition replicas |
| Leader | Broker serving partition operations |
| Producer acknowledgment | Determines write acknowledgment behavior |
| At-most-once | Zero or one processing; possible loss |
| At-least-once | Intended no loss; duplicates possible |
| Exactly-once | Once-only intended effect within supported semantics |
| Idempotency | Repeated operation has same intended effect |
| Retry | Repeat transiently failed processing |
| Exponential backoff | Increasing retry delays |
| Jitter | Randomizes retry timing |
| Dead letter | Isolate permanently failing messages |
| Poison message | Repeatedly failing event |
| Schema evolution | Safely changing event structure |
| Schema registry | Schema management/compatibility |
| Retention | Records remain according to policy |
| Replay | Re-read earlier records using offsets |
| Batch processing | Process multiple records together |
| Backpressure | Consumer capacity below incoming rate |
| Dual write | Updating two systems independently |
| Outbox | Transactionally store event with DB change |

______________________________________________________________________

# 87. Completion Checklist

Before moving to File 29, make sure you can explain:

- [ ] What Kafka is
- [ ] Why Kafka is used
- [ ] Broker
- [ ] Kafka cluster
- [ ] Topic
- [ ] Partition
- [ ] Why partitions matter
- [ ] Partition ordering
- [ ] Global ordering limitations
- [ ] Partition keys
- [ ] Producer
- [ ] Producer flow
- [ ] Producer keys
- [ ] Producer batching
- [ ] Producer compression
- [ ] Consumer
- [ ] Offset
- [ ] Offset scope
- [ ] Consumer groups
- [ ] Consumer-group parallelism
- [ ] More consumers than partitions
- [ ] Multiple consumer groups
- [ ] Consumer rebalancing
- [ ] Consumer lag
- [ ] Causes of lag
- [ ] Reducing lag
- [ ] Replication
- [ ] Partition leaders
- [ ] Replication factor
- [ ] Producer acknowledgments
- [ ] Delivery semantics
- [ ] At-most-once
- [ ] At-least-once
- [ ] Exactly-once concept
- [ ] Why exactly-once is difficult
- [ ] Idempotency
- [ ] Idempotency keys
- [ ] Retry
- [ ] Retry storms
- [ ] Exponential backoff
- [ ] Retry jitter
- [ ] Dead-letter handling
- [ ] Poison messages
- [ ] Schema evolution
- [ ] Backward compatibility
- [ ] Schema registry overview
- [ ] Retention
- [ ] Replay
- [ ] Offset commits
- [ ] Commit timing
- [ ] Batch processing
- [ ] Database integration
- [ ] Dual-write problem
- [ ] Transactional outbox
- [ ] External API idempotency
- [ ] Ordering vs parallelism
- [ ] Partition count trade-offs
- [ ] Backpressure
- [ ] Production monitoring
- [ ] Kafka failure scenarios

______________________________________________________________________

# 88. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is Kafka?
1. What is a broker?
1. What is a Kafka cluster?
1. What is a topic?
1. What is a partition?
1. Why does Kafka use partitions?
1. Does Kafka guarantee global ordering?
1. How would you preserve order for a customer?
1. What is a producer?
1. What is a consumer?
1. What is an offset?
1. Is an offset globally unique?
1. What is a consumer group?
1. How do consumer groups provide parallelism?
1. What happens if there are more consumers than partitions?
1. Can multiple consumer groups consume the same topic?
1. What is consumer rebalancing?
1. What is consumer lag?
1. What causes consumer lag?
1. How would you reduce consumer lag?
1. Does adding consumers always reduce lag?
1. What is Kafka replication?
1. What is a replication factor?
1. What is a partition leader?
1. Why is replication important?
1. Explain `acks=0`, `acks=1` and `acks=all`.
1. What is at-most-once delivery?
1. What is at-least-once delivery?
1. Why can at-least-once produce duplicates?
1. What is exactly-once?
1. Does exactly-once guarantee an external API is called once?
1. What is idempotency?
1. How would you make a Kafka consumer idempotent?
1. What is an idempotency key?
1. What is retry?
1. Which failures should generally be retried?
1. What is exponential backoff?
1. Why use retry jitter?
1. What is a retry storm?
1. What is a dead-letter topic?
1. What is a poison message?
1. Why is dead-letter handling useful?
1. What is schema evolution?
1. Why is backward compatibility important?
1. What is a schema registry?
1. Why is Kafka suitable for replay?
1. Kafka vs a traditional queue?
1. What happens when a consumer crashes?
1. How does offset commit timing affect delivery semantics?
1. What is the database/Kafka dual-write problem?
1. What is the transactional outbox pattern?
1. Why does the outbox pattern help?
1. How would you handle a downstream API that is temporarily unavailable?
1. How would you prevent duplicate payment processing?
1. How would you choose a partition key?
1. How does partition count affect parallelism?
1. What is backpressure?
1. How would you monitor consumer health?
1. When would you use at-least-once instead of attempting exactly-once?
1. Give a senior-level Kafka architecture answer for a high-throughput Python backend.

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

# 89. Final Senior Interview Scenario

You are designing an order-processing platform:

```text
100,000 events/sec
```

The system has:

```text
Order Service
Payment Service
Inventory Service
Notification Service
Analytics Service
```

Design the Kafka architecture.

Your answer should cover:

1. Topics.
1. Partition strategy.
1. Partition key.
1. Ordering requirements.
1. Producer acknowledgments.
1. Replication.
1. Consumer groups.
1. Consumer scaling.
1. Offset management.
1. Consumer lag.
1. At-least-once vs exactly-once.
1. Idempotent consumers.
1. Retry strategy.
1. Dead-letter handling.
1. Schema evolution.
1. Database/Kafka consistency.
1. Transactional outbox.
1. External API idempotency.
1. Failure recovery.
1. Monitoring.

The strongest interview answer should explicitly explain the trade-offs instead of claiming that Kafka automatically
solves ordering, retries, consistency or exactly-once processing.

______________________________________________________________________

**Previous:** [27. Redis Caching & Production](./27-redis-caching.md)

**Next:** [29. RabbitMQ & Celery](./29-rabbitmq-celery.md)
