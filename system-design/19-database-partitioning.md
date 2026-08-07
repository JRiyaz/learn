# Database Partitioning (Horizontal vs Vertical)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand database partitioning, how it differs from sharding, when to use horizontal or vertical partitioning, and how to answer partitioning questions confidently in System Design interviews.

______________________________________________________________________

# Introduction

As databases grow,

performance

starts degrading.

Initially,

the database

contains

```
1 Million Rows
```

Everything is fast.

Eventually

it grows to

```
1 Billion Rows
```

Queries become slower.

Indexes become larger.

Maintenance becomes difficult.

How do databases

handle

very large datasets?

One solution is

```
Partitioning
```

______________________________________________________________________

# What Is Partitioning?

Partitioning means

splitting

a database

or a table

into

smaller pieces

called

```
Partitions
```

Unlike sharding,

partitions

may still belong

to

the same

logical database.

______________________________________________________________________

# Why Partition Data?

Benefits

- Faster queries
- Smaller indexes
- Easier maintenance
- Faster backups
- Better scalability
- Improved archival

______________________________________________________________________

# High-Level View

Instead of

```
Orders Table

↓

1 Billion Rows
```

we create

```
Orders

↓

Partition 1

↓

Partition 2

↓

Partition 3
```

The application

still sees

one table.

______________________________________________________________________

# Partitioning vs Sharding

One of the most common

interview questions.

Partitioning

```
One Database

↓

Multiple Partitions
```

Sharding

```
Multiple Databases

↓

Multiple Servers
```

Partitioning

usually stays

inside

one database instance.

Sharding

spreads data

across

multiple database servers.

______________________________________________________________________

# Types Of Partitioning

Two major types

```
Horizontal

↓

Rows
```

```
Vertical

↓

Columns
```

Let's understand both.

______________________________________________________________________

# Horizontal Partitioning

Horizontal partitioning

splits

rows.

Example

Users table

```
ID

1

2

3

4

5

6
```

becomes

```
Partition A

↓

1

2

3
```

```
Partition B

↓

4

5

6
```

Same columns.

Different rows.

______________________________________________________________________

# Visual Example

Original

| ID | Name | Country |
|----|------|----------|
|1|Alice|India|
|2|Bob|USA|
|3|John|UK|
|4|Tom|India|

Horizontal

```
Partition 1

↓

Rows 1-2
```

```
Partition 2

↓

Rows 3-4
```

______________________________________________________________________

# Vertical Partitioning

Vertical partitioning

splits

columns.

Original

| ID | Name | Email | Photo | Resume |

Becomes

```
User Basic

↓

ID

↓

Name

↓

Email
```

```
User Media

↓

ID

↓

Photo

↓

Resume
```

Different columns.

Same rows.

______________________________________________________________________

# Why Vertical Partitioning?

Suppose

most requests

need

```
Name

Email
```

Very few

need

```
Resume

Photo
```

Keeping

large columns

separate

improves performance.

______________________________________________________________________

# Example

Social Media

```
User

↓

Profile Picture

↓

Biography

↓

Settings

↓

Videos
```

Videos

are large.

Store them

separately.

______________________________________________________________________

# Horizontal Partitioning Strategies

Several approaches

exist.

______________________________________________________________________

# Range Partitioning

Split

using ranges.

Example

```
Orders

2023

↓

Partition A
```

```
Orders

2024

↓

Partition B
```

Useful

for

time-series data.

______________________________________________________________________

# List Partitioning

Split

using

fixed values.

Example

```
India

↓

Partition A
```

```
USA

↓

Partition B
```

Useful

when values

are known.

______________________________________________________________________

# Hash Partitioning

Rows

are assigned

using

a hash function.

Example

```
Hash(UserID)

↓

Partition 2
```

Provides

good distribution.

______________________________________________________________________

# Composite Partitioning

Combine

multiple strategies.

Example

```
Year

↓

Hash(UserID)
```

Very common

in enterprise databases.

______________________________________________________________________

# Partition Pruning

Interview favorite.

Suppose

orders

are partitioned

by year.

Query

```sql
SELECT *
FROM orders
WHERE year=2025;
```

Database

reads only

```
2025 Partition
```

Instead of

every partition.

Huge performance gain.

______________________________________________________________________

# Local Indexes

Each partition

has

its own

index.

Smaller.

Faster.

Easy to rebuild.

______________________________________________________________________

# Global Indexes

One index

covers

all partitions.

Useful

for

cross-partition queries,

but

maintenance

is more expensive.

______________________________________________________________________

# Partition Maintenance

Suppose

2021 data

is archived.

Instead of

deleting

millions of rows,

simply

drop

the partition.

Very fast.

______________________________________________________________________

# Rolling Partitions

Common

for logs.

Example

Every month

create

a new partition.

Remove

old partitions

after

one year.

______________________________________________________________________

# Time-Series Example

```
Logs

↓

January

↓

February

↓

March

↓

April
```

Perfect use case

for partitioning.

______________________________________________________________________

# Vertical Partition Example

E-commerce

```
Product

↓

ID

↓

Name

↓

Price
```

Separate table

```
Description

↓

Images

↓

Videos
```

Most pages

don't need

large blobs.

______________________________________________________________________

# Does Partitioning Improve Writes?

Sometimes.

Smaller indexes

reduce

maintenance overhead.

However,

write performance

depends on

the partitioning strategy

and workload.

______________________________________________________________________

# Partitioning And Replication

Many production systems

combine

partitioning

with

replication.

```
Partition A

↓

Replica
```

```
Partition B

↓

Replica
```

______________________________________________________________________

# Partitioning And Sharding

Large companies

often use

both.

Example

```
Shard 1

↓

Monthly Partitions
```

```
Shard 2

↓

Monthly Partitions
```

______________________________________________________________________

# Advantages

Partitioning

provides

- Faster queries
- Smaller indexes
- Faster maintenance
- Easier archival
- Better manageability

______________________________________________________________________

# Disadvantages

- Increased complexity
- Cross-partition queries
- More maintenance
- Poor partition choice hurts performance

______________________________________________________________________

# Common Interview Questions

## Is partitioning the same as sharding?

No.

Partitioning usually divides data within a single database instance, while sharding distributes data across multiple
independent database servers.

______________________________________________________________________

## When should partitioning be used?

Partitioning is useful when tables become very large, especially for time-series data, logs, historical records, or
datasets where queries naturally target a subset of rows.

______________________________________________________________________

## What is partition pruning?

Partition pruning allows the database to skip irrelevant partitions and read only the partitions required by a query,
significantly improving performance.

______________________________________________________________________

## Does partitioning replace indexing?

No.

Partitioning and indexing solve different problems and are often used together.

______________________________________________________________________

# Common Mistakes

## Confusing Partitioning With Sharding

Partitioning

usually occurs

inside one database.

Sharding

occurs

across

multiple databases.

______________________________________________________________________

## Poor Partition Keys

A bad partition key

causes

uneven data distribution

and poor query performance.

______________________________________________________________________

## Partitioning Small Tables

Small tables

rarely benefit

from partitioning.

______________________________________________________________________

## Ignoring Cross-Partition Queries

Queries

that touch

many partitions

may lose

the performance benefits.

______________________________________________________________________

# Best Practices

✅ Partition only when there is a clear need.

✅ Choose partition keys based on query patterns.

✅ Use partition pruning whenever possible.

✅ Combine partitioning with indexing.

✅ Archive old partitions efficiently.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between horizontal and vertical partitioning?

### Answer

Horizontal partitioning splits rows into different partitions while keeping the same columns. Vertical partitioning
splits columns into separate tables while keeping the same rows.

______________________________________________________________________

## Question

Why is partition pruning important?

### Answer

Partition pruning allows the database to access only the relevant partitions instead of scanning the entire table,
reducing I/O and improving query performance.

______________________________________________________________________

## Question

Can partitioning and sharding be used together?

### Answer

Yes. Large-scale systems often shard data across multiple database servers, and each shard may further partition its
tables by time, range, or hash to improve performance and manageability.

______________________________________________________________________

# Practice Exercise

For each application,

answer

1. Is partitioning required?
1. Horizontal or vertical?
1. Which partitioning strategy would you choose?
1. Would partition pruning help?
1. Would sharding also be needed?

Applications

- Banking Transactions
- Audit Logs
- WhatsApp Messages
- E-commerce Orders
- IoT Sensor Data
- Video Streaming Analytics
- Social Media Posts
- Hospital Records

Explain

your reasoning

using

query patterns,

data growth,

and

maintenance requirements.

______________________________________________________________________

# Summary

Database partitioning is an effective technique for managing very large tables.

It enables

- Faster queries
- Better maintenance
- Smaller indexes
- Efficient archival
- Improved scalability

Unlike sharding,

partitioning typically operates **within a single database**, while sharding distributes data across multiple databases.

Understanding the distinction between partitioning and sharding—and when to use each—is an important interview topic for
senior backend engineers.

______________________________________________________________________

# Next

[Distributed Transactions (2PC, Saga Pattern & Outbox Pattern)](20-distributed-transactions.md)
