# SQLAlchemy Session Management, Connection Pooling & Async - Part 1

## Introduction

If someone asks,

> **"What exactly happens when you call `session.commit()`?"**

or

> **"How does SQLAlchemy manage database connections?"**

this lecture answers those questions.

Most developers learn CRUD.

Very few learn how SQLAlchemy actually works internally.

Understanding Sessions, Connection Pools and Object States separates a **Senior Backend Engineer** from someone who only
knows ORM syntax.

This chapter covers:

- Session Lifecycle
- Object States
- Identity Map
- Unit of Work
- Flush vs Commit
- Refresh
- Expire
- Merge
- Rollback
- Closing Sessions
- Connection Pooling
- Production Patterns

______________________________________________________________________

# SQLAlchemy Architecture

Understanding this diagram is extremely important.

```text id="saint001"
Application

↓

Session

↓

Identity Map

↓

Unit Of Work

↓

Engine

↓

Connection Pool

↓

Database Connection

↓

PostgreSQL
```

Every ORM operation passes through these layers.

______________________________________________________________________

# What is a Session?

A Session is **not** a database connection.

A Session is an ORM object responsible for

- Managing ORM objects
- Tracking changes
- Managing transactions
- Coordinating with the Engine
- Maintaining the Identity Map

Interview Tip

One of the most common interview mistakes is saying

> "Session is a database connection."

It is **not**.

______________________________________________________________________

# Session Lifecycle

A production request usually follows this lifecycle.

```text id="saint002"
Create Session

↓

Execute Queries

↓

Track Changes

↓

Flush

↓

Commit

↓

Close
```

After closing, the Session should no longer be used.

______________________________________________________________________

# Creating a Session

```python id="saint003"
from sqlalchemy.orm import Session

with Session(engine) as session:

    ...
```

Recommended.

The context manager ensures the Session is closed.

______________________________________________________________________

# Manual Session

```python id="saint004"
session = Session(engine)

try:

    ...

    session.commit()

finally:

    session.close()
```

Useful when explicit control is needed.

______________________________________________________________________

# Why Close Sessions?

A Session may hold:

- Database connections
- ORM objects
- Transaction state

If Sessions remain open

↓

Connections remain checked out

↓

Connection Pool exhaustion

↓

Application slowdown

______________________________________________________________________

# Session vs Connection

| Session | Connection |
| --------------------------- | -------------------------- |
| ORM abstraction | Physical DB connection |
| Tracks objects | Executes SQL |
| Unit of Work | Low-level communication |
| Uses connections internally | Talks directly to database |

______________________________________________________________________

# Object States

Every ORM object exists in one of several states.

```text id="saint005"
Transient

↓

Pending

↓

Persistent

↓

Detached

↓

Deleted
```

Interview favorite.

______________________________________________________________________

# Transient

Object exists only in Python.

```python id="saint006"
employee = Employee(
    name="Alice"
)
```

No Session.

No SQL.

No database row.

______________________________________________________________________

# Pending

```python id="saint007"
session.add(employee)
```

Now SQLAlchemy knows about it.

Still

No INSERT executed.

______________________________________________________________________

# Persistent

```python id="saint008"
session.commit()
```

Object now exists in database.

SQL executed

```sql id="saint009"
INSERT INTO employees ...
```

______________________________________________________________________

# Detached

```python id="saint010"
session.close()
```

Object still exists.

Session doesn't.

Accessing unloaded relationships may fail because there is no active Session available to load additional data.

______________________________________________________________________

# Deleted

```python id="saint011"
session.delete(employee)

session.commit()
```

Object removed from database.

______________________________________________________________________

# Identity Map

SQLAlchemy keeps one Python object for one database row.

Example

```python id="saint012"
a = session.get(Employee, 1)

b = session.get(Employee, 1)
```

```python id="saint013"
print(a is b)
```

Output

```text id="saint014"
True
```

No duplicate objects.

______________________________________________________________________

# Why Identity Map Exists

Without Identity Map

```text id="saint015"
Employee #1

↓

Loaded Twice

↓

Two Python Objects
```

Updating one would not automatically update the other.

Identity Map prevents this.

______________________________________________________________________

# Unit of Work

Tracks every modification.

Example

```python id="saint016"
employee.salary = 90000
```

SQL not executed yet.

Changes are collected.

During

```python id="saint017"
session.commit()
```

SQLAlchemy generates

```sql id="saint018"
UPDATE employees
SET salary=90000
WHERE employee_id=1;
```

______________________________________________________________________

# Flush

```python id="saint019"
session.flush()
```

Flush sends SQL.

Transaction remains open.

Example

```python id="saint020"
employee = Employee(name="Alice")

session.add(employee)

session.flush()

print(employee.employee_id)
```

Primary key is now available before commit because the INSERT has been issued.

______________________________________________________________________

# Commit

```python id="saint021"
session.commit()
```

Commit

- Flushes pending changes (if needed)
- Ends the transaction
- Makes changes permanent

______________________________________________________________________

# Flush vs Commit

| Flush | Commit |
| ------------------------ | --------------------------- |
| Sends SQL | Makes transaction permanent |
| Transaction remains open | Transaction ends |
| Can still rollback | Finalizes changes |

Interview favorite.

______________________________________________________________________

# Rollback

```python id="saint022"
try:

    ...

    session.commit()

except:

    session.rollback()

    raise
```

Rollback undoes all uncommitted work in the current transaction.

______________________________________________________________________

# Refresh

Suppose

Database trigger updates salary.

Python object

Still old.

Use

```python id="saint023"
session.refresh(employee)
```

Now object reloads from database.

______________________________________________________________________

# Expire

```python id="saint024"
session.expire(employee)
```

Marks object as expired.

Next attribute access

↓

Automatically reloads from database.

______________________________________________________________________

# expire_all()

```python id="saint025"
session.expire_all()
```

Expires every loaded ORM object.

Useful after external changes to ensure fresh reads.

______________________________________________________________________

# Merge

Suppose

Object comes from another Session.

```python id="saint026"
merged = session.merge(employee)
```

SQLAlchemy returns a managed instance associated with the current Session.

______________________________________________________________________

# Expunge

```python id="saint027"
session.expunge(employee)
```

Removes the object from the Session.

The object becomes detached.

______________________________________________________________________

# Closing Sessions

```python id="saint028"
session.close()
```

Releases ORM resources and returns any checked-out connection to the pool.

Closing a Session does **not** delete data.

______________________________________________________________________

# Session.begin()

Instead of

```python id="saint029"
session.commit()
```

You can write

```python id="saint030"
with Session(engine) as session:

    with session.begin():

        employee.salary = 95000
```

Automatic

- Commit on success
- Rollback on failure

Preferred for many transactional operations.

______________________________________________________________________

# Nested Transactions

Using SAVEPOINT

```python id="saint031"
with session.begin():

    with session.begin_nested():

        ...
```

Equivalent SQL

```sql id="saint032"
SAVEPOINT ...

ROLLBACK TO SAVEPOINT ...
```

Useful for partial rollback scenarios and testing.

______________________________________________________________________

# Connection Pool

Creating database connections is expensive.

SQLAlchemy reuses them.

```text id="saint033"
Application

↓

Pool

↓

Database
```

Instead of

```text id="saint034"
New Connection

Every Query
```

______________________________________________________________________

# Creating a Pool

```python id="saint035"
from sqlalchemy import create_engine

engine = create_engine(

    DATABASE_URL,

    pool_size=10,

    max_overflow=20

)
```

______________________________________________________________________

# pool_size

```python id="saint036"
pool_size=10
```

Keep

10

connections ready.

______________________________________________________________________

# max_overflow

```python id="saint037"
max_overflow=20
```

Pool may temporarily create

20

additional connections.

Maximum simultaneous connections

```text id="saint038"
30
```

______________________________________________________________________

# pool_timeout

```python id="saint039"
pool_timeout=30
```

Wait up to

30 seconds

for a free connection.

If none becomes available, SQLAlchemy raises a timeout error.

______________________________________________________________________

# pool_recycle

```python id="saint040"
pool_recycle=1800
```

Recycle connections every

30 minutes.

Useful for databases that automatically close idle connections.

______________________________________________________________________

# pool_pre_ping

```python id="saint041"
pool_pre_ping=True
```

Before using a pooled connection,

SQLAlchemy checks whether it is still alive.

If not,

it reconnects automatically.

Highly recommended for production.

______________________________________________________________________

# QueuePool

Default pool.

```text id="saint042"
Request

↓

QueuePool

↓

Database
```

Most applications should use it.

______________________________________________________________________

# NullPool

```python id="saint043"
poolclass=NullPool
```

No pooling.

Every Session opens and closes a new connection.

Useful for certain scripts or serverless workloads where persistent pools are not desirable.

______________________________________________________________________

# Common Mistakes

### Global Session

```python id="saint044"
session = Session(engine)
```

Never share one Session across requests.

______________________________________________________________________

### Not Closing Sessions

Connections remain checked out.

Eventually

Pool exhaustion.

______________________________________________________________________

### Long Transactions

Bad

```text id="saint045"
BEGIN

↓

User Thinks

↓

10 Minutes

↓

COMMIT
```

Keep transactions short.

______________________________________________________________________

### Calling Commit Too Frequently

Commit only when a logical unit of work is complete.

______________________________________________________________________

# Best Practices

- One Engine per application.
- One Session per request or unit of work.
- Keep transactions short.
- Always rollback on exceptions.
- Always close Sessions.
- Enable `pool_pre_ping` in production.
- Understand object states and the Identity Map.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Explain what happens internally when `session.commit()` is called.

`session.commit()` first performs an automatic flush if there are pending changes. During the flush, SQLAlchemy's Unit
of Work determines which INSERT, UPDATE, and DELETE statements need to be executed and sends them to the database within
the current transaction. If all statements succeed, the database commits the transaction, making the changes permanent.
If an error occurs before the commit completes, the transaction can be rolled back. Depending on the Session
configuration, ORM objects may then be expired so that future attribute access retrieves fresh values from the database.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a Session?
1. Session vs Connection.
1. Explain the Session lifecycle.
1. What is the Identity Map?
1. What is the Unit of Work?
1. Explain object states.
1. Difference between `flush()` and `commit()`.
1. What does `refresh()` do?
1. What does `expire()` do?
1. What does `merge()` do?
1. Why close Sessions?
1. What is a connection pool?
1. Explain `pool_size`.
1. Explain `max_overflow`.
1. Why use `pool_pre_ping`?

## Coding

1. Create a Session using a context manager.
1. Demonstrate `flush()` before `commit()`.
1. Refresh an ORM object.
1. Merge a detached object.
1. Configure an Engine with connection pooling.
1. Demonstrate nested transactions.

______________________________________________________________________

# Hands-on Exercise

1. Build a small CRUD application.
1. Print object states at each stage.
1. Compare `flush()` vs `commit()`.
1. Experiment with `expire()` and `refresh()`.
1. Configure `pool_size`, `max_overflow`, `pool_timeout`, and `pool_pre_ping`.
1. Observe connection behavior under concurrent requests.

______________________________________________________________________

# Cheat Sheet

```text id="saint046"
Session

↓

Identity Map

↓

Unit of Work

↓

Transient

↓

Pending

↓

Persistent

↓

Detached

↓

Deleted

↓

flush()

↓

commit()

↓

rollback()

↓

refresh()

↓

expire()

↓

merge()

↓

Connection Pool
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Session architecture
- Session lifecycle
- Object states
- Identity Map
- Unit of Work
- `flush()`
- `commit()`
- `rollback()`
- `refresh()`
- `expire()`
- `expire_all()`
- `merge()`
- `expunge()`
- `Session.begin()`
- Nested transactions
- Connection pooling
- Pool configuration
- Production best practices
- Interview patterns

______________________________________________________________________

## Next File

[SQLAlchemy Session Management, Connection Pooling & Async - Part 2](23-sqlalchemy-session-management-async-part-2.md)
