# Distributed Transactions (2PC, Saga Pattern & Outbox Pattern)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand why distributed transactions are difficult, learn Two-Phase Commit (2PC), Saga Pattern, Transactional Outbox Pattern, and confidently answer distributed transaction questions in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

you are building

an

E-commerce application.

A customer

places

an order.

The system

must

```
Create Order

↓

Process Payment

↓

Reserve Inventory

↓

Send Confirmation
```

Everything

must succeed.

What if

payment succeeds,

but

inventory fails?

Now

the system

becomes inconsistent.

This is called

a

```
Distributed Transaction
```

______________________________________________________________________

# What Is A Distributed Transaction?

A distributed transaction

is

a transaction

that spans

multiple services

or databases.

Unlike

a traditional

database transaction,

multiple independent systems

must coordinate.

Example

```
Order Service

↓

Payment Service

↓

Inventory Service

↓

Shipping Service
```

______________________________________________________________________

# Traditional Transaction

Inside

one database

ACID guarantees

everything.

```
BEGIN

↓

INSERT

↓

UPDATE

↓

COMMIT
```

Simple.

______________________________________________________________________

# Distributed Transaction

Now

multiple services

are involved.

```
Order Service

↓

Payment Service

↓

Inventory Service
```

Each service

has

its own

database.

There is

no single

ACID transaction

across all databases.

______________________________________________________________________

# Why Is It Difficult?

Suppose

Payment succeeds.

```
Payment

✓
```

Inventory fails.

```
Inventory

✗
```

Now

what should happen?

Should payment

be refunded?

Should order

be cancelled?

Business rules

become important.

______________________________________________________________________

# Common Problems

Distributed transactions

must handle

- Network failures
- Service crashes
- Timeouts
- Duplicate requests
- Partial success
- Retry logic

______________________________________________________________________

# Solution 1

# Two-Phase Commit (2PC)

Classic approach.

A coordinator

controls

all participants.

______________________________________________________________________

# Phase 1

## Prepare

Coordinator asks

every service

```
Can you commit?
```

Example

```
Coordinator

↓

Payment

Ready?

↓

Yes
```

```
Coordinator

↓

Inventory

Ready?

↓

Yes
```

No changes

are committed yet.

______________________________________________________________________

# Phase 2

## Commit

If

everyone agrees

```
Commit
```

is sent.

```
Coordinator

↓

Commit

↓

Payment

↓

Inventory
```

All services

commit.

______________________________________________________________________

# Failure Example

Suppose

Inventory replies

```
No
```

Coordinator

sends

```
Rollback
```

Everything

is cancelled.

______________________________________________________________________

# Advantages

- Strong consistency
- ACID-like behavior
- No partial commits

______________________________________________________________________

# Disadvantages

Very important

for interviews.

- Slow
- Blocking
- Single coordinator
- Doesn't scale well
- Poor cloud fit

Modern microservices

rarely use

2PC.

______________________________________________________________________

# Why 2PC Is Rare Today

Suppose

Inventory

takes

30 seconds.

Payment

must wait.

Everything

is blocked.

High latency.

Poor scalability.

______________________________________________________________________

# Solution 2

# Saga Pattern

Most common

microservice solution.

Instead of

one transaction,

break

the workflow

into

multiple

local transactions.

______________________________________________________________________

# Example

```
Create Order

↓

Charge Payment

↓

Reserve Inventory

↓

Create Shipment
```

Each service

commits

its own transaction.

______________________________________________________________________

# What If Something Fails?

Suppose

Inventory fails.

Instead of

rolling back

using database rollback,

execute

```
Compensation
```

Example

```
Refund Payment
```

______________________________________________________________________

# Saga Flow

```
Create Order

✓

↓

Payment

✓

↓

Inventory

✗

↓

Refund Payment

↓

Cancel Order
```

Business logic

undoes

previous work.

______________________________________________________________________

# Choreography Saga

No central coordinator.

Each service

publishes events.

```
Order Created

↓

Payment Service

↓

Payment Completed

↓

Inventory Service

↓

Inventory Reserved
```

Every service

listens

for events.

______________________________________________________________________

# Advantages

- Loose coupling
- Easy to scale
- No central controller

______________________________________________________________________

# Disadvantages

Harder to understand.

Many events.

Debugging

becomes difficult.

______________________________________________________________________

# Orchestration Saga

Uses

one coordinator.

```
Saga Orchestrator

↓

Payment

↓

Inventory

↓

Shipping
```

Coordinator

decides

the next step.

______________________________________________________________________

# Advantages

- Easier monitoring
- Simpler workflow
- Centralized logic

______________________________________________________________________

# Disadvantages

Coordinator

becomes

another component

to maintain.

______________________________________________________________________

# Choreography vs Orchestration

| Choreography | Orchestration |
|--------------|---------------|
| Event Driven | Central Coordinator |
| Loose Coupling | Central Control |
| Harder Debugging | Easier Monitoring |
| More Flexible | Easier To Understand |

______________________________________________________________________

# Compensation Transaction

One of the most important

interview concepts.

Example

```
Payment Success

↓

Inventory Failed

↓

Refund Payment
```

Refund

is

a compensation,

not

a database rollback.

______________________________________________________________________

# Idempotency

Suppose

Refund

runs twice.

Should

two refunds

be issued?

No.

Compensation

must be

```
Idempotent
```

______________________________________________________________________

# Solution 3

# Transactional Outbox Pattern

Interview favorite.

Problem

```
Database Updated

↓

Application Crashes

↓

Message Never Published
```

Now

other services

never learn

about

the change.

______________________________________________________________________

# Example

```
Create Order

↓

Database Updated

↓

Crash

↓

RabbitMQ

Never Receives Event
```

System

becomes inconsistent.

______________________________________________________________________

# Outbox Solution

Instead of

publishing

immediately

```
Application

↓

Database

↓

Outbox Table
```

Both

are saved

inside

one database transaction.

______________________________________________________________________

# Outbox Flow

```
BEGIN

↓

Insert Order

↓

Insert Outbox Event

↓

COMMIT
```

Now

both

succeed together.

______________________________________________________________________

# Background Publisher

A background worker

reads

the Outbox Table.

```
Outbox

↓

RabbitMQ

↓

Consumers
```

If publishing fails,

the worker

tries again.

______________________________________________________________________

# Advantages

- No lost events
- Reliable messaging
- Simple retries
- Very common

______________________________________________________________________

# Inbox Pattern

Sometimes

consumers

also keep

an

```
Inbox Table
```

Processed message IDs

are stored.

Duplicate messages

are ignored.

Helps achieve

idempotent processing.

______________________________________________________________________

# Exactly Once?

Interview trick.

Exactly-once delivery

is extremely difficult.

Most production systems

combine

- At-least-once delivery
- Idempotent consumers

to achieve

effectively-once

business behavior.

______________________________________________________________________

# Typical Architecture

```
Order Service

↓

Database

↓

Outbox

↓

RabbitMQ

↓

Inventory

↓

Payment

↓

Notification
```

______________________________________________________________________

# Which Pattern Should You Use?

| Scenario | Best Choice |
|-----------|-------------|
| Single Database | ACID Transaction |
| Multiple Databases | Saga |
| Reliable Events | Outbox Pattern |
| Legacy Enterprise | 2PC (sometimes) |

______________________________________________________________________

# Banking Example

Money Transfer

between

two accounts

inside

one database

```
ACID
```

Across

multiple banks

```
Saga

+

Compensation
```

______________________________________________________________________

# Food Delivery Example

```
Order

↓

Payment

↓

Restaurant

↓

Driver

↓

Notification
```

If

restaurant rejects

the order

```
Refund Payment

↓

Cancel Order
```

Saga

fits well.

______________________________________________________________________

# E-commerce Example

```
Order

↓

Inventory

↓

Payment

↓

Shipping
```

Failure

requires

compensation,

not

database rollback.

______________________________________________________________________

# Common Interview Questions

## Why not use 2PC everywhere?

2PC blocks participants, increases latency, introduces a coordinator dependency, and scales poorly in cloud-native
microservices.

______________________________________________________________________

## Why is Saga more popular?

Saga uses independent local transactions with compensation, making it more scalable, resilient, and better suited for
distributed microservice architectures.

______________________________________________________________________

## What problem does the Outbox Pattern solve?

It prevents the situation where a database transaction commits successfully but the corresponding event is never
published because the application crashes immediately afterward.

______________________________________________________________________

## Is compensation the same as rollback?

No.

Rollback

undoes

an uncommitted transaction.

Compensation

creates

a new business transaction

to reverse

a previously committed action.

______________________________________________________________________

# Common Mistakes

## Thinking Database Rollback Works Across Services

Each service

owns

its own database.

Traditional rollback

doesn't span

multiple services.

______________________________________________________________________

## Forgetting Idempotency

Retries

are common.

Consumers

must safely handle

duplicate requests.

______________________________________________________________________

## Publishing Events Before Database Commit

This can lead

to

messages

about data

that was never committed.

______________________________________________________________________

## Assuming Exactly Once Is Easy

Exactly-once semantics

usually require

additional coordination

and careful system design.

______________________________________________________________________

# Best Practices

✅ Prefer Saga for distributed microservices.

✅ Use compensation instead of distributed rollback.

✅ Use the Transactional Outbox Pattern for reliable event publishing.

✅ Make consumers idempotent.

✅ Monitor failed compensations and retries.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is Saga preferred over 2PC in microservices?

### Answer

Saga avoids blocking distributed transactions by allowing each service to commit independently and using compensation
transactions when failures occur. This provides better scalability and resilience in distributed systems.

______________________________________________________________________

## Question

What is the purpose of the Transactional Outbox Pattern?

### Answer

The Transactional Outbox Pattern ensures that database changes and event publication remain consistent by storing events
in an outbox table within the same database transaction. A background process later publishes those events reliably.

______________________________________________________________________

## Question

Why are idempotent consumers important?

### Answer

Most messaging systems provide at-least-once delivery, meaning duplicate messages are possible. Idempotent consumers
ensure that processing the same message multiple times does not produce duplicate business effects.

______________________________________________________________________

# Practice Exercise

For each application,

decide

1. Would you use ACID, 2PC, Saga, or Outbox?
1. Is compensation required?
1. What failures must be handled?
1. Is idempotency necessary?
1. Should events be published through an Outbox?

Applications

- Banking Transfer
- Food Delivery
- Ride Sharing
- E-commerce Checkout
- Hotel Booking
- Airline Reservation
- Payment Gateway
- Inventory Management

Explain

your reasoning

based on

consistency,

availability,

and

business requirements.

______________________________________________________________________

# Summary

Distributed transactions are one of the most challenging topics in System Design.

Modern systems typically avoid distributed ACID transactions and instead rely on

- Saga Pattern
- Compensation Transactions
- Transactional Outbox Pattern
- Idempotent Consumers

Understanding these patterns—and knowing **why** they are preferred over traditional distributed transactions—is a key
expectation in senior backend and System Design interviews.

______________________________________________________________________

# Next

[System Design Case Studies – URL Shortener](21-design-url-shortener.md)
