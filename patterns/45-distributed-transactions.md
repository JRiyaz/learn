# Software Architecture - Part 45

# Distributed Transactions

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Distributed Transactions are
- Why they are difficult
- Local vs Distributed Transactions
- ACID across multiple services
- Two-Phase Commit (2PC)
- Three-Phase Commit (3PC)
- XA Transactions
- Saga vs 2PC
- Practical approaches in modern systems
- When NOT to use Distributed Transactions

______________________________________________________________________

# Before We Start

This is one of

the most important

system design topics

for

Senior Backend Engineers.

If you've ever wondered

how Amazon,

banks,

or airline booking systems

keep multiple services

consistent,

this lesson

will answer that.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

A member

borrows a book.

The workflow is

```text id="dt4501"
Loan Service

↓

Inventory Service

↓

Payment Service
```

Each service

has

its own database.

Question.

How do we ensure

either

**everything succeeds**

or

**everything fails?**

______________________________________________________________________

# Single Database Transaction

Inside

one database,

this is simple.

```text id="dt4502"
BEGIN

↓

Update Loan

↓

Update Inventory

↓

Update Payment

↓

COMMIT
```

If anything fails,

```text id="dt4503"
ROLLBACK
```

Everything

returns

to

its previous state.

______________________________________________________________________

# Multiple Databases

Now,

suppose

each service

owns

its own database.

```text id="dt4504"
Loan DB

Inventory DB

Payment DB
```

There is

no single

database transaction

covering

all three.

______________________________________________________________________

# What is a Distributed Transaction?

A **Distributed Transaction**

is

a transaction

that spans

multiple independent systems,

such as

multiple databases

or

multiple services,

while attempting

to maintain

data consistency.

______________________________________________________________________

# The Challenge

Suppose

Loan Service

commits.

Inventory Service

commits.

Payment Service

fails.

```text id="dt4505"
Loan

✅

Inventory

✅

Payment

❌
```

The system

is inconsistent.

______________________________________________________________________

# ACID Properties

Traditional databases

provide

ACID.

- Atomicity
- Consistency
- Isolation
- Durability

Distributed systems

make

Atomicity

much harder,

because

multiple systems

must agree.

______________________________________________________________________

# Why is it Hard?

Between services,

many failures

can occur.

- Network failures
- Service crashes
- Timeouts
- Message loss
- Partial commits

Unlike

a single database,

there is

no central authority.

______________________________________________________________________

# Solution 1

## Two-Phase Commit (2PC)

One approach

is

Two-Phase Commit.

A coordinator

manages

the transaction.

______________________________________________________________________

# Phase 1

## Prepare

Coordinator asks

every participant

```text id="dt4506"
Can you commit?
```

Responses

```text id="dt4507"
Loan

↓

YES
```

```text id="dt4508"
Inventory

↓

YES
```

```text id="dt4509"
Payment

↓

YES
```

Nothing

is committed yet.

Participants

only promise

they are ready.

______________________________________________________________________

# Phase 2

## Commit

If

everyone agrees,

the coordinator

sends

```text id="dt4510"
COMMIT
```

Every participant

commits

its local transaction.

______________________________________________________________________

# Failure Example

Suppose

Inventory says

```text id="dt4511"
NO
```

Coordinator sends

```text id="dt4512"
ROLLBACK
```

Everyone

rolls back.

Consistency

is preserved.

______________________________________________________________________

# Problems with 2PC

Although

2PC

provides

strong consistency,

it has drawbacks.

❌ Blocking

❌ Coordinator bottleneck

❌ Long-running locks

❌ Poor scalability

These issues

make it

less suitable

for

large cloud-native systems.

______________________________________________________________________

# Three-Phase Commit (3PC)

3PC

adds

an additional phase

to reduce

blocking.

Workflow

```text id="dt4513"
Can Commit?

↓

Pre Commit

↓

Commit
```

It improves

fault tolerance,

but

is still

rarely used

in practice.

______________________________________________________________________

# XA Transactions

Many enterprise

databases

support

**XA Transactions**,

which implement

distributed transactions

across

multiple resources.

Historically,

they were common

in enterprise systems.

Today,

they are

much less common

in cloud-native

microservice architectures.

______________________________________________________________________

# Modern Approach

Instead of

2PC,

modern systems

often prefer

```text id="dt4514"
Saga

↓

Outbox

↓

Eventual Consistency
```

Why?

Because

they scale better,

avoid distributed locks,

and

fit

microservice architectures.

______________________________________________________________________

# Saga vs 2PC

Interview favorite.

| Two-Phase Commit | Saga |
| ------------------- | -------------------- |
| Strong consistency | Eventual consistency |
| Global transaction | Local transactions |
| Distributed locking | Compensating actions |
| Blocking | Non-blocking |
| Hard to scale | Cloud-friendly |

______________________________________________________________________

# Banking Example

Suppose

transferring money

between accounts

inside

one database.

Strong consistency

is critical.

2PC

or

database transactions

may be appropriate.

______________________________________________________________________

# E-Commerce Example

Suppose

placing

an order.

Workflow

```text id="dt4515"
Payment

↓

Inventory

↓

Shipping
```

Modern systems

typically use

Saga

instead of

2PC.

Temporary inconsistency

is acceptable,

as long as

the workflow

eventually completes

or compensates.

______________________________________________________________________

# Airline Example

Booking

a flight

may involve

multiple systems.

- Seat Reservation
- Payment
- Ticketing

Historically,

many airline systems

used

distributed transaction

technologies.

Modern architectures

often favor

Saga-based workflows

for new cloud-native services.

______________________________________________________________________

# FastAPI Example

Endpoint

↓

```python id="dt4516"
POST /borrow
```

↓

Loan Service

↓

Saga

↓

Inventory Service

↓

Payment Service

No global

database transaction

exists.

Each service

commits

its own data.

______________________________________________________________________

# AI/ML Example

Suppose

creating

a new model.

Workflow

```text id="dt4517"
Register Model

↓

Allocate GPU

↓

Deploy Endpoint

↓

Update Billing
```

Instead of

one

distributed transaction,

an orchestration workflow

coordinates

the steps

and

compensates

if needed.

______________________________________________________________________

# CAP Connection

Distributed Transactions

are closely related

to

the

CAP Theorem.

Maintaining

strong consistency

across

distributed systems

often impacts

availability

or

performance.

We'll study

CAP

next.

______________________________________________________________________

# Benefits

Distributed Transactions provide:

✅ Strong consistency

✅ Atomic updates

✅ Data integrity

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Blocking

❌ Network dependency

❌ Coordinator failures

❌ Scalability challenges

❌ Operational complexity

______________________________________________________________________

# Modern Recommendation

For

cloud-native applications,

prefer:

- Saga
- Outbox
- Idempotency
- Eventual Consistency

Reserve

2PC

for

special cases

where

strong consistency

is absolutely required.

______________________________________________________________________

# Real Company Example

Large financial systems

may still use

distributed transaction

technologies

for

high-value,

strongly consistent

operations.

However,

many modern

e-commerce,

streaming,

and SaaS platforms

favor

Saga-based workflows

because

they scale

more effectively.

______________________________________________________________________

# When NOT to Use Distributed Transactions

Avoid

distributed transactions

when

temporary inconsistency

is acceptable

and

business workflows

can recover

through

compensation.

They add

significant complexity

and

can reduce

system scalability.

______________________________________________________________________

# Best Practices

✅ Prefer local transactions.

✅ Use Saga where appropriate.

✅ Design idempotent operations.

✅ Keep transactions short.

______________________________________________________________________

# Common Mistakes

### Assuming ACID Across Services

Each service

owns

its own database.

Database ACID guarantees

do not

automatically extend

across services.

______________________________________________________________________

### Long Distributed Locks

Long-running locks

reduce throughput

and

increase failure impact.

______________________________________________________________________

### Ignoring Compensation

When using

Saga,

compensation

is part

of

the business workflow,

not

an afterthought.

______________________________________________________________________

### Choosing 2PC by Default

2PC

is powerful,

but

often unnecessary

for

modern microservices.

Evaluate

business requirements

before choosing

a consistency model.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why are distributed transactions difficult, and why do modern microservices often avoid Two-Phase Commit?

Distributed transactions are difficult because they span multiple independent systems, each with its own database,
network connections, and failure modes. Unlike a single database transaction, there is no built-in mechanism to
guarantee atomic commits across all participants. Two-Phase Commit (2PC) provides strong consistency by coordinating all
participants, but it introduces blocking, long-held locks, coordinator dependencies, and scalability challenges. Modern
microservice architectures often prefer patterns such as Saga, Outbox, and Eventual Consistency because they improve
scalability and resilience while accepting temporary inconsistency that can be resolved through business-level
compensation.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Distributed Transactions are
- Why they are difficult
- Two-Phase Commit (2PC)
- Three-Phase Commit (3PC)
- XA Transactions
- Saga vs 2PC
- Modern cloud-native approaches
- Best practices

______________________________________________________________________

# 🧠 Distributed Systems Progress

You now understand:

- ✅ Microservices
- ✅ API Gateway
- ✅ Service Discovery
- ✅ Saga
- ✅ Outbox
- ✅ Circuit Breaker
- ✅ Bulkhead
- ✅ Distributed Transactions

You now have the foundation needed to understand one of the most famous concepts in distributed systems:

> **CAP Theorem**

______________________________________________________________________

# What's Next

[CAP Theorem](46-cap-theorem.md)
