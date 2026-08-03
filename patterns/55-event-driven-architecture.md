# System Design - Part 55

# Event-Driven Architecture (EDA)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Event-Driven Architecture (EDA) is
- Why EDA exists
- What is an Event?
- Event Producers and Consumers
- Event Broker
- Event Flow
- Domain Events
- Event Choreography
- Event Ordering
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

In the previous lesson,

we learned

Message Queues.

A service

placed

a task

into

a queue.

One worker

processed it.

But

what happens

when

multiple services

need

the same information?

Suppose

a member

borrows

a book.

The following

services

are interested.

- Email Service
- Analytics Service
- Recommendation Service
- Audit Service

Should

Borrow Service

call

every service

directly?

______________________________________________________________________

# The Problem

Without

Event-Driven Architecture

```text id="eda5501"
Borrow Service

↓

Email Service

↓

Analytics Service

↓

Recommendation Service

↓

Audit Service
```

Problems:

❌ Tight coupling

❌ Every new service

requires

code changes

inside

Borrow Service.

______________________________________________________________________

# Another Problem

Suppose

tomorrow

Marketing Service

needs

borrow events.

Now,

Borrow Service

must be modified

again.

Every new consumer

creates

another dependency.

______________________________________________________________________

# The Idea

Instead of

calling services,

publish

an event.

Interested services

listen

for

that event.

______________________________________________________________________

# What is an Event?

An **Event**

represents

something

that has already happened

inside

the system.

Examples:

- BookBorrowed
- MemberRegistered
- PaymentCompleted
- FinePaid
- OrderPlaced

Notice

the tense.

Events

describe

facts,

not commands.

______________________________________________________________________

# Event-Driven Architecture

**Event-Driven Architecture (EDA)**

is an architectural style

where

services

communicate

by publishing

and consuming events

instead of

calling each other

directly.

______________________________________________________________________

# Architecture

```text id="eda5502"
Producer

↓

Event Broker

↓

Consumer A

Consumer B

Consumer C
```

The Producer

doesn't know

who

consumes

the event.

______________________________________________________________________

# Producer

A **Producer**

publishes

events.

Example

```text id="eda5503"
Borrow Service

↓

BookBorrowed
```

After publishing,

its work

is finished.

______________________________________________________________________

# Consumer

A **Consumer**

subscribes

to

interesting events.

Example

```text id="eda5504"
BookBorrowed

↓

Recommendation Service
```

Another example

```text id="eda5505"
BookBorrowed

↓

Analytics Service
```

Each consumer

works

independently.

______________________________________________________________________

# Event Broker

The Event Broker

receives

events

and

delivers them

to

all interested consumers.

Popular brokers:

- Apache Kafka
- RabbitMQ
- Amazon EventBridge
- Google Pub/Sub
- Azure Event Grid

______________________________________________________________________

# Event Flow

Suppose

a member

borrows

a book.

```text id="eda5506"
Borrow Service

↓

BookBorrowed

↓

Broker

↓

Email

Analytics

Recommendation

Audit
```

One event.

Multiple consumers.

______________________________________________________________________

# Event Payload

Events

usually contain

only

the information

needed

by consumers.

Example

```json id="eda5507"
{
  "event": "BookBorrowed",
  "book_id": 101,
  "member_id": 55,
  "timestamp": "2026-08-04T10:00:00Z"
}
```

Avoid

sending

large objects.

______________________________________________________________________

# Commands vs Events

Interview favorite.

| Command | Event |
| -------------------- | -------------------------- |
| "Borrow this book" | "BookBorrowed" |
| Requests an action | Reports something happened |
| Usually one receiver | Potentially many receivers |

Commands

ask.

Events

announce.

______________________________________________________________________

# Domain Events

A **Domain Event**

represents

an important

business event.

Examples:

- PaymentCompleted
- LoanCreated
- OrderShipped
- UserRegistered

Domain Events

are often

used

with

DDD

and

Microservices.

______________________________________________________________________

# Choreography

Recall

the Saga Pattern.

Services

react

to events

without

a central orchestrator.

```text id="eda5508"
BookBorrowed

↓

Inventory

↓

InventoryUpdated

↓

Notification

↓

Analytics
```

Each service

decides

what to do

when

an event arrives.

______________________________________________________________________

# Event Ordering

Suppose

two events

occur.

```text id="eda5509"
BookBorrowed

↓

BookReturned
```

Consumers

must process

them

in

the correct order.

Some brokers

guarantee ordering

within

partitions.

Others

do not.

______________________________________________________________________

# Event Replay

One advantage

of

event brokers

like Kafka

is

that

events

can be replayed.

Example

Analytics Service

was offline.

Later,

it reads

older events

from

the broker.

No information

is lost.

______________________________________________________________________

# Event Versioning

Suppose

today

your event

contains

three fields.

Tomorrow,

you add

a fourth field.

Changing

event structures

must be done

carefully

so

older consumers

continue

working.

______________________________________________________________________

# FastAPI Example

Suppose

a user

registers.

```python id="eda5510"
POST /register

↓

save_user()

↓

publish(
    "UserRegistered"
)
```

The API

doesn't call

Email Service

directly.

It publishes

an event.

______________________________________________________________________

# AI/ML Example

Suppose

a customer

uploads

a document.

```text id="eda5511"
DocumentUploaded

↓

Broker

↓

OCR Service

↓

Embedding Service

↓

Search Index
```

Every service

reacts

independently.

New AI services

can subscribe

later

without

changing

the uploader.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

When

an order

is placed,

publish

```text id="eda5512"
OrderPlaced
```

Consumers:

- Inventory
- Billing
- Shipping
- Notification
- Analytics
- Fraud Detection

None

of these services

know

about

each other.

______________________________________________________________________

# Event-Driven vs Request-Driven

| Request-Driven | Event-Driven |
| ------------------ | ----------------------- |
| Direct API calls | Publish events |
| Tight coupling | Loose coupling |
| Immediate response | Asynchronous processing |

Both

are useful.

Choose

based on

business needs.

______________________________________________________________________

# Event-Driven vs Message Queue

Interview favorite.

| Message Queue | Event-Driven Architecture |
| --------------------------------------- | ------------------------------------------ |
| Communication mechanism | Overall architecture style |
| One consumer usually processes the task | Many consumers may react to the same event |
| Focuses on task processing | Focuses on business events |

Message Queues

are often

one building block

used

to implement

Event-Driven Architecture.

______________________________________________________________________

# Benefits

EDA provides:

✅ Loose coupling

✅ Better scalability

✅ Easier extensibility

✅ Independent deployments

✅ Better fault isolation

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Eventual consistency

❌ Harder debugging

❌ Event ordering challenges

❌ More operational complexity

______________________________________________________________________

# Monitoring

Track:

- Event publishing rate
- Consumer lag
- Failed events
- Processing latency
- Retry count

Without monitoring,

event-driven systems

become difficult

to troubleshoot.

______________________________________________________________________

# Real Company Example

Streaming platforms

publish

events

such as:

- VideoStarted
- VideoPaused
- VideoCompleted

Different services

consume

these events

to update:

- Recommendations
- Analytics
- Billing
- User history

without

calling

each other

directly.

______________________________________________________________________

# When NOT to Use Event-Driven Architecture

Avoid EDA

when:

- Immediate consistency

is required

- Simple CRUD applications

with

few integrations

- Small applications

where

direct API calls

are simpler

______________________________________________________________________

# Best Practices

✅ Publish business events.

✅ Keep event payloads small.

✅ Make consumers idempotent.

✅ Version events carefully.

______________________________________________________________________

# Common Mistakes

### Publishing Commands as Events

Events

represent

completed facts.

Don't publish

"CreateUser"

as an event.

Publish

"UserCreated."

______________________________________________________________________

### Huge Event Payloads

Large events

increase

network traffic

and

couple consumers

to producers.

______________________________________________________________________

### Ignoring Consumer Failures

Consumers

can fail.

Use

retries,

DLQs,

and

monitoring.

______________________________________________________________________

### Breaking Event Contracts

Changing

event schemas

without

backward compatibility

can break

multiple services.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Event-Driven Architecture, and why is it used?

Event-Driven Architecture (EDA) is an architectural style where services communicate by publishing and consuming events
instead of making direct synchronous API calls. Producers publish events describing business facts, such as
`OrderPlaced` or `PaymentCompleted`, and consumers independently react to those events. This creates loose coupling,
improves scalability, and allows new services to be added without modifying existing producers. EDA is widely used in
microservices, analytics pipelines, IoT systems, and AI platforms where multiple independent components need to respond
to the same business events.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Event-Driven Architecture is
- Events
- Producers
- Consumers
- Event Broker
- Domain Events
- Choreography
- Event Ordering
- FastAPI example
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand:

- ✅ Message Queues
- ✅ Event-Driven Architecture

These concepts are the foundation for building highly scalable, loosely coupled distributed systems.

______________________________________________________________________

# What's Next

[Publish/Subscribe (Pub/Sub)](56-publish-subscribe.md)
