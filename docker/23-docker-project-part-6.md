# Docker - Part 23

# Docker Project - Part 6

# Integrating Kafka Events

______________________________________________________________________

# Introduction

Our Library API now has:

- FastAPI
- PostgreSQL
- Redis Cache

Every request works correctly.

But one important capability is still missing.

When something important happens,

other applications don't know about it.

For example,

when a book is borrowed,

how would

- Notification Service
- Analytics Service
- Recommendation Service
- Audit Service

know about it?

They shouldn't query our API every second.

Instead,

our application should **publish an event**.

That's exactly what Kafka is for.

______________________________________________________________________

# Current Architecture

```text id="kproject001"
Browser

↓

FastAPI

│

├── PostgreSQL

└── Redis
```

Only our application knows

what happened.

______________________________________________________________________

# New Architecture

```text id="kproject002"
Browser

↓

FastAPI

│

├── PostgreSQL

├── Redis

└── Kafka

        │

        ▼

 Future Services
```

Every important action

produces an event.

______________________________________________________________________

# Event-Driven Flow

Suppose

someone borrows a book.

```text id="kproject003"
Borrow Book

↓

Update Database

↓

Publish Event

↓

Kafka Topic

↓

Consumers
```

Notice

the database

remains

the source of truth.

Kafka

broadcasts

what happened.

______________________________________________________________________

# Which Events?

Our application will publish

```text id="kproject004"
book.created

book.updated

book.deleted

book.borrowed

book.returned
```

Simple

and descriptive.

______________________________________________________________________

# Event Payload

Every event

contains

structured JSON.

Example

```json id="kproject005"
{
    "event": "book.borrowed",
    "book_id": 1,
    "title": "Clean Code"
}
```

This makes events

easy to consume.

______________________________________________________________________

# Project Structure

Add one file.

```text id="kproject006"
app/

├── kafka.py

├── crud.py

├── routes.py

└── ...
```

______________________________________________________________________

# Reading Configuration

```python id="kproject007"
import os

KAFKA_BROKER = os.getenv(
    "KAFKA_BROKER"
)
```

Configuration stays

outside the code.

______________________________________________________________________

# Creating the Producer

```python id="kproject008"
import json

from kafka import KafkaProducer


producer = KafkaProducer(

    bootstrap_servers=[

        KAFKA_BROKER

    ],

    value_serializer=lambda value:

        json.dumps(value).encode(

            "utf-8"

        )
)
```

Now

every dictionary

is automatically converted

to JSON.

______________________________________________________________________

# Topic Name

We'll use

```text id="kproject009"
library-events
```

Every event

goes to

one topic.

Later,

after the Microservices module,

we'll introduce multiple topics.

______________________________________________________________________

# Publish Helper

```python id="kproject010"
def publish_event(
    event: dict
):

    producer.send(

        "library-events",

        event

    )

    producer.flush()
```

This helper

keeps Kafka code

out of our routes.

______________________________________________________________________

# Why flush()?

Kafka batches messages

for performance.

```python id="kproject011"
producer.flush()
```

forces buffered messages to be sent immediately.

> In high-throughput production systems, you typically avoid calling `flush()` after every message because it reduces throughput. We're doing it here to make behavior predictable while learning.

______________________________________________________________________

# Publishing a Create Event

After saving

the book

to PostgreSQL,

publish

```python id="kproject012"
publish_event(

    {

        "event":

        "book.created",

        "book_id":

        book.id,

        "title":

        book.title

    }

)
```

Database first.

Kafka second.

______________________________________________________________________

# Borrow Event

```python id="kproject013"
publish_event(

    {

        "event":

        "book.borrowed",

        "book_id":

        book.id

    }

)
```

Very simple.

______________________________________________________________________

# Return Event

```python id="kproject014"
publish_event(

    {

        "event":

        "book.returned",

        "book_id":

        book.id

    }

)
```

______________________________________________________________________

# Delete Event

```python id="kproject015"
publish_event(

    {

        "event":

        "book.deleted",

        "book_id":

        book.id

    }

)
```

______________________________________________________________________

# Event Flow

```text id="kproject016"
HTTP Request

↓

CRUD

↓

Database

↓

Kafka

↓

Response
```

The client

doesn't interact

with Kafka directly.

______________________________________________________________________

# Temporary Consumer

To verify events,

create

a simple consumer.

```python id="kproject017"
from kafka import KafkaConsumer

consumer = KafkaConsumer(

    "library-events",

    bootstrap_servers=[

        KAFKA_BROKER

    ],

    value_deserializer=lambda value:

        json.loads(

            value.decode(

                "utf-8"

            )

        )
)
```

______________________________________________________________________

# Reading Events

```python id="kproject018"
for message in consumer:

    print(

        message.value

    )
```

Example

```text id="kproject019"
{

event:

book.borrowed,

book_id: 1

}
```

Our event

was successfully published.

______________________________________________________________________

# Current Flow

```text id="kproject020"
Create Book

↓

Save PostgreSQL

↓

Invalidate Redis (if needed)

↓

Publish Kafka Event

↓

Return Response
```

Everything happens

inside one request.

______________________________________________________________________

# Why Publish After Database Commit?

Imagine

this sequence.

```text id="kproject021"
Publish Event

↓

Database Commit Fails
```

Now

other services believe

the book exists,

but the database disagrees.

Always

commit the database transaction first,

then publish the event.

> In large production systems, this ordering alone isn't enough because failures can occur between the database commit and event publication. We'll solve that later using the **Transactional Outbox Pattern** in the Microservices module.

______________________________________________________________________

# Current Architecture

```text id="kproject022"
             Browser

                │

                ▼

            FastAPI

      ┌─────────┼─────────┐

      ▼         ▼         ▼

 PostgreSQL   Redis     Kafka
```

Our backend

is now

event-driven.

______________________________________________________________________

# Common Mistakes

### Publishing Before Commit

Always persist

the database changes

first.

______________________________________________________________________

### Using Random Event Names

Prefer

```text id="kproject023"
book.created

book.updated

book.deleted
```

Use a consistent naming convention.

______________________________________________________________________

### Sending Python Objects

Kafka transports bytes.

Serialize events

to JSON.

______________________________________________________________________

### Placing Kafka Code Inside Routes

Keep messaging logic

in dedicated helper functions or services.

______________________________________________________________________

### Calling flush() Everywhere

Good for learning.

Not ideal

for high-throughput production systems.

______________________________________________________________________

# Best Practices

- Publish structured JSON events.
- Keep event names consistent.
- Commit database changes before publishing.
- Separate Kafka logic from HTTP routes.
- Use environment variables for broker configuration.
- Keep events small and meaningful.

______________________________________________________________________

# Hands-on Exercise

1. Create `kafka.py`.
1. Configure the producer.
1. Implement `publish_event()`.
1. Publish `book.created`.
1. Publish `book.updated`.
1. Publish `book.borrowed`.
1. Publish `book.returned`.
1. Create a simple consumer.
1. Verify every event reaches Kafka.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should an application commit the database transaction before publishing a Kafka event?

The database should remain the source of truth. If an application publishes an event before committing the database
transaction and the transaction later fails, other services may act on an event describing a change that never actually
occurred. In production systems, this problem is commonly addressed using the Transactional Outbox Pattern, which
guarantees reliable event publication after successful database commits.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Kafka integration
- Event-driven architecture
- Kafka producer
- JSON serialization
- Event naming
- Publishing events
- Simple consumer
- Event flow
- Database-first consistency
- Kafka best practices

Our Library API now integrates:

- FastAPI
- PostgreSQL
- Redis
- Kafka

In the next chapter, we'll perform **end-to-end testing**, verifying that all four components work together correctly
inside Docker Compose.

______________________________________________________________________

## Next File

[Docker Project - Part 7](24-docker-project-part-7.md)
