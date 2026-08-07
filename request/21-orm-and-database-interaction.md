# Complete HTTP Request Lifecycle Deep Dive

## 21. ORM and Database Interaction

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand how the Business Logic Layer interacts with the database using an ORM, how SQLAlchemy works, the lifecycle of a database query, and best practices for efficient and secure database access.

______________________________________________________________________

# Introduction

In the previous chapter,

the request reached

the

Business Logic Layer.

Suppose

the application

needs

user information.

It now needs

to communicate

with

the database.

Instead of writing

raw SQL

everywhere,

most modern applications

use an

```
ORM
```

______________________________________________________________________

# High Level Flow

```
Business Logic

↓

Repository

↓

ORM

↓

Database Driver

↓

PostgreSQL

↓

Database Driver

↓

ORM

↓

Business Logic
```

______________________________________________________________________

# What is an ORM?

Interview favorite.

ORM stands for

```
Object Relational Mapper
```

It allows developers

to work with

Python objects

instead of

writing SQL

for every operation.

______________________________________________________________________

# Without ORM

```python
cursor.execute(
    """
    SELECT *

    FROM users

    WHERE id = 1
    """
)
```

______________________________________________________________________

# With ORM

```python
user = session.get(User, 1)
```

Much simpler

and easier

to maintain.

______________________________________________________________________

# Popular Python ORMs

- SQLAlchemy
- Django ORM
- Peewee
- Tortoise ORM

FastAPI

most commonly uses

```
SQLAlchemy
```

______________________________________________________________________

# ORM Architecture

```
Application

↓

Repository

↓

SQLAlchemy

↓

Database Driver

↓

PostgreSQL
```

______________________________________________________________________

# Why Use an ORM?

Benefits

- Less boilerplate
- Database abstraction
- Easier maintenance
- Parameterized queries
- Better readability
- Relationship management

______________________________________________________________________

# ORM Models

Example

```python
class User(Base):

    __tablename__ = "users"

    id = Column(Integer)

    name = Column(String)

    email = Column(String)
```

Each object

maps

to

a database row.

______________________________________________________________________

# CRUD Operations

Interview favorite.

```
Create

↓

Insert
```

```
Read

↓

Select
```

```
Update

↓

Update
```

```
Delete

↓

Delete
```

______________________________________________________________________

# Create Example

```python
user = User(
    name="Riyaz",
    email="riyaz@gmail.com"
)

session.add(user)

session.commit()
```

______________________________________________________________________

# Read Example

```python
user = session.get(User, 1)
```

Equivalent SQL

```sql
SELECT *

FROM users

WHERE id = 1;
```

______________________________________________________________________

# Update Example

```python
user.name = "John"

session.commit()
```

______________________________________________________________________

# Delete Example

```python
session.delete(user)

session.commit()
```

______________________________________________________________________

# Query Lifecycle

```
Python Object

↓

SQLAlchemy

↓

SQL Query

↓

Database Driver

↓

PostgreSQL

↓

Result Set

↓

Python Object
```

______________________________________________________________________

# Repository Pattern

Interview favorite.

Instead of

calling

SQLAlchemy

directly

inside

Business Logic,

many applications

use

Repositories.

```
Business Logic

↓

UserRepository

↓

SQLAlchemy

↓

Database
```

______________________________________________________________________

# Why Repository Pattern?

Benefits

- Cleaner architecture
- Easier testing
- Database abstraction
- Reusable queries

______________________________________________________________________

# Filtering

Example

```python
users = (
    session.query(User)
    .filter(
        User.age > 18
    )
)
```

Equivalent SQL

```sql
SELECT *

FROM users

WHERE age > 18;
```

______________________________________________________________________

# Sorting

```python
.order_by(User.name)
```

Equivalent SQL

```sql
ORDER BY name
```

______________________________________________________________________

# Pagination

Interview favorite.

Never return

millions

of rows.

Use

```python
.limit(20)

.offset(40)
```

Equivalent SQL

```sql
LIMIT 20

OFFSET 40
```

______________________________________________________________________

# Relationships

Example

```
User

↓

Orders
```

One user

may have

many orders.

```python
user.orders
```

SQLAlchemy

loads

related objects.

______________________________________________________________________

# Lazy Loading

Interview favorite.

Related data

is loaded

only when needed.

```
User

↓

Orders?

↓

Load Now
```

Benefits

- Less memory
- Faster queries

______________________________________________________________________

# Eager Loading

Instead of

multiple queries,

load everything

at once.

Useful

when

related data

is definitely needed.

______________________________________________________________________

# Transactions

Business Logic

may perform

multiple operations.

```
Create Order

↓

Reduce Inventory

↓

Create Payment
```

All succeed

or

everything rolls back.

______________________________________________________________________

# Commit

```python
session.commit()
```

Permanently saves

changes

to the database.

______________________________________________________________________

# Rollback

Suppose

an error occurs.

```python
session.rollback()
```

All pending changes

are discarded.

______________________________________________________________________

# Connection Pooling

Interview favorite.

Opening

a new database connection

for every request

is expensive.

Instead,

SQLAlchemy

maintains

a pool

of reusable connections.

```
Application

↓

Connection Pool

↓

Database
```

Benefits

- Faster requests
- Lower overhead
- Better scalability

______________________________________________________________________

# Parameterized Queries

Interview favorite.

ORMs

automatically use

parameterized queries.

This helps prevent

SQL Injection.

Example

Instead of

```sql
WHERE name = 'Riyaz'
```

the value

is sent

as a parameter,

not concatenated

into the SQL string.

______________________________________________________________________

# Common Mistakes

## Forgetting Commit

Without

```python
session.commit()
```

changes

are not saved.

______________________________________________________________________

## Loading Too Much Data

Avoid

```
SELECT *
```

when only

a few columns

are needed.

______________________________________________________________________

## N+1 Query Problem

Interview favorite.

Suppose

you load

100 users.

Then

for each user,

you load

their orders.

```
1 Query

↓

100 Queries
```

Total

```
101 Queries
```

Solution

Use

eager loading

when appropriate.

______________________________________________________________________

## Long Transactions

Keep transactions

short.

Long transactions

can lock rows

and reduce performance.

______________________________________________________________________

# Best Practices

- Use repositories or services
- Keep transactions short
- Use pagination
- Avoid N+1 queries
- Reuse database connections
- Use indexes effectively
- Always handle exceptions

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| ORM | SQLAlchemy |
| Driver | psycopg |
| Database | PostgreSQL |
| Connection Pool | SQLAlchemy Pool |
| Migrations | Alembic |

______________________________________________________________________

# Common Interview Questions

## What is an ORM?

An ORM maps database tables to programming language objects, allowing developers to work with objects instead of writing
raw SQL for every operation.

______________________________________________________________________

## Why use SQLAlchemy?

SQLAlchemy provides powerful ORM capabilities, supports multiple databases, uses parameterized queries, manages
relationships, and integrates well with FastAPI.

______________________________________________________________________

## What is the Repository Pattern?

The Repository Pattern separates database access from business logic, making applications easier to test, maintain, and
extend.

______________________________________________________________________

## What is the N+1 Query Problem?

The N+1 Query Problem occurs when one query retrieves a list of objects and additional queries are executed for each
object to load related data, causing unnecessary database calls.

______________________________________________________________________

## Why use Connection Pooling?

Connection pooling avoids creating a new database connection for every request, reducing latency and improving
scalability.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain how a FastAPI application retrieves data from a database using SQLAlchemy.

### Answer

The Business Logic Layer calls a repository, which uses SQLAlchemy to build a database query. SQLAlchemy translates the
Python query into SQL, sends it through the database driver to PostgreSQL, receives the result set, converts the rows
into Python objects, and returns them to the business logic. The application then processes the data and prepares the
response.

______________________________________________________________________

# Summary

ORMs simplify

database interaction

by mapping

database tables

to Python objects.

Using SQLAlchemy,

applications can

perform CRUD operations,

manage relationships,

handle transactions,

and safely execute queries

without writing SQL for every operation.

After the ORM sends a query,

the next step is understanding

**how the database actually executes that query**, including parsing, planning, indexing, and retrieving data.

______________________________________________________________________

# Next

[22. Database Query Execution](22-database-query-execution.md)
