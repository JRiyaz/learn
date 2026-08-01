# Kafka Order Processing Project - Part 4 (Final)

## Introduction

Congratulations!

You have built a complete event-driven application using:

- FastAPI
- PostgreSQL
- SQLModel
- Kafka
- JSON Events
- Producers
- Consumers
- Retry
- Dead Letter Queue
- Idempotent Consumers

In this final chapter, we'll:

- Run the complete project
- Test the event flow
- Understand the execution sequence
- Discuss possible improvements
- Review interview questions
- Prepare for the production microservices project that we'll build later

______________________________________________________________________

# Final Architecture

```text id="kpf401"
                           Client
                              │
                              ▼
                      FastAPI REST API
                              │
                              ▼
                     PostgreSQL Database
                              │
                              ▼
                     Kafka Producer
                              │
                     orders.created
                              │
      ┌────────────┬─────────────┬─────────────┬──────────────┐
      ▼            ▼             ▼              ▼
 Inventory     Payment       Email        Analytics
 Consumer      Consumer      Consumer      Consumer
      │            │             │              │
      └────────────┴─────────────┴──────────────┘
                              │
                              ▼
                        Dead Letter Queue
```

______________________________________________________________________

# Running the Project

Start PostgreSQL.

Start Kafka.

Create the topic.

```bash id="kpf402"
kafka-topics.sh \
--bootstrap-server localhost:9092 \
--create \
--topic orders.created \
--partitions 3 \
--replication-factor 1
```

Create the DLQ topic.

```bash id="kpf403"
kafka-topics.sh \
--bootstrap-server localhost:9092 \
--create \
--topic orders.dlq \
--partitions 1 \
--replication-factor 1
```

______________________________________________________________________

# Start the API

```bash id="kpf404"
uvicorn app:app --reload
```

______________________________________________________________________

# Start Consumers

Inventory

```bash id="kpf405"
python consumer_inventory.py
```

Payment

```bash id="kpf406"
python consumer_payment.py
```

Email

```bash id="kpf407"
python consumer_email.py
```

Analytics

```bash id="kpf408"
python consumer_analytics.py
```

DLQ

```bash id="kpf409"
python consumer_dlq.py
```

______________________________________________________________________

# Create an Order

Request

```http id="kpf410"
POST /orders
```

```json id="kpf411"
{
    "customer_id": 25,
    "product_name": "Laptop",
    "quantity": 1,
    "price": 85000
}
```

______________________________________________________________________

# What Happens Internally?

Step 1

```text id="kpf412"
Client

↓

FastAPI
```

______________________________________________________________________

Step 2

```text id="kpf413"
Validate Request
```

Pydantic validates the request body.

______________________________________________________________________

Step 3

```text id="kpf414"
Create SQLModel Object
```

______________________________________________________________________

Step 4

```text id="kpf415"
Insert into PostgreSQL
```

______________________________________________________________________

Step 5

```text id="kpf416"
Commit Transaction
```

______________________________________________________________________

Step 6

```text id="kpf417"
Publish

OrderCreated
```

______________________________________________________________________

Step 7

```text id="kpf418"
Kafka

↓

orders.created
```

______________________________________________________________________

Step 8

Inventory receives

```text id="kpf419"
Reserve Stock
```

______________________________________________________________________

Step 9

Payment receives

```text id="kpf420"
Charge Customer
```

______________________________________________________________________

Step 10

Email receives

```text id="kpf421"
Send Confirmation
```

______________________________________________________________________

Step 11

Analytics receives

```text id="kpf422"
Record Revenue
```

One request

↓

Four independent actions

______________________________________________________________________

# Simulating Failure

Suppose Payment throws an exception.

Flow

```text id="kpf423"
Payment

↓

Retry

↓

Retry

↓

Retry

↓

DLQ
```

Other consumers continue working normally.

Inventory

↓

Success

Email

↓

Success

Analytics

↓

Success

Kafka isolates failures effectively.

______________________________________________________________________

# Replay Messages

Analytics crashes.

Inventory

↓

Works

Payment

↓

Works

Email

↓

Works

Analytics

↓

Restart

↓

Resume From Offset

````

Kafka's retained log allows consumers to continue from their last committed offset.

---

# Why Is This Better Than REST?

Without Kafka

```text id="kpf424"
Order Service

↓

Inventory

↓

Payment

↓

Email
````

If Payment is unavailable,

the request may fail.

With Kafka

```text id="kpf425"
Order Service

↓

Kafka

↓

Consumers
```

Services are decoupled.

Consumers process events independently.

______________________________________________________________________

# What We Didn't Build (Yet)

To keep the project focused on Kafka, we intentionally omitted some production patterns.

Examples:

- Transactional Outbox
- Schema Registry
- Avro / Protobuf
- Docker Compose
- Metrics
- Prometheus
- Grafana
- OpenTelemetry
- Distributed Tracing
- Kubernetes
- Authentication
- Authorization
- CI/CD

These will be covered later in the roadmap.

______________________________________________________________________

# How This Project Will Evolve

Later,

after we complete the Microservices section,

this project becomes

```text id="kpf426"
E-Commerce Platform

↓

API Gateway

↓

Order Service

↓

Inventory Service

↓

Payment Service

↓

Notification Service

↓

Kafka

↓

Redis

↓

Docker

↓

Kubernetes
```

Nothing learned here is wasted.

We'll expand it into a real production system.

______________________________________________________________________

# Production Improvements

If this application were deployed to production,

consider the following improvements.

### Configuration

Move every configuration value into environment variables.

______________________________________________________________________

### Logging

Use structured JSON logs.

______________________________________________________________________

### Metrics

Track:

- Consumer Lag
- Retry Count
- Processing Time
- DLQ Count

______________________________________________________________________

### Monitoring

Use Prometheus

↓

Grafana

______________________________________________________________________

### Schema Management

Use Schema Registry.

______________________________________________________________________

### Serialization

Prefer Avro or Protobuf for strongly typed contracts.

______________________________________________________________________

### Reliability

Implement the Transactional Outbox Pattern.

______________________________________________________________________

### Testing

Add

- Unit Tests
- Integration Tests
- End-to-End Tests

______________________________________________________________________

# Common Interview Questions

## Why Kafka?

Answer

Decoupling,

Scalability,

Fault Tolerance,

Replay,

Independent Consumers.

______________________________________________________________________

## Why Multiple Consumer Groups?

Each business capability processes the same event independently.

______________________________________________________________________

## Why Manual Commit?

Avoid losing messages.

______________________________________________________________________

## Why DLQ?

Prevent one bad message from blocking the system.

______________________________________________________________________

## Why Idempotent Consumers?

Kafka provides at-least-once delivery.

Duplicate messages are possible.

______________________________________________________________________

## Why Business Events?

Avoid coupling consumers to database schemas.

______________________________________________________________________

## Why Use order_id as Key?

Maintain event ordering for the same order within a partition.

______________________________________________________________________

# Mini Interview

## Question

How would you improve this project for production?

### Answer

I would:

- Add Docker Compose.
- Use multiple Kafka brokers.
- Enable replication.
- Add Schema Registry.
- Use Avro or Protobuf.
- Implement the Transactional Outbox Pattern.
- Add metrics, tracing, and structured logging.
- Add authentication and authorization.
- Introduce CI/CD.
- Deploy with Kubernetes.

______________________________________________________________________

# Final Revision

You should now understand:

✓ Producers

✓ Consumers

✓ Topics

✓ Partitions

✓ Offsets

✓ Consumer Groups

✓ Replication

✓ Retry

✓ Exponential Backoff

✓ Dead Letter Queue

✓ Idempotent Consumers

✓ Structured Logging

✓ FastAPI Integration

✓ SQLModel Integration

✓ PostgreSQL

✓ Event-Driven Architecture

______________________________________________________________________

# Suggested Extensions

Try implementing these features yourself.

1. Order cancellation events.
1. Inventory rollback.
1. Payment failure events.
1. Shipping service.
1. Discount service.
1. Coupon validation.
1. Fraud detection consumer.
1. SMS notifications.
1. Push notifications.
1. Audit logging.

These exercises reinforce the event-driven mindset.

______________________________________________________________________

# Course Review Questions

1. Why is Kafka different from RabbitMQ?
1. What is a Topic?
1. What is a Partition?
1. Why use message keys?
1. What is an Offset?
1. Why are Consumer Groups important?
1. What is Consumer Lag?
1. What is a DLQ?
1. Why use retries?
1. Why should consumers be idempotent?
1. Why publish business events instead of ORM objects?
1. Why commit offsets after processing?
1. Why use different consumer groups for different services?
1. Why is Kafka good for event-driven systems?
1. How would you scale this application?

______________________________________________________________________

# Final Project Summary

This project demonstrated:

- REST API development with FastAPI.
- Data persistence using SQLModel and PostgreSQL.
- Publishing business events to Kafka.
- Building multiple independent consumers.
- Manual offset management.
- Retry handling.
- Dead Letter Queue processing.
- Idempotent consumer design.
- Structured logging.
- Health checks.
- Event-driven architecture fundamentals.

Although intentionally simple, this project mirrors many patterns used in production systems and provides a strong foundation for the larger microservices project that will combine Kafka with Redis, Docker, Kubernetes, observability, and other production technologies.

______________________________________________________________________

# What's Next?

The next technology in the roadmap should be **Docker**.

You'll learn how to containerize:

- FastAPI
- PostgreSQL
- Kafka applications
- Redis applications

Later, we'll use Docker Compose to run multiple services together before moving to Kubernetes.

______________________________________________________________________

## Next File

[1-docker-fundamentals.md](../docker/1-docker-fundamentals.md)
