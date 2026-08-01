# Software Design & Design Patterns - Part 30

# Event Sourcing

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Event Sourcing is
- Why Event Sourcing exists
- The problems it solves
- Events vs Current State
- Event Store
- Replay
- Snapshots
- CQRS + Event Sourcing
- Real-world backend examples
- When NOT to use Event Sourcing

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**.

A book

was borrowed.

Later,

it was returned.

Later,

it was borrowed again.

Traditional databases

store

only

the latest state.

```text id="es3001"
Book

↓

Status = Borrowed
```

Question:

Can you tell

**who borrowed it first?**

No.

Can you reconstruct

the complete history?

Usually,

No.

______________________________________________________________________

# Traditional Databases

Suppose

our table

looks like this.

| Book | Status |
| ---------- | -------- |
| Clean Code | Borrowed |

That's all we know.

Previous states

have disappeared.

______________________________________________________________________

# The Problem

Businesses

often ask

questions like:

- Who changed this?
- When did it change?
- What was the previous value?
- Can we replay history?
- Can we undo changes?

Traditional CRUD

doesn't preserve

all historical changes.

______________________________________________________________________

# The Idea

Instead of

storing

the current state,

store

every change

that happened.

Current state

can always

be rebuilt

from history.

______________________________________________________________________

# What is Event Sourcing?

Event Sourcing says:

> **Store changes as a sequence of immutable events instead of storing only the latest state.**

Instead of

saving

the final result,

save

everything

that happened.

______________________________________________________________________

# Traditional Storage

```text id="es3002"
Book

↓

Borrowed
```

______________________________________________________________________

# Event Sourcing

```text id="es3003"
Book Created

↓

Book Borrowed

↓

Book Returned

↓

Book Borrowed
```

The history

never disappears.

______________________________________________________________________

# What Is an Event?

An event

represents

something

that already happened.

Examples:

- BookCreated
- BookBorrowed
- BookReturned
- FinePaid

Notice

the tense.

Events

are always

written

in the past tense.

______________________________________________________________________

# Example Event

```python id="es3004"
class BookBorrowed:

    def __init__(

        self,

        book_id,

        member_id,

    ):

        self.book_id = book_id

        self.member_id = member_id
```

Events

describe facts.

They

do not

contain

business logic.

______________________________________________________________________

# Event Store

Instead of

a table

containing

current state,

store

events.

Example

| Event |
| ------------- |
| Book Created |
| Book Borrowed |
| Book Returned |
| Book Borrowed |

This is called

the

**Event Store**.

______________________________________________________________________

# Rebuilding State

Suppose

the system

starts

with

```text id="es3005"
Available
```

Replay

the events.

```text id="es3006"
Borrowed

↓

Returned

↓

Borrowed
```

Final state

↓

Borrowed

The current state

is reconstructed

by replaying

all events.

______________________________________________________________________

# Replay

One powerful feature

is

Replay.

Suppose

your analytics system

contains

a bug.

Fix the bug.

Replay

all historical events.

The analytics

becomes correct

without

changing production data.

______________________________________________________________________

# Another Example

Suppose

the recommendation engine

was improved.

Replay

years

of historical events.

Generate

better recommendations.

No user interaction

is required.

______________________________________________________________________

# Snapshots

Question.

What happens

if

an account

contains

10 million events?

Replaying

everything

would be slow.

Solution:

Snapshots.

Example

```text id="es3007"
Event 1

↓

Event 2

↓

Event 3

↓

Snapshot

↓

Event 4

↓

Event 5
```

Instead of

starting

from

Event 1,

start

from

the latest snapshot.

Replay

only

the remaining events.

______________________________________________________________________

# Real Backend Example

Suppose

a bank account

contains

```text id="es3008"
Deposit ₹1000

↓

Withdraw ₹300

↓

Deposit ₹500

↓

Withdraw ₹200
```

The balance

isn't stored.

It is

derived

from

the event history.

______________________________________________________________________

# CQRS + Event Sourcing

These patterns

are frequently

used together.

Workflow

```text id="es3009"
Command

↓

Validate

↓

Create Event

↓

Store Event

↓

Update Read Model
```

Commands

create events.

Queries

read

optimized views.

______________________________________________________________________

# FastAPI Example

```python id="es3010"
@app.post("/borrow")
```

↓

BorrowBookCommand

↓

BookBorrowed Event

↓

Store Event

↓

Update Search Index

↓

Notify Member

One command

creates

multiple outcomes.

______________________________________________________________________

# Kafka Example

Many teams

publish

events

to Kafka.

Example

```text id="es3011"
OrderCreated

↓

Kafka

↓

Analytics

↓

Billing

↓

Email

↓

Inventory
```

Kafka

is not

an Event Store,

but it often

transports

events

between systems.

______________________________________________________________________

# Event Store vs Database

| Database | Event Store |
| -------------------- | ------------------ |
| Stores current state | Stores history |
| UPDATE rows | Append events |
| History optional | History is primary |

______________________________________________________________________

# Event Sourcing vs Audit Logs

Another common

interview question.

Audit Log

↓

Records

what happened

after

the business action.

Event Sourcing

↓

Events

are

the source

of truth.

Audit logs

are supplementary.

Events

drive

the system.

______________________________________________________________________

# Benefits

Event Sourcing gives you:

✅ Complete history

✅ Easy auditing

✅ Replay capability

✅ Better debugging

✅ Time travel

______________________________________________________________________

# Time Travel

Because

every event

is preserved,

you can answer

questions like:

"What did the system

look like

last Monday

at 9:00 AM?"

Traditional CRUD

often cannot

answer this.

Event Sourcing can.

______________________________________________________________________

# Drawbacks

It also introduces:

❌ More storage

❌ More infrastructure

❌ More complex debugging

❌ Event versioning

❌ Eventual consistency

______________________________________________________________________

# Event Versioning

Suppose

today

you publish

```text id="es3012"
BookBorrowed
```

Next year,

the business

adds

a new field.

Older events

must still

be understood.

Managing

event evolution

becomes important.

______________________________________________________________________

# Real Company Example

Banks,

financial exchanges,

and payment platforms

often require

a complete,

immutable history

of transactions

for compliance,

auditing,

and dispute resolution.

Event Sourcing

is a natural fit

for these domains.

______________________________________________________________________

# When NOT to Use Event Sourcing

Don't use

Event Sourcing

for:

- Simple CRUD applications
- Small admin portals
- Basic inventory systems
- Applications without audit requirements

The added complexity

is rarely justified.

______________________________________________________________________

# Best Practices

✅ Keep events immutable.

✅ Name events in the past tense.

✅ Store business facts,

not implementation details.

✅ Version events carefully.

______________________________________________________________________

# Common Mistakes

### Modifying Old Events

Events

should never

be edited.

If something changes,

create

a new event.

______________________________________________________________________

### Confusing Events with Commands

Commands

request

an action.

Events

record

what happened.

______________________________________________________________________

### Forgetting Snapshots

Large event streams

benefit greatly

from snapshots.

______________________________________________________________________

### Using Event Sourcing Everywhere

Apply it

only

where

history

provides

significant value.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Event Sourcing, and why is it used?

Event Sourcing is an architectural pattern that stores every state change as an immutable event instead of storing only
the latest state. The current state of an entity is reconstructed by replaying its event history. This approach provides
complete auditability, replay capabilities, debugging support, and historical reconstruction. Event Sourcing is commonly
combined with CQRS in financial systems, payment platforms, and other domains where preserving every business event is
essential.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Event Sourcing is
- Events vs Current State
- Event Store
- Replay
- Snapshots
- CQRS integration
- Kafka example
- Event versioning
- Best practices

______________________________________________________________________

# 🎉 Congratulations!

You have now completed the **Design Patterns & Enterprise Architecture Foundation**.

You now understand not only object-oriented design patterns but also modern architectural patterns used in scalable
backend systems.

______________________________________________________________________

# 🚀 What's Next

This is the point where I recommend transitioning from individual design patterns to **software architecture**, because
that's how these patterns are actually used in production systems.

The recommended sequence is:

1. **Clean Architecture** (must learn first)
1. **Hexagonal (Ports & Adapters) Architecture**
1. **Onion Architecture**
1. **Layered Architecture**
1. **Microservices Architecture**
1. **Domain-Driven Design (DDD)**
1. **Saga Pattern**
1. **Outbox Pattern**
1. **API Gateway Pattern**
1. **Circuit Breaker Pattern**
1. **Bulkhead Pattern**
1. **Service Discovery**
1. **Distributed Transactions**
1. **CAP Theorem**
1. **Consensus Algorithms (Raft/Paxos)**
1. **System Design Case Studies**

These topics build directly on the patterns you've just learned and are what senior backend engineers and AI
infrastructure engineers use to design large-scale systems.

______________________________________________________________________

# What's Next

[Clean Architecture](31-clean-architecture.md)
