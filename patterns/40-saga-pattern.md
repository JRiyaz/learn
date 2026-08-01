# Software Architecture - Part 40

# Saga Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Saga Pattern is
- Why distributed transactions are difficult
- Why ACID transactions don't work across microservices
- Choreography vs Orchestration
- Compensating Transactions
- FastAPI examples
- Kafka examples
- AI/ML examples
- Saga vs Two-Phase Commit (2PC)
- When NOT to use Saga

______________________________________________________________________

# Before We Start

This is one of

the most important

topics

for

Microservices

and

System Design interviews.

If you've ever wondered

how Amazon,

Uber,

or food delivery apps

coordinate

multiple services,

this lesson

answers that question.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

A member

borrows a book.

The workflow is

```text id="saga4001"
Borrow Book

↓

Update Loan

↓

Update Inventory

↓

Process Payment

↓

Send Notification
```

Everything

must succeed.

______________________________________________________________________

# The Failure

Suppose

the system

updates

the Loan Service.

Success.

Then

updates

Inventory.

Success.

Then

Payment fails.

Now what?

The system

is inconsistent.

```text id="saga4002"
Loan

✅ Success

Inventory

✅ Success

Payment

❌ Failed
```

The member

appears

to have

borrowed the book,

but

the payment

never completed.

______________________________________________________________________

# Traditional Database Transaction

Inside

one database,

this is easy.

```text id="saga4003"
BEGIN

↓

SQL 1

↓

SQL 2

↓

SQL 3

↓

COMMIT
```

If something fails,

```text id="saga4004"
ROLLBACK
```

Everything

returns

to the previous state.

______________________________________________________________________

# Why Doesn't This Work?

Microservices

have

multiple databases.

```text id="saga4005"
Loan DB

Inventory DB

Payment DB

Notification DB
```

There is

no single

database transaction

covering

all services.

______________________________________________________________________

# The Idea

Instead of

one global transaction,

use

multiple

local transactions.

If one step fails,

undo

the completed steps.

______________________________________________________________________

# What is the Saga Pattern?

The **Saga Pattern**

breaks

a business transaction

into

a sequence

of local transactions.

If a step fails,

previous services

execute

**Compensating Transactions**

to undo

their work.

______________________________________________________________________

# Example

```text id="saga4006"
Reserve Book

↓

Charge Fine

↓

Send Email
```

Suppose

charging

the fine

fails.

The system

executes

```text id="saga4007"
Release Book
```

instead of

rolling back

a database transaction.

______________________________________________________________________

# Compensating Transaction

A compensating transaction

is

an operation

that reverses

a previous action.

Example

```text id="saga4008"
Reserve Book

↓

Release Book
```

```text id="saga4009"
Charge Card

↓

Refund Card
```

Notice

the compensation

is

business logic,

not

database rollback.

______________________________________________________________________

# Two Saga Styles

There are

two ways

to implement

Saga.

- Choreography
- Orchestration

______________________________________________________________________

# Choreography

Each service

publishes events.

Other services

react

to those events.

Example

```text id="saga4010"
Order Created

↓

Payment Service

↓

Payment Completed

↓

Inventory Service

↓

Inventory Reserved

↓

Shipping Service
```

No central coordinator.

Each service

listens

for events.

______________________________________________________________________

# Advantages

✅ Simple

✅ Decentralized

✅ No coordinator

______________________________________________________________________

# Problems

❌ Hard to understand

❌ Difficult debugging

❌ Event chains

can become complex.

______________________________________________________________________

# Orchestration

Instead of

services

communicating

directly,

one component

coordinates

everything.

```text id="saga4011"
Saga Orchestrator

↓

Payment

↓

Inventory

↓

Notification
```

The orchestrator

decides

what happens next.

______________________________________________________________________

# Advantages

✅ Easy monitoring

✅ Central workflow

✅ Easier debugging

______________________________________________________________________

# Problems

❌ One more component

❌ Orchestrator

can become

too large

if poorly designed.

______________________________________________________________________

# FastAPI Example

Suppose

a member

borrows a book.

Endpoint

↓

```python id="saga4012"
POST /borrow
```

↓

Saga Orchestrator

↓

Loan Service

↓

Inventory Service

↓

Payment Service

↓

Notification Service

If

Payment fails,

the orchestrator

calls

```text id="saga4013"
Release Book
```

______________________________________________________________________

# Kafka Example

With choreography,

events

flow

through Kafka.

```text id="saga4014"
BookBorrowed

↓

Kafka

↓

Inventory

↓

Kafka

↓

Payment

↓

Kafka

↓

Notification
```

Every service

reacts

independently.

______________________________________________________________________

# AI/ML Example

Suppose

training

a model

requires

multiple services.

```text id="saga4015"
Allocate GPU

↓

Create Dataset

↓

Train Model

↓

Register Model
```

If

training fails,

execute

```text id="saga4016"
Release GPU

↓

Delete Dataset
```

Each step

has

its own

compensation.

______________________________________________________________________

# Real Backend Example

Suppose

an airline booking.

Workflow

```text id="saga4017"
Reserve Seat

↓

Charge Card

↓

Issue Ticket
```

If

ticket generation

fails,

execute

```text id="saga4018"
Refund Card

↓

Release Seat
```

No distributed

database rollback

is needed.

______________________________________________________________________

# Saga vs ACID Transaction

| ACID Transaction | Saga |
| ------------------ | ------------------------- |
| One database | Multiple services |
| Rollback | Compensating transactions |
| Strong consistency | Eventual consistency |

______________________________________________________________________

# Saga vs Two-Phase Commit (2PC)

A very common

interview question.

| Two-Phase Commit | Saga |
| ------------------- | -------------------------- |
| Distributed locking | Local transactions |
| Strong consistency | Eventual consistency |
| Slow | More scalable |
| Difficult at scale | Designed for microservices |

Modern

cloud-native systems

usually prefer

Saga

over

2PC.

______________________________________________________________________

# Eventual Consistency

After

a Saga starts,

the system

may be

temporarily inconsistent.

Example

```text id="saga4019"
Payment

↓

Pending
```

Inventory

may already

be reserved.

Eventually,

all services

reach

a consistent state.

This is called

**Eventual Consistency**.

______________________________________________________________________

# Benefits

Saga provides:

✅ No distributed transactions

✅ Better scalability

✅ Independent services

✅ Fault recovery

✅ Cloud-friendly architecture

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Complex workflows

❌ Compensating logic

❌ Eventual consistency

❌ Harder testing

______________________________________________________________________

# Real Company Example

Food delivery platforms

typically coordinate

multiple services

when placing an order:

- Payment
- Restaurant
- Delivery Assignment
- Notifications

If

driver assignment

fails,

the system

may refund

the customer

and

release

the restaurant reservation.

This is

a classic

Saga workflow.

______________________________________________________________________

# When NOT to Use Saga

Don't use

Saga

for:

- Monolithic applications
- Single database transactions
- Simple CRUD APIs

If

everything

happens

inside

one database,

normal

ACID transactions

are simpler.

______________________________________________________________________

# Best Practices

✅ Design compensating transactions first.

✅ Keep each local transaction small.

✅ Make compensation idempotent.

✅ Monitor Saga execution.

______________________________________________________________________

# Idempotency

Suppose

a compensation

is retried.

```text id="saga4020"
Refund Payment
```

It should

not

refund

the customer

twice.

Design

compensating actions

to be

**idempotent**,

so repeating them

produces

the same final state.

______________________________________________________________________

# Common Mistakes

### No Compensation

Every important

Saga step

should have

a compensating action

whenever possible.

______________________________________________________________________

### Assuming Immediate Consistency

Sagas

provide

eventual,

not immediate,

consistency.

Design

business processes

accordingly.

______________________________________________________________________

### Giant Orchestrators

Keep

each Saga

focused

on

one business workflow.

______________________________________________________________________

### Long-Running Database Transactions

Never keep

database transactions

open

while waiting

for

other services.

Complete

the local transaction,

then continue

the Saga.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Saga Pattern, and why is it used?

The Saga Pattern is a distributed transaction pattern used in microservices to coordinate business operations across
multiple services without relying on a global database transaction. A Saga consists of a sequence of local transactions,
where each successful step can be undone by a compensating transaction if a later step fails. Sagas can be implemented
using choreography, where services communicate through events, or orchestration, where a central coordinator manages the
workflow. They provide eventual consistency and are widely used in cloud-native systems.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Saga Pattern is
- Why distributed transactions are difficult
- Compensating transactions
- Choreography vs Orchestration
- Kafka example
- FastAPI example
- AI/ML example
- Saga vs 2PC
- Best practices

______________________________________________________________________

# 🧠 Distributed Systems Progress

You now understand:

- ✅ Microservices
- ✅ API Gateway
- ✅ Saga Pattern

Next, we'll learn the **Outbox Pattern**, which solves another critical distributed systems problem:

> **How do you guarantee that database updates and message publishing stay consistent without losing events?**

This pattern is used extensively in production systems that rely on Kafka, RabbitMQ, or other message brokers.

______________________________________________________________________

# What's Next

[Outbox Pattern](41-outbox-pattern.md)
