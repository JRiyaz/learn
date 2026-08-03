# System Design - Part 85

# Apache Kafka System Design (How Kafka Works Internally)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Kafka exists
- Kafka Architecture
- Brokers
- Topics
- Partitions
- Producers
- Consumers
- Consumer Groups
- Offset Management
- Replication
- Leader Election
- ISR (In-Sync Replicas)
- Exactly-Once Semantics
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Apache Kafka.**

This is different from

previous lessons.

Previously,

we used Kafka

as

a component.

Now,

we'll learn

how Kafka

itself

works internally.

______________________________________________________________________

# Why Kafka?

Imagine

an e-commerce system.

```text id="kf8501"
Order Service

↓

Notification

Inventory

Analytics

Shipping
```

Should

Order Service

call

every service

directly?

No.

That creates

tight coupling.

Instead,

publish

an event

to Kafka.

______________________________________________________________________

# Event Flow

```text id="kf8502"
Producer

↓

Kafka

↓

Consumers
```

Producers

don't know

who

consumes

their events.

Consumers

don't know

who

produced them.

This is

decoupling.

______________________________________________________________________

# High-Level Architecture

```text id="kf8503"
Producer

↓

Broker Cluster

↓

Consumer
```

A Kafka cluster

contains

multiple brokers.

______________________________________________________________________

# What is a Broker?

Interview favorite.

A broker

is simply

a Kafka server.

Example

```text id="kf8504"
Broker 1

Broker 2

Broker 3
```

Each broker

stores

partitions

on disk.

______________________________________________________________________

# Topic

Interview favorite.

A Topic

is

a logical stream

of events.

Example

```text id="kf8505"
Orders

Payments

Notifications
```

Applications

publish

to topics.

Consumers

read

from topics.

______________________________________________________________________

# Partition

Interview favorite.

Topics

are divided

into

partitions.

```text id="kf8506"
Orders

↓

Partition 0

Partition 1

Partition 2
```

Why?

Because

partitions

allow

parallelism.

______________________________________________________________________

# Why Not One Partition?

Suppose

a topic

receives

1 Million

messages/sec.

One partition

cannot

handle

that load.

Multiple partitions

allow

multiple brokers

and

multiple consumers

to work

in parallel.

______________________________________________________________________

# Message Ordering

Interview favorite.

Kafka guarantees

ordering

only

within

a partition.

Example

```text id="kf8507"
Partition 0

A

↓

B

↓

C
```

Order

is preserved.

Across partitions,

there is

no global ordering.

______________________________________________________________________

# Producer

A producer

publishes

messages.

Workflow

```text id="kf8508"
Producer

↓

Broker

↓

Partition
```

______________________________________________________________________

# Partition Selection

Question.

How does

Kafka choose

the partition?

Several methods

exist.

### Round Robin

```text id="kf8509"
P0

↓

P1

↓

P2
```

Balanced distribution.

______________________________________________________________________

### Key-Based

Interview favorite.

Example

```text id="kf8510"
User ID

↓

Hash

↓

Partition
```

The same key

always

goes

to

the same partition.

Benefits:

- Message ordering
- Related events together

______________________________________________________________________

# Consumer

Consumers

read messages.

```text id="kf8511"
Kafka

↓

Consumer
```

Consumers

pull

messages.

Kafka

doesn't push them.

______________________________________________________________________

# Consumer Group

Interview favorite.

Suppose

three consumers

belong

to

one group.

```text id="kf8512"
Partition 0

↓

Consumer A

Partition 1

↓

Consumer B

Partition 2

↓

Consumer C
```

Each partition

is processed

by only

one consumer

within

a consumer group.

______________________________________________________________________

# Multiple Consumer Groups

Question.

Can

multiple applications

read

the same topic?

Yes.

Example

```text id="kf8513"
Orders

↓

Analytics Group

↓

Notification Group

↓

Inventory Group
```

Each group

maintains

its own offsets.

______________________________________________________________________

# Offsets

Interview favorite.

Every message

has

an offset.

Example

```text id="kf8514"
0

1

2

3

4
```

Consumers

track

the last

processed offset.

______________________________________________________________________

# Offset Commit

After

processing,

the consumer

commits

its offset.

```text id="kf8515"
Process

↓

Commit Offset
```

If

the consumer

crashes,

it resumes

from

the last committed offset.

______________________________________________________________________

# Replication

Interview favorite.

Partitions

are replicated

across brokers.

Example

```text id="kf8516"
Partition 0

↓

Leader

↓

Follower

↓

Follower
```

Replication

prevents

data loss.

______________________________________________________________________

# Replication Factor

Example

```text id="kf8517"
Replication Factor

=

3
```

One leader

plus

two followers.

______________________________________________________________________

# Leader Election

Interview favorite.

Suppose

the leader

fails.

```text id="kf8518"
Leader

↓

Crash
```

Kafka

elects

a follower

as

the new leader.

Producers

and consumers

continue

using

the new leader.

______________________________________________________________________

# ISR (In-Sync Replicas)

Interview favorite.

Not every follower

is eligible

to become

leader.

Only replicas

that are

fully synchronized

belong

to

the ISR.

```text id="kf8519"
Leader

↓

ISR

↓

Follower
```

Leader election

chooses

from

the ISR.

______________________________________________________________________

# Acknowledgements (acks)

Interview favorite.

Producer

can configure

how many brokers

must acknowledge

a write.

### acks=0

No acknowledgement.

Fastest.

May lose data.

______________________________________________________________________

### acks=1

Leader

acknowledges.

Good performance.

Possible data loss

if

leader crashes

before replication.

______________________________________________________________________

### acks=all

Leader

waits

for ISR.

Safest.

Slightly higher latency.

______________________________________________________________________

# Log Storage

Interview favorite.

Kafka

stores messages

in

append-only logs.

```text id="kf8520"
Offset 0

↓

Offset 1

↓

Offset 2
```

Messages

are never updated.

Only appended.

______________________________________________________________________

# Message Retention

Kafka

doesn't delete

messages

after

consumption.

Retention

may be:

```text id="kf8521"
7 Days
```

or

```text id="kf8522"
100 GB
```

After

the retention policy,

older messages

are removed.

______________________________________________________________________

# Log Compaction

Interview favorite.

Instead

of keeping

every version,

Kafka

can retain

only

the latest value

for each key.

Example

```text id="kf8523"
User 1

Version 1

↓

Version 2

↓

Keep Version 2
```

Useful

for

state reconstruction.

______________________________________________________________________

# Exactly-Once Semantics

Interview favorite.

Question.

Can Kafka

prevent

duplicate processing?

Yes.

Using:

- Idempotent Producers
- Transactions
- Transactional Consumers

This provides

Exactly-Once

Semantics.

______________________________________________________________________

# Scaling Kafka

Scale

by adding:

- Brokers
- Partitions

```text id="kf8524"
Broker 1

Broker 2

Broker 3

Broker 4
```

More brokers

increase:

- Storage
- Throughput
- Availability

______________________________________________________________________

# ZooKeeper vs KRaft

Interview favorite.

Older Kafka

used

ZooKeeper

for:

- Metadata
- Leader election
- Cluster management

Modern Kafka

uses

KRaft

(Kafka Raft Metadata Mode)

and

does not

require ZooKeeper.

______________________________________________________________________

# Failure Scenario

Suppose

Broker 2

fails.

Workflow

```text id="kf8525"
Leader

↓

Follower

↓

New Leader
```

Clients

automatically

switch

to

the new leader.

______________________________________________________________________

# Another Failure

Suppose

a consumer

crashes.

Another consumer

within

the same group

takes ownership

of

the partition

and resumes

from

the last committed offset.

This process

is called

**consumer group rebalancing**.

______________________________________________________________________

# End-to-End Architecture

```text id="kf8526"
Producer

↓

Kafka Broker

↓

Leader Partition

↓

Follower Replicas

↓

Consumer Group

↓

Application
```

______________________________________________________________________

# Trade-offs

More Partitions

vs

Fewer Partitions

| More | Fewer |
| ------------------ | ------------------ |
| Higher throughput | Lower throughput |
| Better parallelism | Simpler management |
| More metadata | Easier operations |

______________________________________________________________________

acks=1

vs

acks=all

| acks=1 | acks=all |
| ------------------ | ----------------- |
| Faster | Safer |
| Possible data loss | Better durability |
| Lower latency | Higher latency |

______________________________________________________________________

Replication Factor

2

vs

3

| RF=2 | RF=3 |
| -------------------- | ---------------------- |
| Lower storage | Higher durability |
| Less network traffic | Better fault tolerance |

______________________________________________________________________

# Best Practices

✅ Use key-based partitioning when ordering matters.

✅ Choose an appropriate replication factor (commonly 3).

✅ Use `acks=all` for critical events.

✅ Monitor consumer lag.

✅ Design for idempotent consumers because duplicates can still occur.

______________________________________________________________________

# Common Mistakes

### Assuming Global Ordering

Kafka guarantees

ordering

only

within

a partition.

______________________________________________________________________

### Too Few Partitions

This limits

consumer parallelism

and

future scalability.

______________________________________________________________________

### Too Many Partitions

Excessive partitions

increase:

- Memory usage
- Metadata size
- Leader elections
- Operational complexity

Choose

based on

expected throughput.

______________________________________________________________________

### Ignoring Consumer Lag

Large consumer lag

means

producers

are generating

messages

faster

than consumers

can process them.

Monitor

lag continuously.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Apache Kafka?

Design Kafka as a distributed append-only log composed of multiple brokers. Organize data into topics, each split into
partitions for scalability and parallelism. Producers publish messages to partitions, typically using key-based hashing
to preserve ordering for related events. Replicate partitions across brokers with one leader and multiple followers to
provide fault tolerance. Consumers read messages by tracking offsets, while consumer groups distribute partitions among
multiple consumers for horizontal scaling. Store messages for a configurable retention period, support leader election
when brokers fail, and use idempotent producers, transactions, and careful offset management to provide exactly-once
processing where required.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Brokers
- Topics
- Partitions
- Producers
- Consumers
- Consumer Groups
- Offsets
- Replication
- ISR
- Leader Election
- Exactly-Once Semantics
- KRaft
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ Core System Designs
- ✅ AI Systems
- ✅ Apache Kafka Internals

You now understand not only **how to use Kafka**, but also **how Kafka itself is built**, which is a common senior
backend interview topic.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll deep dive into **Redis Internals**, including:

- In-memory architecture
- Data structures
- Persistence (RDB & AOF)
- Replication
- Sentinel
- Redis Cluster
- Eviction policies
- Pub/Sub
- Distributed caching

______________________________________________________________________

# What's Next

[Redis System Design](86-redis-system-design.md)
