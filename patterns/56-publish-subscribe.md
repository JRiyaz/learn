# System Design - Part 56

# Publish/Subscribe (Pub/Sub)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Publish/Subscribe (Pub/Sub) is
- Why Pub/Sub exists
- Publisher
- Subscriber
- Topics
- Message Broker
- Fan-Out Messaging
- Consumer Groups
- Ordering
- Kafka implementation
- RabbitMQ implementation
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

In the previous lesson,

we learned

Event-Driven Architecture.

One service

published

an event.

Many services

reacted

to it.

Question.

How does

one message

reach

multiple consumers

without

the producer

knowing

who they are?

The answer is

the

**Publish/Subscribe Pattern**.

______________________________________________________________________

# The Problem

Suppose

our

**Library Management System**

publishes

an event.

```text id="ps5601"
BookBorrowed
```

The following

services

need it.

- Email Service
- Analytics Service
- Recommendation Service
- Audit Service

Should

Borrow Service

send

four API calls?

No.

That creates

tight coupling.

______________________________________________________________________

# The Idea

Instead

of sending

messages

directly,

publish

them

to

a **Topic**.

Interested services

subscribe

to that topic.

______________________________________________________________________

# What is Publish/Subscribe?

**Publish/Subscribe (Pub/Sub)**

is a messaging pattern

where

Publishers

send messages

to

a Topic,

and

Subscribers

receive

those messages

without

direct communication

between them.

______________________________________________________________________

# Architecture

```text id="ps5602"
Publisher

↓

Topic

↓

Subscriber A

Subscriber B

Subscriber C
```

The Publisher

doesn't know

who

the Subscribers are.

______________________________________________________________________

# Publisher

A **Publisher**

creates

messages

and

publishes them

to

a Topic.

Example

```text id="ps5603"
Borrow Service

↓

BookBorrowed
```

After publishing,

its work

is complete.

______________________________________________________________________

# Subscriber

A **Subscriber**

listens

to

one or more

Topics.

Example

```text id="ps5604"
Recommendation Service

↓

BookBorrowed Topic
```

Whenever

a new event

arrives,

the Subscriber

processes it.

______________________________________________________________________

# Topic

A **Topic**

is

a logical channel

that groups

related events.

Examples

```text id="ps5605"
Book Events
```

```text id="ps5606"
Payment Events
```

```text id="ps5607"
User Events
```

Publishers

send

to Topics.

Subscribers

listen

to Topics.

______________________________________________________________________

# Fan-Out

Suppose

one event

is published.

```text id="ps5608"
BookBorrowed

↓

Topic

↓

Email

Analytics

Recommendations

Audit
```

One message

becomes

multiple deliveries.

This is called

**Fan-Out Messaging**.

______________________________________________________________________

# Pub/Sub Flow

```text id="ps5609"
Borrow Service

↓

Topic

↓

Email

↓

Analytics

↓

Audit

↓

Recommendation
```

Every Subscriber

receives

its own copy

of the event.

______________________________________________________________________

# Queue vs Pub/Sub

Interview favorite.

| Queue | Pub/Sub |
| ---------------------------------- | ----------------------------------- |
| One consumer processes the message | All subscribers receive the message |
| Task distribution | Event broadcasting |
| Work sharing | Notification sharing |

______________________________________________________________________

# Example

Suppose

a member

registers.

Publisher

sends

```text id="ps5610"
UserRegistered
```

Subscribers:

- Welcome Email
- Analytics
- Loyalty Program
- CRM

Each service

receives

the event

independently.

______________________________________________________________________

# Consumer Groups

Suppose

Email Service

cannot keep up.

Instead of

one subscriber,

create

multiple workers.

```text id="ps5611"
Email Topic

↓

Worker 1

Worker 2

Worker 3
```

Together,

they form

a

**Consumer Group**.

Each message

is processed

by

only one worker

inside

the group.

______________________________________________________________________

# Multiple Consumer Groups

Now suppose

Analytics

also needs

the events.

```text id="ps5612"
Topic

↓

Email Group

↓

Analytics Group

↓

Audit Group
```

Each group

receives

every message.

Inside

each group,

workers

share

the workload.

______________________________________________________________________

# Ordering

Suppose

events occur.

```text id="ps5613"
PaymentInitiated

↓

PaymentCompleted
```

Consumers

must process

them

in order.

Some brokers,

such as Kafka,

guarantee ordering

within

a partition.

______________________________________________________________________

# Retention

Unlike

traditional queues,

some Pub/Sub systems

keep messages

for

hours

or days.

New subscribers

may read

old events.

Example

```text id="ps5614"
Retention

7 Days
```

______________________________________________________________________

# Kafka Example

Kafka

is built

around

Topics.

```text id="ps5615"
Orders Topic

↓

Partition 1

Partition 2

Partition 3
```

Consumer Groups

read

from

the partitions

in parallel.

______________________________________________________________________

# RabbitMQ Example

RabbitMQ

implements

Pub/Sub

using

**Exchanges**.

```text id="ps5616"
Publisher

↓

Fanout Exchange

↓

Queue A

Queue B

Queue C
```

Each queue

receives

a copy

of the message.

______________________________________________________________________

# FastAPI Example

Suppose

a member

returns

a book.

```python id="ps5617"
POST /return

↓

save_return()

↓

publish(
    "BookReturned"
)
```

Subscribers:

- Analytics
- Recommendation
- Audit

No direct

service calls

are required.

______________________________________________________________________

# AI/ML Example

Suppose

an image

is uploaded.

```text id="ps5618"
ImageUploaded

↓

Topic

↓

OCR

↓

Thumbnail

↓

Virus Scan

↓

Embedding Generator
```

Adding

a new AI service

requires

only

a new subscription.

The Publisher

remains unchanged.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

Publisher

sends

```text id="ps5619"
OrderPlaced
```

Subscribers:

- Shipping
- Billing
- Inventory
- Analytics
- Notifications
- Recommendation Engine

Each service

works

independently.

______________________________________________________________________

# Pub/Sub vs Event-Driven Architecture

Interview favorite.

| Pub/Sub | Event-Driven Architecture |
| --------------------------------- | ------------------------------ |
| Messaging pattern | Overall architectural style |
| Defines message delivery | Defines system design approach |
| Usually implemented using brokers | Often built using Pub/Sub |

Pub/Sub

is one

of the

most common

implementations

of

Event-Driven Architecture.

______________________________________________________________________

# Kafka vs RabbitMQ

| Kafka | RabbitMQ |
| ----------------- | ----------------------------- |
| Event Streaming | Traditional Messaging |
| High throughput | Flexible routing |
| Message retention | Removes acknowledged messages |
| Partition-based | Exchange-based |

Neither

is universally better.

Choose

based on

business requirements.

______________________________________________________________________

# Benefits

Pub/Sub provides:

✅ Loose coupling

✅ Easy extensibility

✅ Independent services

✅ High scalability

✅ Event broadcasting

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Duplicate processing

❌ Event ordering complexity

❌ Monitoring challenges

❌ Eventual consistency

______________________________________________________________________

# Idempotency

Suppose

the same event

is delivered

twice.

Example

```text id="ps5620"
OrderPlaced
```

Inventory Service

must ensure

stock

isn't reduced

twice.

Subscribers

must be

idempotent.

______________________________________________________________________

# Monitoring

Track:

- Topic throughput
- Consumer lag
- Failed deliveries
- Retry count
- Dead Letter Queue size

These metrics

help identify

processing bottlenecks.

______________________________________________________________________

# Real Company Example

Streaming platforms

publish

events

such as

```text id="ps5621"
VideoStarted
```

Subscribers

include:

- Recommendation Engine
- Analytics
- Billing
- Viewing History

Each team

builds

its own

consumer

without

changing

the Publisher.

______________________________________________________________________

# When NOT to Use Pub/Sub

Avoid Pub/Sub

when:

- One service

must receive

exactly one task

(use a Queue)

- Immediate,

synchronous response

is required

- Applications

are small

with

few integrations

______________________________________________________________________

# Best Practices

✅ Design immutable events.

✅ Use meaningful Topic names.

✅ Keep messages small.

✅ Make subscribers idempotent.

______________________________________________________________________

# Common Mistakes

### Confusing Queues with Pub/Sub

Queues

distribute work.

Pub/Sub

broadcasts events.

Choose

the correct pattern.

______________________________________________________________________

### Large Messages

Store

large payloads

externally.

Publish

only

references.

______________________________________________________________________

### Ignoring Consumer Lag

Growing lag

indicates

subscribers

cannot keep up.

Scale

consumer groups

accordingly.

______________________________________________________________________

### Tight Event Coupling

Publish

business events,

not

internal implementation details.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Publish/Subscribe pattern, and how does it differ from a Message Queue?

The Publish/Subscribe (Pub/Sub) pattern is a messaging pattern where publishers send messages to topics, and all
subscribers interested in those topics receive the messages. Publishers are unaware of the subscribers, resulting in
loose coupling. In contrast, a traditional message queue is designed for work distribution, where a message is typically
processed by only one consumer. Pub/Sub is commonly used for broadcasting business events to multiple independent
services, while message queues are better suited for background task processing.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Pub/Sub is
- Publishers
- Subscribers
- Topics
- Fan-Out Messaging
- Consumer Groups
- Kafka Topics
- RabbitMQ Exchanges
- FastAPI example
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand the complete messaging foundation:

- ✅ Message Queues
- ✅ Event-Driven Architecture
- ✅ Publish/Subscribe

These three concepts are fundamental to building scalable, loosely coupled microservice architectures.

______________________________________________________________________

# What's Next

[WebSockets & Long Polling](57-websockets-and-long-polling.md)
