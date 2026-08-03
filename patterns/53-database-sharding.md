# System Design - Part 53

# Database Sharding

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Database Sharding is
- Why Sharding exists
- Horizontal vs Vertical Partitioning
- Shard Keys
- Sharding Strategies
- Rebalancing
- Cross-Shard Queries
- Resharding
- PostgreSQL examples
- Common interview questions

______________________________________________________________________

# Before We Start

In the previous lesson,

we learned

Database Replication.

Replication

helps

with

read scalability.

But

there is

one problem.

Writes

still go

to

one Primary database.

Eventually,

even

the Primary

becomes overloaded.

What do we do then?

______________________________________________________________________

# The Problem

Suppose

our

Library Management System

stores

500 million books.

Everything

is stored

inside

one database.

```text id="sh5301"
Books

↓

One Database
```

Problems

start appearing.

- Slow queries
- Huge indexes
- Expensive backups
- Longer maintenance
- Storage limits

Eventually,

one machine

isn't enough.

______________________________________________________________________

# Replication Doesn't Help

Suppose

you add

10 replicas.

```text id="sh5302"
Primary

↓

Replica 1

Replica 2

...

Replica 10
```

Reads improve.

Writes don't.

Every write

still goes

to

the Primary.

______________________________________________________________________

# The Idea

Instead of

storing

all data

in

one database,

split

the data

across

multiple databases.

Each database

stores

only

part

of the data.

______________________________________________________________________

# What is Database Sharding?

**Database Sharding**

is the process

of horizontally

partitioning data

across

multiple independent databases

called

**Shards**.

Each shard

contains

only

a subset

of

the total data.

______________________________________________________________________

# Architecture

```text id="sh5303"
Application

↓

Shard Router

↓

Shard A

Shard B

Shard C
```

Each shard

stores

different records.

______________________________________________________________________

# Example

Suppose

books

are divided

by

Book ID.

```text id="sh5304"
Shard A

1 - 1,000,000
```

```text id="sh5305"
Shard B

1,000,001 - 2,000,000
```

```text id="sh5306"
Shard C

2,000,001+
```

No shard

contains

all books.

______________________________________________________________________

# Horizontal vs Vertical Partitioning

Interview favorite.

______________________________________________________________________

## Horizontal Partitioning

Rows

are split.

Example

```text id="sh5307"
Users

1-1M

↓

Shard A
```

```text id="sh5308"
Users

1M-2M

↓

Shard B
```

Every shard

has

the same schema.

______________________________________________________________________

## Vertical Partitioning

Columns

are split.

Example

```text id="sh5309"
User Table

↓

Authentication Columns
```

```text id="sh5310"
Profile Columns
```

Less common

than

horizontal sharding.

______________________________________________________________________

# Choosing a Shard Key

One of

the most important

design decisions.

A **Shard Key**

determines

which shard

stores

each record.

Examples:

- User ID
- Customer ID
- Region
- Tenant ID

A poor

Shard Key

creates

hotspots.

______________________________________________________________________

# Range-Based Sharding

Example

```text id="sh5311"
1-1000

↓

Shard A
```

```text id="sh5312"
1001-2000

↓

Shard B
```

Advantages

✅ Easy range queries

Disadvantages

❌ Uneven distribution

______________________________________________________________________

# Hash-Based Sharding

Example

```text id="sh5313"
hash(user_id)

↓

Shard Number
```

Advantages

✅ Even distribution

Disadvantages

❌ Range queries

become harder.

______________________________________________________________________

# Directory-Based Sharding

A lookup table

maps

records

to shards.

```text id="sh5314"
Customer

↓

Lookup Table

↓

Shard
```

Advantages

✅ Flexible

Disadvantages

❌ Extra lookup

______________________________________________________________________

# Geographic Sharding

Global companies

often shard

by region.

```text id="sh5315"
India

↓

Shard India
```

```text id="sh5316"
Europe

↓

Shard Europe
```

This reduces

latency

for regional users.

______________________________________________________________________

# Cross-Shard Queries

Suppose

you ask

```sql id="sh5317"
SELECT COUNT(*)

FROM Books
```

Every shard

must execute

the query.

Results

are combined.

Cross-shard queries

are slower

than

single-shard queries.

______________________________________________________________________

# Joins

Suppose

Books

are stored

in

Shard A

and

Authors

are stored

in

Shard B.

Database joins

become

much harder.

Applications

often perform

the joins

instead.

______________________________________________________________________

# Resharding

Suppose

Shard A

becomes

too large.

```text id="sh5318"
Shard A

↓

Split

↓

Shard A

Shard D
```

Moving data

between shards

is called

**Resharding**.

This can be

a complex

and expensive

operation.

______________________________________________________________________

# Hot Shards

Suppose

all traffic

goes

to

one celebrity's

user account.

If

the Shard Key

is User ID,

one shard

may receive

far more traffic

than others.

This is called

a

**Hot Shard**.

Choosing

the right

Shard Key

helps

avoid this.

______________________________________________________________________

# PostgreSQL Example

PostgreSQL

supports

partitioning,

but

true application-level

sharding

often requires

tools such as:

- Citus
- Vitess (for MySQL)
- YugabyteDB
- CockroachDB

These systems

distribute

data

across

multiple nodes.

______________________________________________________________________

# Kubernetes Example

Suppose

each shard

runs

as

its own

database deployment.

```text id="sh5319"
Shard A Pod

Shard B Pod

Shard C Pod
```

Applications

route

queries

to

the correct shard

using

the Shard Key.

______________________________________________________________________

# AI/ML Example

Suppose

your AI platform

stores

billions

of embeddings.

Instead of

one database,

partition

embeddings

by

customer ID

or

tenant ID.

Each shard

stores

only

its own customers'

vectors,

improving

write throughput

and

storage scalability.

______________________________________________________________________

# Sharding vs Replication

Interview favorite.

| Replication | Sharding |
| ---------------- | ------------------------ |
| Copies data | Splits data |
| Read scalability | Read + Write scalability |
| Same dataset | Different subsets |

Many systems

use

both together.

______________________________________________________________________

# Real Backend Example

Suppose

a social media platform

stores

billions

of users.

Users

are sharded

by

User ID.

Each shard

contains

only

a portion

of the users,

allowing

the platform

to scale

far beyond

the limits

of a single database.

______________________________________________________________________

# Benefits

Database Sharding provides:

✅ Write scalability

✅ Storage scalability

✅ Smaller indexes

✅ Better parallelism

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Complex queries

❌ Cross-shard joins

❌ Resharding

❌ Operational complexity

______________________________________________________________________

# When NOT to Use Sharding

Don't shard

too early.

Most applications

should first use:

- Better indexing
- Query optimization
- Caching
- Replication

Sharding

should be

a last resort

when

a single database

can no longer

meet

storage

or

write requirements.

______________________________________________________________________

# Best Practices

✅ Choose a good Shard Key.

✅ Keep related data together.

✅ Avoid cross-shard joins.

✅ Plan for future resharding.

______________________________________________________________________

# Common Mistakes

### Sharding Too Early

Many systems

never need

sharding.

Start simple.

______________________________________________________________________

### Bad Shard Key

An uneven

Shard Key

creates

hotspots

and

poor load distribution.

______________________________________________________________________

### Ignoring Resharding

Your initial

Shard Key

may not

last forever.

Plan

for growth.

______________________________________________________________________

### Cross-Shard Transactions

Distributed transactions

across shards

are expensive.

Keep

related data

within

the same shard

when possible.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Database Sharding, and how is it different from Replication?

Database Sharding is the process of horizontally partitioning data across multiple independent databases, where each
shard stores a subset of the overall data. It primarily improves write scalability and storage capacity by distributing
data and write traffic across multiple machines. In contrast, replication creates copies of the same data on multiple
databases to improve read scalability and availability. Sharding increases system capacity but introduces challenges
such as shard key selection, cross-shard queries, resharding, and operational complexity.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Database Sharding is
- Horizontal vs Vertical Partitioning
- Shard Keys
- Range, Hash, and Directory-based Sharding
- Cross-Shard Queries
- Resharding
- Sharding vs Replication
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand the core data scaling techniques:

- ✅ Database Replication (scale reads)
- ✅ Database Sharding (scale writes & storage)

A common interview expectation is knowing **when to use each, and when to combine them**.

______________________________________________________________________

# What's Next

[Message Queues](54-message-queues.md)
