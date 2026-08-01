# Software Architecture - Part 31

# Clean Architecture

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Clean Architecture is
- Why Clean Architecture exists
- The problems it solves
- The Dependency Rule
- Layers of Clean Architecture
- FastAPI project structure
- Dependency Injection in Clean Architecture
- How it differs from Layered Architecture
- When NOT to use Clean Architecture

______________________________________________________________________

# Before We Start

This is one of the **most important topics** for becoming a **Senior Backend Engineer**.

Many developers learn:

- SOLID
- Design Patterns
- Dependency Injection
- Repository Pattern

But they don't know

how everything fits together

inside a real project.

**Clean Architecture** answers that question.

It tells us

where code belongs,

how dependencies should flow,

and how to build applications

that are easy to maintain,

test,

and extend.

______________________________________________________________________

# The Problem

Let's continue with our

**Library Management System**.

A typical beginner project

looks like this.

```python id="clean3101"
@app.post("/books")
def create_book():

    data = request.json()

    book = Book(**data)

    db.add(book)

    db.commit()

    send_email()

    kafka.publish()

    redis.delete()

    return {
        "status": "success"
    }
```

Everything

is inside

one function.

______________________________________________________________________

# Six Months Later

The application grows.

Now,

every endpoint contains:

- Authentication
- Validation
- SQLAlchemy
- Business Rules
- Email
- Redis
- Kafka
- Logging
- Metrics

The project

becomes

very difficult

to maintain.

______________________________________________________________________

# Another Problem

Suppose

the company says:

> Replace PostgreSQL with MongoDB.

How many files change?

Maybe hundreds.

______________________________________________________________________

# Another Requirement

Now,

the company says:

> Replace FastAPI with Django.

Again,

business logic

must change.

Should it?

No.

Business rules

shouldn't care

about:

- Database
- Framework
- Cache
- Message Queue

______________________________________________________________________

# The Core Idea

Instead of

building

the application

around

the framework,

build it

around

the business.

Everything else

becomes

a plugin.

______________________________________________________________________

# What is Clean Architecture?

Clean Architecture,

introduced by

Robert C. Martin,

states:

> **Business rules should be independent of frameworks, databases, and external systems.**

Your application

should continue working

even if

you replace:

- FastAPI
- PostgreSQL
- Redis
- Kafka
- AWS

______________________________________________________________________

# The Dependency Rule

This is

the most important rule.

> **Dependencies always point inward.**

Outer layers

can depend

on inner layers.

Inner layers

must never

depend

on outer layers.

Remember this.

Everything else

follows

from this rule.

______________________________________________________________________

# The Architecture

```text id="clean3102"
          Frameworks

               ↓

      Interface Adapters

               ↓

      Application Layer

               ↓

          Domain Layer
```

The arrows

always point

toward

the center.

______________________________________________________________________

# Layer 1

## Domain Layer

This is

the heart

of the application.

It contains:

- Entities
- Business Rules
- Value Objects
- Domain Services

It knows

nothing

about:

- FastAPI
- SQLAlchemy
- Redis
- Kafka
- HTTP

Example

```python id="clean3103"
class Book:

    def __init__(

        self,

        title,

        author,

    ):

        self.title = title

        self.author = author
```

Pure Python.

______________________________________________________________________

# Layer 2

## Application Layer

Contains

use cases.

Examples:

- Borrow Book
- Return Book
- Register Member
- Pay Fine

Example

```python id="clean3104"
class BorrowBookUseCase:

    def execute(

        self,

        command,

    ):

        ...
```

Notice

there is

still

no FastAPI,

no SQLAlchemy.

Only

business workflows.

______________________________________________________________________

# Layer 3

## Interface Adapters

This layer

translates

between

the application

and

the outside world.

Examples:

- Repositories
- Controllers
- DTOs
- Presenters
- API Models

Example

```python id="clean3105"
class BookRepository:

    def save(
        self,
        book,
    ):
        ...
```

______________________________________________________________________

# Layer 4

## Framework Layer

This is

the outermost layer.

Examples:

- FastAPI
- SQLAlchemy
- Redis
- Kafka
- Celery

Example

```python id="clean3106"
@app.post("/books")
```

Frameworks

live here.

______________________________________________________________________

# Dependency Direction

Notice

what depends

on what.

```text id="clean3107"
FastAPI

↓

Use Case

↓

Repository Interface

↓

Domain
```

Not

the other way around.

______________________________________________________________________

# Repository Interfaces

Inside

the Application Layer

define

an abstraction.

```python id="clean3108"
from abc import (
    ABC,
    abstractmethod,
)

class BookRepository(
    ABC
):

    @abstractmethod
    def save(
        self,
        book,
    ):
        ...
```

The application

depends

on

the interface.

______________________________________________________________________

# Repository Implementation

Outside

the application,

implement

the interface.

```python id="clean3109"
class SQLBookRepository(

    BookRepository

):

    def save(
        self,
        book,
    ):

        self.session.add(book)

        self.session.commit()
```

The application

never knows

SQLAlchemy exists.

______________________________________________________________________

# FastAPI Endpoint

The endpoint

becomes

very small.

```python id="clean3110"
@app.post("/books")
def create_book(

    use_case=Depends(
        get_use_case
    ),

):

    return use_case.execute(...)
```

Notice

the endpoint

contains

almost

no business logic.

______________________________________________________________________

# Project Structure

A common

FastAPI structure.

```text id="clean3111"
app/

├── domain/

│   ├── entities/

│   ├── value_objects/

│   └── exceptions/

├── application/

│   ├── use_cases/

│   ├── dto/

│   └── interfaces/

├── infrastructure/

│   ├── database/

│   ├── repositories/

│   ├── cache/

│   └── messaging/

├── api/

│   ├── routers/

│   ├── schemas/

│   └── dependencies/

└── main.py
```

This layout

keeps

responsibilities

separate.

______________________________________________________________________

# Dependency Injection

Clean Architecture

works

beautifully

with DI.

Example

```python id="clean3112"
repository = SQLBookRepository()

use_case = BorrowBookUseCase(
    repository
)
```

The use case

receives

its dependencies.

It doesn't

create them.

______________________________________________________________________

# Testing

Testing

becomes simple.

Instead of

a real database,

inject

a fake repository.

```python id="clean3113"
class FakeRepository(
    BookRepository
):

    def save(
        self,
        book,
    ):
        pass
```

Now,

the use case

can be tested

without

PostgreSQL,

Redis,

or Kafka.

______________________________________________________________________

# Real Backend Example

Suppose

today

you use

```text id="clean3114"
PostgreSQL
```

Tomorrow

the company

moves to

```text id="clean3115"
MongoDB
```

Which layer changes?

Only

the repository implementation.

Business logic

remains untouched.

______________________________________________________________________

# Another Example

Suppose

today

you expose

REST APIs.

Tomorrow

you need

GraphQL.

Only

the API layer

changes.

The domain

and use cases

remain exactly the same.

______________________________________________________________________

# Clean Architecture vs Layered Architecture

This is

an interview favorite.

| Layered Architecture | Clean Architecture |
| ---------------------------------------------- | ---------------------------------------- |
| Dependencies often flow downward | Dependencies always point inward |
| Business logic often depends on infrastructure | Infrastructure depends on business logic |
| Easier to start | Easier to maintain at scale |

______________________________________________________________________

# Benefits

Clean Architecture gives you:

✅ Framework independence

✅ Database independence

✅ High testability

✅ Clear separation of concerns

✅ Easier long-term maintenance

______________________________________________________________________

# Drawbacks

It also introduces:

❌ More folders

❌ More abstractions

❌ More boilerplate

For small projects,

it may feel

like overengineering.

______________________________________________________________________

# When NOT to Use Clean Architecture

Suppose

you're building

a weekend project

with

three endpoints.

Creating

four layers,

interfaces,

and repositories

may slow

development.

Clean Architecture

provides

the greatest value

for

medium

and

large applications.

______________________________________________________________________

# Best Practices

✅ Keep business rules in the domain.

✅ Put workflows in use cases.

✅ Keep frameworks at the edges.

✅ Depend on abstractions.

✅ Keep endpoints thin.

______________________________________________________________________

# Common Mistakes

### Business Logic in FastAPI Endpoints

Endpoints

should coordinate,

not implement

business rules.

______________________________________________________________________

### SQLAlchemy Models as Domain Models

ORM models

belong

to infrastructure,

not

the domain.

Keep

domain entities

independent.

______________________________________________________________________

### Domain Importing FastAPI

Never do

```python id="clean3116"
from fastapi import ...
```

inside

the domain layer.

The domain

should remain

framework-independent.

______________________________________________________________________

### Depending on Concrete Repositories

Use cases

should depend

on repository interfaces,

not

SQLAlchemy implementations.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Clean Architecture, and why is it useful?

Clean Architecture is a software architecture that organizes applications into layers with a strict dependency rule:
dependencies always point inward toward the business logic. The domain and application layers remain independent of
frameworks, databases, and external technologies, while infrastructure and frameworks depend on abstractions defined by
the inner layers. This approach improves maintainability, testability, and flexibility, allowing technologies such as
databases, web frameworks, and messaging systems to be replaced with minimal impact on business logic.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Clean Architecture is
- The Dependency Rule
- The four layers
- Repository interfaces
- FastAPI project structure
- Dependency Injection
- Testing
- Clean vs Layered Architecture
- Best practices

______________________________________________________________________

# 🚀 Important Milestone

Everything you've learned so far:

- SOLID
- Design Patterns
- Repository
- CQRS
- Event Sourcing
- Dependency Injection

comes together

inside

Clean Architecture.

From this point onward,

we'll explore

other architectural styles

that solve similar problems

with different approaches.

______________________________________________________________________

# What's Next

[Hexagonal Architecture (Ports & Adapters)](32-hexagonal-architecture.md)
