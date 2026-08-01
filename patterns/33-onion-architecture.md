# Software Architecture - Part 33

# Onion Architecture

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Onion Architecture is
- Why Onion Architecture exists
- The core principles
- Layers of Onion Architecture
- Dependency Flow
- FastAPI implementation
- Repository interfaces
- Domain Services
- Onion vs Clean vs Hexagonal Architecture
- When NOT to use Onion Architecture

______________________________________________________________________

# Before We Start

By now,

you've learned

about:

- Clean Architecture
- Hexagonal Architecture

You might be wondering,

"Are these all different architectures?"

The answer is:

**Yes... and No.**

They solve

the same problem:

> **Protect the business logic from external technologies.**

They simply

organize

the application

slightly differently.

______________________________________________________________________

# The Problem

Let's continue with our

**Library Management System**.

A typical project

might look like this.

```text id="onion3301"
FastAPI

↓

SQLAlchemy

↓

Business Logic
```

The business logic

depends on

frameworks

and

database libraries.

Tomorrow,

replace

FastAPI,

and

the application

breaks.

______________________________________________________________________

# The Idea

Move

the business logic

to the center.

Everything else

surrounds it.

The closer

you move

toward

the center,

the more important

the code becomes.

______________________________________________________________________

# Why "Onion"?

Imagine

an onion.

```text id="onion3302"
Infrastructure

↓

Application

↓

Domain

↓

Core
```

Every layer

wraps

the one

inside it.

Dependencies

always move

toward

the center.

______________________________________________________________________

# What is Onion Architecture?

Onion Architecture,

introduced by

Jeffrey Palermo,

states:

> **The domain model should be at the center, with all dependencies pointing inward.**

The innermost layer

contains

the business rules.

Everything else

supports it.

______________________________________________________________________

# The Dependency Rule

Exactly like

Clean Architecture,

Onion Architecture

follows

one simple rule.

> **Inner layers never depend on outer layers.**

Outer layers

may depend

on

inner layers.

Never

the reverse.

______________________________________________________________________

# The Layers

```text id="onion3303"
Infrastructure

↓

Application

↓

Domain

↓

Entities
```

Let's examine

each layer.

______________________________________________________________________

# Layer 1

## Entities

The innermost layer.

Contains

pure business objects.

Example

```python id="onion3304"
class Book:

    def __init__(

        self,

        title,

        author,

    ):

        self.title = title

        self.author = author
```

No

FastAPI.

No

SQLAlchemy.

No

database code.

Only

business concepts.

______________________________________________________________________

# Layer 2

## Domain Layer

Contains

business rules.

Examples:

- Borrow Book
- Calculate Fine
- Validate Membership

Sometimes

this layer

also contains

Domain Services

and

Value Objects.

______________________________________________________________________

# Layer 3

## Application Layer

Coordinates

business workflows.

Examples:

- BorrowBookUseCase
- RegisterMemberUseCase
- ReturnBookUseCase

The application

orchestrates

domain objects,

but

still

knows nothing

about

FastAPI

or

PostgreSQL.

______________________________________________________________________

# Layer 4

## Infrastructure Layer

Contains

everything external.

Examples:

- FastAPI
- SQLAlchemy
- Redis
- Kafka
- Celery
- Email
- Payment APIs

This layer

implements

interfaces

defined

inside

the application.

______________________________________________________________________

# Dependency Direction

```text id="onion3305"
FastAPI

↓

Use Case

↓

Repository Interface

↓

Domain

↓

Entity
```

Notice

how

dependencies

always move

toward

the center.

______________________________________________________________________

# Repository Example

Inside

the application

define

an interface.

```python id="onion3306"
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

______________________________________________________________________

# SQLAlchemy Repository

Outside

the application,

implement it.

```python id="onion3307"
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

Business logic

doesn't know

this class exists.

______________________________________________________________________

# FastAPI Example

```python id="onion3308"
@app.post("/borrow")
def borrow_book(

    use_case=Depends(
        get_use_case
    ),

):

    use_case.execute(...)
```

The endpoint

acts

as

an entry point.

Nothing more.

______________________________________________________________________

# Project Structure

A common

Onion Architecture

layout.

```text id="onion3309"
app/

├── domain/

│   ├── entities/

│   ├── services/

│   ├── value_objects/

│   └── events/

├── application/

│   ├── use_cases/

│   ├── interfaces/

│   └── dto/

├── infrastructure/

│   ├── database/

│   ├── repositories/

│   ├── cache/

│   ├── messaging/

│   └── api/

└── main.py
```

Notice

the outer layer

contains

all technology-specific code.

______________________________________________________________________

# Real Backend Example

Suppose

today

we use

```text id="onion3310"
Redis
```

Tomorrow,

replace it

with

```text id="onion3311"
Memcached
```

Only

the infrastructure

changes.

The domain

remains

identical.

______________________________________________________________________

# Another Example

Suppose

today

we expose

REST.

Tomorrow,

we expose

GraphQL.

Again,

only

the outer layer

changes.

Business logic

remains untouched.

______________________________________________________________________

# AI/ML Example

Suppose

your application

supports

multiple LLM providers.

Inside

the application,

define

an interface.

```python id="onion3312"
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

Outside,

implement

multiple providers.

- OpenAI
- Anthropic
- Local Llama

Switch providers

without

changing

business logic.

______________________________________________________________________

# Onion vs Clean Architecture

A common

interview question.

| Onion | Clean |
| ------------------------------- | -------------------------------------------- |
| Centered around the domain | Centered around business rules and use cases |
| Concentric layers | Concentric layers |
| Same dependency rule | Same dependency rule |
| Strong emphasis on domain model | Strong emphasis on use cases |

In practice,

they look

very similar.

Many teams

combine ideas

from both.

______________________________________________________________________

# Onion vs Hexagonal

| Onion | Hexagonal |
| ------------------------ | ----------------------------- |
| Focuses on layered rings | Focuses on ports and adapters |
| Organizes code by layers | Organizes code by interfaces |
| Dependency direction | Integration boundaries |

Again,

they solve

the same problem

from

different perspectives.

______________________________________________________________________

# Onion vs Layered Architecture

| Traditional Layered | Onion |
| ------------------------- | -------------------------------- |
| UI → Service → Repository | Infrastructure surrounds domain |
| Often framework-centric | Domain-centric |
| Dependencies may leak | Dependencies always point inward |

______________________________________________________________________

# Benefits

Onion Architecture gives you:

✅ High testability

✅ Technology independence

✅ Strong domain focus

✅ Easy replacement of infrastructure

✅ Better long-term maintainability

______________________________________________________________________

# Drawbacks

It also introduces:

❌ More abstractions

❌ More interfaces

❌ More project structure

For small applications,

this may be excessive.

______________________________________________________________________

# Real Company Example

Suppose

an insurance platform

must integrate

with:

- Multiple payment providers
- Government APIs
- Notification systems
- Fraud detection services

These integrations

change frequently.

By isolating them

in

the infrastructure layer,

the core business rules

remain stable

for years.

______________________________________________________________________

# When NOT to Use Onion Architecture

Don't use

Onion Architecture

for:

- Small scripts
- Tiny CRUD services
- Proof-of-concept projects
- Internal automation tools

The architecture

is most valuable

when

the business logic

is expected

to grow

and evolve

over time.

______________________________________________________________________

# Best Practices

✅ Keep entities framework-independent.

✅ Keep business rules in the domain.

✅ Define interfaces inward.

✅ Implement integrations outward.

✅ Keep infrastructure replaceable.

______________________________________________________________________

# Common Mistakes

### ORM Models as Domain Entities

Don't let

SQLAlchemy models

become

your domain entities.

Keep

the domain

independent.

______________________________________________________________________

### Business Logic in Controllers

FastAPI endpoints

should coordinate,

not implement

business rules.

______________________________________________________________________

### Domain Depending on Infrastructure

Never import

database,

framework,

or messaging libraries

inside

the domain.

______________________________________________________________________

### Too Much Logic in Repositories

Repositories

persist

and retrieve data.

Complex business rules

belong

to

the domain

or

application layer.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Onion Architecture, and how does it compare to Clean Architecture?

Onion Architecture is a software architecture that organizes an application into concentric layers with the domain model
at the center. Dependencies always point inward, ensuring that business logic remains independent of frameworks,
databases, and external systems. Like Clean Architecture, it emphasizes separation of concerns and dependency inversion.
The primary difference is that Onion Architecture places stronger emphasis on the domain model, while Clean Architecture
often emphasizes use cases and application workflows. In practice, the two architectures are highly compatible and
frequently combined.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Onion Architecture is
- Why it exists
- The dependency rule
- Onion layers
- FastAPI implementation
- AI/ML example
- Onion vs Clean
- Onion vs Hexagonal
- Best practices

______________________________________________________________________

# 🧠 Architecture Comparison So Far

You now understand three of the most popular enterprise architectures:

- **Clean Architecture** → Organize around use cases and dependency direction.
- **Hexagonal Architecture** → Isolate the core using ports and adapters.
- **Onion Architecture** → Place the domain model at the center with concentric layers.

All three share the same fundamental goal:

> **Keep business logic independent of frameworks and infrastructure.**

The differences are mainly in emphasis and organization rather than core principles.

______________________________________________________________________

# What's Next

[Layered Architecture](34-layered-architecture.md)
