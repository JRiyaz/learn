# Database Integration (SQLAlchemy)

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 9 - Database Integration
>
> **File:** `30_database_integration_sqlalchemy.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why ORM is Needed
- What SQLAlchemy is
- SQLAlchemy Architecture
- Engine
- Session
- Models
- Declarative Base
- Database Lifecycle
- FastAPI Integration
- Production Best Practices

______________________________________________________________________

# Why Database Integration?

Most backend applications need persistent storage.

Examples

- Users
- Orders
- Products
- Payments
- Logs

Flow

```
Client

↓

FastAPI

↓

Database

↓

Response
```

______________________________________________________________________

# Without an ORM

Raw SQL

```sql
SELECT *

FROM users

WHERE id = 1;
```

Application

↓

String Construction

↓

Manual Mapping

↓

Python Objects

More code,

more opportunities for errors.

______________________________________________________________________

# What is an ORM?

ORM stands for

```
Object Relational Mapper
```

It maps

```
Python Objects

↓

Database Tables
```

Instead of writing SQL everywhere,

you work with Python classes.

______________________________________________________________________

# ORM Mapping

```
Python Class

↓

User

↓

Database Table

↓

users
```

Object

```
User(name="Riyaz")
```

↓

Row

```
users
```

______________________________________________________________________

# What is SQLAlchemy?

SQLAlchemy is Python's most widely used ORM and SQL toolkit.

It provides

- ORM
- SQL Expression Language
- Connection Management
- Session Management
- Database Abstraction

FastAPI commonly uses SQLAlchemy for relational databases.

______________________________________________________________________

# SQLAlchemy Components

```
Application

↓

Session

↓

Engine

↓

Database
```

______________________________________________________________________

# Engine

The **Engine** manages database connectivity.

Example

```python
from sqlalchemy import create_engine
```

```python
engine = create_engine(

    DATABASE_URL
)
```

The engine knows

- Which database to connect to
- Connection pooling
- Driver configuration

______________________________________________________________________

# DATABASE_URL

Examples

SQLite

```text
sqlite:///app.db
```

PostgreSQL

```text
postgresql+psycopg://user:password@localhost/db
```

MySQL

```text
mysql+pymysql://user:password@localhost/db
```

______________________________________________________________________

# Declarative Base

Models inherit from a common base.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(

    DeclarativeBase

):

    pass
```

Every ORM model inherits from `Base`.

______________________________________________________________________

# Creating a Model

```python
from sqlalchemy import Integer

from sqlalchemy import String

from sqlalchemy.orm import Mapped

from sqlalchemy.orm import mapped_column
```

```python
class User(

    Base

):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True

    )

    name: Mapped[str] = mapped_column(

        String
    )
```

The class maps directly to the `users` table.

______________________________________________________________________

# Table Mapping

```
Python

↓

User

↓

SQLAlchemy

↓

users Table
```

______________________________________________________________________

# Session

A **Session** represents a conversation with the database.

```
Session

↓

Query

↓

Insert

↓

Update

↓

Delete

↓

Commit
```

______________________________________________________________________

# Creating a Session Factory

```python
from sqlalchemy.orm import sessionmaker
```

```python
SessionLocal = sessionmaker(

    bind=engine
)
```

Each request typically creates its own session.

______________________________________________________________________

# FastAPI Dependency

```python
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
```

This is the standard FastAPI pattern.

______________________________________________________________________

# Dependency Flow

```
Request

↓

get_db()

↓

Session

↓

Route

↓

Close Session
```

______________________________________________________________________

# CRUD Example

Insert

```python
db.add(user)
```

Commit

```python
db.commit()
```

Refresh

```python
db.refresh(user)
```

These operations persist the new object and synchronize it with the database.

______________________________________________________________________

# Query Example

```python
user = db.get(

    User,

    1
)
```

or

```python
from sqlalchemy import select

user = db.execute(

    select(User)

).scalar_one_or_none()
```

SQLAlchemy 2.x encourages the `select()` style.

______________________________________________________________________

# Update Example

```
Query

↓

Modify Object

↓

Commit
```

```python
user.name = "Riyaz"

db.commit()
```

______________________________________________________________________

# Delete Example

```python
db.delete(

    user
)

db.commit()
```

______________________________________________________________________

# Transaction Flow

```
Session

↓

Changes

↓

Commit

↓

Database Updated
```

or

```
Session

↓

Error

↓

Rollback
```

______________________________________________________________________

# Why Use Sessions?

Sessions provide

- Transaction Management
- Identity Map
- Change Tracking
- Connection Management

Without sessions,

every SQL operation must be managed manually.

______________________________________________________________________

# Identity Map

Within a session

```
User ID 1

↓

Loaded Once

↓

Reused
```

Avoids unnecessary duplicate objects.

______________________________________________________________________

# Connection Pooling

```
Application

↓

Engine

↓

Connection Pool

↓

Database
```

Connections are reused instead of recreated.

This improves performance.

______________________________________________________________________

# Layered Architecture

```
Route

↓

Service

↓

Repository

↓

Session

↓

Database
```

Routes should not contain SQL queries.

______________________________________________________________________

# SQLAlchemy vs Raw SQL

| SQLAlchemy | Raw SQL |
|------------|----------|
| Python Objects | SQL Strings |
| Type Safety | Manual Mapping |
| ORM Support | Full Control |
| Portable | Database Specific |

Both approaches have valid use cases.

______________________________________________________________________

# Common Mistakes

❌ Creating one global session for the entire application

❌ Forgetting to close sessions

❌ Performing database queries directly inside routes

❌ Ignoring transactions

❌ Mixing ORM models with API response models

______________________________________________________________________

# Production Best Practices

- Use one session per request.
- Manage sessions with dependency injection.
- Separate ORM models from Pydantic schemas.
- Use transactions appropriately.
- Keep SQL inside repositories or data-access layers.
- Reuse connections through pooling.
- Close sessions reliably using `yield`.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why does FastAPI typically create one SQLAlchemy session per request instead of using a global session?**

### Answer

A SQLAlchemy session is **not thread-safe** and represents a single unit of work.

Creating one session per request provides:

- Isolation between concurrent requests.
- Proper transaction boundaries.
- Reliable cleanup.
- Better error handling.
- Safe concurrent execution.

A global shared session could cause data corruption, stale state, transaction conflicts, and concurrency issues.

______________________________________________________________________

# Summary

In this chapter you learned:

- ORM
- SQLAlchemy
- Engine
- Declarative Base
- Models
- Sessions
- CRUD Operations
- Transactions
- Connection Pooling
- Production Best Practices

SQLAlchemy provides a robust and scalable way to interact with relational databases, while FastAPI's dependency
injection makes request-scoped session management clean and reliable.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is an ORM?
1. Why are ORMs useful?
1. What is SQLAlchemy?

______________________________________________________________________

## Components

4. What is the purpose of the SQLAlchemy engine?
1. What is a session?
1. Why do models inherit from `DeclarativeBase`?

______________________________________________________________________

## CRUD

7. How do you insert a record?
1. How do you query a record?
1. How do you update a record?
1. How do you delete a record?

______________________________________________________________________

## Architecture

11. Why should database sessions be created per request?
01. Why should SQL queries stay out of route handlers?
01. Why should ORM models be separated from API schemas?

______________________________________________________________________

## Production

14. What is connection pooling?
01. Why should transactions be committed or rolled back explicitly?

______________________________________________________________________

## Scenario-Based

16. Your application shares one global SQLAlchemy session across all requests. What concurrency problems could occur?
01. A route opens a database session but never closes it. What issues might develop over time?
01. Your API directly returns SQLAlchemy ORM objects to clients. Why is this discouraged, and what should be returned instead?
01. Your application performs all SQL queries directly inside route handlers. How would introducing service and repository layers improve the architecture?
01. Your application experiences a database error halfway through creating an order. Why is transaction management important, and what should happen to the partially completed changes?

______________________________________________________________________

# Next

[SQLAlchemy Relationships & CRUD Patterns](31_sqlalchemy_relationships_crud.md)
