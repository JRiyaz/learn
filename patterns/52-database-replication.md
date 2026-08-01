# System Design - Part 52

# Database Replication

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Database Replication is
- Why Replication exists
- Primary-Replica Architecture
- Synchronous vs Asynchronous Replication
- Read Replicas
- Replication Lag
- Failover
- Multi-Primary Replication
- PostgreSQL examples
- Common interview questions

______________________________________________________________________

# Before We Start

Our **Library Management System**

has become

very popular.

Initially,

the architecture

looked like this.

```text id="rep5201"
Application

↓

Database
```

Everything

worked.

Until

millions

of users

started

reading books.

______________________________________________________________________

# The Problem

Suppose

the database

receives

100,000 requests

per second.

Most requests

are

reads.

Only

a few

are writes.

```text id="rep5202"
Reads

99%
```

```text id="rep5203"
Writes

1%
```

Question.

Why should

one database

handle

both?

______________________________________________________________________

# Another Problem

Suppose

the database

crashes.

```text id="rep5204"
Database

❌
```

The application

becomes unavailable.

One database

is

a

single point

of failure.

______________________________________________________________________

# The Idea

Instead of

one database,

create

multiple copies.

One database

accepts writes.

Others

serve reads.

______________________________________________________________________

# What is Database Replication?

**Database Replication**

is the process

of copying data

from

one database

to

one or more

replica databases

to improve

availability,

scalability,

and fault tolerance.

______________________________________________________________________

# Primary-Replica Architecture

The most common

replication model.

```text id="rep5205"
Primary

↓

Replica 1

Replica 2

Replica 3
```

The Primary

handles

writes.

Replicas

handle

reads.

______________________________________________________________________

# Write Flow

Suppose

a member

borrows

a book.

```text id="rep5206"
Application

↓

Primary Database

↓

Replicas
```

Every write

goes

to

the Primary.

______________________________________________________________________

# Read Flow

Suppose

another user

searches

for books.

```text id="rep5207"
Application

↓

Replica
```

The Primary

doesn't need

to handle

the read.

______________________________________________________________________

# Benefits

Read traffic

is distributed.

Instead of

one database

handling

100,000 reads,

multiple replicas

share

the workload.

______________________________________________________________________

# Synchronous Replication

The Primary

waits

until

replicas

confirm

the write.

Workflow

```text id="rep5208"
Primary

↓

Replica

↓

Acknowledged

↓

Commit
```

Advantages

✅ Strong consistency

Disadvantages

❌ Higher latency

______________________________________________________________________

# Asynchronous Replication

The Primary

commits

immediately.

Replication

occurs

later.

```text id="rep5209"
Primary

↓

Commit

↓

Later

↓

Replica
```

Advantages

✅ Faster writes

Disadvantages

❌ Replication lag

______________________________________________________________________

# Replication Lag

Suppose

the Primary

updates

a book.

The Replica

receives

the update

two seconds later.

During

those

two seconds,

clients

may read

stale data.

This delay

is called

**Replication Lag**.

______________________________________________________________________

# Example

Time

12:00:00

↓

Primary

```text id="rep5210"
Book Available = False
```

Replica

still returns

```text id="rep5211"
Book Available = True
```

Eventually,

the Replica

catches up.

______________________________________________________________________

# Read Replicas

Read Replicas

exist

only

to

serve

read queries.

They should

not

accept

writes.

Example

```text id="rep5212"
GET /books

↓

Replica
```

```text id="rep5213"
POST /borrow

↓

Primary
```

______________________________________________________________________

# Failover

Suppose

the Primary

fails.

```text id="rep5214"
Primary

❌
```

A Replica

is promoted

to

become

the new Primary.

This process

is called

**Failover**.

______________________________________________________________________

# Automatic Failover

Modern systems

detect

Primary failures

automatically.

Workflow

```text id="rep5215"
Primary

↓

Failure

↓

Promote Replica

↓

Resume Writes
```

Applications

continue

with

minimal downtime.

______________________________________________________________________

# Multi-Primary Replication

Instead of

one Primary,

multiple databases

accept writes.

```text id="rep5216"
Primary A

↔

Primary B
```

Advantages

✅ Geographic writes

Disadvantages

❌ Conflict resolution

Much more

complex.

______________________________________________________________________

# Conflict Example

Suppose

two Primaries

update

the same row

simultaneously.

Which value

wins?

This is

the biggest challenge

of

Multi-Primary Replication.

______________________________________________________________________

# PostgreSQL Example

PostgreSQL

supports

streaming replication.

```text id="rep5217"
Primary

↓

Streaming

↓

Replica
```

Read Replicas

are commonly used

to

offload

read-heavy workloads.

______________________________________________________________________

# MySQL Example

MySQL

also supports

Primary-Replica Replication.

Historically,

the terms

"Master" and "Slave"

were used,

but

modern documentation

generally uses

"Primary" and "Replica."

______________________________________________________________________

# Kubernetes Example

Suppose

PostgreSQL

runs

inside Kubernetes.

One Pod

acts

as

Primary.

Multiple Pods

act

as

Replicas.

Operators

such as

CloudNativePG

or

Patroni

can automate

replication,

failover,

and recovery.

______________________________________________________________________

# AI/ML Example

Suppose

an AI platform

stores

model metadata.

Thousands

of inference requests

read

the metadata.

Only

occasional updates

occur.

Read Replicas

allow

high read throughput

without

overloading

the Primary.

______________________________________________________________________

# Replication vs Backup

Interview favorite.

| Replication | Backup |
| --------------------- | ---------------------- |
| Copies live data | Stores historical copy |
| Improves availability | Disaster recovery |
| Near real-time | Periodic snapshots |

Replication

does **not**

replace

backups.

If

data is deleted

on

the Primary,

that deletion

may also

replicate

to

the Replicas.

______________________________________________________________________

# Replication vs Sharding

Another common

interview question.

| Replication | Sharding |
| ------------------------- | -------------------------- |
| Copies the same data | Splits data |
| Improves read scalability | Improves write scalability |
| Same dataset | Different subsets |

Many systems

use

both.

______________________________________________________________________

# Real Backend Example

An online shopping platform

may have:

- One Primary
- Ten Read Replicas

Checkout

writes

to

the Primary.

Product search

reads

from

Replicas.

This architecture

handles

high read traffic

efficiently.

______________________________________________________________________

# Benefits

Database Replication provides:

✅ High availability

✅ Read scalability

✅ Fault tolerance

✅ Disaster recovery support

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Replication lag

❌ Failover complexity

❌ Replica management

❌ Eventual consistency

with asynchronous replication

______________________________________________________________________

# When NOT to Use Replication

Replication

may not

provide much value

for:

- Small applications
- Single-user systems
- Write-heavy systems

where

reads

are minimal.

______________________________________________________________________

# Best Practices

✅ Send writes to the Primary.

✅ Send reads to Replicas.

✅ Monitor replication lag.

✅ Automate failover.

______________________________________________________________________

# Common Mistakes

### Writing to Replicas

Read Replicas

should not

accept

application writes.

______________________________________________________________________

### Ignoring Replication Lag

Don't assume

Replicas

contain

the latest data

immediately.

______________________________________________________________________

### Treating Replication as Backup

Replication

protects

availability,

not

historical recovery.

Always

maintain

regular backups.

______________________________________________________________________

### Manual Failover

Automate

failover

where possible

to reduce

downtime.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Database Replication, and how does it improve scalability?

Database Replication is the process of maintaining one or more copies of a database by replicating data from a primary
database to replica databases. In a Primary-Replica architecture, all writes go to the Primary, while Replicas handle
read requests. This improves read scalability, increases availability, and provides fault tolerance through failover.
Replication can be synchronous, providing stronger consistency with higher latency, or asynchronous, providing better
performance at the cost of temporary replication lag.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Database Replication is
- Primary-Replica Architecture
- Read Replicas
- Synchronous vs Asynchronous Replication
- Replication Lag
- Failover
- Multi-Primary Replication
- PostgreSQL example
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand four fundamental infrastructure components:

- ✅ Load Balancers
- ✅ Caching
- ✅ CDN
- ✅ Database Replication

The next topic answers another common interview question:

> **What should you do when a single database is no longer large enough, even after adding replicas?**

______________________________________________________________________

# What's Next

[Database Sharding](53-database-sharding.md)
