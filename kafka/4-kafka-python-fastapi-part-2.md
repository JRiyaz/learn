# Kafka with Python & FastAPI - Part 2

## Introduction

In Part 1, we built a production-ready Kafka foundation:

- Project Structure
- Configuration
- Producer Wrapper
- Consumer Wrapper
- Pydantic Models
- Dependency Injection
- Serialization

In this chapter, we'll move to production-grade Kafka integration.

Topics covered:

- Background Consumers
- Graceful Shutdown
- Manual Offset Commit
- Error Handling
- Retry Strategy
- Dead Letter Queue (DLQ)
- Idempotent Consumers
- Logging
- Health Checks
- Testing
- Production Architecture

These are the concepts that differentiate a simple Kafka demo from a production system.

______________________________________________________________________

# Running Consumers

A consumer is **not** normally started inside an API endpoint.

Wrong

```text id="kfp201"
Client

↓

API

↓

Start Consumer
```

A consumer should be a long-running process.

Correct

```text id="kfp202"
Kafka

↓

Consumer Service

↓

Business Logic
```

______________________________________________________________________

# Consumer Service

Example

```python id="kfp203"
consumer = KafkaConsumer(
    group="inventory-service"
)

consumer.consumer.subscribe(
    ["orders"]
)

while True:

    message = consumer.consumer.poll(1.0)

    if message is None:
        continue

    process_order(message)
```

This process runs continuously.

______________________________________________________________________

# Business Logic Separation

Avoid

```python id="kfp204"
while True:

    ...

    update_inventory()

    send_email()

    process_payment()
```

Instead

```text id="kfp205"
Consumer

↓

Order Service

↓

Inventory Service
```

The consumer should receive the event and delegate processing.

______________________________________________________________________

# Manual Offset Commit

Disable automatic commits.

```python id="kfp206"
Consumer(
    {
        "enable.auto.commit": False
    }
)
```

After successful processing

```python id="kfp207"
consumer.consumer.commit(
    message=message
)
```

This prevents acknowledging messages before business logic completes.

______________________________________________________________________

# Why Manual Commit?

Bad sequence

```text id="kfp208"
Commit Offset

↓

Crash

↓

Message Lost
```

Correct

```text id="kfp209"
Process Message

↓

Database Commit

↓

Commit Kafka Offset
```

This minimizes the chance of losing messages.

______________________________________________________________________

# Error Handling

Example

```python id="kfp210"
try:

    process_order(message)

    consumer.consumer.commit(
        message=message
    )

except Exception as exc:

    logger.exception(exc)
```

Do **not** commit offsets for failed messages.

______________________________________________________________________

# Retry Strategy

Some failures are temporary.

Example:

- Database unavailable
- Network timeout
- External API unavailable

Simple retry

```python id="kfp211"
import time

MAX_RETRIES = 3

for attempt in range(MAX_RETRIES):

    try:

        process_order(message)

        break

    except Exception:

        time.sleep(2)
```

Production systems often use exponential backoff instead of a fixed delay.

______________________________________________________________________

# Exponential Backoff

Instead of

```text id="kfp212"
2

2

2
```

Use

```text id="kfp213"
1

2

4

8
```

This reduces pressure on failing services.

______________________________________________________________________

# Dead Letter Queue (DLQ)

Some messages cannot be processed successfully.

Instead of blocking the consumer forever,

send them to another topic.

```text id="kfp214"
Orders Topic

↓

Consumer

↓

Failure

↓

orders-dlq
```

______________________________________________________________________

# Publishing to DLQ

```python id="kfp215"
producer.publish(

    topic="orders-dlq",

    key=message.key(),

    message={

        "payload":

        message.value().decode(),

        "reason":

        "Processing Failed"

    }

)
```

Operations teams can inspect the DLQ later.

______________________________________________________________________

# Why Use a DLQ?

Without DLQ

```text id="kfp216"
Bad Message

↓

Infinite Retry

↓

Consumer Stops
```

With DLQ

```text id="kfp217"
Bad Message

↓

DLQ

↓

Continue Processing
```

______________________________________________________________________

# Idempotent Consumers

A Kafka message may be delivered more than once.

Your business logic should safely handle duplicates.

Example

```text id="kfp218"
Order

101

Processed

↓

Duplicate

↓

Ignore
```

______________________________________________________________________

# Example Strategy

Suppose the database stores processed event IDs.

```python id="kfp219"
if already_processed(
    event_id
):
    return
```

Otherwise

```python id="kfp220"
process()

mark_processed(
    event_id
)
```

This ensures repeated deliveries do not create duplicate business operations.

______________________________________________________________________

# Idempotent Producer

Kafka also supports idempotent producers.

Configuration

```python id="kfp221"
Producer(
    {
        "bootstrap.servers": "localhost:9092",
        "enable.idempotence": True
    }
)
```

Benefits

- Prevents duplicate records caused by producer retries.
- Improves delivery guarantees.

______________________________________________________________________

# Health Check Endpoint

FastAPI

```python id="kfp222"
@app.get("/health")

def health():

    return {

        "status": "healthy"

    }
```

In production,

health endpoints may also verify connectivity to Kafka, databases, and other dependencies.

______________________________________________________________________

# Logging

Use structured logging.

Example

```python id="kfp223"
logger.info(

    "Order Received",

    extra={

        "order_id":101,

        "customer":42

    }

)
```

Avoid logging only plain text when richer context is available.

______________________________________________________________________

# Graceful Shutdown

Suppose

Application receives

```text id="kfp224"
SIGTERM
```

Don't terminate immediately.

Instead

```python id="kfp225"
try:

    while True:

        ...

finally:

    consumer.consumer.close()
```

Closing the consumer leaves the consumer group cleanly and releases resources.

______________________________________________________________________

# Producer Flush on Shutdown

Always flush outstanding messages.

```python id="kfp226"
producer.producer.flush()
```

before application exit.

______________________________________________________________________

# Testing Producers

Instead of testing Kafka itself,

test your application logic.

Example

```python id="kfp227"
mock_producer.publish(
    ...
)
```

Verify

- Topic
- Key
- Payload

______________________________________________________________________

# Testing Consumers

Mock

```text id="kfp228"
Kafka Message
```

Verify

```text id="kfp229"
Business Logic
```

was executed correctly.

______________________________________________________________________

# Production Folder Structure

```text id="kfp230"
order_service/

├── api/

├── kafka/

│      producer.py

│      consumer.py

│      serializer.py

│      config.py

├── services/

├── repositories/

├── schemas/

├── models/

├── workers/

└── main.py
```

Background workers are separated from API endpoints.

______________________________________________________________________

# Production Architecture

```text id="kfp231"
                Client
                   │
                   ▼
             FastAPI API
                   │
            Kafka Producer
                   │
             Orders Topic
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
Inventory     Payment      Notification
 Consumer      Consumer       Consumer
     │             │             │
 PostgreSQL    Payment API     Email API
```

Each service owns its business logic independently.

______________________________________________________________________

# Common Mistakes

### Automatic Offset Commit

Messages may be acknowledged before processing succeeds.

______________________________________________________________________

### No Retry Strategy

Temporary failures become permanent failures.

______________________________________________________________________

### Infinite Retry

A single bad message blocks the entire consumer.

Use a DLQ.

______________________________________________________________________

### Ignoring Duplicate Messages

Consumers should be idempotent.

______________________________________________________________________

### Mixing API and Consumer Logic

Keep API servers and background consumers as separate processes.

______________________________________________________________________

# Best Practices

- Use manual offset commits.
- Process first, commit later.
- Implement retries with exponential backoff.
- Send unrecoverable messages to a DLQ.
- Design consumers to be idempotent.
- Use structured logging.
- Gracefully shut down consumers.
- Flush producers before exit.
- Separate API servers from worker processes.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should Kafka consumers be idempotent?

Kafka provides at-least-once delivery by default. This means a consumer may receive the same message multiple times,
especially after failures or retries. If processing is not idempotent, duplicate deliveries can result in repeated
business operations such as charging a customer twice or creating duplicate orders. Designing consumers to recognize and
safely ignore duplicates ensures correct application behavior.

______________________________________________________________________

# Practice Questions

## Conceptual

1. Why use manual offset commits?
1. What is a Dead Letter Queue?
1. Why use retries?
1. What is exponential backoff?
1. What is an idempotent consumer?
1. What is an idempotent producer?
1. Why separate consumers from API servers?
1. Why flush producers before shutdown?
1. How should Kafka applications be tested?
1. Why are health checks important?

## Coding

1. Disable automatic offset commits.
1. Commit offsets manually.
1. Implement retry logic.
1. Publish failed messages to a DLQ.
1. Enable idempotent producer mode.
1. Build a graceful shutdown handler.
1. Mock a producer in unit tests.
1. Create a FastAPI health endpoint.

______________________________________________________________________

# Hands-on Exercise

Upgrade the Order Service.

Requirements:

1. Disable automatic offset commits.
1. Commit offsets after successful processing.
1. Add retry logic with exponential backoff.
1. Publish failed messages to `orders-dlq`.
1. Prevent duplicate order processing.
1. Add structured logging.
1. Implement graceful shutdown.
1. Add health check endpoints.
1. Write unit tests using mocked Kafka components.

______________________________________________________________________

# Cheat Sheet

```text id="kfp232"
Producer

↓

FastAPI

↓

Orders Topic

↓

Consumer

↓

Retry

↓

DLQ

↓

Manual Commit

↓

Idempotency

↓

Graceful Shutdown
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Background consumer architecture
- Manual offset commits
- Retry strategies
- Exponential backoff
- Dead Letter Queues
- Idempotent producers
- Idempotent consumers
- Graceful shutdown
- Structured logging
- Health checks
- Testing strategies
- Production architecture
- Interview patterns

You now have the knowledge to build production-ready Kafka applications using Python and FastAPI. The next lecture
focuses on **Kafka production deployment, performance tuning, monitoring, exactly-once semantics, and operational best
practices**, preparing you for real-world backend systems.

______________________________________________________________________

## Next File

[5-kafka-production-performance.md](5-kafka-production-performance.md)
