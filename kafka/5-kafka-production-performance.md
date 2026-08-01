# Kafka Production, Performance & Exactly-Once Processing

## Introduction

Most developers know how to produce and consume messages.

Senior Backend Engineers are expected to understand:

- Kafka internals
- Performance tuning
- Monitoring
- Scaling
- Message delivery guarantees
- Exactly-Once Processing
- Idempotency
- Transactions
- Security
- Production deployment

This chapter focuses on operating Kafka in production.

______________________________________________________________________

# Kafka in Production

A typical production architecture looks like this.

```text id="kpp001"
                Clients
                    │
                    ▼
              API Gateway
                    │
                    ▼
            Order Service
                    │
                    ▼
            Kafka Producer
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
     Kafka Cluster        Schema Registry
         │
 ┌───────┼────────────┬──────────────┐
 ▼       ▼            ▼              ▼
Inventory Payment   Analytics    Notification
Consumer  Consumer   Consumer      Consumer
         │
         ▼
    PostgreSQL
```

______________________________________________________________________

# Kafka Cluster

A production Kafka deployment usually consists of multiple brokers.

```text id="kpp002"
Broker 1

Broker 2

Broker 3
```

Advantages

- Fault tolerance
- Horizontal scaling
- Replication
- High availability

______________________________________________________________________

# Broker Responsibilities

Each broker stores partitions.

Example

```text id="kpp003"
Broker 1

P0

P3

Broker 2

P1

P4

Broker 3

P2

P5
```

The cluster distributes work.

______________________________________________________________________

# Partition Count

Choosing partition count is important.

Too few

↓

Limited throughput.

Too many

↓

Operational overhead.

______________________________________________________________________

# General Guidelines

Partition count depends on:

- Expected throughput
- Consumer parallelism
- Future growth

Avoid creating an excessive number of partitions "just in case."

______________________________________________________________________

# Compression

Kafka supports message compression.

Common algorithms

- gzip
- snappy
- lz4
- zstd

Example

```python id="kpp004"
Producer(
    {
        "bootstrap.servers": "localhost:9092",
        "compression.type": "zstd"
    }
)
```

Compression reduces network traffic and storage usage.

______________________________________________________________________

# Batch Processing

Instead of sending one message at a time,

Kafka batches messages.

```text id="kpp005"
Message

Message

Message

↓

One Batch

↓

Broker
```

Batching improves throughput.

______________________________________________________________________

# Producer Batching

Example

```python id="kpp006"
Producer(
    {
        "linger.ms": 10,
        "batch.size": 65536
    }
)
```

`linger.ms`

Wait briefly to accumulate a larger batch.

`batch.size`

Maximum batch size in bytes.

______________________________________________________________________

# Delivery Guarantees

Kafka supports three delivery models.

```text id="kpp007"
At Most Once

At Least Once

Exactly Once
```

______________________________________________________________________

# At Most Once

Flow

```text id="kpp008"
Commit Offset

↓

Process
```

Fast.

Messages may be lost if processing fails after the commit.

______________________________________________________________________

# At Least Once

Flow

```text id="kpp009"
Process

↓

Commit Offset
```

Most common.

Messages may be processed more than once.

Consumers should be idempotent.

______________________________________________________________________

# Exactly Once

Kafka provides support for Exactly-Once Semantics (EOS) when producers, brokers, and consumers are configured
appropriately.

The goal is:

```text id="kpp010"
One Event

↓

One Result
```

Exactly-once processing often combines:

- Idempotent producer
- Kafka transactions
- Transaction-aware consumers
- Correct application design

______________________________________________________________________

# Idempotent Producer

Enable

```python id="kpp011"
Producer(
    {
        "bootstrap.servers": "localhost:9092",
        "enable.idempotence": True
    }
)
```

Benefits

- Eliminates duplicate records caused by producer retries.
- Preserves ordering for retried sends.

______________________________________________________________________

# Producer Transactions

Create producer

```python id="kpp012"
Producer(
    {
        "bootstrap.servers": "localhost:9092",
        "transactional.id": "order-service"
    }
)
```

Initialize

```python id="kpp013"
producer.init_transactions()
```

Begin

```python id="kpp014"
producer.begin_transaction()
```

Produce

```python id="kpp015"
producer.produce(
    "orders",
    value="..."
)
```

Commit

```python id="kpp016"
producer.commit_transaction()
```

Abort on failure

```python id="kpp017"
producer.abort_transaction()
```

Transactions help coordinate multiple Kafka writes atomically.

______________________________________________________________________

# Why Transactions?

Suppose

```text id="kpp018"
Order Created

↓

Inventory Event

↓

Payment Event
```

If the application crashes halfway,

transactions help avoid partially published event sequences.

______________________________________________________________________

# Consumer Idempotency

Even with advanced Kafka features,

business logic should remain idempotent.

Example

```python id="kpp019"
if already_processed(
    event_id
):
    return

process()

mark_processed(
    event_id
)
```

______________________________________________________________________

# Monitoring

Production systems monitor:

- Consumer lag
- Throughput
- Broker health
- Under-replicated partitions
- Request latency
- Disk usage
- Network traffic

______________________________________________________________________

# Consumer Lag

One of the most important metrics.

```text id="kpp020"
Latest Offset

5000

Consumer Offset

4900

Lag

100
```

Increasing lag often means consumers cannot keep up.

______________________________________________________________________

# Under-Replicated Partitions

If replicas fall behind,

Kafka reports

```text id="kpp021"
Under Replicated Partitions
```

This is an important operational alert.

______________________________________________________________________

# Retention

Kafka keeps messages for a configurable period.

Example

```text id="kpp022"
7 Days
```

After retention expires,

old records are removed according to the configured cleanup policy.

Kafka does **not** delete a message immediately after a consumer reads it.

______________________________________________________________________

# Retention vs Offset

Reading a message

↓

Does **not**

delete it.

Consumers maintain offsets independently.

______________________________________________________________________

# Schema Evolution

Changing event formats is common.

Bad

```json id="kpp023"
{
    "id":101
}
```

Later

```json id="kpp024"
{
    "order_id":101
}
```

Older consumers may break.

Use versioned schemas and backward-compatible changes.

Many production systems use a Schema Registry with formats such as Avro, Protobuf, or JSON Schema.

______________________________________________________________________

# Security

Production Kafka commonly uses:

- TLS
- SASL authentication
- ACLs (Access Control Lists)

Never expose brokers directly to the public Internet.

______________________________________________________________________

# Logging

Log

- Topic
- Partition
- Offset
- Event ID
- Processing time

Avoid logging sensitive information such as passwords or payment credentials.

______________________________________________________________________

# Scaling Consumers

Suppose

```text id="kpp025"
Lag

Increasing
```

Options

- Add consumers
- Increase partitions (with planning)
- Optimize processing
- Batch downstream work

______________________________________________________________________

# Scaling Producers

Usually straightforward.

Multiple producers can publish to the same topic simultaneously.

Kafka handles concurrent producers efficiently.

______________________________________________________________________

# Disaster Recovery

Best practices:

- Multiple brokers
- Replication
- Backups
- Monitoring
- Alerting
- Tested recovery procedures

______________________________________________________________________

# Production Folder Structure

```text id="kpp026"
order-service/

├── api/

├── kafka/

│      producer.py

│      consumer.py

│      config.py

├── services/

├── repositories/

├── workers/

├── tests/

└── main.py
```

______________________________________________________________________

# Common Mistakes

### Auto Commit for Critical Workloads

Manual commits are generally safer.

______________________________________________________________________

### Ignoring Consumer Lag

Lag should be monitored continuously.

______________________________________________________________________

### No Replication

Single-broker deployments are unsuitable for production.

______________________________________________________________________

### Large Messages

Store files externally.

Publish references.

______________________________________________________________________

### Ignoring Schema Compatibility

Event evolution must be planned.

______________________________________________________________________

### No Monitoring

Production Kafka requires observability.

______________________________________________________________________

# Best Practices

- Use idempotent producers.
- Design idempotent consumers.
- Monitor consumer lag.
- Configure replication.
- Enable compression.
- Batch messages when appropriate.
- Version event schemas.
- Use TLS and authentication.
- Keep events immutable.
- Benchmark before tuning.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between At-Least-Once and Exactly-Once processing?

At-Least-Once processing guarantees that every message will be processed, but duplicates are possible if failures occur
after processing and before offset commits. Consumers must therefore be idempotent. Exactly-Once processing combines
Kafka's idempotent producers, transactions, and transaction-aware processing to prevent duplicate effects in supported
workflows. Even when using Exactly-Once Semantics, application logic is often still designed to be idempotent for
robustness.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is consumer lag?
1. What are Kafka delivery guarantees?
1. Explain At-Most-Once.
1. Explain At-Least-Once.
1. Explain Exactly-Once.
1. Why use idempotent producers?
1. Why use transactions?
1. Why monitor under-replicated partitions?
1. Why use compression?
1. Why version event schemas?

## Coding

1. Enable compression.
1. Enable idempotent producers.
1. Configure a transactional producer.
1. Begin and commit a Kafka transaction.
1. Implement an idempotent consumer.
1. Record processing metrics.

______________________________________________________________________

# Hands-on Exercise

Improve the Order Event System.

Requirements:

1. Enable message compression.
1. Enable producer idempotence.
1. Publish events using Kafka transactions.
1. Make consumers idempotent.
1. Track consumer lag.
1. Log topic, partition, and offset.
1. Add schema version information.
1. Simulate consumer failures and recovery.

______________________________________________________________________

# Cheat Sheet

```text id="kpp027"
Compression

↓

Batching

↓

At-Most-Once

↓

At-Least-Once

↓

Exactly-Once

↓

Idempotent Producer

↓

Transactions

↓

Consumer Lag

↓

Retention

↓

Monitoring

↓

Schema Evolution
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Kafka production architecture
- Broker responsibilities
- Partition planning
- Compression
- Producer batching
- Delivery guarantees
- Idempotent producers
- Kafka transactions
- Consumer idempotency
- Monitoring
- Consumer lag
- Retention
- Schema evolution
- Security
- Scaling
- Disaster recovery
- Production best practices
- Interview patterns

You now understand how Kafka is operated in production and how to build reliable, scalable event-driven systems with
Python.

______________________________________________________________________

## Next File

[6-kafka-interview-masterclass-part-1.md](6-kafka-interview-masterclass-part-1.md)
