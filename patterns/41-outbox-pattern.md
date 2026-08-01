# Software Architecture - Part 41

# Outbox Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Outbox Pattern is
- Why the Outbox Pattern exists
- The Dual Write Problem
- Transactional Outbox
- Outbox Worker
- Event Publishing
- Kafka integration
- FastAPI implementation
- Saga integration
- When NOT to use the Outbox Pattern

______________________________________________________________________

# Before We Start

The Outbox Pattern

is one of

the most important

patterns

in modern

microservices.

If your system

uses:

- Kafka
- RabbitMQ
- Amazon SQS
- Azure Service Bus

or

any message broker,

you'll likely

encounter

this pattern.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

A member

borrows a book.

The application

must:

- Save the loan
- Publish `BookBorrowed`

Seems simple.

______________________________________________________________________

# A Naive Implementation

```python id="out4101"
def borrow_book():

    database.save(loan)

    kafka.publish(
        BookBorrowed()
    )
```

Looks correct.

But

there is

a hidden problem.

______________________________________________________________________

# Failure Scenario 1

```text id="out4102"
Database Save

↓

✅ Success

↓

Kafka Publish

↓

❌ Failed
```

Now,

the loan exists

in the database,

but

other services

never receive

the event.

The system

is inconsistent.

______________________________________________________________________

# Failure Scenario 2

Suppose

the order

is reversed.

```text id="out4103"
Kafka Publish

↓

✅ Success

↓

Database Save

↓

❌ Failed
```

Now,

other services

believe

the loan exists,

but

it doesn't.

Another inconsistency.

______________________________________________________________________

# This is called

the

**Dual Write Problem.**

Two different systems

must be updated.

- Database
- Message Broker

There is

no single transaction

covering both.

______________________________________________________________________

# Why Not Use One Transaction?

Database

↓

PostgreSQL

Message Broker

↓

Kafka

Kafka

cannot participate

in

a PostgreSQL

database transaction.

Distributed transactions

are expensive

and

rarely used

in modern

cloud-native systems.

______________________________________________________________________

# The Idea

Instead of

writing

to

two systems,

write

to

only one.

Specifically,

the database.

______________________________________________________________________

# The Outbox Pattern

The **Outbox Pattern**

stores

business events

inside

the same database transaction

as

the business data.

Later,

a background worker

publishes

those events

to

Kafka,

RabbitMQ,

or another broker.

______________________________________________________________________

# Architecture

```text id="out4104"
Application

↓

Database Transaction

↓

Business Table

+

Outbox Table

↓

Commit
```

Later

```text id="out4105"
Outbox Worker

↓

Kafka

↓

Other Services
```

______________________________________________________________________

# Outbox Table

Example

| ID | Event | Published |
| -- | ------------ | --------- |
| 1 | BookBorrowed | No |
| 2 | FinePaid | Yes |

Every event

is stored

before

being published.

______________________________________________________________________

# Database Transaction

Suppose

a member

borrows

a book.

Inside

one transaction

the application

stores:

```text id="out4106"
Loan

↓

BookBorrowed Event
```

If

the transaction fails,

neither

is saved.

Consistency

is preserved.

______________________________________________________________________

# Outbox Worker

A background process

periodically

checks

the Outbox Table.

Workflow

```text id="out4107"
Find Unpublished Events

↓

Publish to Kafka

↓

Mark Published
```

No events

are lost.

______________________________________________________________________

# FastAPI Example

Endpoint

↓

```python id="out4108"
POST /borrow
```

↓

Save Loan

↓

Save Outbox Event

↓

Commit Transaction

The endpoint

does **not**

publish

directly

to Kafka.

______________________________________________________________________

# Worker Example

```python id="out4109"
while True:

    events = load_events()

    for event in events:

        kafka.publish(event)

        mark_as_published(event)
```

Simple.

Reliable.

______________________________________________________________________

# Kafka Example

```text id="out4110"
Database

↓

Outbox

↓

Worker

↓

Kafka

↓

Inventory Service

↓

Recommendation Service
```

Every service

receives

the event

only after

the transaction

has committed.

______________________________________________________________________

# Retry Logic

Suppose

Kafka

is temporarily down.

Worker

tries

again later.

```text id="out4111"
Attempt 1

↓

Failed

↓

Attempt 2

↓

Success
```

No business data

is lost.

______________________________________________________________________

# At-Least-Once Delivery

The Outbox Pattern

usually provides

**At-Least-Once Delivery**.

Meaning

an event

may be delivered

more than once.

Consumers

must therefore

be

**idempotent**.

______________________________________________________________________

# Idempotency

Suppose

Inventory Service

receives

```text id="out4112"
BookBorrowed
```

twice.

Processing it

twice

must produce

the same

final result.

Idempotency

is essential

for

reliable

distributed systems.

______________________________________________________________________

# Outbox + Saga

These patterns

are commonly

used together.

Workflow

```text id="out4113"
Saga Step

↓

Database Transaction

↓

Outbox Event

↓

Worker

↓

Kafka

↓

Next Service
```

Saga

coordinates

the workflow.

Outbox

guarantees

reliable event delivery.

______________________________________________________________________

# AI/ML Example

Suppose

model training

completes.

Database

stores

```text id="out4114"
Model Version
```

and

```text id="out4115"
ModelTrainingCompleted
```

inside

one transaction.

Worker

publishes

the event

later.

Inference Service

loads

the new model

only after

the database

is consistent.

______________________________________________________________________

# CDC (Change Data Capture)

Some teams

don't use

a polling worker.

Instead,

they use

**Change Data Capture (CDC).**

Example

```text id="out4116"
PostgreSQL WAL

↓

Debezium

↓

Kafka
```

Changes

to

the Outbox Table

are streamed

automatically.

______________________________________________________________________

# Polling vs CDC

| Polling Worker | CDC |
| --------------- | ------------------- |
| Simpler | More scalable |
| Periodic checks | Real-time streaming |
| Easier setup | More infrastructure |

Both

implement

the Outbox Pattern.

______________________________________________________________________

# Outbox vs Direct Kafka Publish

| Direct Publish | Outbox |
| ------------------- | ------------------------- |
| Dual Write Problem | Transactional consistency |
| Risk of lost events | Reliable delivery |
| Simpler | More robust |

______________________________________________________________________

# Benefits

The Outbox Pattern

provides:

✅ Reliable event publishing

✅ Transactional consistency

✅ Retry capability

✅ Better fault tolerance

✅ Works well with Saga

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Extra database table

❌ Background workers

❌ Eventual consistency

❌ Duplicate message handling

______________________________________________________________________

# Real Company Example

Suppose

an e-commerce platform.

After

an order

is placed,

the system

must notify:

- Inventory
- Shipping
- Billing
- Analytics

Instead of

publishing

directly,

the application

writes

the order

and

an Outbox Event

inside

one database transaction.

A worker

publishes

the event

afterward,

ensuring

reliable delivery.

______________________________________________________________________

# When NOT to Use the Outbox Pattern

Don't use

the Outbox Pattern

for:

- Monolithic applications
- Systems without messaging
- Small CRUD APIs

If

no external

event publication

is required,

the additional complexity

is unnecessary.

______________________________________________________________________

# Best Practices

✅ Store events in the same transaction as business data.

✅ Keep Outbox Events immutable.

✅ Make consumers idempotent.

✅ Monitor unpublished events.

______________________________________________________________________

# Common Mistakes

### Publishing Before Commit

Never publish

events

before

the database transaction

commits.

______________________________________________________________________

### Deleting Failed Events

Retain

failed events

until

they are

successfully published

or

explicitly handled.

______________________________________________________________________

### Ignoring Duplicate Delivery

Always assume

messages

may arrive

more than once.

______________________________________________________________________

### Long Polling Intervals

Very slow polling

can increase

event latency.

Choose

an interval

appropriate

for

your business needs.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What problem does the Outbox Pattern solve?

The Outbox Pattern solves the Dual Write Problem, where an application must update a database and publish a message to a
broker such as Kafka as part of the same business operation. Instead of writing to both systems directly, the
application stores both the business data and an Outbox Event in the same database transaction. A background worker or
Change Data Capture (CDC) process later publishes the event to the message broker. This guarantees that events are not
lost if failures occur between the database update and message publication, while supporting reliable, at-least-once
event delivery.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Outbox Pattern is
- The Dual Write Problem
- Transactional Outbox
- Outbox Worker
- Kafka integration
- Saga integration
- CDC
- Polling vs CDC
- Best practices

______________________________________________________________________

# 🧠 Distributed Systems Progress

You now understand four essential production patterns:

- ✅ API Gateway
- ✅ Saga Pattern
- ✅ Outbox Pattern
- ✅ Domain Events

Together, these patterns form the backbone of many event-driven microservice architectures used in production.

______________________________________________________________________

# 🏗️ Production Workflow

A common production flow now looks like this:

```text id="out4117"
Client
        ↓
API Gateway
        ↓
Microservice
        ↓
Database Transaction
        ↓
Outbox Table
        ↓
Outbox Worker / CDC
        ↓
Kafka
        ↓
Other Microservices
```

This architecture is widely used because it balances reliability, scalability, and loose coupling.

______________________________________________________________________

# What's Next

[Circuit Breaker Pattern](42-circuit-breaker-pattern.md)
