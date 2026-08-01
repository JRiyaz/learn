# Kafka Interview Masterclass - Part 2

## Introduction

In Part 1, we covered:

- Kafka fundamentals
- Topics
- Partitions
- Producers
- Consumers
- Consumer Groups
- Replication
- ACKs
- Offsets

This chapter covers **Senior Backend Engineer** and **Distributed Systems** interview topics.

Topics include:

- Kafka Internals
- Log Segments
- Zero Copy
- Page Cache
- Controller
- KRaft vs ZooKeeper
- Exactly-Once Semantics
- Transactions
- Schema Registry
- Event Versioning
- Security
- Performance Tuning
- System Design
- Production Debugging
- Final Interview Checklist

______________________________________________________________________

# Kafka Internals

## 1. How Does Kafka Store Messages?

Kafka stores messages in an **append-only log**.

```text id="kip001"
Partition

↓

Message 1

↓

Message 2

↓

Message 3
```

Kafka never inserts messages in the middle of a partition.

It only appends.

______________________________________________________________________

## 2. Why Append-Only Logs?

Appending avoids random disk writes.

Benefits:

- Higher throughput
- Simpler storage
- Sequential disk access
- Better operating system caching

______________________________________________________________________

## 3. What are Log Segments?

A partition is divided into multiple log segment files.

```text id="kip002"
Partition

├── Segment 1

├── Segment 2

└── Segment 3
```

Kafka creates new segments as existing ones reach configured size or age limits.

This makes retention and cleanup more efficient.

______________________________________________________________________

## 4. Why Use Log Segments?

Instead of rewriting a huge log,

Kafka deletes or compacts individual segments.

Benefits:

- Efficient retention
- Faster cleanup
- Better disk management

______________________________________________________________________

# Page Cache

## 5. What is the Page Cache?

Kafka relies heavily on the operating system's page cache.

```text id="kip003"
Application

↓

Operating System

↓

Page Cache

↓

Disk
```

Frequently accessed data is served from memory instead of requiring disk reads.

______________________________________________________________________

## 6. Why Does This Make Kafka Fast?

Sequential writes and page cache usage reduce expensive disk operations.

______________________________________________________________________

# Zero Copy

## 7. What is Zero Copy?

Instead of repeatedly copying message data between buffers,

Kafka can transfer data more efficiently using operating system support.

```text id="kip004"
Disk

↓

Page Cache

↓

Network
```

This reduces CPU usage and improves throughput.

______________________________________________________________________

# KRaft vs ZooKeeper

## 8. What is ZooKeeper?

Historically,

Kafka used ZooKeeper for:

- Cluster metadata
- Leader election
- Broker coordination

______________________________________________________________________

## 9. What is KRaft?

Modern Kafka versions support **KRaft (Kafka Raft Metadata mode)**.

Benefits:

- No ZooKeeper dependency
- Simpler deployment
- Improved scalability
- Fewer operational components

Interview Tip

For new Kafka deployments,

KRaft is the recommended architecture.

______________________________________________________________________

## 10. Why Did Kafka Remove ZooKeeper?

Maintaining two distributed systems increased operational complexity.

KRaft integrates metadata management directly into Kafka.

______________________________________________________________________

# Exactly-Once Semantics

## 11. What is Exactly-Once Processing?

Goal

```text id="kip005"
One Event

↓

One Result
```

Exactly-Once Semantics (EOS) reduce duplicate processing by combining idempotent producers, Kafka transactions, and
coordinated consumer behavior.

______________________________________________________________________

## 12. Is Exactly-Once Easy?

No.

It requires:

- Idempotent producer
- Transactions
- Proper offset management
- Careful application design

______________________________________________________________________

## 13. Why Still Build Idempotent Consumers?

Even with EOS,

external systems such as databases or third-party APIs may introduce duplicate side effects.

Idempotent business logic remains a best practice.

______________________________________________________________________

# Transactions

## 14. Why Use Kafka Transactions?

Suppose

```text id="kip006"
Inventory Event

↓

Payment Event

↓

Notification Event
```

Transactions help ensure these Kafka writes are committed together or aborted together.

______________________________________________________________________

## 15. Are Kafka Transactions the Same as SQL Transactions?

No.

Kafka transactions coordinate Kafka records and offsets.

They are not a replacement for relational database transactions.

______________________________________________________________________

# Schema Registry

## 16. What is Schema Registry?

Schema Registry stores message schemas.

Instead of relying on undocumented JSON structures,

applications share versioned schemas.

Common formats:

- Avro
- Protobuf
- JSON Schema

______________________________________________________________________

## 17. Why Use It?

Benefits:

- Validation
- Compatibility checks
- Version management
- Safer deployments

______________________________________________________________________

## 18. Schema Evolution

Bad

Version 1

```json id="kip007"
{
    "id":101
}
```

Version 2

```json id="kip008"
{
    "order_id":101
}
```

Older consumers may fail.

Prefer backward-compatible changes.

Example

```json id="kip009"
{
    "id":101,
    "status":"CREATED"
}
```

Adding optional fields is generally safer than renaming existing ones.

______________________________________________________________________

# Security

## 19. How is Kafka Secured?

Production Kafka commonly uses:

- TLS
- SASL
- ACLs

Never expose brokers directly to the public Internet.

______________________________________________________________________

## 20. What are ACLs?

Access Control Lists define which users or applications may:

- Read topics
- Write topics
- Create topics
- Manage consumer groups

______________________________________________________________________

# Performance Tuning

## 21. Important Producer Settings

- `acks`
- `linger.ms`
- `batch.size`
- `compression.type`
- `enable.idempotence`

______________________________________________________________________

## 22. Important Consumer Settings

- `group.id`
- `enable.auto.commit`
- `auto.offset.reset`
- `max.poll.interval.ms`
- `session.timeout.ms`

Understand their purpose before changing defaults.

______________________________________________________________________

## 23. How Do You Increase Throughput?

Options include:

- More partitions
- Better batching
- Compression
- Faster consumers
- More consumer instances
- Optimized business logic

______________________________________________________________________

# Production Debugging

## Scenario 1

Consumer lag increases continuously.

Investigate:

- Database performance
- Consumer processing time
- Number of consumers
- Number of partitions

______________________________________________________________________

## Scenario 2

One broker becomes overloaded.

Possible causes:

- Hot partition
- Uneven key distribution
- Skewed workload

______________________________________________________________________

## Scenario 3

Consumers repeatedly rebalance.

Investigate:

- Frequent deployments
- Consumer crashes
- Timeout configuration
- Network instability

______________________________________________________________________

## Scenario 4

Producer throughput suddenly drops.

Check:

- Broker health
- Compression settings
- Network latency
- Batch configuration

______________________________________________________________________

## Scenario 5

Duplicate orders appear.

Investigate:

- Offset commits
- Retry logic
- Consumer idempotency
- Producer retries

______________________________________________________________________

# System Design Questions

## Design an Order Processing System

Expected discussion:

```text id="kip010"
FastAPI

↓

Kafka Producer

↓

Orders Topic

↓

Inventory Consumer

↓

Payment Consumer

↓

Notification Consumer

↓

Analytics Consumer
```

Explain:

- Consumer Groups
- Idempotency
- DLQ
- Retries
- Monitoring
- Scaling

______________________________________________________________________

## Design a Notification System

Suggested architecture:

```text id="kip011"
User Service

↓

Kafka

↓

Email

SMS

Push Notification
```

Multiple independent consumers.

______________________________________________________________________

## Design an Audit Log

Kafka is a strong choice because events can be retained and replayed for compliance or debugging.

______________________________________________________________________

# Rapid Fire

1. Kafka vs RabbitMQ
1. Kafka vs Redis Streams
1. ZooKeeper vs KRaft
1. Segment vs Partition
1. Topic vs Partition
1. Leader vs Follower
1. Replica vs ISR
1. Offset vs Message ID
1. At-Least-Once vs Exactly-Once
1. Transaction vs Idempotency
1. Page Cache vs RAM
1. Zero Copy
1. Batch vs Compression
1. Schema Registry
1. DLQ
1. Consumer Lag
1. Rebalancing
1. Hot Partition
1. Event Versioning
1. Immutable Events

______________________________________________________________________

# Common Interview Mistakes

- Claiming Kafka guarantees global ordering.
- Confusing partitions with brokers.
- Assuming Kafka deletes messages after consumption.
- Ignoring schema evolution.
- Ignoring consumer lag.
- Believing Exactly-Once processing removes the need for idempotent consumers.
- Treating Kafka as a relational database.

______________________________________________________________________

# Final Interview Checklist

You should now be able to explain:

- Kafka architecture
- Append-only logs
- Partitions
- Offsets
- Consumer groups
- Rebalancing
- Replication
- ISR
- ACKs
- Delivery guarantees
- Exactly-Once Semantics
- Transactions
- Page cache
- Zero copy
- Log segments
- KRaft
- Schema Registry
- Event versioning
- Security
- Monitoring
- Performance tuning
- Production debugging
- Event-driven system design

______________________________________________________________________

# Final Kafka Cheat Sheet

```text id="kip012"
Producer

↓

Topic

↓

Partition

↓

Offset

↓

Broker

↓

Consumer Group

↓

Leader

↓

Follower

↓

ISR

↓

Batching

↓

Compression

↓

Transactions

↓

Exactly-Once

↓

Schema Registry

↓

KRaft

↓

Monitoring
```

______________________________________________________________________

# Summary

Congratulations!

You have completed the Kafka section of the backend roadmap.

You should now be comfortable with:

- Kafka fundamentals
- Producers and consumers
- Partitions
- Offsets
- Replication
- Consumer groups
- FastAPI integration
- Python implementation
- Production architecture
- Performance tuning
- Monitoring
- Exactly-Once processing
- Distributed systems concepts
- Senior backend interview questions

Combined with the final project we'll build, this gives you a production-level understanding of Kafka suitable for
modern Python backend engineering roles.

______________________________________________________________________

## Next File

[7-kafka-order-processing-project-part-1.md](7-kafka-order-processing-project-part-1.md)
