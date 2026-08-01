# Software Architecture - Part 46

# CAP Theorem

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the CAP Theorem is
- Why CAP exists
- Consistency, Availability, and Partition Tolerance
- Network Partitions
- CP, AP, and why CA is impractical in distributed systems
- Real-world database examples
- Kubernetes examples
- FastAPI examples
- CAP vs ACID
- Common interview questions

______________________________________________________________________

# Before We Start

If you ask

10 senior engineers

about

distributed systems,

one topic

will appear

every time.

**CAP Theorem.**

It is one of

the most frequently asked

System Design

interview questions.

Many developers

memorize

the letters.

Few

actually understand

what they mean.

Let's fix that.

______________________________________________________________________

# The Problem

Suppose

our **Library Management System**

runs

on

two servers.

```text id="cap4601"
Server A

↔

Server B
```

Both servers

contain

the same data.

Everything

works.

Until...

______________________________________________________________________

# Network Failure

The network cable

breaks.

```text id="cap4602"
Server A

❌

Server B
```

The servers

cannot communicate.

But

users

are still

sending requests.

Now what?

______________________________________________________________________

# The Question

Suppose

a member

borrows a book

through

Server A.

At the same time,

another member

tries to borrow

the same book

through

Server B.

Since

the servers

cannot communicate,

how should

the system behave?

There is

no perfect answer.

______________________________________________________________________

# What is CAP Theorem?

CAP Theorem,

proposed by

Eric Brewer,

states:

> **When a network partition occurs, a distributed system can provide at most two of the following three properties:**

- Consistency (C)
- Availability (A)
- Partition Tolerance (P)

______________________________________________________________________

# What is Consistency?

Consistency means

every client

sees

the same data

after

a successful write.

Example

Server A

stores

```text id="cap4603"
Book Available = False
```

Immediately,

Server B

must also

return

```text id="cap4604"
Book Available = False
```

No stale data.

______________________________________________________________________

# What is Availability?

Availability means

every request

receives

a response,

even

if

the response

contains

older data.

Example

A user

queries

Server B.

Instead of

returning

an error,

Server B

returns

its current view

of the data.

The system

remains usable.

______________________________________________________________________

# What is Partition Tolerance?

A **Partition**

means

some machines

cannot communicate

because

of

a network failure.

Partition Tolerance

means

the system

continues operating

despite

that communication failure.

In modern

distributed systems,

network partitions

are unavoidable.

Therefore,

Partition Tolerance

is generally

not optional.

______________________________________________________________________

# The Three Properties

```text id="cap4605"
Consistency

Availability

Partition Tolerance
```

The key point

is this:

When

a partition happens,

you must

choose

between

Consistency

and

Availability.

______________________________________________________________________

# CP Systems

Choose:

```text id="cap4606"
Consistency

+

Partition Tolerance
```

If

communication

fails,

the system

rejects

some requests

to avoid

returning

inconsistent data.

Example

```text id="cap4607"
Client

↓

Server

↓

503 Service Unavailable
```

Availability

is sacrificed.

______________________________________________________________________

# AP Systems

Choose:

```text id="cap4608"
Availability

+

Partition Tolerance
```

Even

during

a partition,

every request

receives

a response.

The response

may contain

stale data.

Eventually,

all replicas

become consistent.

______________________________________________________________________

# Can We Have CA?

Many people

think

CA

is an option.

Technically,

yes,

if

there is

no partition.

But

real distributed systems

must assume

network failures

will happen.

Therefore,

in practice,

distributed systems

choose

between

CP

and

AP

when

partitions occur.

______________________________________________________________________

# Example

Library Inventory

Suppose

only

one copy

of

a book

exists.

Should

two users

be allowed

to borrow it

during

a network partition?

A CP system

says

"No."

It may

reject requests.

An AP system

may

temporarily allow

conflicting operations,

then

resolve

the conflict later.

______________________________________________________________________

# Real Database Examples

Generally speaking,

different systems

lean toward

different choices.

**CP-oriented examples**

- Apache ZooKeeper
- etcd
- Consul

These systems

prefer

correct,

consistent data,

even

if

some requests

must wait

or fail.

______________________________________________________________________

**AP-oriented examples**

- Apache Cassandra
- Amazon DynamoDB
- Riak

These systems

prefer

remaining available,

accepting

temporary inconsistency

that will

eventually converge.

______________________________________________________________________

# PostgreSQL Example

A single

PostgreSQL instance

doesn't really

face

CAP trade-offs,

because

it's not

a distributed system.

However,

when

PostgreSQL

is configured

with replication

across

multiple nodes,

CAP considerations

begin to matter.

______________________________________________________________________

# Kubernetes Example

Suppose

Kubernetes

stores

cluster state

inside

etcd.

Why?

Because

incorrect cluster state

is worse

than

temporarily rejecting

requests.

etcd

leans

toward

CP.

______________________________________________________________________

# FastAPI Example

Suppose

your application

reads

product inventory

from

multiple replicas.

Question.

If

one replica

is isolated,

should

the API

return

stale inventory,

or

an error?

That decision

depends

on

whether

your business

prefers

Availability

or

Consistency.

______________________________________________________________________

# Banking Example

Suppose

transferring

₹10,000.

Would you

rather:

Return

an error,

or

allow

an incorrect balance?

Banks

typically prefer

Consistency.

Returning

an error

is acceptable.

Incorrect balances

are not.

______________________________________________________________________

# Social Media Example

Suppose

someone

likes

your post.

If

your friend

sees

the updated count

two seconds later,

is that acceptable?

Usually,

yes.

Social platforms

often prefer

Availability

and

Eventual Consistency.

______________________________________________________________________

# AI/ML Example

Suppose

a recommendation system

uses

cached embeddings.

A user

may briefly

see

slightly outdated

recommendations.

That's often acceptable.

Availability

is more important

than

immediate consistency.

______________________________________________________________________

# CAP vs ACID

Another

interview favorite.

| ACID | CAP |
| ---------------------------------- | ----------------------------- |
| Database transactions | Distributed systems |
| Focuses on transaction correctness | Focuses on network partitions |
| Single database | Multiple nodes/services |

They solve

different problems.

______________________________________________________________________

# Eventual Consistency

AP systems

often rely

on

**Eventual Consistency.**

Example

```text id="cap4609"
Write

↓

Replica A

↓

Replica B

↓

Replica C
```

For

a short time,

replicas

may disagree.

Eventually,

they converge

to

the same state.

______________________________________________________________________

# Why Partition Tolerance Matters

Many beginners ask:

"Can't we just choose CA?"

In a single machine,

perhaps.

But

once

multiple machines

communicate

over

a network,

partitions

are inevitable.

Ignoring

Partition Tolerance

isn't realistic

for modern

distributed systems.

______________________________________________________________________

# Benefits

Understanding CAP

helps you:

✅ Design distributed systems

✅ Choose databases wisely

✅ Make business trade-offs

✅ Explain eventual consistency

______________________________________________________________________

# Common Misconceptions

### "CAP says you choose two."

Not exactly.

The important point is:

**Only when a network partition occurs** do you have to choose between Consistency and Availability.

When there is

no partition,

many systems

can provide

both.

______________________________________________________________________

### "CA databases don't exist."

Single-node databases

effectively provide

Consistency

and

Availability,

because

they don't need

to tolerate

network partitions.

CAP

applies

to

distributed systems.

______________________________________________________________________

### "AP means incorrect forever."

No.

AP systems

typically aim for

Eventual Consistency.

Temporary differences

are expected.

Permanent inconsistency

is not.

______________________________________________________________________

# Benefits and Trade-offs

| Prefer CP | Prefer AP |
| -------------- | --------------- |
| Banking | Social Media |
| Inventory | Recommendations |
| Payments | Analytics |
| Authentication | Logging |

The correct choice

depends

on

business requirements.

______________________________________________________________________

# Best Practices

✅ Understand business priorities.

✅ Don't optimize for CAP alone.

✅ Combine CAP thinking

with

Saga,

Outbox,

and

Circuit Breakers.

✅ Accept

Eventual Consistency

where appropriate.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the CAP Theorem, and why is it important?

The CAP Theorem states that when a network partition occurs in a distributed system, it is impossible to simultaneously
guarantee both strong consistency and high availability. Systems must choose whether to reject requests to preserve
consistency (CP) or continue serving requests with potentially stale data (AP). Partition Tolerance is generally
considered mandatory in distributed systems because network failures are inevitable. Understanding CAP helps engineers
choose appropriate databases, consistency models, and architectural patterns based on business requirements rather than
assuming one approach fits every system.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the CAP Theorem is
- Consistency
- Availability
- Partition Tolerance
- CP vs AP
- Eventual Consistency
- CAP vs ACID
- Real-world examples
- Common misconceptions

______________________________________________________________________

# 🧠 Distributed Systems Progress

You now understand nearly all of the core concepts behind modern distributed systems:

- ✅ Microservices
- ✅ API Gateway
- ✅ Service Discovery
- ✅ Saga
- ✅ Outbox
- ✅ Circuit Breaker
- ✅ Bulkhead
- ✅ Distributed Transactions
- ✅ CAP Theorem

One final foundational topic remains before we move into full system design:

**Consensus Algorithms**, which explain how distributed systems agree on a single truth even when machines fail.

______________________________________________________________________

# What's Next

[Consensus Algorithms (Raft & Paxos)](47-consensus-algorithms.md)
