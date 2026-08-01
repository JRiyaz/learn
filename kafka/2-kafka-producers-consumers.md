# Kafka Producers & Consumers

## Introduction

In the previous chapter, you learned the basic Kafka architecture.

```text id="kp001"
Producer

↓

Topic

↓

Broker

↓

Consumer
```

In this chapter, we'll study the two most important Kafka components:

- Producers
- Consumers

We'll also learn:

- Producer Internals
- Consumer Internals
- Message Keys
- Serialization
- Delivery Guarantees
- Acknowledgements (ACKs)
- Offsets (Introduction)
- Error Handling
- Python (`confluent-kafka`)
- FastAPI Integration
- Production Best Practices

______________________________________________________________________

# Producer

A Producer publishes events to Kafka.

Example

```text id="kp002"
Order Service

↓

Kafka
```

Example event

```json id="kp003"
{
    "order_id": 101,
    "user_id": 42,
    "amount": 500
}
```

______________________________________________________________________

# Producer Workflow

```text id="kp004"
Application

↓

Serialize Event

↓

Kafka Producer

↓

Broker

↓

Topic
```

______________________________________________________________________

# Creating a Producer

Install

```bash id="kp005"
pip install confluent-kafka
```

Python

```python id="kp006"
from confluent_kafka import Producer

producer = Producer(
    {
        "bootstrap.servers": "localhost:9092"
    }
)
```

______________________________________________________________________

# Sending Messages

```python id="kp007"
producer.produce(

    topic="orders",

    value='{"order_id":101}'

)

producer.flush()
```

______________________________________________________________________

# Why flush()?

Kafka sends messages asynchronously.

```python id="kp008"
producer.flush()
```

waits until all queued messages have been delivered before the application exits.

Without it,

messages may remain in memory.

______________________________________________________________________

# Message Keys

A message can contain:

```text id="kp009"
Key

+

Value
```

Example

```python id="kp010"
producer.produce(

    topic="orders",

    key="customer-25",

    value='{"order_id":101}'

)
```

______________________________________________________________________

# Why Use Keys?

Messages with the same key go to the same partition.

Benefits:

- Ordering
- Consistency
- Customer affinity

Interview Tip

Keys become extremely important when partitions are introduced.

______________________________________________________________________

# Serializing JSON

Instead of plain strings,

use JSON.

```python id="kp011"
import json

order = {

    "order_id":101,

    "amount":500

}

producer.produce(

    "orders",

    value=json.dumps(order)

)

producer.flush()
```

______________________________________________________________________

# Delivery Callback

Kafka can notify you when a message has been delivered.

```python id="kp012"
def delivery_report(err, msg):

    if err:

        print(err)

    else:

        print(

            msg.topic(),

            msg.partition(),

            msg.offset()

        )
```

Usage

```python id="kp013"
producer.produce(

    "orders",

    value="hello",

    on_delivery=delivery_report

)

producer.flush()
```

______________________________________________________________________

# Producer ACKs

Producer reliability depends on acknowledgements.

```text id="kp014"
Producer

↓

Broker

↓

ACK
```

______________________________________________________________________

# ACK = 0

```text id="kp015"
Producer

↓

Send

↓

Done
```

No confirmation.

Fastest.

Least reliable.

______________________________________________________________________

# ACK = 1

Leader broker confirms the write.

Good balance between speed and durability.

______________________________________________________________________

# ACK = all

Leader waits for all required replicas to acknowledge the write before responding.

Highest durability.

Higher latency.

______________________________________________________________________

# Producer Configuration

```python id="kp016"
Producer(

{

"bootstrap.servers":"localhost:9092",

"acks":"all"

}

)
```

______________________________________________________________________

# Producer Retries

Temporary failures happen.

Enable retries.

```python id="kp017"
Producer(

{

"bootstrap.servers":"localhost:9092",

"retries":5

}

)
```

______________________________________________________________________

# Consumer

Consumers read events.

```text id="kp018"
Kafka

↓

Consumer
```

______________________________________________________________________

# Creating Consumer

```python id="kp019"
from confluent_kafka import Consumer

consumer = Consumer(

{

"bootstrap.servers":"localhost:9092",

"group.id":"inventory",

"auto.offset.reset":"earliest"

}

)
```

______________________________________________________________________

# Subscribe

```python id="kp020"
consumer.subscribe(

["orders"]

)
```

______________________________________________________________________

# Reading Messages

```python id="kp021"
while True:

    message = consumer.poll(1.0)

    if message is None:

        continue

    if message.error():

        print(message.error())

        continue

    print(

        message.value().decode()

    )
```

______________________________________________________________________

# Message Structure

Each Kafka message contains

```text id="kp022"
Topic

Partition

Offset

Key

Value

Timestamp
```

______________________________________________________________________

# Reading Keys

```python id="kp023"
print(

message.key()

)
```

______________________________________________________________________

# Reading JSON

```python id="kp024"
import json

order = json.loads(

message.value()

)
```

______________________________________________________________________

# Consumer Workflow

```text id="kp025"
Topic

↓

Read Event

↓

Deserialize

↓

Business Logic

↓

Next Event
```

______________________________________________________________________

# Error Handling

Example

```python id="kp026"
if message.error():

    print(

        message.error()

    )

    continue
```

Never assume every poll returns a valid message.

______________________________________________________________________

# Auto Offset Reset

Configuration

```python id="kp027"
"auto.offset.reset":"earliest"
```

Options

### earliest

Read from beginning.

### latest

Read only new messages.

______________________________________________________________________

# FastAPI Producer Example

```python id="kp028"
from fastapi import FastAPI
from confluent_kafka import Producer
import json

app = FastAPI()

producer = Producer(
    {
        "bootstrap.servers":"localhost:9092"
    }
)

@app.post("/orders")

def create_order(order: dict):

    producer.produce(

        "orders",

        value=json.dumps(order)

    )

    producer.flush()

    return {

        "status":"published"

    }
```

______________________________________________________________________

# Inventory Consumer

```python id="kp029"
while True:

    message = consumer.poll(1)

    if message is None:

        continue

    order = json.loads(

        message.value()

    )

    print(

        "Reserve Inventory",

        order

    )
```

______________________________________________________________________

# Email Consumer

Same topic.

Different service.

```text id="kp030"
Orders Topic

↓

Inventory Service

↓

Email Service

↓

Analytics Service
```

One event.

Many consumers.

______________________________________________________________________

# Real Production Flow

```text id="kp031"
Client

↓

FastAPI

↓

Kafka Producer

↓

Orders Topic

↓

Inventory Consumer

↓

Payment Consumer

↓

Email Consumer

↓

Analytics Consumer
```

Completely decoupled.

______________________________________________________________________

# Common Mistakes

### Forgetting flush()

Messages may never be sent before the process exits.

______________________________________________________________________

### Large Messages

Store files in object storage.

Publish references.

______________________________________________________________________

### Ignoring Delivery Errors

Always inspect delivery callbacks in production.

______________________________________________________________________

### Using Strings Everywhere

Prefer structured JSON or an agreed serialization format.

______________________________________________________________________

# Best Practices

- Use message keys when ordering matters.
- Enable retries.
- Use `acks=all` for critical data.
- Handle delivery failures.
- Keep messages reasonably small.
- Validate message payloads.
- Treat messages as immutable events.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should you use a message key?

A Kafka message key determines the partition to which the message is written. Messages with the same key are
consistently routed to the same partition, preserving their relative order. This is especially important for entities
such as users, orders, or accounts, where events must be processed sequentially.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a Producer?
1. What is a Consumer?
1. Why use message keys?
1. What is serialization?
1. Why call `flush()`?
1. What are ACKs?
1. Difference between ACK=1 and ACK=all.
1. What is `auto.offset.reset`?
1. Why use JSON?
1. What information does a Kafka message contain?

## Coding

1. Create a Producer.
1. Publish a JSON message.
1. Add a delivery callback.
1. Configure retries.
1. Create a Consumer.
1. Subscribe to a topic.
1. Deserialize JSON.
1. Build a FastAPI producer endpoint.

______________________________________________________________________

# Hands-on Exercise

Build a basic Order Event Service.

Requirements:

1. Create an `orders` topic.
1. Build a FastAPI endpoint to publish order events.
1. Serialize events as JSON.
1. Create an inventory consumer.
1. Create an email consumer.
1. Configure `acks=all`.
1. Add retries.
1. Print delivery confirmations.

______________________________________________________________________

# Cheat Sheet

```text id="kp032"
Producer

↓

produce()

↓

Key

↓

Value

↓

ACK

↓

flush()

↓

Consumer

↓

poll()

↓

Deserialize

↓

Business Logic
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Kafka Producer internals
- Kafka Consumer internals
- Message keys
- JSON serialization
- Delivery callbacks
- ACKs
- Retries
- Consumer polling
- Error handling
- FastAPI integration
- Production best practices
- Interview patterns

You now understand how events are produced and consumed in Kafka. In the next lecture, we'll explore **partitions,
offsets, replication, and consumer groups**, which are the core concepts behind Kafka's scalability.

______________________________________________________________________

## Next File

[3-kafka-partitions-replication-consumer-groups.md](3-kafka-partitions-replication-consumer-groups.md)
