# Kafka Order Processing Project - Part 3

## Introduction

In Part 2, every consumer successfully processed the `orders.created` event.

But real systems fail.

Examples:

- Database unavailable
- Payment gateway timeout
- Inventory service crash
- Invalid message
- Network failure
- Third-party API unavailable

A production system should **never crash because of one bad message**.

In this chapter, we'll improve our project by adding:

- Retry mechanism
- Exponential Backoff
- Dead Letter Queue (DLQ)
- Idempotent Consumers
- Structured Logging
- Health Check Endpoint

These patterns are used in real production systems.

______________________________________________________________________

# Current Architecture

```text id="kpp301"
                FastAPI

                    │

                    ▼

             orders.created

                    │

        ┌───────────┼─────────────┐

        ▼           ▼             ▼

 Inventory      Payment      Email

                    │

                    ▼

             Business Logic
```

Now let's make it fault tolerant.

______________________________________________________________________

# What Happens When Processing Fails?

Suppose

```text id="kpp302"
Order Created

↓

Payment Consumer

↓

Payment Gateway

↓

Timeout
```

Should we lose the message?

No.

Should we commit the offset?

No.

Instead,

retry.

______________________________________________________________________

# Retry Strategy

Simple retry

```text id="kpp303"
Attempt 1

↓

Failed

↓

Attempt 2

↓

Failed

↓

Attempt 3

↓

Success
```

______________________________________________________________________

# Retry Helper

Create

**retry.py**

```python id="kpp304"
import time


def retry(

    operation,

    retries=3,

    delay=2

):

    for attempt in range(retries):

        try:

            return operation()

        except Exception:

            if attempt == retries - 1:

                raise

            time.sleep(delay)
```

Now every consumer can reuse this function.

______________________________________________________________________

# Using Retry

Example

```python id="kpp305"
def process_payment():

    print(

        "Calling Payment API"

    )


retry(

    process_payment

)
```

If the function raises an exception,

it will automatically retry.

______________________________________________________________________

# Exponential Backoff

Instead of waiting

```text id="kpp306"
2

2

2
```

Use

```text id="kpp307"
1

↓

2

↓

4

↓

8
```

This reduces pressure on overloaded systems.

______________________________________________________________________

# Improved Retry Helper

```python id="kpp308"
import time


def retry(

    operation,

    retries=5

):

    delay = 1

    for attempt in range(retries):

        try:

            return operation()

        except Exception:

            if attempt == retries - 1:

                raise

            time.sleep(delay)

            delay *= 2
```

______________________________________________________________________

# Dead Letter Queue (DLQ)

Suppose

```text id="kpp309"
Retry

↓

Retry

↓

Retry

↓

Still Failed
```

Don't retry forever.

Publish the message to another Kafka topic.

Example

```text id="kpp310"
orders.created

↓

Payment Consumer

↓

orders.dlq
```

______________________________________________________________________

# Why a DLQ?

Without DLQ

```text id="kpp311"
Bad Message

↓

Consumer Stops

↓

Everything Stops
```

With DLQ

```text id="kpp312"
Bad Message

↓

DLQ

↓

Continue Processing
```

Only the problematic message is isolated.

______________________________________________________________________

# Publishing to the DLQ

Add a helper to the producer.

```python id="kpp313"
def publish_dlq(

    event,

    reason

):

    producer.produce(

        topic="orders.dlq",

        key=str(

            event["order_id"]

        ),

        value=json.dumps(

            {

                "reason": reason,

                "event": event

            }

        )

    )

    producer.flush()
```

______________________________________________________________________

# Payment Consumer with DLQ

```python id="kpp314"
try:

    retry(

        process_payment

    )

    consumer.commit(

        message=message

    )

except Exception:

    publish_dlq(

        event,

        "Payment Failed"

    )
```

Notice

Offset is **not committed** until processing succeeds.

______________________________________________________________________

# Dead Letter Consumer

Create

**consumer_dlq.py**

```python id="kpp315"
consumer = create_consumer(

    "dlq-group"

)

consumer.subscribe(

    [

        "orders.dlq"

    ]

)

while True:

    message = consumer.poll(1)

    if message is None:

        continue

    print(

        message.value().decode()

    )

    consumer.commit(

        message=message

    )
```

Operations teams can inspect these failed events later.

______________________________________________________________________

# Idempotent Consumer

Kafka provides **At-Least-Once Delivery** by default.

A message may be delivered more than once.

Your business logic should safely handle duplicates.

______________________________________________________________________

# Simple Strategy

Keep a record of processed event IDs.

Example

```python id="kpp316"
processed_events = set()
```

Before processing

```python id="kpp317"
event_id = event["event_id"]

if event_id in processed_events:

    consumer.commit(

        message=message

    )

    return
```

Process

```python id="kpp318"
process_payment()
```

Mark

```python id="kpp319"
processed_events.add(

    event_id

)
```

> **Note:** Using an in-memory `set` is suitable only for learning. In production, store processed event IDs in a durable store (for example, PostgreSQL, Redis, or another persistent mechanism) so duplicate detection survives process restarts.

______________________________________________________________________

# Structured Logging

Instead of

```python id="kpp320"
print(

    event

)
```

Use

```python id="kpp321"
import logging

logger = logging.getLogger(

    "payment"

)

logger.info(

    "Payment Started",

    extra={

        "order_id":

        event["order_id"]

    }

)
```

Structured logs are easier to search and analyze.

______________________________________________________________________

# Error Logging

```python id="kpp322"
logger.exception(

    "Payment Failed"

)
```

Always include context:

- Order ID
- Customer ID
- Topic
- Partition
- Offset

______________________________________________________________________

# Health Check

Add to FastAPI.

```python id="kpp323"
@app.get("/health")

def health():

    return {

        "status": "healthy"

    }
```

In production,

health endpoints often verify:

- PostgreSQL
- Kafka
- Redis

______________________________________________________________________

# Complete Processing Flow

```text id="kpp324"
Order Created

↓

Kafka

↓

Payment Consumer

↓

Retry

↓

Success?

├── Yes

│      ↓

│   Commit Offset

│

└── No

       ↓

 Publish DLQ

       ↓

 Commit Offset
```

After moving an unrecoverable message to the DLQ, we commit the original message's offset so the consumer can continue
processing new messages.

______________________________________________________________________

# Why Commit After Sending to DLQ?

Suppose

```text id="kpp325"
DLQ Published

↓

Crash
```

If we never commit,

the same bad message keeps returning.

Publishing to the DLQ records the failure.

Now the consumer can safely continue.

______________________________________________________________________

# Monitoring

Useful metrics

- Consumer Lag
- Retry Count
- DLQ Count
- Success Count
- Failed Payments
- Processing Time

These metrics help identify bottlenecks and failures before they affect users.

______________________________________________________________________

# Production Architecture

```text id="kpp326"
FastAPI

↓

Kafka

↓

Payment Consumer

↓

Retry

↓

DLQ

↓

DLQ Consumer

↓

Operations Dashboard
```

______________________________________________________________________

# Common Mistakes

### Infinite Retry

A permanently bad message blocks the consumer.

______________________________________________________________________

### No DLQ

Difficult to investigate failures later.

______________________________________________________________________

### Committing Before Processing

Can lose messages.

______________________________________________________________________

### Ignoring Duplicate Delivery

Always assume duplicates are possible.

______________________________________________________________________

### Using print()

Use structured logging.

______________________________________________________________________

# Best Practices

- Retry transient failures.
- Use exponential backoff.
- Move unrecoverable messages to a DLQ.
- Make consumers idempotent.
- Log useful context.
- Monitor retry and DLQ metrics.
- Commit offsets after successful processing or after successfully publishing to the DLQ.

______________________________________________________________________

# Hands-on Exercise

Improve the project.

Requirements

1. Add retry with exponential backoff.
1. Create the `orders.dlq` topic.
1. Publish failed messages to the DLQ.
1. Create a DLQ consumer.
1. Add structured logging.
1. Add health endpoints.
1. Track processed event IDs.
1. Measure processing time.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should failed Kafka messages be moved to a Dead Letter Queue instead of being retried forever?

Some failures are temporary and can be resolved through retries, but others are permanent, such as invalid data or
unsupported event formats. Retrying these messages indefinitely blocks the consumer from processing new events. A Dead
Letter Queue isolates problematic messages for later investigation while allowing normal processing to continue,
improving system reliability and operational visibility.

______________________________________________________________________

# Summary

In this chapter, you upgraded the project with:

- Retry handling
- Exponential backoff
- Dead Letter Queue
- DLQ consumer
- Idempotent consumer pattern
- Structured logging
- Health checks
- Monitoring considerations
- Production best practices

Your Kafka application is now significantly closer to a production-ready event-driven system.

______________________________________________________________________

## Next File

[7-kafka-order-processing-project-part-4.md](7-kafka-order-processing-project-part-4.md)
