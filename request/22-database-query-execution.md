# Complete HTTP Request Lifecycle Deep Dive

## 22. Database Query Execution

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand what happens inside the database after an ORM sends a query, including query parsing, optimization, execution, indexing, transactions, locking, and returning the results.

______________________________________________________________________

# Introduction

In the previous chapter,

our application

used

SQLAlchemy

to execute

a query.

Example

```python
user = session.get(User, 1)
```

SQLAlchemy

generated

SQL

and sent it

to

PostgreSQL.

Now the question is

```
What happens

inside

PostgreSQL?
```

This chapter

answers that.

______________________________________________________________________

# High Level Flow

```
Business Logic

↓

SQLAlchemy

↓

Database Driver

↓

PostgreSQL

↓

SQL Parser

↓

Query Planner

↓

Query Optimizer

↓

Execution Engine

↓

Storage Engine

↓

Indexes / Tables

↓

Result Set

↓

Application
```

______________________________________________________________________

# Example Query

```sql
SELECT *

FROM users

WHERE id = 100;
```

Although

this looks simple,

the database

performs

many internal steps

before returning

the result.

______________________________________________________________________

# Step 1

# Receive Query

The database

receives

the SQL query

through

an existing

database connection.

```
Application

↓

Database Connection

↓

PostgreSQL
```

______________________________________________________________________

# Step 2

# SQL Parsing

Interview favorite.

The SQL parser

checks

whether

the query

is valid.

It verifies

- SQL syntax
- Keywords
- Table names
- Column names

Example

```
SELECT *

FROM users
```

Valid.

______________________________________________________________________

Invalid example

```sql
SELEC *

FROM users
```

Parser returns

```
Syntax Error
```

______________________________________________________________________

# Step 3

# Semantic Analysis

The database

checks

whether

referenced objects

exist.

Example

```
users

↓

Table Exists?
```

```
id

↓

Column Exists?
```

If not,

the query fails.

______________________________________________________________________

# Step 4

# Query Planner

Interview favorite.

The planner

generates

multiple ways

to execute

the query.

Example

```
Use Index

OR

Scan Entire Table
```

______________________________________________________________________

# Step 5

# Query Optimizer

The optimizer

chooses

the fastest plan.

Factors considered

- Table size
- Available indexes
- Estimated rows
- Query cost

______________________________________________________________________

# Example

Suppose

the table

contains

10 million rows.

Using

an index

is much faster

than

scanning

every row.

______________________________________________________________________

# Step 6

# Index Lookup

Interview favorite.

Suppose

an index exists

on

```
id
```

Flow

```
Query

↓

Primary Key Index

↓

Locate Row

↓

Return Data
```

Instead of

reading

the entire table.

______________________________________________________________________

# What is an Index?

An index

is a special

data structure

that helps

the database

find rows quickly.

Think of it

like

the index

at the back

of a book.

Instead of

reading

every page,

you directly

jump

to

the correct page.

______________________________________________________________________

# Without Index

```
Row 1

↓

Row 2

↓

Row 3

↓

...

↓

Row 10,000,000
```

This is called

```
Full Table Scan
```

______________________________________________________________________

# With Index

```
Index

↓

Matching Row

↓

Done
```

Much faster.

______________________________________________________________________

# Primary Key Index

Interview favorite.

Every primary key

automatically gets

an index.

Example

```sql
id
```

Searching

by primary key

is usually

very fast.

______________________________________________________________________

# Secondary Index

Indexes

can also

be created

on other columns.

Example

```sql
CREATE INDEX

idx_email

ON users(email);
```

Useful

for

frequently searched

columns.

______________________________________________________________________

# Step 7

# Read Data

After

finding

the matching rows,

PostgreSQL

reads

the actual data

from disk

or memory.

If the page

is already

in memory,

the query

is much faster.

______________________________________________________________________

# Buffer Cache

Interview favorite.

Frequently used

database pages

are stored

in memory.

```
Query

↓

Buffer Cache

↓

Found?

↓

Yes

↓

Return
```

Otherwise

read from disk.

______________________________________________________________________

# Step 8

# Execute Filters

Suppose

the query contains

```sql
WHERE age > 18
```

The execution engine

applies

the condition

to matching rows.

______________________________________________________________________

# Step 9

# Build Result Set

The matching rows

are assembled

into

a result set.

Example

```
Row 1

↓

Row 2

↓

Row 3
```

______________________________________________________________________

# Step 10

# Return Results

The result

is sent

back

through

the database driver.

```
PostgreSQL

↓

Driver

↓

SQLAlchemy

↓

Python Objects
```

______________________________________________________________________

# INSERT Query

Example

```sql
INSERT INTO users
```

Flow

```
Parse

↓

Validate

↓

Check Constraints

↓

Insert Row

↓

Update Index

↓

Commit
```

______________________________________________________________________

# UPDATE Query

Flow

```
Find Row

↓

Modify Data

↓

Update Indexes

↓

Commit
```

______________________________________________________________________

# DELETE Query

Flow

```
Find Row

↓

Delete

↓

Update Indexes

↓

Commit
```

______________________________________________________________________

# Transactions

Interview favorite.

Suppose

multiple queries

must succeed

together.

```
Update Balance

↓

Insert Transaction

↓

Update History
```

If one fails

everything

rolls back.

______________________________________________________________________

# Locks

Interview favorite.

Suppose

two users

try

to update

the same row.

The database

uses

locks

to prevent

data corruption.

```
User A

↓

Lock Row
```

```
User B

↓

Wait
```

______________________________________________________________________

# Isolation Levels

Databases

provide

different

transaction isolation levels.

Common ones

- Read Committed
- Repeatable Read
- Serializable

Higher isolation

provides

better consistency

but may reduce

performance.

______________________________________________________________________

# Query Execution Plan

Interview favorite.

Developers

can inspect

how PostgreSQL

executes a query

using

```sql
EXPLAIN
```

or

```sql
EXPLAIN ANALYZE
```

Useful

for

performance tuning.

______________________________________________________________________

# Example

Instead of

```
Seq Scan
```

you want

```
Index Scan
```

for

large tables

when appropriate.

______________________________________________________________________

# Common Performance Problems

## Full Table Scan

Occurs when

no useful index

exists.

Solution

Add

appropriate indexes.

______________________________________________________________________

## Too Many Indexes

Indexes improve

reads

but slow down

writes.

Only create

indexes

that are needed.

______________________________________________________________________

## Returning Too Much Data

Avoid

```sql
SELECT *
```

if only

two columns

are required.

______________________________________________________________________

## Missing Pagination

Never return

millions of rows

in a single request.

Use

```
LIMIT

OFFSET
```

or

cursor-based pagination.

______________________________________________________________________

# Best Practices

- Index frequently searched columns
- Avoid unnecessary indexes
- Keep transactions short
- Use EXPLAIN for slow queries
- Fetch only required columns
- Use pagination for large datasets

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Driver | psycopg |
| Query Analysis | EXPLAIN |
| Connection Pool | SQLAlchemy Pool |

______________________________________________________________________

# Common Interview Questions

## What happens inside the database after a query is received?

The database parses the SQL, validates it, creates possible execution plans, chooses the most efficient plan, retrieves
data using indexes or table scans, builds the result set, and returns it to the application.

______________________________________________________________________

## What is a Query Optimizer?

The Query Optimizer evaluates multiple execution plans and selects the one with the lowest estimated cost.

______________________________________________________________________

## What is the difference between an Index Scan and a Sequential Scan?

An Index Scan uses an index to locate matching rows efficiently, while a Sequential Scan reads every row in the table.

______________________________________________________________________

## Why is `EXPLAIN ANALYZE` useful?

It shows the actual execution plan and execution time, helping developers identify slow queries and optimization
opportunities.

______________________________________________________________________

## Why shouldn't every column have an index?

Indexes improve read performance but increase storage usage and slow down INSERT, UPDATE, and DELETE operations because
indexes also need to be maintained.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain what happens inside PostgreSQL when a SELECT query is executed.

### Answer

When PostgreSQL receives a query, it parses and validates the SQL, checks that the referenced tables and columns exist,
generates possible execution plans, selects the most efficient plan using the query optimizer, retrieves the required
data using indexes or table scans, applies filters, builds the result set, and returns it through the database driver to
the application.

______________________________________________________________________

# Summary

Database query execution involves much more than simply running SQL.

Key concepts include

- SQL Parsing
- Semantic Analysis
- Query Planner
- Query Optimizer
- Index Scan
- Sequential Scan
- Buffer Cache
- Transactions
- Locks
- Execution Plans

Once the application receives the database results,

it processes the data, builds the final response, serializes it into JSON, and sends it back to the client.

______________________________________________________________________

# Next

[23. Response Serialization and Client Response](23-response-serialization-and-client-response.md)
