# SQLAlchemy Session Management, Connection Pooling & Async - Part 2

## Introduction

In Part 1, we covered:

- Session lifecycle
- Identity Map
- Unit of Work
- Object states
- Connection pooling
- Session methods

In this lecture, we'll cover production topics that are frequently asked in Senior Backend Engineer interviews:

- Async SQLAlchemy
- Async Engine
- AsyncSession
- async_sessionmaker
- FastAPI Integration
- Dependency Injection
- Thread Safety
- Scoped Sessions
- Connection Leaks
- Pool Exhaustion
- Monitoring
- Production Architecture

______________________________________________________________________

# Why Async?

Traditional SQLAlchemy

```text id="asa001"
Request

↓

Database Query

↓

Thread Waits

↓

Response
```

During the database query, the thread waits.

Async SQLAlchemy allows the event loop to work on other requests while waiting for I/O.

Interview Tip

Async does **not** make the database faster.

It improves application scalability by making better use of waiting time.

______________________________________________________________________

# Installing Async Driver

For PostgreSQL

```bash id="asa002"
pip install sqlalchemy psycopg
```

For async support

```bash id="asa003"
pip install "psycopg[binary]"
```

SQLite

```bash id="asa004"
pip install aiosqlite
```

______________________________________________________________________

# Async Database URL

PostgreSQL

```text id="asa005"
postgresql+psycopg://user:password@localhost/company
```

SQLite

```text id="asa006"
sqlite+aiosqlite:///company.db
```

Notice the async SQLite driver.

______________________________________________________________________

# Creating an Async Engine

```python id="asa007"
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(

    DATABASE_URL,

    echo=True,

    pool_pre_ping=True

)
```

This Engine manages asynchronous database connections.

______________________________________________________________________

# Async Session Factory

Recommended pattern

```python id="asa008"
from sqlalchemy.ext.asyncio import (
    async_sessionmaker
)

AsyncSessionLocal = async_sessionmaker(

    engine,

    expire_on_commit=False

)
```

Why `expire_on_commit=False`?

In async applications, immediately reloading expired objects may require another awaited database round trip. Many web
applications disable expiration after commit for convenience, though the right choice depends on your consistency
requirements.

______________________________________________________________________

# Creating an Async Session

```python id="asa009"
async with AsyncSessionLocal() as session:

    ...
```

The context manager automatically returns the connection to the pool.

______________________________________________________________________

# Insert Example

```python id="asa010"
employee = Employee(

    name="Alice",

    salary=80000

)

session.add(employee)

await session.commit()

await session.refresh(employee)
```

Equivalent SQL

```sql id="asa011"
INSERT INTO employees(

name,

salary

)

VALUES(

'Alice',

80000

);
```

______________________________________________________________________

# Query Example

```python id="asa012"
from sqlalchemy import select

stmt = select(Employee)

result = await session.scalars(stmt)

employees = result.all()
```

Equivalent SQL

```sql id="asa013"
SELECT *
FROM employees;
```

______________________________________________________________________

# Query by Primary Key

```python id="asa014"
employee = await session.get(
    Employee,
    1
)
```

Equivalent SQL

```sql id="asa015"
SELECT *
FROM employees
WHERE employee_id = 1;
```

______________________________________________________________________

# Filtering

```python id="asa016"
stmt = (

    select(Employee)

    .where(

        Employee.salary > 90000

    )

)

employees = (

    await session.scalars(stmt)

).all()
```

Equivalent SQL

```sql id="asa017"
SELECT *
FROM employees
WHERE salary > 90000;
```

______________________________________________________________________

# Updating

```python id="asa018"
employee = await session.get(
    Employee,
    1
)

employee.salary = 95000

await session.commit()
```

Equivalent SQL

```sql id="asa019"
UPDATE employees
SET salary = 95000
WHERE employee_id = 1;
```

______________________________________________________________________

# Deleting

```python id="asa020"
employee = await session.get(
    Employee,
    1
)

await session.delete(employee)

await session.commit()
```

Equivalent SQL

```sql id="asa021"
DELETE
FROM employees
WHERE employee_id = 1;
```

______________________________________________________________________

# Async Transactions

Recommended

```python id="asa022"
async with AsyncSessionLocal() as session:

    async with session.begin():

        employee = Employee(
            name="Alice"
        )

        session.add(employee)
```

Automatic

- Commit
- Rollback

______________________________________________________________________

# FastAPI Dependency

Production pattern

```python id="asa023"
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator[
    AsyncSession,
    None
]:

    async with AsyncSessionLocal() as session:

        yield session
```

Usage

```python id="asa024"
from fastapi import Depends

@app.get("/employees")

async def get_employees(

    session: AsyncSession = Depends(get_session)

):

    result = await session.scalars(
        select(Employee)
    )

    return result.all()
```

This is the pattern used in most production FastAPI applications.

______________________________________________________________________

# Engine Lifetime

Create the Engine

Once

```text id="asa025"
Application Starts

↓

Create Engine

↓

Reuse

↓

Application Stops
```

Never

```text id="asa026"
Request

↓

Create Engine

↓

Destroy Engine
```

That is extremely expensive.

______________________________________________________________________

# Session Lifetime

Correct

```text id="asa027"
Request

↓

Session

↓

Commit

↓

Close
```

Incorrect

```text id="asa028"
Application

↓

Single Session

↓

Everything
```

Sessions are **not thread-safe** and should not be shared across requests.

______________________________________________________________________

# Thread Safety

Interview favorite.

Engine

✅ Thread-safe

Session

❌ Not thread-safe

AsyncSession

❌ Not safe to share across concurrent tasks

Each request should receive its own Session or AsyncSession instance.

______________________________________________________________________

# Scoped Sessions

Traditional synchronous applications sometimes use:

```python id="asa029"
from sqlalchemy.orm import scoped_session
```

`scoped_session` provides a registry that gives each thread its own Session.

In modern FastAPI applications, dependency injection is usually preferred over `scoped_session`.

______________________________________________________________________

# Connection Leak

Suppose

```python id="asa030"
session = Session(engine)
```

No

```python id="asa031"
session.close()
```

Eventually

```text id="asa032"
Pool

↓

No Connections

↓

Timeout
```

This is called a **connection leak**.

______________________________________________________________________

# Pool Exhaustion

Suppose

Pool Size

```text id="asa033"
10
```

Requests

```text id="asa034"
500
```

If Sessions are not returned promptly,

every request waits.

Eventually

```text id="asa035"
Timeout
```

Always close Sessions.

______________________________________________________________________

# Detecting Slow Queries

Enable SQL logging

```python id="asa036"
engine = create_async_engine(

    DATABASE_URL,

    echo=True

)
```

Then

- Inspect generated SQL.
- Use `EXPLAIN ANALYZE`.
- Check indexes.
- Measure execution time.

______________________________________________________________________

# Monitoring Connection Pool

Useful metrics:

- Checked-out connections
- Checked-in connections
- Pool utilization
- Average query time
- Transaction duration
- Connection wait time

High connection wait time often indicates pool exhaustion or long-running transactions.

______________________________________________________________________

# Production Architecture

```text id="asa037"
FastAPI

↓

Dependency Injection

↓

AsyncSession

↓

Engine

↓

QueuePool

↓

PostgreSQL
```

Simple.

Scalable.

Production ready.

______________________________________________________________________

# Sync vs Async

| Sync | Async |
| ----------------- | ----------------------- |
| `Session` | `AsyncSession` |
| `create_engine()` | `create_async_engine()` |
| `commit()` | `await commit()` |
| `refresh()` | `await refresh()` |
| `execute()` | `await execute()` |
| `scalars()` | `await scalars()` |

Choose async only if your application architecture benefits from it.

______________________________________________________________________

# Common Mistakes

### Creating Engine Per Request

Wrong

```python id="asa038"
create_async_engine(...)
```

inside every endpoint.

Create one Engine for the application's lifetime.

______________________________________________________________________

### Sharing AsyncSession

One AsyncSession

↓

Many requests

↓

Race conditions

Each request needs its own AsyncSession.

______________________________________________________________________

### Forgetting await

Wrong

```python id="asa039"
session.commit()
```

Correct

```python id="asa040"
await session.commit()
```

______________________________________________________________________

### Long Transactions

Keep transactions short.

Don't perform external API calls while holding an open database transaction.

______________________________________________________________________

### Blocking Code in Async Endpoints

Avoid CPU-intensive work or blocking I/O inside async request handlers.

Move heavy work to background workers when appropriate.

______________________________________________________________________

# Best Practices

- Create one Engine for the application.
- Create one Session or AsyncSession per request.
- Use dependency injection.
- Keep transactions short.
- Enable `pool_pre_ping`.
- Always close Sessions.
- Understand generated SQL.
- Measure before optimizing.
- Prefer async only when the application architecture benefits.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is `Session` not thread-safe?

A Session maintains mutable state, including the Identity Map, pending changes, transaction state, and ORM-managed
objects. If multiple threads or concurrent tasks modify the same Session simultaneously, its internal state can become
inconsistent, leading to race conditions and incorrect behavior. Therefore, SQLAlchemy recommends creating a separate
Session (or AsyncSession) for each request or unit of work while sharing a single Engine across the application.

______________________________________________________________________

# Practice Questions

## Conceptual

1. Why use Async SQLAlchemy?
1. What is an AsyncEngine?
1. What is an AsyncSession?
1. Why use `async_sessionmaker()`?
1. Why create one Engine?
1. Why create one Session per request?
1. Why isn't Session thread-safe?
1. What is a connection leak?
1. What is pool exhaustion?
1. Why use dependency injection?

## Coding

1. Create an AsyncEngine.
1. Configure an AsyncSession factory.
1. Insert a row asynchronously.
1. Retrieve employees asynchronously.
1. Build a FastAPI dependency for AsyncSession.
1. Implement an async transaction using `session.begin()`.

______________________________________________________________________

# Hands-on Exercise

Build an asynchronous Employee Management API.

Requirements:

1. Configure an AsyncEngine.
1. Configure `async_sessionmaker`.
1. Implement CRUD operations.
1. Build FastAPI dependency injection.
1. Measure generated SQL.
1. Simulate connection leaks and fix them.
1. Compare sync and async implementations.
1. Monitor connection pool behavior.

______________________________________________________________________

# Cheat Sheet

```text id="asa041"
create_async_engine()

↓

async_sessionmaker()

↓

AsyncSession

↓

await commit()

↓

await refresh()

↓

Dependency Injection

↓

Engine

↓

QueuePool

↓

PostgreSQL
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Async SQLAlchemy architecture
- AsyncEngine
- AsyncSession
- `async_sessionmaker`
- Async CRUD
- Async transactions
- FastAPI dependency injection
- Engine lifetime
- Session lifetime
- Thread safety
- Scoped sessions
- Connection leaks
- Pool exhaustion
- Monitoring
- Production architecture
- Sync vs Async
- Best practices
- Interview patterns

You now understand how SQLAlchemy is used in modern production applications, both synchronously and asynchronously, and
how to design safe, scalable database access layers.

______________________________________________________________________

## Next File

[24-sql-library-management-project-part-1.md](24-sql-library-management-project-part-1.md)
