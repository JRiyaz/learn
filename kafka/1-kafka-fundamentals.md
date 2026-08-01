# Kafka Fundamentals

## Introduction

Modern applications often consist of multiple independent services.

Consider an e-commerce application.

When a customer places an order, several systems need to react:

- Inventory Service
- Payment Service
- Email Service
- Notification Service
- Analytics Service
- Recommendation Engine

Calling every service synchronously creates tight coupling and poor scalability.

Apache Kafka solves this problem by acting as a high-throughput event streaming platform.

Kafka is one of the most important technologies for modern backend engineering and distributed systems.

Companies like LinkedIn, Netflix, Uber, Microsoft, Walmart, Airbnb, and many others use Kafka extensively.

In this chapter, you'll learn:

- What Kafka is
- Why Kafka exists
- Event-Driven Architecture
- Kafka Components
- Topics
- Producers
- Consumers
- Brokers
- Basic CLI
- Python Introduction
- Real-world use cases

______________________________________________________________________

# What is Kafka?

Apache Kafka is a **distributed event streaming platform**.

Kafka allows applications to:

- Publish events
- Store events
- Process events
- Consume events

Unlike traditional message brokers, Kafka is designed for:

- High throughput
- Fault tolerance
- Scalability
- Durability

______________________________________________________________________

# Why Do We Need Kafka?

Without Kafka

```text id="kafka001"
Order Service

├── Payment Service

├── Email Service

├── Inventory Service

├── Notification Service

└── Analytics Service
```

Every service directly communicates with every other service.

Problems:

- Tight coupling
- Difficult scaling
- Failure propagation
- Complex deployments

______________________________________________________________________

With Kafka

```text id="kafka002"
Order Service

↓

Kafka

├── Payment Service

├── Email Service

├── Inventory Service

├── Notification Service

└── Analytics Service
```

Services become independent.

______________________________________________________________________

# Event-Driven Architecture

Kafka is built around events.

Example event

```json id="kafka003"
{
    "order_id": 101,
    "user_id": 25,
    "amount": 500
}
```

This event is published once.

Many services can consume it independently.

______________________________________________________________________

# Kafka Architecture

```text id="kafka004"
Producer

↓

Topic

↓

Broker

↓

Consumer
```

We'll study each component in detail.

______________________________________________________________________

# Producer

A Producer sends messages to Kafka.

Example

```text id="kafka005"
Order Service

↓

Kafka Topic
```

Examples of producers:

- Payment Service
- User Service
- Inventory Service
- Logging Service

______________________________________________________________________

# Consumer

A Consumer reads messages.

```text id="kafka006"
Kafka Topic

↓

Email Service
```

Consumers process events independently.

______________________________________________________________________

# Topic

A Topic is a named stream of events.

Examples

```text id="kafka007"
orders

payments

users

notifications
```

Think of a Topic as a continuously growing log.

______________________________________________________________________

# Broker

A Broker is a Kafka server.

```text id="kafka008"
Producer

↓

Broker

↓

Consumer
```

A Kafka cluster typically contains multiple brokers.

______________________________________________________________________

# Kafka Cluster

```text id="kafka009"
Broker 1

Broker 2

Broker 3
```

Multiple brokers provide:

- High availability
- Scalability
- Fault tolerance

______________________________________________________________________

# Installing Kafka

The easiest way for development is Docker (we'll cover Docker later).

Alternatively, download Kafka from the official Apache distribution and start a local broker.

______________________________________________________________________

# Kafka CLI

List Topics

```bash id="kafka010"
kafka-topics.sh \
--bootstrap-server localhost:9092 \
--list
```

Create Topic

```bash id="kafka011"
kafka-topics.sh \
--bootstrap-server localhost:9092 \
--create \
--topic orders \
--partitions 3 \
--replication-factor 1
```

Delete Topic

```bash id="kafka012"
kafka-topics.sh \
--bootstrap-server localhost:9092 \
--delete \
--topic orders
```

______________________________________________________________________

# Python Client

The recommended production client is **Confluent's** Python library.

Install

```bash id="kafka013"
pip install confluent-kafka
```

______________________________________________________________________

# Simple Producer

```python id="kafka014"
from confluent_kafka import Producer

producer = Producer(
    {
        "bootstrap.servers": "localhost:9092"
    }
)

producer.produce(
    "orders",
    key="101",
    value='{"order_id":101}'
)

producer.flush()
```

`flush()` waits until outstanding messages are delivered.

______________________________________________________________________

# Simple Consumer

```python id="kafka015"
from confluent_kafka import Consumer

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "order-service",
        "auto.offset.reset": "earliest"
    }
)

consumer.subscribe(["orders"])

while True:

    message = consumer.poll(1.0)

    if message is None:
        continue

    if message.error():
        print(message.error())
        continue

    print(message.value().decode())
```

______________________________________________________________________

# Kafka vs RabbitMQ

| Kafka | RabbitMQ |
| -------------------- | ---------------- |
| Event Streaming | Message Broker |
| Durable Log | Queue |
| Replay Messages | Limited Replay |
| Very High Throughput | Flexible Routing |
| Partition Based | Queue Based |

Interview Tip

Kafka and RabbitMQ solve overlapping but different problems.

______________________________________________________________________

# Kafka vs Redis Streams

| Kafka | Redis Streams |
| -------------------------- | --------------------------- |
| Distributed Event Platform | Redis Data Structure |
| Massive Scale | Moderate Scale |
| Long-Term Retention | Typically Shorter Retention |
| Independent Cluster | Redis Feature |

______________________________________________________________________

# Real Production Use Cases

Kafka is commonly used for:

- Order processing
- Payment events
- Log aggregation
- Audit trails
- Recommendation engines
- Fraud detection
- Analytics pipelines
- IoT event ingestion

______________________________________________________________________

# Common Mistakes

### Using Kafka as a Database

Kafka stores events, not relational data.

______________________________________________________________________

### Creating Too Many Topics

Each topic has operational overhead.

______________________________________________________________________

### Sending Extremely Large Messages

Store large files externally and publish references.

______________________________________________________________________

### Ignoring Consumer Failures

Consumers should handle retries and failures gracefully.

______________________________________________________________________

# Best Practices

- Design meaningful topic names.
- Keep events immutable.
- Use message keys when ordering matters.
- Monitor consumer lag.
- Design consumers to be idempotent.
- Treat Kafka as an event log, not a relational database.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do companies use Kafka instead of direct service-to-service communication?

Kafka decouples producers from consumers. A producer publishes an event once without knowing which services will consume
it. Multiple independent consumers can process the same event at their own pace, improving scalability, fault tolerance,
and maintainability. New services can subscribe to existing topics without modifying the producer, making event-driven
architectures easier to evolve.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is Kafka?
1. What is an event?
1. What is a Producer?
1. What is a Consumer?
1. What is a Topic?
1. What is a Broker?
1. Kafka vs RabbitMQ.
1. Kafka vs Redis Streams.
1. Why use event-driven architecture?
1. Why is Kafka scalable?

## Coding

1. Create a topic.
1. Produce a message.
1. Consume a message.
1. Publish multiple events.
1. Create multiple consumers.

______________________________________________________________________

# Hands-on Exercise

Build a simple Order Event System.

Requirements:

1. Create an `orders` topic.
1. Publish order events.
1. Create an inventory consumer.
1. Create a payment consumer.
1. Create an email consumer.
1. Verify that all consumers receive the published events independently.

______________________________________________________________________

# Cheat Sheet

```text id="kafka016"
Producer

↓

Topic

↓

Broker

↓

Consumer

↓

Event Streaming

↓

Kafka Cluster
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- What Kafka is
- Why Kafka exists
- Event-driven architecture
- Producers
- Consumers
- Topics
- Brokers
- Kafka clusters
- Basic CLI commands
- Python producer
- Python consumer
- Production use cases
- Best practices
- Interview patterns

You now understand the core concepts of Kafka and are ready to explore partitions, replication, offsets, and consumer
groups.

______________________________________________________________________

## Next File

[2-kafka-producers-consumers.md](2-kafka-producers-consumers.md)
