# Apache Kafka Complete Guide

## Beginner to Advanced Architecture and Configuration

______________________________________________________________________

# Table of Contents

1. Kafka Fundamentals
1. Kafka Core Architecture
1. Kafka Installation Models
1. Kafka Message Flow
1. Topics and Partitions
1. Producers
1. Consumers
1. Offsets and Commit Management
1. Replication and Fault Tolerance
1. Leaders, Followers and ISR
1. Kafka Cluster Controller and KRaft
1. Rebalancing
1. Kafka Internal Topics
1. Kafka Configuration Reference
1. Production Cluster Design
1. Advanced Kafka Concepts

______________________________________________________________________

# 1. Kafka Fundamentals

## What is Apache Kafka?

Apache Kafka is a distributed event streaming platform.

It is used for:

- High-throughput messaging
- Event-driven architectures
- Log aggregation
- Data pipelines
- Real-time processing

A simple view:

```
Application
    |
    |
    v

   Kafka

    |
    |
    v

Another Application
```

Kafka stores events and allows multiple applications to consume those events independently.

______________________________________________________________________

# Why Kafka Exists?

Traditional messaging systems:

```
Producer
   |
   v
Message Queue
   |
   v
Consumer
```

Usually:

- Message is removed after consumption.
- Limited scalability.
- Lower throughput.

Kafka works differently:

```
Producer
   |
   v

Kafka Log

0  1  2  3  4  5

   |
   |
   +------------+
                |
                v

           Consumer A

                |
                v

           Consumer B
```

Messages remain stored.

Consumers track their own position.

______________________________________________________________________

# Kafka as a Distributed Commit Log

Kafka stores messages as an ordered log.

Example:

```
Topic: orders


Offset     Message
-------------------------

0          Order Created

1          Payment Completed

2          Order Shipped

3          Order Delivered
```

Messages are immutable.

Consumers move through this log using offsets.

______________________________________________________________________

# 2. Kafka Core Architecture

A Kafka system contains:

```
                 Kafka Cluster


        +-----------------------------+

        Broker 1
        Broker 2
        Broker 3

        +-----------------------------+
```

______________________________________________________________________

# Kafka Cluster

A Kafka cluster is a group of Kafka brokers working together.

Example:

```
                 Kafka Cluster


+-------------+-------------+-------------+
|             |             |             |
| Broker 1    | Broker 2    | Broker 3    |
|             |             |             |
+-------------+-------------+-------------+
```

The cluster provides:

- Scalability
- Fault tolerance
- High availability

______________________________________________________________________

# Broker

A broker is a Kafka server.

Example:

```
Machine 1

+----------------+
| Kafka Process  |
|                |
| Broker ID: 1   |
+----------------+
```

Responsibilities:

- Store messages
- Serve producers
- Serve consumers
- Replicate data

A Kafka cluster contains multiple brokers:

```
Kafka Cluster

Broker 1
Broker 2
Broker 3
```

______________________________________________________________________

# Topic

A topic is a logical stream of messages.

Examples:

```
orders

payments

notifications

user-events
```

Example:

```
Topic: orders


Order Created

Payment Received

Order Shipped
```

Topics are divided into partitions.

______________________________________________________________________

# Partition

A partition is the physical storage unit of Kafka.

Example:

```
Topic: orders


Partition 0

Message 0
Message 1
Message 2


Partition 1

Message 3
Message 4
Message 5
```

Partitions provide:

- Parallel processing
- Scalability
- Ordering

______________________________________________________________________

# Offset

Every message inside a partition has a unique position.

Example:

```
Partition 0


Offset       Message

0            Order Created

1            Payment Done

2            Order Shipped

3            Delivered
```

Offset means:

> The position of a message inside a partition.

______________________________________________________________________

# Producer

A producer sends messages to Kafka.

Example:

```
Application

    |
    |
    v

Kafka Topic
```

Example:

```python
producer.send(
    topic="orders",
    key="order-123",
    value="created"
)
```

Producer decides:

- Topic
- Key
- Partition (optional)

______________________________________________________________________

# Consumer

A consumer reads messages from Kafka.

Example:

```
Kafka

Partition 0

0
1
2
3


        |
        |
        v

    Consumer
```

Consumer tracks:

- Topic
- Partition
- Offset

______________________________________________________________________

# 3. Kafka Installation Models

## Single Broker Kafka

Used for:

- Development
- Testing
- Learning

Architecture:

```
             Kafka


        +-------------+
        | Broker 1    |
        |             |
        | orders      |
        | Partition 0 |
        +-------------+
```

Characteristics:

- No fault tolerance
- No replication
- One machine failure stops Kafka

______________________________________________________________________

## Multi Broker Kafka Cluster

Production setup:

```
                 Kafka Cluster


+-------------+-------------+-------------+
|             |             |             |
| Broker 1    | Broker 2    | Broker 3    |
|             |             |             |
+-------------+-------------+-------------+
```

Benefits:

- Data replication
- Failover
- More throughput

______________________________________________________________________

# Example: 3 Broker Cluster

```
Kafka Cluster


Broker 1             Broker 2             Broker 3


orders-P0            orders-P0            orders-P0
Leader               Replica              Replica


orders-P1            orders-P1            orders-P1
Replica              Leader                Replica


orders-P2            orders-P2            orders-P2
Replica              Replica              Leader
```

______________________________________________________________________

# Broker vs Cluster

Important distinction:

```
Kafka Installation
        |
        v

Kafka Broker
```

Multiple brokers:

```
Broker 1
Broker 2
Broker 3

        |
        v

Kafka Cluster
```

The cluster is not a separate installation.

The cluster is the collection of brokers.

______________________________________________________________________

# Redis Comparison

Redis Sentinel:

```
Redis Master

      |
      |
Redis Replicas
```

Kafka:

```
Partition Leader

      |
      |
Partition Replicas
```

Kafka does NOT have one master broker.

Leadership exists at partition level.

______________________________________________________________________

# Kafka Cluster Example

```
Kafka Cluster


Broker 1

Leader:
orders Partition 0


Broker 2

Leader:
orders Partition 1


Broker 3

Leader:
orders Partition 2
```

All brokers are active.

```
No master broker exists.
```

______________________________________________________________________

# Continue in Part 2:

# - Partitioning in depth

# - Key based partition selection

# - Producer flow

# - Bootstrap servers

# - Metadata discovery

# - Consumer groups

# - Offsets

# - auto.offset.reset

# 4. Kafka Message Flow

Understanding Kafka becomes easier by following the lifecycle of a message.

Complete flow:

```
                 Producer

                    |
                    |
                    v

              Kafka Cluster

        +-----------------------+
        |                       |
        | Topic: orders         |
        |                       |
        | Partition 0           |
        | Partition 1           |
        | Partition 2           |
        |                       |
        +-----------------------+

                    |
                    |
                    v

                Consumer
```

______________________________________________________________________

# Producer to Kafka Flow

Example:

Producer sends:

```
Topic:
orders

Key:
order-123

Value:
{
 "status":"CREATED"
}
```

Flow:

```
Producer

   |
   |
   v

Find partition

   |
   |
   v

Send message to partition leader

   |
   |
   v

Leader stores message

   |
   |
   v

Replicas copy the message
```

______________________________________________________________________

# 5. How Kafka Selects a Partition

A topic can have multiple partitions.

Example:

```
Topic: orders


Partition 0

Partition 1

Partition 2
```

Kafka must decide where a new message goes.

There are three common methods:

1. Key-based partitioning
1. Round-robin partitioning
1. Explicit partition selection

______________________________________________________________________

# Key Based Partitioning

Example:

```
Message:

key = order-123

value =
{
 orderStatus:"CREATED"
}
```

Kafka calculates:

```
hash(key) % number_of_partitions
```

Example:

```
hash(order-123) % 3

Result:

Partition 1
```

Message goes to:

```
orders Partition 1
```

______________________________________________________________________

# Example With Orders

Assume:

```
Topic:

orders


Partitions:

Partition 0

Partition 1

Partition 2
```

Messages:

```
order-1
order-2
order-3
order-4
order-5
```

Kafka calculates:

```
hash(order-id) % 3
```

Example:

```
order-1 -> Partition 0

order-2 -> Partition 2

order-3 -> Partition 1

order-4 -> Partition 0

order-5 -> Partition 2
```

Result:

```
Partition 0

order-1
order-4


Partition 1

order-3


Partition 2

order-2
order-5
```

______________________________________________________________________

# Important

You do NOT create partitions for every order.

Wrong design:

```
orders-1 partition

orders-2 partition

orders-3 partition
```

Correct design:

```
Topic:

orders


Partition 0
Partition 1
Partition 2
```

Kafka distributes orders across partitions.

______________________________________________________________________

# Ordering Guarantee

Kafka guarantees ordering only inside a partition.

Example:

```
Partition 0


Offset 0

order-created


Offset 1

payment-completed


Offset 2

order-shipped
```

Order is preserved.

______________________________________________________________________

Across partitions:

```
Partition 0

order-1
order-3


Partition 1

order-2
order-4
```

Kafka does NOT guarantee:

```
order-1
order-2
order-3
order-4
```

globally.

______________________________________________________________________

# Explicit Partition Selection

A producer can directly specify a partition.

Example:

```python
producer.send(
    topic="orders",
    partition=2,
    value="order-created"
)
```

Message goes directly:

```
orders

Partition 2
```

Use cases:

- Special routing requirements
- Testing
- Custom partition strategy

______________________________________________________________________

# 6. Bootstrap Servers

Producer and consumer configuration:

Example:

```properties
bootstrap.servers=
broker1:9092,
broker2:9092,
broker3:9092
```

These are NOT load balancers.

They are entry points for discovering Kafka.

______________________________________________________________________

# Can I Configure Only One Broker?

Yes.

Example:

```properties
bootstrap.servers=broker1:9092
```

Flow:

```
Producer

    |
    v

Broker 1

    |
    |
    v

Cluster Metadata


Broker 1
Broker 2
Broker 3
```

Kafka returns:

- Brokers
- Topics
- Partitions
- Leaders

______________________________________________________________________

# Metadata Discovery

Example:

Producer connects:

```
Producer

   |
   v

Broker 1

"Give me metadata"
```

Kafka returns:

```
Broker 1
Broker 2
Broker 3


orders:

Partition 0 -> Broker 2

Partition 1 -> Broker 3

Partition 2 -> Broker 1
```

Now producer sends directly:

```
Producer

   |
   +----> Broker 2
   |
   +----> Broker 3
   |
   +----> Broker 1
```

______________________________________________________________________

# Why Configure Multiple Bootstrap Servers?

Because the first broker may be unavailable.

Bad:

```
bootstrap.servers=broker1
```

If:

```
broker1 ❌
```

Client cannot discover the cluster.

______________________________________________________________________

Better:

```
bootstrap.servers=

broker1,
broker2,
broker3
```

If:

```
broker1 ❌
```

Client connects:

```
broker2 ✅
```

and gets metadata.

______________________________________________________________________

# 7. Consumer Architecture

A consumer reads messages from Kafka.

Example:

```
Consumer

    |
    |
    v

Kafka Partition


Offset 0
Offset 1
Offset 2
```

Consumer does not delete messages.

It only maintains its position.

______________________________________________________________________

# Consumer Group

A consumer group is a collection of consumers working together.

Example:

Topic:

```
orders

Partition 0
Partition 1
Partition 2
```

Consumer group:

```
order-service


Consumer 1

   |
   v

Partition 0


Consumer 2

   |
   v

Partition 1


Consumer 3

   |
   v

Partition 2
```

______________________________________________________________________

# Partition Assignment Rules

Important rule:

```
One partition
can be consumed by
only one consumer
inside the same group
```

Example:

```
Topic:

Partition 0
Partition 1


Consumer Group A


Consumer 1 -> Partition 0

Consumer 2 -> Partition 1
```

______________________________________________________________________

# Multiple Consumer Groups

Different groups consume independently.

Example:

Topic:

```
orders


Partition 0
Partition 1
Partition 2
```

Group 1:

```
order-processing


Partition 0 -> Consumer A
Partition 1 -> Consumer B
```

Group 2:

```
analytics


Partition 0 -> Consumer X
Partition 1 -> Consumer Y
Partition 2 -> Consumer Z
```

Both receive the same messages.

______________________________________________________________________

# 8. Offset Management

Kafka messages have offsets.

Example:

```
orders Partition 0


Offset

0  Order Created

1  Payment Done

2  Shipped

3  Delivered
```

Consumer stores:

```
"I have processed until offset 3"
```

______________________________________________________________________

# Where Are Offsets Stored?

Kafka stores offsets in:

```
__consumer_offsets
```

internal topic.

Example:

```
__consumer_offsets


Consumer Group:

order-service


Topic:

orders


Partition:

0


Committed Offset:

3
```

______________________________________________________________________

# Offset Commit Flow

Consumer processes:

```
Offset 0

Offset 1

Offset 2
```

Then commits:

```
Next offset = 3
```

Flow:

```
Consumer

   |
   |
   v

__consumer_offsets


order-service

orders partition 0

offset=3
```

______________________________________________________________________

# Consumer Restart Scenario

Before crash:

```
Processed:

0
1
2


Committed offset:

3
```

Consumer crashes.

After restart:

```
Kafka says:

Last committed offset = 3
```

Consumer continues:

```
3
4
5
```

It does NOT start from 0.

______________________________________________________________________

# What If No Offset Exists?

Example:

- New consumer group
- Offset deleted
- First time reading topic

Kafka uses:

```
auto.offset.reset
```

______________________________________________________________________

# auto.offset.reset

Controls where consumer starts when no offset exists.

Values:

```
earliest

latest

none
```

______________________________________________________________________

# earliest

Start from beginning.

Example:

```
Messages:

0
1
2
3


New consumer starts:

0
```

Useful for:

- Replaying events
- Analytics
- Data processing

______________________________________________________________________

# latest

Start from new messages only.

Example:

Existing:

```
0
1
2
```

Consumer starts.

New message:

```
3
```

Consumer reads:

```
3
```

______________________________________________________________________

# none

If no offset exists:

```
Throw error
```

Used when missing offsets should be treated as a problem.

______________________________________________________________________

# Continue in Part 3:

# - Commit strategies

# - Rebalancing

# - Leader and follower

# - Replication

# - ISR

# - Fault tolerance

# - Controller and KRaft

# 9. Consumer Offset Commit Strategies

A consumer must tell Kafka:

> "I have successfully processed messages up to this offset."

This is called committing an offset.

There are two common approaches.

______________________________________________________________________

# Automatic Commit

Configuration:

```properties
enable.auto.commit=true
```

Kafka automatically commits offsets periodically.

Example:

```properties
auto.commit.interval.ms=5000
```

Meaning:

Every 5 seconds Kafka commits the consumer position.

Flow:

```
Consumer

Reads:

0
1
2
3


After interval:

Commit offset 4


__consumer_offsets

offset = 4
```

______________________________________________________________________

## Problem With Auto Commit

Example:

```
Consumer reads:

0
1
2
3
```

Kafka commits:

```
offset = 4
```

Then:

```
Message 3 processing fails
```

Consumer restarts:

```
Starts from offset 4
```

Message 3 is skipped.

______________________________________________________________________

# Manual Commit

Configuration:

```properties
enable.auto.commit=false
```

Application decides when to commit.

Example:

```
Read message

        |
        v

Process message

        |
        v

Commit offset
```

______________________________________________________________________

Example:

```
Consumer reads:

0
1
2
3


Processing successful


Commit:

offset=4
```

______________________________________________________________________

# Commit After Every Message

Example:

```
Read message 0

Process

Commit offset 1


Read message 1

Process

Commit offset 2
```

Advantages:

- Lowest duplicate risk

Disadvantages:

- More network calls
- Lower throughput

______________________________________________________________________

# Commit in Batches

Example:

```
Read:

0
1
2
3
4
5


Process all


Commit:

offset=6
```

Advantages:

- Better performance

Disadvantage:

If consumer crashes:

```
Messages may be processed again
```

Example:

```
Processed:

0
1
2
3
4


Crash before commit
```

Restart:

```
Read:

0
1
2
3
4
```

This creates duplicates.

______________________________________________________________________

# 10. Consumer Rebalancing

A rebalance happens when Kafka redistributes partitions among consumers.

Triggers:

- Consumer joins
- Consumer leaves
- Consumer crashes
- Partition count changes

______________________________________________________________________

# Example Before Rebalance

Topic:

```
orders


Partition 0
Partition 1
Partition 2
```

Consumers:

```
Consumer Group:

order-service


Consumer A

Partition 0
Partition 1


Consumer B

Partition 2
```

______________________________________________________________________

# Consumer Joins

New consumer:

```
Consumer C joins
```

Kafka pauses consumption and redistributes.

After rebalance:

```
Consumer A

Partition 0


Consumer B

Partition 1


Consumer C

Partition 2
```

______________________________________________________________________

# Why Rebalancing Matters

During rebalance:

```
Consumers temporarily stop reading
```

This causes:

- Small pause
- Increased latency

Production systems try to minimize unnecessary rebalances.

______________________________________________________________________

# 11. Kafka Replication

Replication provides fault tolerance.

Example:

```
Topic:

orders


Partition 0


Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

There are three copies of the partition.

______________________________________________________________________

# Replication Factor

Replication factor defines number of copies.

Example:

```
Replication factor = 3
```

means:

```
One partition


Copy 1
Broker 1


Copy 2
Broker 2


Copy 3
Broker 3
```

______________________________________________________________________

# Leader and Follower

Each partition has:

- One leader
- Zero or more followers

Example:

```
Partition 0


Broker 1

Leader


Broker 2

Follower


Broker 3

Follower
```

______________________________________________________________________

# Leader Responsibilities

The leader handles:

## Producer writes

```
Producer

    |
    v

Partition Leader
```

______________________________________________________________________

## Consumer reads

```
Consumer

    |
    v

Partition Leader
```

______________________________________________________________________

## Replication

Leader sends data:

```
Leader

   |
   +--------> Follower

   |
   +--------> Follower
```

______________________________________________________________________

# Follower Responsibilities

Followers:

- Copy leader data
- Stay synchronized
- Can become leader

They normally do not serve client requests.

______________________________________________________________________

# Leader Failure

Before:

```
Partition 0


Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

Broker 1 fails:

```
Broker 1 ❌
```

Kafka elects:

```
Partition 0


Broker 2

New Leader


Broker 3

Replica
```

Producer and consumer continue.

______________________________________________________________________

# 12. ISR (In Sync Replicas)

ISR means:

> Replicas that are fully caught up with the leader.

Example:

```
Partition 0


Leader

Broker 1


ISR:

Broker 1
Broker 2
Broker 3
```

All replicas are healthy.

______________________________________________________________________

If Broker 3 falls behind:

```
Partition 0


Leader

Broker 1


Follower

Broker 2


Follower

Broker 3
(lagging)
```

ISR becomes:

```
Broker 1
Broker 2
```

Broker 3 is removed from ISR.

______________________________________________________________________

# 13. min.insync.replicas

Controls minimum number of replicas required for writes.

Example:

```
Replication Factor = 3

min.insync.replicas = 2
```

Cluster:

```
Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

Write succeeds:

```
Leader + one replica

= 2 replicas
```

______________________________________________________________________

If:

```
Broker 2 ❌

Broker 3 ❌
```

Only:

```
Broker 1
Leader
```

Available.

Write fails because:

```
1 < min.insync.replicas(2)
```

______________________________________________________________________

# 14. Producer Durability Configuration

Producer setting:

```
acks
```

Controls acknowledgment behavior.

______________________________________________________________________

# acks=0

Producer does not wait.

```
Producer

   |
   v

Kafka
```

Fastest.

Risk:

Message loss possible.

______________________________________________________________________

# acks=1

Leader confirms.

```
Producer

   |
   v

Leader

"Stored"
```

Followers may not have copied yet.

______________________________________________________________________

# acks=all

Wait for replicas.

```
Producer


    |
    v


Leader

    |
    +---- Replica

    |
    +---- Replica
```

Safest.

Recommended with:

```
min.insync.replicas=2
```

______________________________________________________________________

# 15. Kafka Controller

Kafka needs someone to manage cluster metadata.

This role is called:

```
Controller
```

Important:

Controller != Master Broker

______________________________________________________________________

# Controller Responsibilities

The controller manages:

- Broker registration
- Broker failure detection
- Partition leader election
- Partition assignment
- Cluster metadata

______________________________________________________________________

# What Controller Does NOT Do

Controller does NOT:

```
Receive producer messages
```

Controller does NOT:

```
Serve consumer reads
```

Partition leaders do those jobs.

______________________________________________________________________

# Example

```
Kafka Cluster


Broker 1

Controller

Leader:
orders-0


Broker 2

Leader:
orders-1


Broker 3

Leader:
orders-2
```

Broker 1 is controller.

But:

```
Broker 2 and Broker 3
still handle traffic
```

______________________________________________________________________

# 16. KRaft Architecture

Modern Kafka uses KRaft.

KRaft replaces ZooKeeper.

KRaft uses:

```
Raft Consensus Algorithm
```

______________________________________________________________________

# Controller Quorum

Example:

```
          KRaft Controller Quorum


       Controller 1

       Controller 2

       Controller 3
```

They maintain Kafka metadata.

______________________________________________________________________

# Active Controller Election

Initial state:

```
Controller 1

ACTIVE
```

Others:

```
Controller 2

FOLLOWER


Controller 3

FOLLOWER
```

______________________________________________________________________

Controller 1 fails:

```
Controller 1 ❌
```

Remaining nodes vote:

```
Controller 2
Controller 3
```

New leader:

```
Controller 2

ACTIVE CONTROLLER
```

______________________________________________________________________

# Combined Broker + Controller Mode

Small clusters commonly use:

```
Node 1

Broker
Controller


Node 2

Broker
Controller


Node 3

Broker
Controller
```

______________________________________________________________________

# Dedicated Controller Mode

Large clusters:

```
Controllers:

Controller 1
Controller 2
Controller 3


Brokers:

Broker 1
Broker 2
Broker 3
Broker 4
Broker 5
```

______________________________________________________________________

# Kafka vs Redis Sentinel Comparison

Redis:

```
Sentinel

   |
   v

Redis Master

   |
   v

Replicas
```

Kafka:

```
KRaft Controller Quorum

   |
   v

Partition Leaders

   |
   v

Partition Replicas
```

Kafka does not have one master broker.

______________________________________________________________________

# Continue in Part 4:

# - Internal Kafka topics

# - Complete configuration reference

# - Single broker vs production configuration

# - Real production cluster example

# - Advanced concepts

# 17. Kafka Internal Topics

Kafka uses some internal topics to store metadata.

The most important one:

```
__consumer_offsets
```

______________________________________________________________________

# \_\_consumer_offsets Topic

Kafka stores consumer progress here.

Example:

```
Consumer Group:

order-service


Topic:

orders


Partition:

0


Committed Offset:

500
```

Meaning:

```
order-service has processed
messages before offset 500
```

______________________________________________________________________

# Offset Storage Architecture

Your application data:

```
Topic:

orders


Partition 0


Offset 0
Order Created


Offset 1
Payment Done


Offset 2
Shipped
```

Separate internal topic:

```
__consumer_offsets


order-service

orders partition 0

offset = 3
```

They are separate.

______________________________________________________________________

# Is Offset Information Replicated?

Yes.

Because:

```
__consumer_offsets
```

is a Kafka topic.

It has:

- Partitions
- Leaders
- Replicas

Example:

```
__consumer_offsets


Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

______________________________________________________________________

# offsets.topic.replication.factor

Configuration:

```properties
offsets.topic.replication.factor=3
```

Controls how many copies of:

```
__consumer_offsets
```

exist.

______________________________________________________________________

## Development

Single broker:

```properties
offsets.topic.replication.factor=1
```

Because:

```
Broker 1 only
```

______________________________________________________________________

## Production

Three brokers:

```properties
offsets.topic.replication.factor=3
```

Result:

```
Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

______________________________________________________________________

# 18. Kafka Configuration Overview

Kafka configuration is divided into:

```
1. Broker configuration

2. Topic configuration

3. Producer configuration

4. Consumer configuration
```

______________________________________________________________________

# 19. Broker Configurations

Broker configurations are applied to Kafka servers.

______________________________________________________________________

# broker.id

Example:

```properties
broker.id=1
```

Purpose:

Unique ID for each broker.

Example:

```
Broker 1

broker.id=1


Broker 2

broker.id=2


Broker 3

broker.id=3
```

______________________________________________________________________

# listeners

Example:

```properties
listeners=PLAINTEXT://0.0.0.0:9092
```

Defines where Kafka accepts connections.

Example:

```
Kafka Server

Listening:

9092
```

______________________________________________________________________

# advertised.listeners

Example:

```properties
advertised.listeners=
PLAINTEXT://kafka1.company.com:9092
```

The address Kafka gives to clients.

Example:

```
Producer connects:


bootstrap broker


Kafka replies:


Use:

kafka2.company.com:9092
```

If this is wrong:

```
Clients cannot connect
```

______________________________________________________________________

# log.dirs

Example:

```properties
log.dirs=/data/kafka
```

Where Kafka stores messages.

Example:

```
/data/kafka


orders-0


000000000.log
000000001.log
```

______________________________________________________________________

# num.partitions

Example:

```properties
num.partitions=3
```

Default partitions for new topics.

Example:

Create:

```
orders
```

Kafka creates:

```
orders

Partition 0
Partition 1
Partition 2
```

Existing topics are not changed.

______________________________________________________________________

# default.replication.factor

Example:

```properties
default.replication.factor=3
```

Default number of copies for new topics.

Example:

```
Topic:

orders


Replication factor:

3
```

Result:

```
Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

______________________________________________________________________

# offsets.topic.replication.factor

Example:

```properties
offsets.topic.replication.factor=3
```

Controls replication of:

```
__consumer_offsets
```

Used for:

- Consumer recovery
- Offset durability

______________________________________________________________________

# transaction.state.log.replication.factor

Example:

```properties
transaction.state.log.replication.factor=3
```

Controls replication of:

```
__transaction_state
```

Used by Kafka transactions.

______________________________________________________________________

# transaction.state.log.min.isr

Example:

```properties
transaction.state.log.min.isr=2
```

Minimum replicas needed for transaction metadata writes.

______________________________________________________________________

# min.insync.replicas

Example:

```properties
min.insync.replicas=2
```

Minimum replicas required for successful writes.

Example:

```
Replication factor:

3


Need:

2 healthy replicas
```

______________________________________________________________________

# 20. Topic Configuration

Topic configurations can override broker defaults.

Example:

```
Broker default:

replication.factor=3


Topic:

orders

replication.factor=2
```

Topic setting wins.

______________________________________________________________________

# Topic Creation Example

```
Topic:

orders


Partitions:

6


Replication Factor:

3
```

Result:

```
Partition 0

Broker 1 Leader
Broker 2 Replica
Broker 3 Replica


Partition 1

Broker 2 Leader
Broker 3 Replica
Broker 1 Replica
```

______________________________________________________________________

# log.retention.hours

Example:

```properties
log.retention.hours=168
```

Kafka keeps messages:

```
168 hours

=
7 days
```

After that:

```
Old segments deleted
```

______________________________________________________________________

# log.retention.bytes

Example:

```properties
log.retention.bytes=1073741824
```

Keep maximum size:

```
1 GB
```

______________________________________________________________________

# cleanup.policy

Example:

```properties
cleanup.policy=delete
```

Options:

```
delete

compact
```

______________________________________________________________________

# Delete Policy

Normal event streaming.

Example:

```
orders

Keep for 7 days

Delete old messages
```

______________________________________________________________________

# Compact Policy

Keeps latest value per key.

Example:

```
User topic


Before:

user-1 = Name:A

user-1 = Name:B


After compaction:

user-1 = Name:B
```

Used for:

- Current state
- Config topics

______________________________________________________________________

# 21. Producer Configurations

______________________________________________________________________

# bootstrap.servers

Example:

```properties
bootstrap.servers=
broker1:9092,
broker2:9092
```

Used for:

Cluster discovery.

Not a load balancer.

______________________________________________________________________

# acks

Controls write acknowledgment.

______________________________________________________________________

## acks=0

No confirmation.

```
Producer

  |
  v

Kafka
```

Fast.

Risk:

Data loss.

______________________________________________________________________

## acks=1

Leader confirmation.

```
Producer

  |
  v

Leader


OK
```

______________________________________________________________________

## acks=all

All required replicas confirm.

```
Producer


Leader

 |
 +---- Replica

 |
 +---- Replica
```

Safest.

______________________________________________________________________

# retries

Example:

```properties
retries=5
```

Retry failed sends.

______________________________________________________________________

# enable.idempotence

Example:

```properties
enable.idempotence=true
```

Prevents duplicate messages during retries.

Example:

Without idempotence:

```
Message A

Retry

Message A

Duplicate
```

With idempotence:

```
Message A

Retry

Kafka ignores duplicate
```

______________________________________________________________________

# compression.type

Example:

```properties
compression.type=snappy
```

Options:

```
gzip

snappy

lz4

zstd
```

Benefits:

- Lower network usage
- Less storage

______________________________________________________________________

# 22. Consumer Configurations

______________________________________________________________________

# group.id

Example:

```properties
group.id=order-service
```

Identifies the consumer group.

______________________________________________________________________

# enable.auto.commit

Example:

```properties
enable.auto.commit=false
```

Controls automatic offset commits.

______________________________________________________________________

# auto.commit.interval.ms

Example:

```properties
auto.commit.interval.ms=5000
```

Commit interval.

______________________________________________________________________

# auto.offset.reset

Controls starting position.

______________________________________________________________________

## earliest

```
Start from beginning
```

______________________________________________________________________

## latest

```
Start from new messages
```

______________________________________________________________________

## none

```
Throw error
```

______________________________________________________________________

# max.poll.records

Example:

```properties
max.poll.records=500
```

Maximum messages returned per poll.

______________________________________________________________________

# session.timeout.ms

Controls consumer failure detection.

If consumer does not send heartbeat:

```
Kafka considers consumer dead
```

______________________________________________________________________

# heartbeat.interval.ms

Consumer sends:

```
"I'm alive"
```

to Kafka.

______________________________________________________________________

# Continue in Part 5:

# - Complete production cluster design

# - Failure scenarios

# - Recommended configurations

# - Advanced Kafka concepts

# 23. Production Kafka Cluster Design

A typical production Kafka cluster uses multiple brokers.

Example:

```
                         Kafka Cluster


        +----------------+----------------+----------------+
        |                |                |                |
        |   Broker 1     |   Broker 2     |   Broker 3     |
        |                |                |                |
        +----------------+----------------+----------------+


                 Controller Quorum (KRaft)

        Broker 1        Broker 2        Broker 3

```

______________________________________________________________________

# Example Production Topic

Topic:

```
orders
```

Configuration:

```
Partitions:

3


Replication Factor:

3
```

Kafka distributes:

```
                 orders topic


Partition 0


Broker 1

Leader


Broker 2

Replica


Broker 3

Replica



Partition 1


Broker 2

Leader


Broker 3

Replica


Broker 1

Replica



Partition 2


Broker 3

Leader


Broker 1

Replica


Broker 2

Replica
```

______________________________________________________________________

# Why Multiple Partitions?

Partitions provide:

## Parallelism

Example:

```
Partition 0 ---> Consumer 1

Partition 1 ---> Consumer 2

Partition 2 ---> Consumer 3
```

Three consumers process simultaneously.

______________________________________________________________________

## Higher Throughput

Single partition:

```
Producer

    |
    v

Partition 0

    |
    v

Consumer
```

Limited by one partition.

______________________________________________________________________

Multiple partitions:

```
Producer

    |
    |
    +----------+
    |          |
    v          v

Partition 0  Partition 1


    |
    |
    v

Multiple Consumers
```

______________________________________________________________________

# 24. Kafka Failure Scenarios

## Scenario 1: Broker Failure

Before:

```
Partition 0


Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

Broker 1 fails:

```
Broker 1 ❌
```

Controller detects:

```
Leader unavailable
```

Election:

```
Broker 2

New Leader
```

After:

```
Partition 0


Broker 2

Leader


Broker 3

Replica
```

Application continues.

______________________________________________________________________

# Scenario 2: Controller Failure

Before:

```
Broker 1

Active Controller


Broker 2

Controller follower


Broker 3

Controller follower
```

Broker 1 fails:

```
Broker 1 ❌
```

KRaft quorum votes:

```
Broker 2

New Active Controller
```

______________________________________________________________________

# Scenario 3: Replica Failure

Before:

```
Partition 0


Broker 1

Leader


Broker 2

Replica


Broker 3

Replica
```

Broker 3 fails:

```
Broker 3 ❌
```

ISR changes:

Before:

```
ISR:

Broker 1
Broker 2
Broker 3
```

After:

```
ISR:

Broker 1
Broker 2
```

Kafka continues.

______________________________________________________________________

# Scenario 4: Producer Failure

Producer sends:

```
Order Created
```

Network problem occurs.

Producer retries.

Without idempotence:

```
Order Created

Order Created

Duplicate
```

With:

```properties
enable.idempotence=true
```

Kafka removes duplicate.

______________________________________________________________________

# 25. Recommended Production Configuration

Example:

```
Kafka Cluster:

3 Brokers
```

______________________________________________________________________

## Broker Configuration

```properties
broker.id=<unique-id>


process.roles=broker,controller


num.partitions=6


default.replication.factor=3


offsets.topic.replication.factor=3


transaction.state.log.replication.factor=3


min.insync.replicas=2
```

______________________________________________________________________

# Producer Configuration

Recommended:

```properties
acks=all

enable.idempotence=true

retries=10

compression.type=zstd
```

Meaning:

```
Wait for replicas

Avoid duplicates

Retry failures

Compress messages
```

______________________________________________________________________

# Consumer Configuration

Recommended:

```properties
enable.auto.commit=false

auto.offset.reset=earliest
```

Application controls commits.

______________________________________________________________________

# 26. Kafka Architecture Complete View

```
                         PRODUCER


                            |
                            |
                            v


                  Kafka Bootstrap Server

                            |
                            |
                            v


                  Cluster Metadata


                            |
                            v


+--------------------------------------------------+

                 Kafka Cluster


     Broker 1             Broker 2             Broker 3


     Leader               Leader               Leader

     P0                   P1                   P2


     Replica              Replica              Replica


+--------------------------------------------------+


                            |
                            |
                            v


                     Consumer Group



              Consumer 1     Consumer 2     Consumer 3

              P0             P1             P2
```

______________________________________________________________________

# 27. Advanced Kafka Concepts

______________________________________________________________________

# Exactly Once Semantics (EOS)

Kafka can provide:

```
Exactly once processing
```

Meaning:

A message is processed:

```
Once

not

Zero times

not

Multiple times
```

Used in:

- Financial systems
- Payment processing
- Critical workflows

______________________________________________________________________

# Kafka Transactions

Transactions allow multiple operations to succeed together.

Example:

Transfer money:

```
Account A

-100


Account B

+100
```

Either:

```
Both succeed
```

or:

```
Both rollback
```

______________________________________________________________________

# Idempotent Producer

Problem:

```
Send message


Network failure


Retry


Duplicate
```

Solution:

```
enable.idempotence=true
```

Kafka assigns:

```
Producer ID

Sequence number
```

Duplicate messages are detected.

______________________________________________________________________

# 28. Kafka Streams

Kafka Streams is a processing library.

Architecture:

```
Kafka Topic


      |
      v


Kafka Streams Application


      |
      v


Output Topic
```

Used for:

- Filtering
- Aggregation
- Joins
- Real-time calculations

______________________________________________________________________

# Example

Input:

```
orders
```

Streams application:

```
Filter:

Only successful orders
```

Output:

```
completed-orders
```

______________________________________________________________________

# 29. Performance Tuning Concepts

______________________________________________________________________

# Increase Partitions

More partitions:

Advantages:

```
More consumers

More parallelism

Higher throughput
```

Disadvantages:

```
More metadata

More resource usage
```

______________________________________________________________________

# Batch Processing

Producer batches messages.

Configuration:

```
batch.size

linger.ms
```

Example:

Instead of:

```
Send

Send

Send

Send
```

Kafka sends:

```
Batch:

Message 1
Message 2
Message 3
Message 4
```

______________________________________________________________________

# Compression

Compression reduces:

- Network traffic
- Disk usage

Options:

```
gzip

snappy

lz4

zstd
```

______________________________________________________________________

# Consumer Parallelism Rule

Important:

```
Number of consumers
cannot exceed
number of partitions
```

Example:

Topic:

```
3 partitions
```

Consumers:

```
Consumer 1
Consumer 2
Consumer 3
Consumer 4
```

Result:

```
Consumer 4 gets no partition
```

______________________________________________________________________

# 30. Kafka Mental Model Summary

Remember these rules:

______________________________________________________________________

## Cluster

```
Multiple brokers together
```

______________________________________________________________________

## Broker

```
Kafka server
```

______________________________________________________________________

## Topic

```
Logical message stream
```

______________________________________________________________________

## Partition

```
Physical storage unit
```

______________________________________________________________________

## Offset

```
Message position
```

______________________________________________________________________

## Producer

```
Writes messages
```

______________________________________________________________________

## Consumer

```
Reads messages
```

______________________________________________________________________

## Leader

```
Handles reads/writes for a partition
```

______________________________________________________________________

## Replica

```
Copy of partition data
```

______________________________________________________________________

## Controller

```
Manages cluster metadata
```

______________________________________________________________________

## KRaft

```
Elects controller
Stores metadata
```

______________________________________________________________________

## Replication Factor

```
Number of copies
```

______________________________________________________________________

## ISR

```
Healthy replicas
```

______________________________________________________________________

## acks=all + min.insync.replicas

```
Strong durability
```

______________________________________________________________________

# Final Kafka Architecture

```
                           Kafka Cluster


        +------------------------------------------------+

                         KRaft Controller


        +------------------------------------------------+


     Broker 1              Broker 2              Broker 3


     Topic: orders


     P0 Leader             P0 Replica            P0 Replica


     P1 Replica            P1 Leader             P1 Replica


     P2 Replica            P2 Replica            P2 Leader



        Producer
            |
            |
            v

        Partition Leader



        Consumer Group

            |
            |
            v

        Read From Partition Leaders

```

______________________________________________________________________

# End of Kafka Complete Guide
