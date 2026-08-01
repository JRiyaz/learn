# Database Scaling Masterclass - Part 7

# Database Partitioning

______________________________________________________________________

# Introduction

In the previous lecture, we learned about **Database Sharding**.

Many developers confuse **Partitioning** and **Sharding**.

Although they both split data,

they solve different problems.

Let's compare them.

______________________________________________________________________

# Sharding

```text id="dbpt001"
Application

↓

Shard Router

↓

DB-1

DB-2

DB-3
```

The application decides

which database to use.

______________________________________________________________________

# Partitioning

```text id="dbpt002"
Application

↓

PostgreSQL

↓

Partition 1

Partition 2

Partition 3
```

The application still connects to

**one PostgreSQL database**.

PostgreSQL decides

which partition stores the data.

This is the biggest difference.

______________________________________________________________________

# What is Partitioning?

Partitioning means

splitting one large table

into multiple smaller tables

called

```text id="dbpt003"
Partitions
```

To the application,

it still appears as

one table.

______________________________________________________________________

# Example

Instead of

```text id="dbpt004"
Orders

500 Million Rows
```

we create

```text id="dbpt005"
Orders

├── Orders_2023

├── Orders_2024

└── Orders_2025
```

Each partition stores

part of the data.

______________________________________________________________________

# Why Partition?

Large tables create problems.

Imagine

```text id="dbpt006"
orders

2 Billion Rows
```

Simple queries

become slower.

Maintenance

takes longer.

Backups

become larger.

Partitioning solves many of these issues.

______________________________________________________________________

# Types of Partitioning

PostgreSQL supports

```text id="dbpt007"
Range

List

Hash
```

We'll learn each one.

______________________________________________________________________

# Range Partitioning

Most common.

Example

```text id="dbpt008"
Orders

2023

↓

Partition 1

Orders

2024

↓

Partition 2

Orders

2025

↓

Partition 3
```

Each year

has its own partition.

______________________________________________________________________

# PostgreSQL Example

```sql id="dbpt009"
CREATE TABLE orders (

    id BIGINT,

    order_date DATE

)

PARTITION BY RANGE (

    order_date

);
```

Now create partitions.

```sql id="dbpt010"
CREATE TABLE orders_2024

PARTITION OF orders

FOR VALUES FROM (

'2024-01-01'

)

TO (

'2025-01-01'

);
```

______________________________________________________________________

# Insert Example

```sql id="dbpt011"
INSERT INTO orders

VALUES

(

1,

'2024-05-10'

);
```

The application inserts into

```text id="dbpt012"
orders
```

PostgreSQL automatically stores the row in

```text id="dbpt013"
orders_2024
```

The application doesn't need to know.

______________________________________________________________________

# Query Example

```sql id="dbpt014"
SELECT *

FROM orders

WHERE order_date

BETWEEN

'2024-06-01'

AND

'2024-06-30';
```

PostgreSQL reads only

```text id="dbpt015"
orders_2024
```

instead of scanning every partition.

This optimization is called

```text id="dbpt016"
Partition Pruning
```

______________________________________________________________________

# Partition Pruning

Without pruning

```text id="dbpt017"
Orders_2023

Orders_2024

Orders_2025

↓

Scan Everything
```

With pruning

```text id="dbpt018"
Orders_2024

↓

Only One Partition
```

Huge performance improvement.

______________________________________________________________________

# List Partitioning

Useful when values belong

to fixed categories.

Example

```text id="dbpt019"
India

USA

Germany
```

Each country

gets its own partition.

______________________________________________________________________

## PostgreSQL Example

```sql id="dbpt020"
CREATE TABLE customers (

    id BIGINT,

    country TEXT

)

PARTITION BY LIST (

    country

);
```

Partition

```sql id="dbpt021"
CREATE TABLE customers_india

PARTITION OF customers

FOR VALUES IN (

'India'

);
```

______________________________________________________________________

# Hash Partitioning

Instead of ranges,

PostgreSQL hashes

the partition key.

Example

```text id="dbpt022"
Customer ID

↓

Hash

↓

Partition
```

Useful when data

should be evenly distributed.

______________________________________________________________________

## PostgreSQL Example

```sql id="dbpt023"
CREATE TABLE users (

    id BIGINT,

    name TEXT

)

PARTITION BY HASH (

    id

);
```

Create partitions.

```sql id="dbpt024"
CREATE TABLE users_p0

PARTITION OF users

FOR VALUES WITH (

MODULUS 4,

REMAINDER 0

);
```

Additional partitions follow the same pattern with different remainders.

______________________________________________________________________

# Choosing a Partition Key

A good partition key

should

- Match query patterns
- Evenly distribute data
- Support partition pruning

Examples

Good

```text id="dbpt025"
order_date
```

Bad

```text id="dbpt026"
first_name
```

Most applications

rarely query users

by first name.

______________________________________________________________________

# SQLAlchemy Example

Nothing changes.

```python id="dbpt027"
statement = (

    select(Order)

    .where(

        Order.order_date

        >= start_date

    )

)
```

SQLAlchemy

doesn't know

partitions exist.

PostgreSQL handles them.

This is a huge advantage

over sharding.

______________________________________________________________________

# Partition Maintenance

Suppose

new year

2027.

Create

```text id="dbpt028"
orders_2027
```

Old partitions

can later be archived

or removed.

______________________________________________________________________

# Dropping Old Data

Without partitioning

```sql id="dbpt029"
DELETE

FROM orders

WHERE order_date

< '2020-01-01';
```

Millions of row deletions.

Very slow.

______________________________________________________________________

With partitioning

```sql id="dbpt030"
DROP TABLE

orders_2019;
```

Instant.

This is one of the biggest operational benefits of partitioning.

______________________________________________________________________

# Partitioning vs Indexing

Indexes

↓

Find rows faster.

Partitioning

↓

Reduce

how much data

must be searched.

They solve different problems.

Often,

both are used together.

______________________________________________________________________

# Partitioning vs Sharding

| Partitioning | Sharding |
| ---------------------------- | ---------------------------------------- |
| One database | Multiple databases |
| PostgreSQL chooses partition | Application chooses shard |
| Simple application code | Requires routing |
| Easier joins | Cross-shard joins are difficult |
| Easier transactions | Distributed transactions may be required |

______________________________________________________________________

# Real Example

E-commerce

Orders

```text id="dbpt031"
2022

↓

Partition

2023

↓

Partition

2024

↓

Partition

2025

↓

Partition
```

Queries usually target

recent orders.

Older partitions

are rarely accessed.

______________________________________________________________________

# Advantages

Partitioning provides

- Faster queries
- Easier maintenance
- Smaller indexes
- Faster archival
- Better scalability
- Transparent to applications

______________________________________________________________________

# Disadvantages

Partitioning is not a complete solution.

- Poor partition keys reduce benefits.
- Some queries still scan multiple partitions.
- Managing many partitions requires planning.
- It does not increase write capacity across multiple servers like sharding.

______________________________________________________________________

# Common Mistakes

### Wrong Partition Key

Choose keys based on query patterns,

not random columns.

______________________________________________________________________

### Too Many Partitions

Thousands of tiny partitions

increase maintenance overhead.

______________________________________________________________________

### Expecting Partitioning to Replace Sharding

Partitioning and sharding solve different problems.

______________________________________________________________________

### Ignoring Partition Maintenance

Create future partitions

before they are needed.

Archive old ones when appropriate.

______________________________________________________________________

# Best Practices

- Partition large tables only.
- Choose the partition key carefully.
- Monitor partition sizes.
- Use partition pruning.
- Combine partitioning with indexes.
- Automate partition creation for time-based tables.

______________________________________________________________________

# Hands-on Exercise

Answer these questions.

1. What is partitioning?
1. How is it different from sharding?
1. Name the three partitioning strategies.
1. What is partition pruning?
1. Why is `order_date` a good partition key?
1. Why is partitioning transparent to SQLAlchemy?
1. When should you partition a table?

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is partitioning often easier to adopt than sharding?

Partitioning is implemented inside the database engine, so the application continues querying a single logical table.
PostgreSQL automatically routes rows to the correct partition and performs partition pruning when possible. In contrast,
sharding distributes data across multiple independent databases, requiring application-level routing, more complex
transactions, and additional operational management.

______________________________________________________________________

# Summary

In this chapter, you learned:

- What database partitioning is
- How partitioning differs from sharding
- Range partitioning
- List partitioning
- Hash partitioning
- Partition pruning
- Choosing partition keys
- SQLAlchemy compatibility
- Partition maintenance
- Advantages and limitations
- Real-world use cases

In the next lecture, we'll learn about **Multi-Tenant Database Architectures**, including shared-schema,
separate-schema, and separate-database approaches used in SaaS applications.

______________________________________________________________________

## Next File

[Redis Fundamentals](../redis/1-redis-fundamentals.md)

[28-database-scaling-multi-tenant-databases.md](28-database-scaling-multi-tenant-databases.md)

28 28-database-scaling-multi-tenant-databases.md Next 29 29-database-scaling-distributed-transactions.md Pending 30
30-database-scaling-consistent-hashing.md Pending 31 31-database-scaling-industry-architecture-patterns.md Pending 32
32-database-scaling-project-part-1.md Pending 33 33-database-scaling-project-part-2.md Pending 34
34-database-scaling-project-part-3.md Pending 35 35-database-scaling-project-part-4-final.md
