# Software Architecture - Part 32

# Hexagonal Architecture (Ports & Adapters)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Hexagonal Architecture is
- Why Hexagonal Architecture exists
- What Ports and Adapters are
- Primary vs Secondary Adapters
- Dependency Flow
- FastAPI implementation
- Repository interfaces
- External integrations
- How it differs from Clean Architecture
- When NOT to use Hexagonal Architecture

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**

today.

Users access it through

- FastAPI
- REST APIs

Tomorrow,

the company wants

- GraphQL
- CLI
- Background Jobs
- gRPC

Should

the business logic

change?

No.

Next,

the company changes

the database.

From

```text id="hex3201"
PostgreSQL
```

to

```text id="hex3202"
MongoDB
```

Should

business logic

change?

Again,

No.

Hexagonal Architecture

was created

to solve

exactly this problem.

______________________________________________________________________

# The Problem

A typical application

looks like this.

```text id="hex3203"
FastAPI

↓

Business Logic

↓

SQLAlchemy

↓

PostgreSQL
```

Business logic

depends on

both

the framework

and

the database.

Tomorrow,

replace

FastAPI

or

PostgreSQL,

and

business logic

starts changing.

______________________________________________________________________

# The Idea

Instead of

placing

business logic

between

framework

and

database,

place it

at the center.

Everything else

connects

through

interfaces.

______________________________________________________________________

# What is Hexagonal Architecture?

Hexagonal Architecture,

also called

**Ports and Adapters**,

states:

> **The application core communicates with the outside world only through well-defined ports.**

External systems

never

communicate

directly

with

the business logic.

They use

adapters.

______________________________________________________________________

# Why "Hexagonal"?

The hexagon

is symbolic.

It shows

that

the application

can have

many entry points

and

many exit points.

Not just

one user interface

and

one database.

______________________________________________________________________

# The Architecture

```text id="hex3204"
          REST API

              │

          GraphQL

              │

CLI ─── Application ─── Database

              │

          Kafka

              │

          Scheduler
```

Everything

connects

through

ports.

The shape

isn't important.

The separation is.

______________________________________________________________________

# Core Concepts

Hexagonal Architecture

has

three main concepts.

- Application Core
- Ports
- Adapters

______________________________________________________________________

# Application Core

This contains

the business rules.

Examples:

- Borrow Book
- Return Book
- Register Member

The core

knows nothing

about

- FastAPI
- SQLAlchemy
- Redis
- Kafka

______________________________________________________________________

# What is a Port?

A Port

is simply

an interface.

Example

```python id="hex3205"
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

Notice

there is

no SQLAlchemy.

No PostgreSQL.

Only

an abstraction.

______________________________________________________________________

# Primary Ports

Primary Ports

represent

operations

that

outside systems

can invoke.

Examples:

- Borrow Book
- Return Book
- Search Books

These are

your

Use Cases.

______________________________________________________________________

# Secondary Ports

Secondary Ports

represent

services

that

the application

needs.

Examples:

- Repository
- Email Service
- Payment Gateway
- Cache
- Message Queue

______________________________________________________________________

# What is an Adapter?

An Adapter

implements

a port.

Example

```python id="hex3206"
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

Tomorrow,

replace

SQLAlchemy.

Create

another adapter.

The application

doesn't change.

______________________________________________________________________

# Primary Adapter

A FastAPI endpoint

is

a Primary Adapter.

Example

```python id="hex3207"
@app.post("/books")
def create_book(

    use_case=Depends(
        get_use_case
    ),

):

    use_case.execute(...)
```

The endpoint

converts

HTTP requests

into

application calls.

______________________________________________________________________

# Secondary Adapter

A repository

is

a Secondary Adapter.

Example

```python id="hex3208"
class MongoRepository(
    BookRepository
):
    ...
```

Or

```python id="hex3209"
class SQLRepository(
    BookRepository
):
    ...
```

Both satisfy

the same port.

______________________________________________________________________

# Dependency Flow

Dependencies

always point

toward

the application.

```text id="hex3210"
FastAPI

↓

Use Case

↓

Repository Interface

↑

SQL Repository
```

Notice

the implementation

depends

on

the interface.

Not

the reverse.

______________________________________________________________________

# Project Structure

A common

FastAPI project.

```text id="hex3211"
app/

├── application/

│   ├── ports/

│   ├── use_cases/

│   └── domain/

├── adapters/

│   ├── api/

│   ├── database/

│   ├── cache/

│   ├── messaging/

│   └── external/

└── main.py
```

Notice

everything

outside

the application

is an adapter.

______________________________________________________________________

# Real Backend Example

Suppose

today

notifications

use

```text id="hex3212"
SMTP
```

Tomorrow,

the company

uses

```text id="hex3213"
SendGrid
```

Only

the adapter

changes.

The application

continues

calling

```python id="hex3214"
notification.send()
```

______________________________________________________________________

# Payment Gateway Example

Suppose

today

payments

use

Stripe.

Tomorrow,

Razorpay.

Create

another adapter.

Business logic

remains unchanged.

______________________________________________________________________

# FastAPI Example

Suppose

today

users interact

through REST.

Tomorrow,

the company

adds

GraphQL.

Instead of

changing

business logic,

create

a GraphQL adapter.

Both adapters

call

the same

use cases.

______________________________________________________________________

# AI/ML Example

Suppose

today

your application

uses

OpenAI.

Tomorrow,

it switches

to

Anthropic.

Define

a port.

```python id="hex3215"
class LLMService(
    ABC
):

    @abstractmethod
    def generate(
        self,
        prompt,
    ):
        ...
```

Then implement

multiple adapters.

```text id="hex3216"
OpenAI Adapter
```

```text id="hex3217"
Anthropic Adapter
```

```text id="hex3218"
Local Llama Adapter
```

The application

never changes.

______________________________________________________________________

# Hexagonal vs Clean Architecture

A very common

interview question.

| Clean Architecture | Hexagonal Architecture |
| ------------------------------------- | -------------------------------- |
| Focuses on layered dependencies | Focuses on ports and adapters |
| Organizes code into concentric layers | Organizes code around interfaces |
| Framework-independent | Framework-independent |
| Business rules at the center | Business rules at the center |

In practice,

many teams

combine

both approaches.

Clean Architecture

defines

the dependency rules.

Hexagonal Architecture

defines

how external systems

connect

to the application.

They complement

each other.

______________________________________________________________________

# Hexagonal vs Layered Architecture

| Layered | Hexagonal |
| ------------------------ | --------------------- |
| Fixed layers | Flexible ports |
| Often tied to frameworks | Framework-independent |
| Usually one entry point | Multiple entry points |

______________________________________________________________________

# Benefits

Hexagonal Architecture gives you:

✅ Framework independence

✅ Database independence

✅ Easy testing

✅ Easy replacement of integrations

✅ Multiple interfaces

______________________________________________________________________

# Drawbacks

It also introduces:

❌ More interfaces

❌ More folders

❌ More abstractions

For small applications,

it can feel

heavyweight.

______________________________________________________________________

# Real Company Example

Suppose

an e-commerce platform

supports

multiple channels.

- Mobile App
- Web App
- Admin Portal
- Partner API
- CLI Tool

All of them

invoke

the same

Order Use Case.

Each client

has

its own adapter.

The business logic

is shared.

______________________________________________________________________

# When NOT to Use Hexagonal Architecture

Don't use

Hexagonal Architecture

for

small utilities,

scripts,

or

simple CRUD APIs

with

only

a few endpoints.

Its strengths

appear

when

applications

have

multiple integrations,

multiple interfaces,

or

long-term maintenance needs.

______________________________________________________________________

# Best Practices

✅ Keep the application core pure.

✅ Define ports as interfaces.

✅ Keep adapters thin.

✅ Place framework code outside the core.

______________________________________________________________________

# Common Mistakes

### Putting Business Logic in Adapters

Adapters

should translate

between

external systems

and

the application.

Business rules

belong

inside

use cases

and

the domain.

______________________________________________________________________

### Letting the Core Import Frameworks

Never import

FastAPI,

SQLAlchemy,

or Redis

inside

the application core.

______________________________________________________________________

### Too Many Ports

Not every method

needs

its own port.

Create

meaningful,

cohesive interfaces.

______________________________________________________________________

### Confusing Ports with Adapters

Remember:

**Port**

↓

Contract

**Adapter**

↓

Implementation

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Hexagonal Architecture, and how is it different from Clean Architecture?

Hexagonal Architecture, also known as Ports and Adapters, organizes an application around its business logic by
separating the core from external systems through well-defined interfaces called ports. Adapters implement these ports
for technologies such as databases, web frameworks, message brokers, and third-party APIs. This allows external
technologies to change without affecting the application's core. While Clean Architecture focuses on dependency
direction and layered organization, Hexagonal Architecture focuses on isolating the application through ports and
adapters. The two approaches are complementary and are often used together.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Hexagonal Architecture is
- Ports and Adapters
- Primary and Secondary Ports
- Primary and Secondary Adapters
- FastAPI implementation
- AI/ML example
- Hexagonal vs Clean Architecture
- Best practices

______________________________________________________________________

# What's Next

[Onion Architecture](33-onion-architecture.md)
