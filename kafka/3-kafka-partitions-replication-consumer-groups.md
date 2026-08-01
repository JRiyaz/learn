# Kafka Partitions, Offsets, Replication & Consumer Groups

## Introduction

This is **the most important Kafka chapter**.

If you understand this lecture, you'll understand why Kafka can process millions of messages per second while remaining
fault tolerant.

Nearly every Kafka interview eventually reaches these topics.

In this chapter, you'll learn:

- Partitions
- Offsets
- Leaders and Followers
- Replication
- In-Sync Replicas (ISR)
- Consumer Groups
- Rebalancing
- Ordering Guarantees
- Parallel Processing
- Python Examples
- FastAPI Integration
- Production Best Practices
- Interview Questions

______________________________________________________________________

# Why Partitions?

Suppose all messages were stored in a single file.

```text id="kpc001"
Producer

↓

Topic

↓

1 File

↓

Consumer
```

Problems:

- One consumer
- Limited throughput
- No parallelism
- Difficult to scale

Kafka solves this using **partitions**.

______________________________________________________________________

# What is a Partition?

A topic is divided into multiple partitions.

```text id="kpc002"
Orders Topic

├── Partition 0

├── Partition 1

└── Partition 2
```

Each partition is an **append-only log**.

Messages are written only at the end.

______________________________________________________________________

# Why Append-Only?

Appending is much faster than inserting in the middle.

```text id="kpc003"
Offset 0

↓

Offset 1

↓

Offset 2

↓

Offset 3
```

Kafka never inserts between existing messages.

______________________________________________________________________

# Creating Partitions

CLI

```bash id="kpc004"
kafka-topics.sh \
--bootstrap-server localhost:9092 \
--create \
--topic orders \
--partitions 3 \
--replication-factor 1
```

Three independent logs are created.

______________________________________________________________________

# Message Distribution

Without a key

```text id="kpc005"
Message A

↓

Partition 0

Message B

↓

Partition 2

Message C

↓

Partition 1
```

Kafka distributes messages across partitions using its partitioning strategy.

______________________________________________________________________

# Distribution Using Keys

Producer

```python id="kpc006"
producer.produce(

    topic="orders",

    key="customer-10",

    value='{"id":1}'

)
```

Messages with the same key

↓

Always go to the same partition.

______________________________________________________________________

# Why?

Ordering.

Suppose

Customer

```text id="kpc007"
Deposit

Withdraw

Transfer
```

If messages went to different partitions,

order could be lost.

Using the same key preserves ordering **within a partition**.

______________________________________________________________________

# Ordering Guarantee

Kafka guarantees ordering

```text id="kpc008"
Inside One Partition
```

Not across different partitions.

Interview Tip

Many candidates incorrectly answer:

> Kafka guarantees global ordering.

It does **not**.

______________________________________________________________________

# Offsets

Every message has an offset.

```text id="kpc009"
Partition 0

Offset 0

Offset 1

Offset 2

Offset 3
```

Offsets uniquely identify a message **within a partition**.

______________________________________________________________________

# Why Offsets?

Consumers remember

```text id="kpc010"
Last Read Offset
```

Instead of deleting messages,

Kafka lets consumers track their own progress.

______________________________________________________________________

# Reading Messages

Consumer

```text id="kpc011"
Offset 0

↓

Offset 1

↓

Offset 2
```

The consumer stores its current position.

______________________________________________________________________

# Replay Messages

Consumers can restart from older offsets.

Benefits:

- Debugging
- Recovery
- Event replay
- Analytics

Unlike traditional queues,

Kafka retains messages based on retention policies.

______________________________________________________________________

# Offset Commit

Consumers periodically commit offsets.

Automatic

```python id="kpc012"
Consumer(

{

"enable.auto.commit":True

}

)
```

Manual

```python id="kpc013"
consumer.commit()
```

______________________________________________________________________

# Auto Commit vs Manual Commit

| Auto Commit | Manual Commit |
| ---------------------------------------------- | ---------------------------------- |
| Simpler | More control |
| Risk of committing before processing completes | Commit after successful processing |
| Good for simple consumers | Preferred for critical processing |

Interview Tip

Production systems often use manual commits after successful business logic.

______________________________________________________________________

# Consumer Groups

Without groups

```text id="kpc014"
Topic

↓

Consumer A

↓

Consumer B

↓

Consumer C
```

Every consumer receives every message.

______________________________________________________________________

With a Consumer Group

```text id="kpc015"
Topic

↓

Consumer Group

├── Consumer 1

├── Consumer 2

└── Consumer 3
```

Each partition is assigned to **one consumer within the group**.

______________________________________________________________________

# Partition Assignment

Topic

```text id="kpc016"
P0

P1

P2
```

Consumers

```text id="kpc017"
Consumer A → P0

Consumer B → P1

Consumer C → P2
```

Perfect parallelism.

______________________________________________________________________

# More Consumers Than Partitions

Suppose

```text id="kpc018"
Partitions = 3

Consumers = 5
```

Two consumers remain idle.

Kafka cannot assign more than one consumer in the same group to a single partition simultaneously.

______________________________________________________________________

# More Partitions Than Consumers

```text id="kpc019"
Partitions = 8

Consumers = 2
```

Each consumer handles multiple partitions.

______________________________________________________________________

# Rebalancing

Suppose

Consumer B crashes.

Before

```text id="kpc020"
A → P0

B → P1

C → P2
```

After

```text id="kpc021"
A → P0

C → P1

C → P2
```

Kafka redistributes partitions among the remaining consumers.

This process is called **rebalancing**.

______________________________________________________________________

# Rebalancing Costs

During a rebalance:

- Consumption pauses briefly.
- Partitions are reassigned.
- Consumers resume processing.

Frequent rebalances reduce throughput.

______________________________________________________________________

# Replication

Kafka replicates partitions.

```text id="kpc022"
Partition 0

↓

Leader

↓

Follower

↓

Follower
```

Replication improves durability and availability.

______________________________________________________________________

# Leader

All reads and writes occur through the leader.

```text id="kpc023"
Producer

↓

Leader

↓

Followers
```

Followers replicate the leader's data.

______________________________________________________________________

# Follower

Followers continuously copy data from the leader.

If the leader fails,

one follower can become the new leader.

______________________________________________________________________

# Replication Factor

Example

```text id="kpc024"
Replication Factor = 3
```

Each partition exists on three brokers.

Interview Tip

Replication factor cannot exceed the number of brokers.

______________________________________________________________________

# In-Sync Replicas (ISR)

ISR stands for

```text id="kpc025"
In-Sync Replicas
```

These are replicas that are sufficiently caught up with the leader.

The leader waits for acknowledgements from ISR members depending on producer configuration.

______________________________________________________________________

# ACK = all

Producer

↓

Leader

↓

ISR

↓

ACK

Highest durability.

______________________________________________________________________

# What Happens If a Broker Fails?

Suppose

```text id="kpc026"
Broker 2

↓

Offline
```

Kafka elects a new leader from the ISR.

Applications continue working with minimal interruption.

______________________________________________________________________

# Consumer Lag

Lag

\=

Latest Offset

-

Consumer Offset

Example

```text id="kpc027"
Latest Offset

1000

Consumer Offset

950

Lag

50
```

High lag indicates the consumer is falling behind.

______________________________________________________________________

# Monitoring Consumer Lag

One of the most important Kafka production metrics.

Monitor:

- Consumer lag
- Processing latency
- Throughput
- Failed messages

______________________________________________________________________

# Python Producer with Key

```python id="kpc028"
producer.produce(

    "orders",

    key="customer-42",

    value='{"order":101}'

)

producer.flush()
```

______________________________________________________________________

# Python Consumer

```python id="kpc029"
consumer = Consumer(

{

"bootstrap.servers":"localhost:9092",

"group.id":"inventory"

}

)
```

Kafka automatically assigns partitions within the consumer group.

______________________________________________________________________

# FastAPI Example

```python id="kpc030"
@app.post("/orders")

def create_order(order: dict):

    producer.produce(

        "orders",

        key=str(order["customer_id"]),

        value=json.dumps(order)

    )

    producer.flush()

    return {

        "status":"accepted"

    }
```

Orders from the same customer remain ordered within their assigned partition.

______________________________________________________________________

# Real Production Architecture

```text id="kpc031"
FastAPI

↓

Producer

↓

Orders Topic

├── Partition 0

├── Partition 1

├── Partition 2

↓

Inventory Group

↓

Payment Group

↓

Email Group

↓

Analytics Group
```

Each consumer group processes the same events independently.

______________________________________________________________________

# Common Mistakes

### Believing Kafka Guarantees Global Ordering

Ordering is guaranteed **only within a partition**.

______________________________________________________________________

### Too Few Partitions

Limits parallelism.

______________________________________________________________________

### Too Many Partitions

Increases operational overhead.

______________________________________________________________________

### Auto-Committing Before Processing

Can result in lost messages if the application crashes after the offset is committed but before processing completes.

______________________________________________________________________

### Ignoring Consumer Lag

Lag is one of the most important indicators of consumer health.

______________________________________________________________________

# Best Practices

- Choose partition counts carefully.
- Use meaningful message keys.
- Monitor consumer lag.
- Use manual offset commits for critical workloads.
- Keep replication factor greater than one in production.
- Design consumers to be idempotent.
- Plan for rebalancing events.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why are message keys important in Kafka?

Message keys determine the partition to which a record is written. Kafka uses the key to consistently route related
messages to the same partition. Because Kafka preserves ordering within a partition, using the same key ensures that
events for the same entity—such as a customer, order, or account—are processed in the correct sequence. Without keys,
ordering across related events cannot be guaranteed.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a partition?
1. Why does Kafka use partitions?
1. What is an offset?
1. Why are offsets needed?
1. What is a consumer group?
1. Explain rebalancing.
1. What is replication?
1. What is a leader?
1. What is a follower?
1. What is ISR?
1. What is consumer lag?
1. Why use message keys?

## Coding

1. Create a topic with three partitions.
1. Publish messages using keys.
1. Create a consumer group.
1. Commit offsets manually.
1. Measure consumer lag.
1. Simulate a rebalance by stopping one consumer.

______________________________________________________________________

# Hands-on Exercise

Extend the Order Event System.

Requirements:

1. Create an `orders` topic with three partitions.
1. Publish events using `customer_id` as the message key.
1. Create an inventory consumer group with multiple consumers.
1. Observe partition assignments.
1. Stop one consumer and observe rebalancing.
1. Enable manual offset commits.
1. Monitor consumer lag.
1. Verify ordering for events with the same customer ID.

______________________________________________________________________

# Cheat Sheet

```text id="kpc032"
Topic

↓

Partitions

↓

Offsets

↓

Producer Keys

↓

Consumer Groups

↓

Rebalancing

↓

Leader

↓

Follower

↓

ISR

↓

Replication

↓

Consumer Lag
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Kafka partitions
- Append-only logs
- Message keys
- Ordering guarantees
- Offsets
- Offset commits
- Consumer groups
- Partition assignment
- Rebalancing
- Replication
- Leaders and followers
- In-Sync Replicas (ISR)
- Consumer lag
- FastAPI integration
- Production best practices
- Interview patterns

You now understand the core mechanisms that make Kafka scalable, fault tolerant, and highly performant. These concepts
form the foundation for advanced Kafka topics such as exactly-once processing, dead letter queues, retries, and
production-grade event-driven systems.

______________________________________________________________________

## Next File

[4-kafka-python-fastapi-part-1.md](4-kafka-python-fastapi-part-1.md)
