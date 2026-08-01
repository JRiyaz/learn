# Redis Pub/Sub, Streams, Transactions & Pipelines

## Introduction

Redis is much more than a cache.

It also provides powerful messaging and event-processing capabilities.

In this chapter, you'll learn:

- Publish / Subscribe (Pub/Sub)
- Streams
- Consumer Groups
- Transactions
- WATCH
- Optimistic Locking
- Pipelines
- Lua Scripts
- Python (`redis-py`) examples
- FastAPI integration
- Production use cases
- Interview questions

This chapter covers many of the advanced Redis topics frequently discussed in backend interviews.

______________________________________________________________________

# Redis Messaging

Redis supports two major messaging models.

```text id="rps001"
Messaging

├── Pub/Sub

└── Streams
```

Although both involve sending messages, they behave very differently.

______________________________________________________________________

# Pub/Sub

Pub/Sub stands for

> **Publish / Subscribe**

One application publishes messages.

Multiple applications subscribe to receive them.

```text id="rps002"
Publisher

↓

Redis

↓

Subscriber A

Subscriber B

Subscriber C
```

______________________________________________________________________

# Characteristics

- Real-time
- No persistence
- Fire-and-forget
- Very low latency

If no subscriber is listening,

the message is lost.

Interview Tip

Pub/Sub is **not** a message queue.

______________________________________________________________________

# Publish Message

CLI

```bash id="rps003"
PUBLISH news "Redis 8 Released"
```

Python

```python id="rps004"
import redis

client = redis.Redis(
    decode_responses=True
)

client.publish(
    "news",
    "Redis 8 Released"
)
```

______________________________________________________________________

# Subscribe

CLI

```bash id="rps005"
SUBSCRIBE news
```

Python

```python id="rps006"
subscriber = client.pubsub()

subscriber.subscribe("news")

for message in subscriber.listen():

    print(message)
```

______________________________________________________________________

# Real Use Cases

- Chat applications
- Live dashboards
- Notifications
- WebSocket broadcasting
- Multiplayer games

______________________________________________________________________

# Pub/Sub Limitations

If subscribers disconnect

↓

Messages disappear.

No history.

No replay.

No acknowledgements.

For reliable messaging,

Redis Streams are preferred.

______________________________________________________________________

# Redis Streams

Streams were introduced to provide durable event streaming.

Unlike Pub/Sub,

messages are stored.

```text id="rps007"
Producer

↓

Redis Stream

↓

Consumer
```

______________________________________________________________________

# Add Message

CLI

```bash id="rps008"
XADD orders * \
user Alice \
amount 500
```

Python

```python id="rps009"
client.xadd(
    "orders",
    {
        "user": "Alice",
        "amount": 500
    }
)
```

Redis automatically generates a unique message ID.

______________________________________________________________________

# Read Messages

CLI

```bash id="rps010"
XRANGE orders - +
```

Python

```python id="rps011"
client.xrange(
    "orders"
)
```

Unlike Pub/Sub,

messages remain stored.

______________________________________________________________________

# Consumer Groups

Multiple workers can process one stream.

```text id="rps012"
Orders Stream

↓

Consumer Group

↓

Worker 1

Worker 2

Worker 3
```

Each message is delivered to one consumer within the group.

______________________________________________________________________

# Create Consumer Group

CLI

```bash id="rps013"
XGROUP CREATE \
orders \
workers \
$
```

Python

```python id="rps014"
client.xgroup_create(
    "orders",
    "workers",
    id="$",
    mkstream=True
)
```

______________________________________________________________________

# Read as Consumer

CLI

```bash id="rps015"
XREADGROUP \
GROUP workers worker1 \
STREAMS orders >
```

Python

```python id="rps016"
client.xreadgroup(
    groupname="workers",
    consumername="worker1",
    streams={
        "orders": ">"
    }
)
```

______________________________________________________________________

# Acknowledge Message

CLI

```bash id="rps017"
XACK orders workers \
1680000000-0
```

Python

```python id="rps018"
client.xack(
    "orders",
    "workers",
    "1680000000-0"
)
```

Acknowledgement tells Redis the message has been processed successfully.

______________________________________________________________________

# Pub/Sub vs Streams

| Pub/Sub | Streams |
| ------------------- | ------------------------- |
| No persistence | Persistent |
| Fire-and-forget | Durable |
| No acknowledgements | Supports acknowledgements |
| No replay | Replay supported |
| Broadcast | Event log |
| Live communication | Reliable messaging |

Interview Tip

If the interviewer asks:

> Which would you choose for an order-processing system?

The answer is almost always:

```text id="rps019"
Redis Streams
```

______________________________________________________________________

# Transactions

Redis transactions allow multiple commands to execute sequentially.

Commands

```text id="rps020"
MULTI

↓

Commands

↓

EXEC
```

______________________________________________________________________

# CLI Example

```bash id="rps021"
MULTI

SET name Alice

INCR visits

EXEC
```

______________________________________________________________________

# Python Example

```python id="rps022"
pipe = client.pipeline()

pipe.set(
    "name",
    "Alice"
)

pipe.incr(
    "visits"
)

pipe.execute()
```

The pipeline object can also execute commands as a Redis transaction when configured appropriately.

______________________________________________________________________

# Important Note

Redis transactions differ from SQL transactions.

Redis does **not** provide full ACID semantics comparable to relational databases.

Commands queued in a transaction are executed sequentially without interleaving, but Redis does not roll back already
executed commands if a later command fails.

______________________________________________________________________

# WATCH

WATCH implements optimistic locking.

Example

```bash id="rps023"
WATCH balance

MULTI

SET balance 500

EXEC
```

If another client changes `balance` before `EXEC`, the transaction is aborted.

______________________________________________________________________

# Python Example

```python id="rps024"
with client.pipeline() as pipe:

    while True:

        try:

            pipe.watch("balance")

            balance = int(
                pipe.get("balance")
            )

            pipe.multi()

            pipe.set(
                "balance",
                balance - 100
            )

            pipe.execute()

            break

        except redis.WatchError:

            continue
```

Useful for preventing lost updates.

______________________________________________________________________

# Pipelines

Normally

```text id="rps025"
Command

↓

Network

↓

Redis

↓

Response
```

Repeated thousands of times.

______________________________________________________________________

Pipeline

```text id="rps026"
Command

Command

Command

↓

One Network Round Trip

↓

Redis
```

Much faster.

______________________________________________________________________

# CLI

The Redis CLI doesn't have a direct pipeline command like `redis-py`; pipelining is primarily a client-side
optimization.

______________________________________________________________________

# Python

```python id="rps027"
pipe = client.pipeline()

for i in range(1000):

    pipe.set(
        f"user:{i}",
        i
    )

pipe.execute()
```

One network trip.

1000 commands.

______________________________________________________________________

# Lua Scripts

Sometimes multiple operations must execute atomically on the server.

Redis supports Lua scripting.

CLI

```bash id="rps028"
EVAL \
"return redis.call('GET','counter')" \
0
```

Python

```python id="rps029"
script = """

return redis.call(
'GET',
KEYS[1]
)

"""

client.eval(
    script,
    1,
    "counter"
)
```

Lua scripts execute atomically.

______________________________________________________________________

# FastAPI Example

```python id="rps030"
@app.post("/orders")

def create_order():

    client.xadd(

        "orders",

        {

            "user": "Alice",

            "amount": 500

        }

    )

    return {

        "status": "queued"

    }
```

A worker service can consume the stream asynchronously.

______________________________________________________________________

# Real Production Use Cases

Pub/Sub

- Live notifications
- Chat
- WebSockets
- Multiplayer games

Streams

- Order processing
- Email queues
- Payment events
- Audit logs

Pipelines

- Bulk writes
- Cache warm-up
- Batch updates

WATCH

- Inventory management
- Wallet balances
- Stock reservations

Lua

- Atomic business operations
- Distributed counters
- Rate limiting

______________________________________________________________________

# Common Mistakes

### Using Pub/Sub as a Queue

Messages disappear if subscribers are offline.

______________________________________________________________________

### Forgetting XACK

Pending messages accumulate and may be redelivered.

______________________________________________________________________

### Not Using Pipelines

Thousands of small network round trips hurt performance.

______________________________________________________________________

### Assuming Redis Transactions Behave Like SQL Transactions

Redis transactions have different guarantees.

______________________________________________________________________

### Overusing Lua

Use Lua only when atomic server-side logic is required.

______________________________________________________________________

# Best Practices

- Use Pub/Sub for live communication.
- Use Streams for reliable event processing.
- Use Consumer Groups for worker pools.
- Use Pipelines for bulk operations.
- Use WATCH for optimistic locking.
- Use Lua for complex atomic operations.
- Monitor pending stream messages.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** When would you choose Redis Streams instead of Pub/Sub?

I would choose Redis Streams when messages must be stored reliably and processed even if consumers are temporarily
offline. Streams support persistence, acknowledgements, replay, consumer groups, and pending message tracking, making
them suitable for order processing, background jobs, and event-driven architectures. Pub/Sub is better suited for
real-time broadcasts such as chat or notifications where losing a message is acceptable if no subscriber is connected.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is Pub/Sub?
1. What are Redis Streams?
1. Difference between Pub/Sub and Streams.
1. What is a Consumer Group?
1. Why acknowledge messages?
1. What is a Redis transaction?
1. What does WATCH do?
1. What is optimistic locking?
1. Why use pipelines?
1. Why use Lua scripts?

## Coding

1. Publish a message.
1. Subscribe to a channel.
1. Create a Redis Stream.
1. Create a Consumer Group.
1. Read messages from a stream.
1. Acknowledge processed messages.
1. Execute bulk writes using a pipeline.
1. Implement optimistic locking using WATCH.
1. Execute a Lua script.

______________________________________________________________________

# Hands-on Exercise

Build an Order Processing System.

Requirements:

1. Publish notifications using Pub/Sub.
1. Store orders in a Redis Stream.
1. Create a Consumer Group.
1. Process orders using multiple workers.
1. Acknowledge processed messages.
1. Batch updates using pipelines.
1. Protect inventory updates using WATCH.
1. Implement an atomic stock check using Lua.

______________________________________________________________________

# Cheat Sheet

```text id="rps031"
Pub/Sub

↓

Streams

↓

Consumer Groups

↓

MULTI

↓

EXEC

↓

WATCH

↓

Pipelines

↓

Lua Scripts
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Pub/Sub
- Streams
- Consumer Groups
- Message acknowledgements
- Transactions
- WATCH
- Optimistic locking
- Pipelines
- Lua scripting
- FastAPI integration
- Production use cases
- Best practices
- Interview patterns

You now understand Redis's messaging and atomic operation capabilities and how to choose the right feature for reliable,
high-performance backend systems.

______________________________________________________________________

## Next File

[5-redis-production-performance.md](5-redis-production-performance.md)
