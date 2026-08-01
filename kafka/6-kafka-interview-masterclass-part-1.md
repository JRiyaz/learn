# Kafka Interview Masterclass - Part 1

## Introduction

This chapter is designed specifically for **backend engineering interviews**.

Unlike previous lectures that focused on implementation, this file focuses on:

- Interview questions
- Internal architecture
- Distributed systems concepts
- Production scenarios
- Coding discussions
- Best practices
- Common misconceptions

These are the questions commonly asked in interviews at companies such as Amazon, Microsoft, Uber, Walmart, Atlassian,
LinkedIn, Netflix, and many others.

______________________________________________________________________

# Kafka Fundamentals

## 1. What is Kafka?

### Answer

Apache Kafka is a distributed event streaming platform used for publishing, storing, and consuming streams of events.

Kafka is designed for:

- High throughput
- Fault tolerance
- Horizontal scalability
- Durability

Unlike traditional message queues, Kafka stores events for a configurable retention period, allowing consumers to replay
them later.

______________________________________________________________________

## 2. Why was Kafka created?

### Answer

Before Kafka,

applications communicated directly.

```text id="ki001"
Order Service

↓

Payment

↓

Inventory

↓

Email
```

Problems:

- Tight coupling
- Difficult scaling
- Cascading failures

Kafka introduces an event log.

```text id="ki002"
Producer

↓

Kafka

↓

Consumers
```

Every service becomes independent.

______________________________________________________________________

## 3. Kafka vs RabbitMQ

| Kafka | RabbitMQ |
| ---------------- | --------------------------------------------------- |
| Event Streaming | Message Queue |
| Replay supported | Limited replay |
| High throughput | Rich routing capabilities |
| Partition based | Queue based |
| Long retention | Messages are commonly removed after acknowledgement |

Interview Tip

Neither is "better."

Choose based on requirements.

______________________________________________________________________

## 4. Kafka vs Redis Streams

| Kafka | Redis Streams |
| -------------------- | --------------------------- |
| Distributed platform | Redis feature |
| Massive scale | Smaller scale |
| Long-term retention | Typically shorter retention |
| Independent cluster | Built into Redis |

______________________________________________________________________

## 5. Why is Kafka Fast?

### Answer

Kafka achieves high performance through several design choices:

- Sequential disk writes
- Append-only logs
- Batching
- Compression
- Zero-copy optimizations (where supported)
- Efficient networking

______________________________________________________________________

# Topics

## 6. What is a Topic?

A Topic is a named stream of events.

Example

```text id="ki003"
orders

payments

inventory
```

Applications publish and consume from topics.

______________________________________________________________________

## 7. Can Multiple Producers Write to One Topic?

Yes.

Many producers can publish concurrently.

Kafka preserves ordering only within each partition.

______________________________________________________________________

## 8. Can Multiple Consumers Read One Topic?

Yes.

Different consumer groups can independently read the same topic.

______________________________________________________________________

# Partitions

## 9. What is a Partition?

A partition is an append-only log.

```text id="ki004"
Offset 0

↓

Offset 1

↓

Offset 2
```

Each topic consists of one or more partitions.

______________________________________________________________________

## 10. Why Does Kafka Use Partitions?

Benefits:

- Parallelism
- Scalability
- Higher throughput
- Distributed storage

______________________________________________________________________

## 11. Does Kafka Guarantee Ordering?

### Answer

Kafka guarantees ordering **within a partition**.

It does **not** guarantee ordering across multiple partitions.

______________________________________________________________________

## 12. Why Are Message Keys Important?

Messages with the same key are routed to the same partition.

Example

```python id="ki005"
producer.produce(
    "orders",
    key="customer-42",
    value="..."
)
```

This preserves ordering for that customer.

______________________________________________________________________

# Offsets

## 13. What is an Offset?

An offset uniquely identifies a message within a partition.

```text id="ki006"
Partition

↓

Offset

15
```

______________________________________________________________________

## 14. Why Doesn't Kafka Delete Messages After Reading?

Consumers track their own offsets.

This allows:

- Replay
- Recovery
- Multiple consumer groups
- Analytics

______________________________________________________________________

## 15. Auto Commit vs Manual Commit

| Auto | Manual |
| ------------------ | ---------------------------- |
| Easy | More control |
| Possible data loss | Safer for critical workloads |

______________________________________________________________________

# Consumer Groups

## 16. What is a Consumer Group?

A Consumer Group is a set of consumers working together.

Each partition is assigned to only one consumer within that group.

______________________________________________________________________

## 17. More Consumers Than Partitions?

Example

```text id="ki007"
Partitions

3

Consumers

5
```

Two consumers remain idle.

______________________________________________________________________

## 18. More Partitions Than Consumers?

Consumers receive multiple partitions.

______________________________________________________________________

## 19. What is Rebalancing?

Suppose

Consumer crashes.

Kafka redistributes partitions.

This process is called

```text id="ki008"
Rebalancing
```

______________________________________________________________________

## 20. Why Are Frequent Rebalances Bad?

Because consumption pauses temporarily while partitions are reassigned.

Frequent rebalances reduce throughput.

______________________________________________________________________

# Replication

## 21. What is Replication?

Kafka copies partition data across multiple brokers.

Benefits

- High availability
- Fault tolerance

______________________________________________________________________

## 22. Leader vs Follower

Leader

Handles reads and writes.

Followers

Replicate the leader's data.

______________________________________________________________________

## 23. What is ISR?

ISR means

```text id="ki009"
In-Sync Replicas
```

These replicas are sufficiently caught up with the leader.

______________________________________________________________________

## 24. What Happens if the Leader Crashes?

Kafka elects a new leader from the ISR.

Clients continue communicating with the new leader.

______________________________________________________________________

# Producers

## 25. What is ACK?

Acknowledgement from Kafka that a message has been received according to the configured durability level.

______________________________________________________________________

## 26. ACK = 0

Fastest.

Least reliable.

______________________________________________________________________

## 27. ACK = 1

Leader acknowledges after writing the record.

______________________________________________________________________

## 28. ACK = all

Leader waits for acknowledgements from the required in-sync replicas.

Highest durability.

______________________________________________________________________

## 29. Why Use Compression?

Benefits:

- Less network traffic
- Lower storage usage
- Higher throughput

______________________________________________________________________

## 30. Why Use Batching?

Without batching

```text id="ki010"
1000

Network Trips
```

With batching

```text id="ki011"
1

Batch
```

Throughput improves significantly.

______________________________________________________________________

# Consumers

## 31. What is Consumer Lag?

Consumer Lag

\=

Latest Offset

-

Consumer Offset

______________________________________________________________________

## 32. Why is Lag Important?

High lag means consumers cannot process messages as quickly as producers generate them.

______________________________________________________________________

## 33. Why Should Consumers Be Idempotent?

Kafka typically provides at-least-once delivery.

Duplicate messages may occur.

Consumers should safely ignore duplicate processing.

______________________________________________________________________

## 34. What is a DLQ?

Dead Letter Queue.

Failed messages are redirected to another topic for later analysis instead of blocking normal processing.

______________________________________________________________________

## 35. Why Use Manual Commits?

To commit offsets only after successful business processing.

______________________________________________________________________

# Production Scenarios

## Scenario 1

Consumer lag grows continuously.

Possible causes:

- Slow database
- Expensive business logic
- Too few consumers
- Too few partitions

______________________________________________________________________

## Scenario 2

Messages are processed twice.

Possible causes:

- Consumer restart before offset commit
- Retry behavior
- At-least-once delivery

______________________________________________________________________

## Scenario 3

One partition receives almost all messages.

Possible cause:

Poor key distribution.

______________________________________________________________________

## Scenario 4

Consumers stop receiving messages after a deployment.

Possible areas to investigate:

- Consumer group configuration
- Rebalancing
- Topic subscription
- Offsets

______________________________________________________________________

## Scenario 5

A producer reports delivery failures.

Investigate:

- Broker availability
- Network connectivity
- Authentication
- Timeouts

______________________________________________________________________

# Rapid Fire

1. Kafka vs RabbitMQ
1. Kafka vs Redis Streams
1. Topic vs Partition
1. Partition vs Offset
1. Producer vs Consumer
1. ACK=1 vs ACK=all
1. Auto Commit vs Manual Commit
1. Leader vs Follower
1. ISR vs Replica
1. Consumer Group vs Consumer
1. Rebalance vs Restart
1. Throughput vs Latency
1. Batch vs Single Message
1. Compression vs No Compression
1. Retention vs Deletion

______________________________________________________________________

# Common Mistakes

- Claiming Kafka guarantees global ordering.
- Assuming messages are deleted immediately after consumption.
- Ignoring consumer lag.
- Using automatic commits for critical workflows.
- Creating poor partition keys that cause hot partitions.
- Treating Kafka as a relational database.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why doesn't Kafka delete a message after a consumer reads it?

Kafka separates message storage from message consumption. Messages remain in the log according to the configured
retention policy, while each consumer group tracks its own offsets independently. This allows multiple consumer groups
to process the same data, supports replaying historical events, and enables recovery after failures without requiring
producers to resend events.

______________________________________________________________________

# Practice Questions

## Conceptual

1. Why was Kafka created?
1. Why is Kafka fast?
1. What is a Topic?
1. What is a Partition?
1. What is an Offset?
1. What is Consumer Lag?
1. What is ISR?
1. What is ACK?
1. Why use message keys?
1. Why are consumers idempotent?

## Coding

1. Create a topic.
1. Publish keyed messages.
1. Configure `acks=all`.
1. Create a consumer group.
1. Implement manual offset commits.
1. Publish failed messages to a DLQ.

______________________________________________________________________

# Summary

After this chapter you should confidently explain:

- Kafka fundamentals
- Topics
- Partitions
- Offsets
- Consumer groups
- Replication
- ACKs
- Producer behavior
- Consumer behavior
- Common production issues

______________________________________________________________________

## Next File

[6-kafka-interview-masterclass-part-2.md](6-kafka-interview-masterclass-part-2.md)
