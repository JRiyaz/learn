# Database Indexing

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how database indexes work internally, why they improve performance, their trade-offs, and how to answer indexing questions confidently in interviews.

______________________________________________________________________

# Introduction

Imagine

your database

contains

```
10 Records
```

Finding

one user

is easy.

Now imagine

```
100 Million Records
```

Without an index,

the database

may need to examine

every row.

```
Record 1

↓

Record 2

↓

Record 3

↓

...

↓

Record 100,000,000
```

Very slow.

Indexes solve

this problem.

______________________________________________________________________

# What Is An Index?

An index

is a special

data structure

that helps

the database

locate rows

quickly.

Think of it as

the index

at the back

of a book.

Without the index,

you read

every page.

With the index,

you jump

directly

to the correct page.

______________________________________________________________________

# Why Do We Need Indexes?

Without Index

```
Application

↓

Database

↓

Scan Entire Table

↓

Return Result
```

With Index

```
Application

↓

Database

↓

Index

↓

Target Row

↓

Return Result
```

Much faster.

______________________________________________________________________

# Real World Example

Imagine

a library

with

1 million books.

Without

an organized catalog,

finding one book

takes hours.

The catalog

is

the database index.

______________________________________________________________________

# Full Table Scan

Suppose

we execute

```sql
SELECT *
FROM users
WHERE email='riyaz@email.com';
```

Without an index,

the database

checks

every row.

```
Row 1

↓

Row 2

↓

Row 3

↓

...

↓

Target Found
```

This is called

```
Full Table Scan
```

______________________________________________________________________

# Indexed Lookup

Now

suppose

an index exists

on

```
email
```

The database

uses

the index

to jump

directly

to the row.

```
Index

↓

Pointer

↓

Row
```

Only

a few operations

are required.

______________________________________________________________________

# Internal Structure

Most relational databases

use

```
B-Tree

or

B+ Tree
```

indexes.

These structures

keep data

sorted,

allowing

fast searches,

insertions,

and deletions.

______________________________________________________________________

# Simplified B-Tree

```
             50
          /      \
       20         80
     /   \      /    \
   10    30   70     90
```

Searching

for

70

doesn't require

checking

every value.

The tree

eliminates

large portions

of the data.

______________________________________________________________________

# Time Complexity

Without Index

```
O(n)
```

With B-Tree Index

```
O(log n)
```

Huge improvement

for

large datasets.

______________________________________________________________________

# Primary Key Index

Every primary key

automatically

has

an index.

Example

```sql
CREATE TABLE users(
    id INT PRIMARY KEY,
    name TEXT
);
```

Searching

by

```
id
```

is already

optimized.

______________________________________________________________________

# Secondary Index

Indexes

can also be created

on

other columns.

Example

```sql
CREATE INDEX idx_email
ON users(email);
```

Now

searching

by email

becomes fast.

______________________________________________________________________

# Composite Index

Sometimes

queries

filter

using

multiple columns.

Example

```sql
SELECT *
FROM orders
WHERE customer_id=10
AND status='PAID';
```

Composite index

```sql
(customer_id, status)
```

works well.

______________________________________________________________________

# Left-Most Prefix Rule

Interview favorite.

Suppose

index

```
(first_name,

last_name,

age)
```

Good

```
first_name

✓
```

```
first_name,

last_name

✓
```

```
first_name,

last_name,

age

✓
```

Usually not useful

```
last_name

alone

✗
```

Understand

the order

of indexed columns.

______________________________________________________________________

# Unique Index

Prevents duplicates.

Example

```sql
CREATE UNIQUE INDEX
idx_email
ON users(email);
```

Now

duplicate emails

cannot exist.

______________________________________________________________________

# Clustered Index

The table

is physically stored

in index order.

Only

one

clustered index

can exist

because

rows

can only be stored

in one physical order.

Example

Primary Key

often uses

a clustered index

(depending on the database).

______________________________________________________________________

# Non-Clustered Index

Stores

index

separately

from

table data.

```
Index

↓

Pointer

↓

Actual Row
```

A table

can have

many

non-clustered indexes.

______________________________________________________________________

# Clustered vs Non-Clustered

| Clustered | Non-Clustered |
|------------|---------------|
| Data stored in index order | Separate index structure |
| One per table | Many allowed |
| Faster range scans | Extra lookup may be required |

Database implementations

vary slightly,

but

this is the general idea.

______________________________________________________________________

# Covering Index

Suppose

query

needs only

```sql
SELECT email
FROM users
```

If

email

already exists

inside

the index,

the database

doesn't need

to access

the table.

Very fast.

______________________________________________________________________

# Range Queries

Indexes

are excellent

for

```sql
salary > 50000
```

```sql
created_at
BETWEEN
Jan
AND
March
```

B-Tree indexes

excel

at ordered data.

______________________________________________________________________

# Equality Queries

Example

```sql
WHERE id=100
```

Extremely fast.

______________________________________________________________________

# When Indexes Don't Help

Example

```sql
WHERE salary + 100 > 1000
```

The database

may not

use the index

because

the indexed value

is modified

inside the query.

______________________________________________________________________

# LIKE Queries

Good

```sql
LIKE 'Riy%'
```

Often uses

the index.

Bad

```sql
LIKE '%iyaz'
```

Leading wildcard

usually prevents

index usage.

______________________________________________________________________

# Too Many Indexes

Indexes

improve reads,

but

they slow

writes.

Why?

Every

INSERT,

UPDATE,

DELETE

must also

update

the indexes.

______________________________________________________________________

# Read vs Write Trade-off

More Indexes

```
Reads

↓

Faster
```

Writes

```
Slower
```

Always

balance

workload.

______________________________________________________________________

# Storage Cost

Indexes

consume

disk space.

Example

```
Table

100 GB
```

Indexes

may add

another

20–80 GB,

depending

on the schema.

______________________________________________________________________

# Index Selectivity

Interview favorite.

Good index

```
Email

Unique
```

Bad index

```
Gender

Male

Female
```

Very low selectivity.

The database

may ignore

the index.

______________________________________________________________________

# Explain Plan

Never guess

whether

an index

is used.

Use

```
EXPLAIN
```

Example

```sql
EXPLAIN
SELECT *
FROM users
WHERE email='riyaz@email.com';
```

The execution plan

shows

whether

the database

uses

an index

or performs

a table scan.

______________________________________________________________________

# Common Indexed Columns

Usually

- Primary Keys
- Foreign Keys
- Email
- Username
- Created At
- Status
- Order ID

Frequently searched columns

are

good candidates.

______________________________________________________________________

# Common Mistakes

Indexing

every column.

Wrong.

Indexes

have costs.

______________________________________________________________________

# Don't Index

Usually avoid

- Boolean fields
- Very small tables
- Frequently updated columns
- Low-selectivity columns

Unless

query patterns

justify it.

______________________________________________________________________

# SQL Example

Without Index

```sql
SELECT *
FROM users
WHERE email='abc@gmail.com';
```

Execution

```
Scan

1 Million Rows
```

With Index

```
Find

Index

↓

One Row
```

Huge difference.

______________________________________________________________________

# Indexes In NoSQL

NoSQL databases

also support

indexes.

Example

MongoDB

```javascript
db.users.createIndex(
    {email:1}
)
```

Concept

is similar,

implementation

varies.

______________________________________________________________________

# Common Interview Questions

## Why not create indexes on every column?

Because indexes consume storage, increase memory usage, and slow down INSERT, UPDATE, and DELETE operations.

______________________________________________________________________

## Why are reads faster with indexes?

Indexes organize data into efficient structures like B-Trees, allowing the database to locate rows without scanning the
entire table.

______________________________________________________________________

## What is a covering index?

A covering index contains all the columns required by a query, allowing the database to answer the query directly from
the index without reading the table.

______________________________________________________________________

## What happens after creating an index?

Future writes become slightly slower because the database must keep both the table and its indexes updated.

______________________________________________________________________

# Common Mistakes

## Believing Indexes Always Improve Performance

They improve

many reads,

but

can hurt

write-heavy workloads.

______________________________________________________________________

## Ignoring Query Patterns

Create indexes

based on

actual queries,

not guesses.

______________________________________________________________________

## Never Checking Execution Plans

Always verify

using

```
EXPLAIN
```

instead of assuming.

______________________________________________________________________

## Forgetting Composite Index Order

Column order

matters.

______________________________________________________________________

# Best Practices

✅ Index frequently searched columns.

✅ Use composite indexes for common multi-column queries.

✅ Verify index usage with execution plans.

✅ Remove unused indexes.

✅ Balance read performance with write performance.

______________________________________________________________________

# Interview Deep Dive

## Question

When should you create an index?

### Answer

Create an index on columns that are frequently used in WHERE clauses, JOIN conditions, ORDER BY clauses, or as foreign
keys. Avoid indexing columns with low selectivity or those that change frequently unless query performance justifies it.

______________________________________________________________________

## Question

Why do indexes slow down writes?

### Answer

Whenever data is inserted, updated, or deleted, the database must also update all relevant indexes. This additional work
increases write latency.

______________________________________________________________________

## Question

What is the difference between a clustered and a non-clustered index?

### Answer

A clustered index determines the physical order of data in the table, so only one can exist. A non-clustered index is
stored separately and points to the actual table rows, allowing multiple indexes on the same table.

______________________________________________________________________

# Practice Exercise

For each table below,

decide

1. Which columns should be indexed?
1. Which columns should not?
1. Would a composite index help?
1. Is a covering index possible?

Tables

- Users
- Orders
- Products
- Payments
- Messages
- Notifications
- Audit Logs

Explain

your reasoning

based on

query patterns.

______________________________________________________________________

# Summary

Indexes are one of the most powerful tools for improving database performance.

They

- Speed up searches
- Reduce table scans
- Improve JOIN performance
- Accelerate sorting and filtering

But they also

- Consume storage
- Slow writes
- Require maintenance

The best engineers create indexes based on **actual query patterns**, not assumptions.

______________________________________________________________________

# Next

[Database Replication](12-database-replication.md)
