# System Design - Part 91

# CQRS & Event Sourcing System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why CQRS exists
- Why Event Sourcing exists
- CRUD vs Event Sourcing
- Command Model
- Query Model
- Event Store
- Event Replay
- Read Models
- Projections
- Snapshots
- Versioning
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design a CQRS & Event Sourcing System.**

This is one of the

most advanced

system design topics.

Large companies

like

Amazon,

Microsoft,

Uber,

and banking systems

use

these patterns

for complex domains.

______________________________________________________________________

# Traditional CRUD

Suppose

a customer

changes

their address.

Traditional database

stores

only

the latest value.

```text id="cq9101"
Customer

↓

Address = Delhi
```

Yesterday

it was

Mumbai,

but

that information

is lost.

______________________________________________________________________

# Problem with CRUD

Suppose

the auditor asks,

> What was the customer's address last month?

Traditional CRUD

cannot answer

unless

audit tables

exist.

______________________________________________________________________

# Event Sourcing

Interview favorite.

Instead of

storing

the latest state,

store

every change

as an event.

```text id="cq9102"
Customer Created

↓

Address Changed

↓

Phone Updated

↓

Email Updated
```

Nothing

is overwritten.

______________________________________________________________________

# What is an Event?

An event

represents

something

that already happened.

Examples:

- Order Created
- Payment Completed
- Inventory Reserved
- User Registered

Events

are immutable.

Never

modify

or delete them.

______________________________________________________________________

# Event Store

Interview favorite.

Instead of

updating rows,

append events.

```text id="cq9103"
Event 1

↓

Event 2

↓

Event 3
```

This is

an append-only log.

Very similar

to Kafka,

but

the Event Store

is

the source of truth.

______________________________________________________________________

# Rebuilding State

Question.

How do

we know

the current balance?

Replay

events.

Example

```text id="cq9104"
+100

↓

-20

↓

+50

↓

Balance = 130
```

Current state

is derived

from

past events.

______________________________________________________________________

# Event Replay

Interview favorite.

Suppose

a bug

corrupted

your read database.

Simply

replay

all events.

```text id="cq9105"
Event Store

↓

Replay

↓

Rebuild Database
```

No data

is lost.

______________________________________________________________________

# CQRS

Interview favorite.

CQRS stands for

Command Query Responsibility Segregation.

Separate

writes

from

reads.

______________________________________________________________________

# Command Side

Commands

change state.

Examples:

- Create Order
- Cancel Order
- Pay Invoice

Workflow

```text id="cq9106"
Client

↓

Command API

↓

Validation

↓

Event Store
```

______________________________________________________________________

# Query Side

Queries

read data.

Examples:

- Get Order
- Search Products
- Dashboard

Workflow

```text id="cq9107"
Client

↓

Read API

↓

Read Database
```

______________________________________________________________________

# Why Separate Reads?

Suppose

Amazon

has

100 million

searches

per day,

but

only

2 million

orders.

Reads

and

writes

have

very different

scaling requirements.

______________________________________________________________________

# Read Model

Interview favorite.

The read database

is optimized

for queries.

```text id="cq9108"
Event Store

↓

Projection

↓

Read Database
```

Examples:

- PostgreSQL
- Elasticsearch
- Redis
- MongoDB

Choose

based on

query patterns.

______________________________________________________________________

# Projection

Interview favorite.

A Projection

converts

events

into

read models.

Example

```text id="cq9109"
Order Created

↓

Projection

↓

Orders Table
```

Multiple projections

can exist.

______________________________________________________________________

# Multiple Read Models

Example

```text id="cq9110"
Event Store

↓

Projection A

↓

Dashboard DB
```

```text id="cq9111"
Event Store

↓

Projection B

↓

Search Index
```

```text id="cq9112"
Event Store

↓

Projection C

↓

Analytics DB
```

One event

can update

multiple read models.

______________________________________________________________________

# Snapshots

Interview favorite.

Suppose

an account

has

1 million events.

Replaying

every event

is slow.

Instead,

save

a snapshot.

```text id="cq9113"
Snapshot

↓

Event 999001

↓

...

↓

Event 1000000
```

Recovery

starts

from

the snapshot,

not

the beginning.

______________________________________________________________________

# Versioning

Events

last forever.

Schemas

change.

Example

```text id="cq9114"
OrderCreatedV1
```

↓

```text id="cq9115"
OrderCreatedV2
```

Support

multiple versions

during migration.

______________________________________________________________________

# Event Ordering

Interview favorite.

Events

must be processed

in order

for

one aggregate.

Example

```text id="cq9116"
Deposit

↓

Withdraw

↓

Withdraw
```

Changing

the order

changes

the result.

______________________________________________________________________

# Aggregate

Interview favorite.

An Aggregate

is

the consistency boundary.

Examples:

- Order
- Bank Account
- Shopping Cart

Events

within

one aggregate

must remain

ordered.

Different aggregates

can be processed

in parallel.

______________________________________________________________________

# Optimistic Concurrency

Suppose

two users

update

the same order.

Use

an

expected version.

```text id="cq9117"
Current Version

↓

15
```

If

the expected version

doesn't match,

reject

the command.

______________________________________________________________________

# Event Bus

After

storing

an event,

publish it.

```text id="cq9118"
Event Store

↓

Kafka

↓

Consumers
```

Consumers

update:

- Search
- Analytics
- Notifications

______________________________________________________________________

# Eventual Consistency

Interview favorite.

The read model

may lag

slightly

behind

the write model.

```text id="cq9119"
Command

↓

Event

↓

Projection

↓

Read DB
```

Queries

may briefly

show

old data.

______________________________________________________________________

# Failure Scenario

Suppose

the Projection Service

crashes.

Events

remain safe

inside

the Event Store.

After recovery,

replay

the missing events.

______________________________________________________________________

# Another Failure

Suppose

the Read Database

is corrupted.

Delete it.

Replay

events.

Rebuild

the read model.

______________________________________________________________________

# End-to-End Architecture

```text id="cq9120"
Client

↓

Command API

↓

Validation

↓

Event Store

↓

Kafka

↓

Projection Workers

↓

Read Database

↓

Query API
```

______________________________________________________________________

# Trade-offs

CRUD

vs

Event Sourcing

| CRUD | Event Sourcing |
| ----------------- | ------------------- |
| Simpler | Full history |
| Latest state only | Every change stored |
| Easy queries | Replay possible |

______________________________________________________________________

CQRS

vs

Traditional CRUD

| CQRS | CRUD |
| -------------------- | --------------------- |
| Separate read/write | Single model |
| Better scalability | Simpler |
| Eventual consistency | Immediate consistency |

______________________________________________________________________

Snapshots

vs

Replay

| Snapshot | Replay |
| ---------------- | ---------------- |
| Fast recovery | Complete rebuild |
| Extra storage | No snapshots |
| Less computation | More computation |

______________________________________________________________________

# Best Practices

✅ Keep events immutable.

✅ Design meaningful event names.

✅ Build multiple read models.

✅ Use snapshots for long event streams.

✅ Version events carefully.

______________________________________________________________________

# Common Mistakes

### Treating Events Like Database Rows

Events

represent

facts

that happened.

Never

update

or delete them.

______________________________________________________________________

### One Read Database for Everything

Different applications

need

different query models.

Create

specialized

read databases.

______________________________________________________________________

### Forgetting Versioning

Events

may live

for

years.

Always

plan

for schema evolution.

______________________________________________________________________

### Using Event Sourcing Everywhere

Simple CRUD

applications

do not

benefit much.

Use

Event Sourcing

only when:

- Audit history matters
- Replay is valuable
- Complex business workflows exist

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design a CQRS and Event Sourcing system?

Separate the write model from the read model. On the command side, validate commands and persist immutable domain events
to an append-only Event Store instead of updating records directly. Publish these events so projection workers can build
specialized read models optimized for different query patterns, such as dashboards, search indexes, or analytics
databases. Queries are served from these read models, allowing independent scaling of reads and writes. Use snapshots to
reduce replay time for aggregates with long event histories, optimistic concurrency to prevent conflicting updates, and
event versioning to support schema evolution. Accept eventual consistency between the write model and read models as the
trade-off for scalability and flexibility.

______________________________________________________________________

# Summary

In this lesson, you learned:

- CQRS
- Event Sourcing
- Event Store
- Command Model
- Query Model
- Projections
- Read Models
- Event Replay
- Snapshots
- Versioning
- Optimistic Concurrency
- Eventual Consistency
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
- ✅ CQRS & Event Sourcing

You now understand one of the most advanced architectural patterns used in banking, fintech, logistics, and other
event-driven distributed systems.

______________________________________________________________________

# 🚀 What's Coming Next

The final lesson of the course brings everything together:

- Multi-region deployment
- Active-Active vs Active-Passive
- Global load balancing
- Geo-replication
- Disaster recovery
- CAP theorem in practice
- Data consistency
- Global traffic routing
- Cross-region failover

We'll design **Global Scale Architecture**.

______________________________________________________________________

# What's Next

[Global Scale Architecture System Design](92-global-scale-architecture-system-design.md)
