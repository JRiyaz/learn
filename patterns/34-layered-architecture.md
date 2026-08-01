# Software Architecture - Part 34

# Layered Architecture (N-Tier Architecture)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Layered Architecture is
- Why Layered Architecture exists
- The common layers
- Dependency flow
- Real-world FastAPI project structure
- How requests move through layers
- Layered vs Clean vs Hexagonal vs Onion
- Advantages and disadvantages
- When NOT to use Layered Architecture

______________________________________________________________________

# Before We Start

Before learning

Layered Architecture,

let's answer

one question.

**Haven't we already learned this?**

Not exactly.

Most enterprise applications

today

still use

Layered Architecture.

In fact,

many projects

that claim

to use

Clean Architecture

are actually

Layered Architecture

with

a few improvements.

If you've worked

as a backend engineer,

you've almost certainly

used it already.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

A beginner project

might look like this.

```python id="layer3401"
@app.post("/books")
def create_book():

    validate()

    calculate_price()

    db.add(book)

    db.commit()

    send_email()

    return response
```

Everything

is inside

the endpoint.

Soon,

every endpoint

contains

the same code.

Problems:

❌ Code duplication

❌ Difficult testing

❌ Difficult maintenance

______________________________________________________________________

# The Idea

Separate

the application

into

layers.

Each layer

has

one responsibility.

Instead of

one large function,

the request

moves

through

multiple layers.

______________________________________________________________________

# What is Layered Architecture?

Layered Architecture,

also called

**N-Tier Architecture**,

organizes

an application

into

independent layers,

where

each layer

has

a specific responsibility.

A layer

can only

communicate

with

its neighboring layers.

______________________________________________________________________

# Typical Layers

Most backend applications

use

four layers.

```text id="layer3402"
Presentation Layer

↓

Service Layer

↓

Repository Layer

↓

Database
```

Some projects

add

extra layers,

but

these four

are the most common.

______________________________________________________________________

# Layer 1

## Presentation Layer

This layer

handles

user interaction.

Examples:

- FastAPI Endpoints
- Flask Routes
- Django Views
- GraphQL Resolvers

Responsibilities:

- Parse requests
- Validate input
- Return responses

It should

not

contain

business logic.

______________________________________________________________________

# Example

```python id="layer3403"
@app.post("/books")
def create_book(

    service=Depends(
        get_service
    ),

):

    return service.create_book(...)
```

Notice

the endpoint

delegates

the work.

______________________________________________________________________

# Layer 2

## Service Layer

Contains

business logic.

Examples:

- Borrow Book
- Register Member
- Calculate Fine
- Process Payment

Example

```python id="layer3404"
class LibraryService:

    def borrow_book(
        self,
        request,
    ):

        ...
```

This is

where

most business rules

belong.

______________________________________________________________________

# Layer 3

## Repository Layer

Handles

data access.

Examples:

- SQLAlchemy
- MongoDB
- Redis
- Elasticsearch

Example

```python id="layer3405"
class BookRepository:

    def save(
        self,
        book,
    ):
        ...
```

Repositories

should not

contain

business rules.

______________________________________________________________________

# Layer 4

## Database

Stores

persistent data.

Examples:

- PostgreSQL
- MySQL
- MongoDB

The application

communicates

with

the database

through

repositories.

______________________________________________________________________

# Request Flow

Suppose

a user

borrows a book.

The request

travels

like this.

```text id="layer3406"
Client

↓

FastAPI

↓

Service

↓

Repository

↓

Database
```

Then

the response

returns

back

through

the same path.

______________________________________________________________________

# FastAPI Project Structure

A common

Layered Architecture

project.

```text id="layer3407"
app/

├── api/

│   └── routes/

├── services/

├── repositories/

├── models/

├── schemas/

├── database/

└── main.py
```

This is

probably

the most common

structure

used

by Python teams.

______________________________________________________________________

# Example

Borrowing a book.

Endpoint

↓

```python id="layer3408"
service.borrow_book()
```

Service

↓

```python id="layer3409"
repository.get_book()
```

Repository

↓

SQLAlchemy

↓

PostgreSQL

Simple.

Easy to follow.

______________________________________________________________________

# Real Backend Example

Suppose

today

the company

changes

from

PostgreSQL

to

MySQL.

Which layer changes?

Only

the Repository Layer.

The API

and

Service Layer

remain unchanged.

______________________________________________________________________

# Another Example

Suppose

today

the frontend

uses

REST.

Tomorrow,

it switches

to

GraphQL.

Only

the Presentation Layer

changes.

Everything else

stays

the same.

______________________________________________________________________

# AI/ML Example

Suppose

your AI application

contains

these layers.

```text id="layer3410"
REST API

↓

Inference Service

↓

Model Repository

↓

LLM
```

The service

handles:

- Prompt Validation
- Prompt Engineering
- Retry Logic

The repository

loads

the model.

The API

returns

the response.

______________________________________________________________________

# Layered vs Clean Architecture

One of

the most common

interview questions.

| Layered | Clean |
| -------------------------------------------- | -------------------------------- |
| Organizes by technical layers | Organizes around business rules |
| Services may depend on repositories directly | Use cases depend on abstractions |
| Simpler | More flexible |

Layered Architecture

works well

for many projects.

Clean Architecture

improves

long-term flexibility.

______________________________________________________________________

# Layered vs Hexagonal

| Layered | Hexagonal |
| ----------------------- | ---------------------- |
| Fixed layers | Ports and adapters |
| One primary interface | Multiple interfaces |
| Framework often central | Business logic central |

______________________________________________________________________

# Layered vs Onion

| Layered | Onion |
| ---------------- | ----------------- |
| Technical layers | Concentric layers |
| Service-centered | Domain-centered |

______________________________________________________________________

# Advantages

Layered Architecture gives you:

✅ Simple organization

✅ Easy onboarding

✅ Familiar structure

✅ Clear responsibilities

✅ Widely used

______________________________________________________________________

# Drawbacks

It also has

limitations.

❌ Business logic

may leak

into controllers.

❌ Services

may become

very large.

❌ Tight coupling

between layers.

❌ Harder

to replace

infrastructure

than

Clean Architecture.

______________________________________________________________________

# Common Anti-Pattern

Many projects

eventually become

this.

```text id="layer3411"
Controller

↓

God Service

↓

Repository
```

The Service Layer

contains

thousands

of lines

of code.

Everything

ends up

inside

one class.

Avoid this.

Split

services

by

business capability.

______________________________________________________________________

# Real Company Example

A banking application

might use

Layered Architecture.

```text id="layer3412"
API

↓

Account Service

↓

Account Repository

↓

PostgreSQL
```

For many

internal business systems,

this architecture

is sufficient

and

easy to maintain.

______________________________________________________________________

# When NOT to Use Layered Architecture

Layered Architecture

works well

for

most applications.

However,

if your system

needs:

- Multiple interfaces
- Frequent technology changes
- Long-term scalability
- Rich domain models

Clean,

Hexagonal,

or

Onion Architecture

may provide

better separation.

______________________________________________________________________

# Best Practices

✅ Keep controllers thin.

✅ Put business rules in services.

✅ Keep repositories focused on persistence.

✅ Don't let repositories call services.

______________________________________________________________________

# Common Mistakes

### Fat Controllers

Controllers

should validate,

delegate,

and respond.

Nothing more.

______________________________________________________________________

### God Services

Split services

by

business capability,

not

by database table.

______________________________________________________________________

### Business Logic in Repositories

Repositories

retrieve

and store data.

They don't

implement

business workflows.

______________________________________________________________________

### Layer Skipping

Avoid

controllers

calling

repositories

directly.

Follow

the layer boundaries.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Layered Architecture, and how does it compare to Clean Architecture?

Layered Architecture organizes an application into technical layers such as Presentation, Service, Repository, and
Database. Each layer has a specific responsibility and typically communicates only with adjacent layers. It is simple,
widely understood, and works well for many enterprise applications. Compared to Clean Architecture, Layered Architecture
places greater emphasis on technical separation, while Clean Architecture emphasizes business independence and
dependency inversion. Many production systems start with Layered Architecture and gradually adopt principles from Clean
Architecture as they grow.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Layered Architecture is
- Why it exists
- The four common layers
- FastAPI project structure
- Request flow
- AI/ML example
- Layered vs Clean
- Layered vs Hexagonal
- Best practices

______________________________________________________________________

# 📌 Architecture Comparison

You now understand four major architectural styles:

| Architecture | Main Focus |
| ------------ | -------------------------------------------------- |
| Layered | Separate code into technical layers |
| Clean | Protect business logic using dependency inversion |
| Hexagonal | Connect the application through ports and adapters |
| Onion | Place the domain model at the center |

In real-world projects, it's common to see a combination of these ideas rather than a single "pure" architecture.

______________________________________________________________________

# What's Next

[Domain-Driven Design (DDD) Fundamentals](35-domain-driven-design-fundamentals.md)
