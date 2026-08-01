# Kafka Order Processing Project - Part 2

## Introduction

In Part 1, we built the producer side of our application.

Workflow so far:

```text id="kopp201"
Client

↓

FastAPI

↓

PostgreSQL

↓

Kafka Producer

↓

orders.created
```

Now we'll build the consumers.

Instead of one consumer doing everything, we'll create **multiple independent consumers**, just like a real event-driven
system.

Each consumer has **one responsibility**.

______________________________________________________________________

# Consumer Architecture

```text id="kopp202"
                orders.created
                      │
      ┌───────────────┼───────────────┬───────────────┐
      ▼               ▼               ▼               ▼
Inventory        Payment        Email         Analytics
 Consumer         Consumer      Consumer       Consumer
```

Notice:

Every service receives the same event.

None of them communicate with each other.

They only communicate through Kafka.

______________________________________________________________________

# Why Multiple Consumers?

Imagine adding a new service next month.

For example:

```text id="kopp203"
Fraud Detection
```

Do we modify the Order Service?

**No.**

We simply create another Kafka consumer.

This is the biggest advantage of Event-Driven Architecture.

______________________________________________________________________

# Suggested Project Structure

```text id="kopp204"
order_processing/

producer.py

consumer_inventory.py

consumer_payment.py

consumer_email.py

consumer_analytics.py
```

Although we're showing separate files, remember that **all code is contained in this Markdown document**.

______________________________________________________________________

# Common Kafka Consumer Helper

All consumers share similar configuration.

Instead of repeating code,

create a helper.

**consumer_base.py**

```python id="kopp205"
from confluent_kafka import Consumer


def create_consumer(group_id: str):

    consumer = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False
        }
    )

    consumer.subscribe(
        ["orders.created"]
    )

    return consumer
```

Every consumer will reuse this helper.

______________________________________________________________________

# Why Different Consumer Groups?

Inventory

```text id="kopp206"
Group

inventory-group
```

Payment

```text id="kopp207"
payment-group
```

Email

```text id="kopp208"
email-group
```

Analytics

```text id="kopp209"
analytics-group
```

Each service belongs to **its own consumer group**.

Therefore,

every service receives **every event**.

______________________________________________________________________

# Inventory Consumer

Purpose

Reserve stock.

**consumer_inventory.py**

```python id="kopp210"
import json

from consumer_base import create_consumer


consumer = create_consumer(
    "inventory-group"
)

while True:

    message = consumer.poll(1.0)

    if message is None:
        continue

    if message.error():
        print(message.error())
        continue

    event = json.loads(
        message.value().decode()
    )

    print(
        f"""
        Reserving inventory

        Order:

        {event["order_id"]}
        """
    )

    consumer.commit(
        message=message
    )
```

______________________________________________________________________

# Inventory Workflow

```text id="kopp211"
OrderCreated

↓

Inventory Consumer

↓

Reserve Stock

↓

Commit Offset
```

______________________________________________________________________

# Payment Consumer

Purpose

Charge the customer.

**consumer_payment.py**

```python id="kopp212"
import json

from consumer_base import create_consumer


consumer = create_consumer(
    "payment-group"
)

while True:

    message = consumer.poll(1)

    if message is None:
        continue

    if message.error():
        continue

    event = json.loads(
        message.value().decode()
    )

    print(

        f"""
        Charging customer

        {event["customer_id"]}
        """

    )

    consumer.commit(
        message=message
    )
```

______________________________________________________________________

# Payment Workflow

```text id="kopp213"
OrderCreated

↓

Payment Consumer

↓

Payment Gateway

↓

Commit Offset
```

In a real application,

this consumer would call a payment provider such as Stripe, Razorpay, or Adyen.

______________________________________________________________________

# Email Consumer

Purpose

Send confirmation email.

**consumer_email.py**

```python id="kopp214"
import json

from consumer_base import create_consumer


consumer = create_consumer(
    "email-group"
)

while True:

    message = consumer.poll(1)

    if message is None:
        continue

    if message.error():
        continue

    event = json.loads(
        message.value().decode()
    )

    print(

        f"""
        Sending email

        for order

        {event["order_id"]}
        """

    )

    consumer.commit(
        message=message
    )
```

______________________________________________________________________

# Analytics Consumer

Purpose

Collect business metrics.

**consumer_analytics.py**

```python id="kopp215"
import json

from consumer_base import create_consumer


consumer = create_consumer(
    "analytics-group"
)

while True:

    message = consumer.poll(1)

    if message is None:
        continue

    if message.error():
        continue

    event = json.loads(
        message.value().decode()
    )

    print(

        f"""
        Analytics

        Revenue

        {event["price"]}
        """

    )

    consumer.commit(
        message=message
    )
```

______________________________________________________________________

# Complete Event Flow

```text id="kopp216"
POST /orders

↓

Save PostgreSQL

↓

Publish OrderCreated

↓

Kafka

↓

Inventory Consumer

↓

Payment Consumer

↓

Email Consumer

↓

Analytics Consumer
```

One event.

Four independent services.

______________________________________________________________________

# Why Don't Consumers Call Each Other?

Bad

```text id="kopp217"
Inventory

↓

Payment

↓

Email
```

Tightly coupled.

Failure in one service affects others.

Good

```text id="kopp218"
Kafka

↓

Inventory

Kafka

↓

Payment

Kafka

↓

Email
```

Every service is independent.

______________________________________________________________________

# Event Replay

Suppose

Analytics service crashes.

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

Offline

When Analytics returns,

it can resume from its committed offset.

No producer changes are required.

______________________________________________________________________

# Consumer Groups Revisited

Inventory Group

```text id="kopp219"
Consumer A

Consumer B

Consumer C
```

Kafka distributes partitions among these consumers.

This allows Inventory to scale independently from Payment or Email.

______________________________________________________________________

# Why Manual Offset Commit?

Notice every consumer commits **after** processing.

```python id="kopp220"
consumer.commit(
    message=message
)
```

If the application crashes before this line,

Kafka can redeliver the message.

This provides **At-Least-Once Delivery**.

______________________________________________________________________

# Running the Project

Terminal 1

```bash id="kopp221"
uvicorn app:app --reload
```

Terminal 2

```bash id="kopp222"
python consumer_inventory.py
```

Terminal 3

```bash id="kopp223"
python consumer_payment.py
```

Terminal 4

```bash id="kopp224"
python consumer_email.py
```

Terminal 5

```bash id="kopp225"
python consumer_analytics.py
```

Now create an order using the API.

Every consumer should receive the event.

______________________________________________________________________

# Expected Output

Inventory

```text id="kopp226"
Reserving inventory

Order 101
```

Payment

```text id="kopp227"
Charging customer

42
```

Email

```text id="kopp228"
Sending email

for order 101
```

Analytics

```text id="kopp229"
Revenue

6999
```

______________________________________________________________________

# Common Mistakes

### Using One Consumer for Everything

Bad

```text id="kopp230"
Consumer

↓

Inventory

↓

Payment

↓

Email
```

Split responsibilities.

______________________________________________________________________

### Sharing Consumer Groups

Inventory and Payment should not belong to the same consumer group if both need to process every order event.

______________________________________________________________________

### Committing Before Processing

Always commit offsets **after** successful processing.

______________________________________________________________________

### Ignoring Consumer Errors

Handle malformed messages, external API failures, and database errors.

______________________________________________________________________

# Best Practices

- One responsibility per consumer.
- Different consumer groups for different business capabilities.
- Manual offset commits.
- Keep consumers stateless where possible.
- Deserialize once, then pass domain objects to business logic.
- Log failures with enough context for debugging.

______________________________________________________________________

# Hands-on Exercise

Extend the project.

Requirements

1. Add a Shipping Consumer.
1. Add an Audit Consumer.
1. Print the event timestamp.
1. Count processed orders in the Analytics consumer.
1. Add logging instead of `print()`.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should Inventory, Payment, and Email use different consumer groups instead of sharing one?

A consumer group is designed for parallel processing of the same workload. Within a single consumer group, each message
is processed by only one consumer. Inventory, Payment, and Email are different business capabilities, and each must
process every order event independently. Therefore, each service should belong to its own consumer group, allowing all
of them to receive the same event without interfering with one another.

______________________________________________________________________

# Summary

In this part, you built:

- Shared consumer configuration
- Inventory consumer
- Payment consumer
- Email consumer
- Analytics consumer
- Independent consumer groups
- Manual offset commits
- Complete event flow

In the next part, we'll make this project production-ready by adding:

- Retry handling
- Exponential backoff
- Dead Letter Queue (DLQ)
- Idempotent consumers
- Structured logging
- Health checks

______________________________________________________________________

## Next File

[7-kafka-order-processing-project-part-3.md](7-kafka-order-processing-project-part-3.md)
