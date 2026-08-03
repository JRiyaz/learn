# System Design - Part 90

# Distributed Transactions System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Distributed Transactions are needed
- ACID vs BASE
- Local vs Distributed Transactions
- Two-Phase Commit (2PC)
- Three-Phase Commit (3PC)
- Saga Pattern
- Choreography vs Orchestration
- Compensation Transactions
- Transactional Outbox Pattern
- Idempotency
- Exactly-Once Processing
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design a Distributed Transaction System.**

In a monolith,

one database

handles everything.

```text id="dt9001"
Application

↓

Database
```

A single

database transaction

is enough.

But

in microservices,

every service

owns

its own database.

```text id="dt9002"
Order Service

↓

Order DB

Inventory Service

↓

Inventory DB

Payment Service

↓

Payment DB
```

Now,

one transaction

must span

multiple databases.

______________________________________________________________________

# Why Distributed Transactions?

Suppose

a customer

places an order.

Steps:

1. Reserve inventory
1. Charge payment
1. Create order
1. Schedule shipping

If

payment succeeds,

but

inventory fails,

the system

must recover.

______________________________________________________________________

# The Problem

Example

```text id="dt9003"
Payment

✅ Success

↓

Inventory

❌ Failed
```

Should

the customer

lose money?

No.

The payment

must be

rolled back

or refunded.

______________________________________________________________________

# ACID vs BASE

Interview favorite.

## ACID

- Atomicity
- Consistency
- Isolation
- Durability

Best for

single databases.

______________________________________________________________________

## BASE

- Basically Available
- Soft State
- Eventual Consistency

Common

in

distributed systems.

______________________________________________________________________

# Local Transaction

```text id="dt9004"
BEGIN

↓

Update Inventory

↓

Update Payment

↓

COMMIT
```

Easy

because

everything

uses

one database.

______________________________________________________________________

# Distributed Transaction

```text id="dt9005"
Order Service

↓

Inventory Service

↓

Payment Service

↓

Shipping Service
```

Each service

has

its own

database.

______________________________________________________________________

# Solution 1

# Two-Phase Commit (2PC)

Interview favorite.

A coordinator

controls

the transaction.

______________________________________________________________________

# Phase 1

Prepare

```text id="dt9006"
Coordinator

↓

Prepare Order

↓

Prepare Payment

↓

Prepare Inventory
```

Every service

responds:

```text id="dt9007"
YES

or

NO
```

No changes

are committed yet.

______________________________________________________________________

# Phase 2

Commit

If

everyone replies

YES

```text id="dt9008"
Coordinator

↓

Commit All
```

Otherwise

```text id="dt9009"
Rollback All
```

______________________________________________________________________

# Problems with 2PC

Interview favorite.

Suppose

the coordinator

crashes

after

everyone

prepared.

Participants

must wait.

Resources

remain locked.

This is called

the

**Blocking Problem**.

______________________________________________________________________

# Solution 2

# Three-Phase Commit (3PC)

3PC

adds

another phase.

```text id="dt9010"
Prepare

↓

Pre-Commit

↓

Commit
```

Benefits:

- Reduces blocking

Disadvantages:

- More messages
- More complexity

Rarely used

in practice.

______________________________________________________________________

# Solution 3

# Saga Pattern

Interview favorite.

Instead

of

one big transaction,

break

the workflow

into

multiple

local transactions.

```text id="dt9011"
Reserve Inventory

↓

Charge Payment

↓

Create Order

↓

Ship
```

Each step

commits

locally.

If

a later step

fails,

execute

compensation.

______________________________________________________________________

# Compensation Transaction

Example

```text id="dt9012"
Charge Payment

↓

Inventory Failed

↓

Refund Payment
```

Instead

of

rolling back,

perform

the opposite action.

______________________________________________________________________

# Choreography Saga

Interview favorite.

Services

communicate

using events.

```text id="dt9013"
Order Created

↓

Inventory Reserved

↓

Payment Completed

↓

Shipping Started
```

No central coordinator.

Advantages:

- Loose coupling
- Highly scalable

Disadvantages:

- Hard to debug
- Event chains become complex

______________________________________________________________________

# Orchestration Saga

Interview favorite.

A central

orchestrator

controls

the workflow.

```text id="dt9014"
Orchestrator

↓

Inventory

↓

Payment

↓

Shipping
```

Advantages:

- Easy monitoring
- Simple workflows

Disadvantages:

- Coordinator dependency

______________________________________________________________________

# Which Saga Style?

| Choreography | Orchestration |
| --------------------------- | ----------------------------- |
| Event-driven | Central coordinator |
| Loosely coupled | Easier control |
| Harder debugging | Easier debugging |
| Better for large ecosystems | Better for business workflows |

______________________________________________________________________

# Transactional Outbox Pattern

Interview favorite.

Suppose

the database

commits

successfully,

but

publishing

to Kafka

fails.

Now

the database

and Kafka

are inconsistent.

______________________________________________________________________

# Outbox Solution

Write

both

the business data

and

an event

inside

the same database transaction.

```text id="dt9015"
Order Table

+

Outbox Table

↓

Single Commit
```

Later,

an Outbox Worker

publishes

events

to Kafka.

______________________________________________________________________

# Inbox Pattern

Sometimes

consumers

receive

duplicate events.

Maintain

an Inbox table.

```text id="dt9016"
Event ID

↓

Already Processed?
```

If yes,

ignore it.

______________________________________________________________________

# Idempotency

Interview favorite.

Processing

the same event

twice

should produce

the same result.

Example

```text id="dt9017"
Payment Event

↓

Already Processed

↓

Ignore
```

______________________________________________________________________

# Exactly-Once Processing

Exactly-once

is difficult

across

distributed systems.

Common approach:

- Idempotent processing
- Outbox Pattern
- Inbox Pattern
- Kafka Transactions

Together,

they provide

practical

exactly-once behavior.

______________________________________________________________________

# Failure Scenario

Suppose

Inventory succeeds,

Payment fails.

Workflow

```text id="dt9018"
Inventory Reserved

↓

Payment Failed

↓

Release Inventory
```

Compensation

restores

system consistency.

______________________________________________________________________

# Another Failure

Suppose

Kafka

is unavailable.

The Outbox Worker

cannot

publish events.

Events

remain

inside

the Outbox table

and

are retried

later.

No data

is lost.

______________________________________________________________________

# End-to-End Architecture

```text id="dt9019"
Client

↓

Order Service

↓

Order DB

↓

Outbox Table

↓

Outbox Worker

↓

Kafka

↓

Inventory Service

↓

Payment Service

↓

Shipping Service
```

______________________________________________________________________

# Trade-offs

2PC

vs

Saga

| 2PC | Saga |
| ------------------ | -------------------- |
| Strong consistency | Eventual consistency |
| Blocking | Non-blocking |
| Simpler rollback | Compensation logic |
| Poor scalability | Better scalability |

______________________________________________________________________

Choreography

vs

Orchestration

| Choreography | Orchestration |
| ------------- | ----------------- |
| Distributed | Centralized |
| More scalable | Easier debugging |
| Event chains | Explicit workflow |

______________________________________________________________________

Rollback

vs

Compensation

| Rollback | Compensation |
| --------------------- | ----------------------- |
| Undo database changes | New business action |
| Single DB | Distributed systems |
| Automatic | Explicit implementation |

______________________________________________________________________

# Best Practices

✅ Prefer Saga for microservices.

✅ Keep local transactions short.

✅ Make every operation idempotent.

✅ Use the Outbox Pattern for reliable event publishing.

✅ Use compensation instead of distributed rollback.

______________________________________________________________________

# Common Mistakes

### Using 2PC Everywhere

2PC

locks resources,

blocks participants,

and

doesn't scale well

for large systems.

______________________________________________________________________

### Forgetting Compensation

Every Saga step

must have

a corresponding

compensation action.

______________________________________________________________________

### Publishing Events After Commit

Never

update

the database

and then

publish

directly.

Use

the Outbox Pattern

to avoid

inconsistencies.

______________________________________________________________________

### Assuming Exactly-Once is Easy

In distributed systems,

exactly-once

usually means

careful coordination

between:

- Idempotency
- Outbox
- Inbox
- Message brokers

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design distributed transactions across microservices?

Avoid extending traditional ACID transactions across multiple services because they introduce blocking and reduce
scalability. Instead, decompose the workflow into local transactions coordinated using the Saga pattern. Each service
commits its own data independently and publishes events to trigger the next step. If a later step fails, execute
compensation transactions to reverse previous business actions, such as releasing inventory or refunding payments. Use
orchestration when centralized workflow management is required and choreography for loosely coupled event-driven
systems. Ensure reliable event delivery with the Transactional Outbox Pattern, implement idempotent consumers, and use
Inbox tables where necessary to safely handle duplicate events.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ACID vs BASE
- Two-Phase Commit (2PC)
- Three-Phase Commit (3PC)
- Saga Pattern
- Choreography vs Orchestration
- Compensation Transactions
- Transactional Outbox Pattern
- Inbox Pattern
- Idempotency
- Exactly-once processing
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ Kafka Internals
- ✅ Redis Internals
- ✅ Nginx Internals
- ✅ Elasticsearch Internals
- ✅ Distributed Locking
- ✅ Distributed Transactions

You now understand how modern distributed systems maintain consistency across multiple independent services without
relying on global database transactions.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll cover another advanced architecture pattern used heavily in event-driven systems:

- Command Query Responsibility Segregation (CQRS)
- Event Sourcing
- Event Store
- Projections
- Read Models
- Snapshots
- Replay
- Versioning

We'll design **CQRS & Event Sourcing**.

______________________________________________________________________

# What's Next

[CQRS & Event Sourcing System Design](91-cqrs-event-sourcing-system-design.md)
